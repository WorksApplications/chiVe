
import argparse
from datetime import datetime
import logging
from pathlib2 import Path
from sys import argv
import yaml

from dataset.pairwise import build_pairwise_similarity_datasets
from eval.evaluator import W2VSimilarityEvaluator
from models.w2v import build_gensim_w2v, build_w2v_api

logger = logging.getLogger(argv[0])


def run_wordsim(vconfig_path, tconfig_path, log_path=None):
    # setup logger
    if log_path == None:
        log_path = datetime.now().strftime('%Y%m%d_%H:%M')
    logging.basicConfig(level=logging.INFO)
    file_handler = logging.FileHandler(log_path)
    fmt = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    logger.info("Arguments...")
    for arg, val in sorted(vars(args).items()):
        logger.info("{}: {}".format(arg, val))

    with open(vconfig_path) as fv, open(tconfig_path) as ft:
        vec_config = yaml.load(fv)
        task_config = yaml.load(ft)
    logger.info("vector configulatation: {}".format(vec_config))
    logger.info("task configulatation: {}".format(task_config))

    logger.info("Setup...")
    w2v = build_gensim_w2v(w2v_path=vec_config["vec-path"],
                           load_config=vec_config["loading"],
                           other_config=vec_config["gensim-others"])
    w2v_api = build_w2v_api(w2v=w2v,
                            config=vec_config["api-setting"],
                            w2v_desc=vec_config["description"])
    dats = build_pairwise_similarity_datasets(name=task_config["name"],
                                              dir_path=task_config["data-path"],
                                              process_config=task_config["process"])

    logger.info("Do evaluation")
    name2score = {}
    for d in dats:
        logger.info("In {}".format(d.name))
        eval = W2VSimilarityEvaluator(d, w2v_api)
        score = eval.run()
        name2score[d.name] = score
        logger.info("Out {}".format(d.name))

    logger.info("Results...")
    for (k, v) in name2score.items():
        logger.info("{}: {}".format(k, v))
    logger.info("DOne")



if __name__ == '__main__':
    p = argparse.ArgumentParser("Word similarity Evaluation")
    p.add_argument("--vconfig", type=str, help="Vector Configulation file path")
    p.add_argument("--tconfig", type=str, help="Task Configulation file path")
    p.add_argument("--log", type=str, help="Log path")
    args = p.parse_args()

    run_wordsim(args.vconfig, args.tconfig, args.log)
