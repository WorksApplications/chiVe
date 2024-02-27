
import pandas as pd
from pathlib2 import Path

from dataset.base import BaseDataset, BaseInstance
from utils import build_tokenizer


class PairwiseSimilarityDataset(BaseDataset):
    def __init__(self, samples, name=None):
        super(PairwiseSimilarityDataset, self).__init__(samples, name)

    @staticmethod
    def build_from_triplet(col1s, col2s, sims):
        """
        args:
            - col1s (list<?>): first elements in the given pairs
            - col2s (list<?>): second elements in the given pairs
            - sims (list<float>): scores
            - tok (Tokenizer): Tokenizer for entryies. If None, no tokenization
        """
        assert len(col1s) == len(col2s) and len(col1s) == len(sims), \
               "Inconsistent length: {} / {} / {}" \
               .format(len(col1s), len(col2s), len(sims))
        insts = [PairwiseSimilarityInstance(c1, c2, sim) \
                 for (c1, c2, sim) in zip(col1s, col2s, sims)]
        return PairwiseSimilarityDataset(samples=insts)


class PairwiseSimilarityInstance(BaseInstance):
    def __init__(self, e1, e2, score):
        """
        args:
            - e1, e2 (list<str>): Pair of (tokenized) Strings to be evaluated.
        """
        super(PairwiseSimilarityInstance, self).__init__()
        assert type(e1) == list
        assert type(e2) == list
        assert type(score) in [int, float], "Invalid type: {}".format(type(score))
        self._triple = (e1, e2, score)
        self.gold = score

    def get_content(self):
        return self._triple


def build_pairwise_similarity_datasets(name, dir_path, process_config):
    # prepare to generate dataset
    if process_config["use-tokenizer"] == True:
        tok = build_tokenizer(process_config["tokenizer"]["name"],
                              process_config["tokenizer"]["others"])
    else:
        tok = None
    if name == "tmu":
        datasets = build_tmu(dir_path, tok)
    elif name == "jwsan":
        datasets = build_jwsan(dir_path, tok)
    else:
        raise ValueError("Invalid dataset name: {}".format(name))
    return datasets


def build_tmu(dir_path, tok=None):
    _filenames = ['score_adj.csv.nkf', 'score_adv.csv.nkf.tr_space',
                  'score_noun.csv.nkf.tr_space', 'score_verb.csv.nkf']
    base = Path(dir_path)
    dats = []
    for fn in _filenames:
        df = pd.read_csv(str((base/fn).absolute()), encoding="utf-8")
        if tok == None:
            col1s = [[c] for c in list(df["word1"])]
            col2s = [[c] for c in list(df["word2"])]
        else:
            col1s = [tok.wakati(c) for c in list(df["word1"])]
            col2s = [tok.wakati(c) for c in list(df["word2"])]
        scores = [float(score) for score in list(df["mean"])]
        dat = PairwiseSimilarityDataset.build_from_triplet(col1s, col2s, scores)
        dat.name = "tmu-{}".format(fn)
        dats.append(dat)
    return dats


def build_jwsan(dir_path, tok=None):
    _filenames = ['jwsan-1400.csv', 'jwsan-2145.csv']
    _elms = ['similarity', 'association']
    base = Path(dir_path)
    dats = []
    for fn in _filenames:
        df = pd.read_csv(str((base/fn).absolute()), encoding="utf-8")
        if tok == None:
            col1s = [[c] for c in list(df["word1"])]
            col2s = [[c] for c in list(df["word2"])]
        else:
            col1s = [tok.wakati(c) for c in list(df["word1"])]
            col2s = [tok.wakati(c) for c in list(df["word2"])]
        for e in _elms:
            scores = [float(score) for score in list(df[e])]
            dat = PairwiseSimilarityDataset.build_from_triplet(col1s, col2s, scores)
            dat.name = "jwsan-{}-{}".format(fn, e)
            dats.append(dat)
    return dats
