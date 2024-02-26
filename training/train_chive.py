import argparse
from dataclasses import dataclass
import json
import logging
from pathlib import Path
import time

from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence, PathLineSentences
from gensim.models.callbacks import CallbackAny2Vec


logging.basicConfig(
    style="{",
    format='{levelname} {asctime} [{module}:{funcName}:{lineno}] {message}',
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

CHIVE_VERSION = "1.3"


@dataclass
class Config():
    """Configuration for training word2vec model.

    ref: https://radimrehurek.com/gensim/models/word2vec.html#gensim.models.word2vec.Word2Vec
    """

    vector_size: int = 300
    window: int = 8
    sg: 0 | 1 = 1  # Training algorithm: 1 for skip-gram; otherwise CBOW.
    hs: 0 | 1 = 0  # 1 for hierachical softmax, 0 for negative sampling
    n_negative: int = 5
    threshold_downsample: float = 1e-5

    # value to resume training
    alpha: float = 0.025       # default value of gensim
    min_alpha: float = 0.0001  # default value of gensim

    @staticmethod
    def from_file(config_file: Path | None):
        """Load values from json file."""
        conf = {}
        if config_file is not None:
            with config_file.open() as fi:
                conf = json.load(fi)
        return Config(**conf)


class LogLossCallback(CallbackAny2Vec):
    """callback to log loss and time.

    Note that training loss is reset when you resume training."""

    def __init__(self, logfile: Path, start_time: float, start_epoch: int = 0):
        self.epochs = start_epoch
        self.start_time = start_time

        self.loss_previous_step = 0
        self.time_previous_step = start_time

        self.logfile = logfile
        return

    def _get_and_record_loss(self, model):
        total_loss = model.get_latest_training_loss()
        current_time = total_loss - self.loss_previous_step

        self.loss_previous_step = total_loss
        return total_loss, current_time

    def _get_and_record_time(self):
        now = time.time()
        total_time = now - self.start_time
        current_time = now - self.time_previous_step

        self.time_previous_step = now
        return total_time, current_time

    def on_epoch_end(self, model):
        total_loss, current_loss = self._get_and_record_loss(model)
        total_time, current_time = self._get_and_record_time()

        with self.logfile.open("a") as f:
            f.write(f"{self.epochs},"
                    f"{total_loss},{current_loss},"
                    f"{total_time},{current_time}\n")

        self.epochs += 1
        return


class CheckpointHandler():
    def __init__(self, output_dir: Path, min_count: int, version: str = CHIVE_VERSION, keep_ckpt: int = 3):
        # values used to generate filename
        self.output_dir = output_dir
        self.version = version
        self.min_count = min_count

        self.keep = keep_ckpt
        self.checkpoints = self.list_checkpoints()
        return

    @staticmethod
    def epoch_from_file(filename: Path) -> int:
        """parse epoch count from a ckpt file name."""
        # NOTE: this depends on the filename pattern
        stem = filename.stem
        len_prefix = stem.find("_epoch") + len("_epoch")
        return int(stem[len_prefix:])

    def list_checkpoints(self) -> list[Path]:
        """list ckpt files under output directory."""
        files = self.output_dir.glob(self.ckpt_filepath(epoch="*").name)
        files = list(sorted(files, key=self.epoch_from_file))
        return files

    def latest_ckpt(self) -> Path | None:
        """return ckpt with largest epoch, or None if no ckpt found."""
        if len(self.checkpoints) == 0:
            return None
        return self.checkpoints[-1]

    def ckpt_filepath(self, epoch: int) -> Path:
        """generate a path to the ckpt file with given epoch"""
        filename = f"chiVe-{self.version}-mc{self.min_count}_epoch{epoch}.bin"
        return self.output_dir / filename

    def save_ckpt(self, epoch: int, save_func):
        """save ckpt using given func and remove old ckpts.

        :param save_func: saves data to the given path.
        """
        new_ckpt = self.ckpt_filepath(epoch)
        save_func(new_ckpt)
        self.checkpoints.append(new_ckpt)
        self.remove_old_ckpt()
        return

    def remove_old_ckpt(self):
        """remove old ckpts, keeping self.keep_ckpt ckpts."""
        for i in range(len(self.checkpoints) - self.keep):
            logger.info(f"remove ckpt {self.checkpoints[i]}")
            self.checkpoints[i].unlink()
        self.checkpoints = self.checkpoints[-self.keep:]
        return


class SaveCheckpointCallback(CallbackAny2Vec):
    """callback to save ckpts per specified epochs."""

    def __init__(self, ckpt_handler: CheckpointHandler, save_epochs: int = 5, start_epoch: int = 0):
        self.ckpt_handler = ckpt_handler
        self.epochs = start_epoch
        self.save_epochs = save_epochs
        return

    def on_epoch_end(self, model):
        self.epochs += 1
        if self.epochs % self.save_epochs == 0:
            self.ckpt_handler.save_ckpt(
                epoch=self.epochs,
                save_func=lambda p: model.save(str(p)))
        return


def parse_args():
    p = argparse.ArgumentParser("Training word embedding by gensim")
    p.add_argument("--input", type=Path,
                   help="tokenized text data (line-by-line) or directory contains them")
    p.add_argument("--output", type=Path,
                   help="directory to output")

    p.add_argument("--epochs", type=int, default=15,
                   help="how many epochs to run training (default 15)")
    p.add_argument("--min-count", type=int, default=90,
                   help="words that appears less than this would be ignored (default 90)")
    p.add_argument("--save-epochs", type=int, default=5,
                   help="save model every this epochs as checkpoint (default 5)")
    p.add_argument("--keep-ckpt", type=int, default=3,
                   help="how many checkpoints to keep (default 3)")
    p.add_argument("--worker", type=int, default=12,
                   help="how many threads to use during training (default 12)")

    p.add_argument("--config", type=Path, default=None,
                   help="json file to load config parameters from (optional)")

    args = p.parse_args()
    return args


def restart_alpha(conf: Config, total_epochs: int, ckpt_epochs: int) -> float:
    """calculate alpha for restarting from the given ckpt epochs.

    - learning rate decaies linearly from alpha to min_alpha
        - it depends on alpha/min_alpha/total_epoch/crr_epoch
        - https://github.com/piskvorky/gensim/blob/e7b441b87a967e22668a2365bcb60a13e9496215/gensim/models/word2vec.py#L1441
    - resuming training requires adjusted epochs (i.e. remaining epochs).
        - it affects to lr calculation, and we also need to adjust start_alpha
    """
    alpha = conf.alpha
    min_alpha = conf.min_alpha
    return alpha - (alpha - min_alpha) / total_epochs * ckpt_epochs


def main():
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    train_ops = Config.from_file(args.config)

    sents = LineSentence(args.input) if args.input.is_file() \
        else PathLineSentences(args.input)

    ckpt_handler = CheckpointHandler(
        args.output, args.min_count, keep_ckpt=args.keep_ckpt)
    logfile = args.output / f"TrainLog-mc{args.min_count}.csv"

    latest_ckpt = ckpt_handler.latest_ckpt()
    if latest_ckpt is None:
        logger.info(f"training from scratch")
        model = Word2Vec(
            sents,
            workers=args.worker,
            vector_size=train_ops.vector_size,
            window=train_ops.window,
            sample=train_ops.threshold_downsample,
            sg=train_ops.sg,
            hs=train_ops.hs,
            negative=train_ops.n_negative,
            epochs=args.epochs,
            min_count=args.min_count,
            alpha=train_ops.alpha,
            min_alpha=train_ops.min_alpha,
            compute_loss=True,
            callbacks=[
                SaveCheckpointCallback(ckpt_handler, args.save_epochs),
                LogLossCallback(logfile, time.time()),
            ],
        )
    else:
        # Resume training from the checkpoint.
        # Assume to use same corpus and parameters.
        logger.info(f"checkpoint found: {latest_ckpt}")
        ckpt_epochs = ckpt_handler.epoch_from_file(latest_ckpt)
        if ckpt_epochs >= args.epochs:
            logger.info(
                f"training seems already finished ({latest_ckpt} exists).")
            return

        model = Word2Vec.load(str(latest_ckpt))
        model.train(
            sents,
            total_examples=model.corpus_count,
            epochs=args.epochs - ckpt_epochs,
            start_alpha=restart_alpha(train_ops, args.epochs, ckpt_epochs),
            end_alpha=train_ops.min_alpha,
            compute_loss=True,
            callbacks=[
                SaveCheckpointCallback(
                    ckpt_handler, args.save_epochs, start_epoch=ckpt_epochs),
                LogLossCallback(logfile, time.time(), start_epoch=ckpt_epochs),
            ],
        )
        # fix value changed by calling model.train
        model.alpha = train_ops.alpha
        model.epochs = args.epochs

    logger.info(f"finish training and save model.")
    model.save(str(ckpt_handler.ckpt_filepath(args.epochs)))
    return


if __name__ == '__main__':
    main()
