import argparse
import logging
from pathlib import Path

from gensim.models import Word2Vec


logging.basicConfig(
    style="{",
    format='{levelname} {asctime} [{module}:{funcName}:{lineno}] {message}',
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def parse_args():
    p = argparse.ArgumentParser(
        "Convert trained gensim.Word2Vec full model into release formats.")
    p.add_argument("--input", type=Path,
                   help="target model data (.bin of gensim.Word2Vec)")
    p.add_argument("--output", type=Path, default=Path("./output"),
                   help="directory to output")
    args = p.parse_args()
    return args


def main():
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    stem = args.input.stem
    fullmodel = Word2Vec.load(str(args.input))

    # ref:
    #   https://radimrehurek.com/gensim/models/word2vec.html#gensim.models.word2vec.Word2Vec
    #   https://radimrehurek.com/gensim/models/keyedvectors.html#how-to-obtain-word-vectors
    logger.info(f"gensim.KeyedVectors")
    outfile = args.output / f"{stem}_gensim" / f"{stem}.kv"
    outfile.parent.mkdir()
    fullmodel.wv.save(str(outfile))

    # ref: https://radimrehurek.com/gensim/models/keyedvectors.html#gensim.models.keyedvectors.KeyedVectors.save_word2vec_format
    logger.info(f"text format")
    outfile = args.output / f"{stem}_text" / f"{stem}.txt"
    outfile.parent.mkdir()
    fullmodel.wv.save_word2vec_format(str(outfile))

    # ref: https://github.com/plasticityai/magnitude/tree/master?tab=readme-ov-file#file-format-and-converter
    # logger.info(f"magnitude")
    # from pymagnitude.third_party_mock.converter import convert as convert_magnitude
    # outfile = args.output / f"{stem}.magnitude"
    # convert_magnitude(
    #     input_file_path=str(args.input),
    #     output_file_path=str(outfile),
    # )

    return


if __name__ == '__main__':
    main()
