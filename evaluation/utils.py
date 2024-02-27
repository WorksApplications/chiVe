
import numpy as np
from scipy.spatial import distance

from manalib.text.tokenizer import MeCabTokenizer, SudachiTokenizer, LargestMatchTokenizer


def cos_sim(v1, v2):
    return 1.0 - distance.cosine(v1, v2)


def get_zero_vector(dim, eps=1e-8):
    return eps * np.ones(dim)


def build_tokenizer(tok_name, config):
    if tok_name == 'sudachi':
        return SudachiTokenizer(config["mode"], config["dic-name"])
    elif tok_name == 'mecab':
        return MeCabTokenizer(config["dic-path"])
    elif tok_name == 'lm':
        return LargestMatchTokenizer.build_from_word_list(config["word_list"])
    else:
        raise ValueError("Invalid Tokenizer Name: {}".format(tok_name))
