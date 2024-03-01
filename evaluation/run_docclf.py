
import argparse
from datetime import datetime
import logging
from pathlib import Path
import yaml

from dataset.labeled import build_doc_classification_dataset
from eval.evaluator import ClassificationEvaluator
from models.classifier import build_classifier
from models.w2v import build_gensim_w2v, build_w2v_api


logging.basicConfig(
    style="{",
    format='{levelname} {asctime} [{module}:{funcName}:{lineno}] {message}',
    datefmt="%m-%d-%Y %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def add_file_handler(logfile: Path) -> None:
    file_handler = logging.FileHandler(logfile)
    logger.addHandler(file_handler)
    return


def run_docclf(vconfig_path, tconfig_path):
    with open(vconfig_path) as fv, open(tconfig_path) as ft:
        vec_config = yaml.load(fv, Loader=yaml.CLoader)
        task_config = yaml.load(ft, Loader=yaml.CLoader)
    logger.info(f"vector configulatation: {vec_config}")
    logger.info(f"task configulatation: {task_config}")

    logger.info("Setup...")
    w2v = build_gensim_w2v(w2v_path=vec_config["vec-path"],
                           load_config=vec_config["loading"],
                           other_config=vec_config["gensim-others"])
    w2v_api = build_w2v_api(w2v=w2v,
                            config=vec_config["api-setting"],
                            w2v_desc=vec_config["description"])
    dat = build_doc_classification_dataset(name=task_config["name"],
                                           dir_path=task_config["data-path"],
                                           process_config=task_config["process"])
    clf = build_classifier(method=task_config["classifier"]["method"],
                           other_config=task_config["classifier"]["others"])

    logger.info("Do evaluation")
    eval = ClassificationEvaluator(dat, w2v_api, clf)
    res = eval.run_kfold()

    logger.info("Results...")
    logger.info(res)
    logger.info("Done")
    return


if __name__ == '__main__':
    p = argparse.ArgumentParser("Word similarity Evaluation")
    p.add_argument("--vconfig", type=Path,
                   help="Vector Configulation file path")
    p.add_argument("--tconfig", type=Path, help="Task Configulation file path")
    p.add_argument("--log", type=Path, default=None, help="Log path")
    args = p.parse_args()

    # setup logger
    logfile = args.log if args.log is not None else Path(
        f"{datetime.now().strftime('%Y%m%d_%H:%M')}.log")
    add_file_handler(logfile)

    logger.info("Arguments...")
    for arg, val in sorted(vars(args).items()):
        logger.info("{}: {}".format(arg, val))

    # main
    run_docclf(args.vconfig, args.tconfig)
