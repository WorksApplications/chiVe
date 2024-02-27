"""
Basically this is for Japanese
"""

from gensim.models import Word2Vec, KeyedVectors
from gensim.models.keyedvectors import Word2VecKeyedVectors
import logging
import numpy as np
from sklearn.decomposition import PCA
from sys import argv
from warnings import warn

from utils import cos_sim, get_zero_vector

logger = logging.getLogger(argv[0]).getChild(__file__)


class WordVectorizer():
    def __init__(self):
        pass

    def query(self, surface, return_oov_flag=False):
        """
        generate the vector for the given word.
        --- Don't OVERRIDE ---
        args:
            - surface (str): target token
        return:
            - vec (np.ndarray): generated vector
            - is_oov (bool): OOV flag
        """
        v, oov_flag = self._get_vec_with_oov(surface)
        if return_oov_flag:
            return v, oov_flag
        else:
            return v

    def _get_vec_with_oov(self, surface):
        raise NotImplementedError()

    def query_as_batch(self, surface_list, return_oov_flag=False):
        if return_oov_flag == False:
            return np.array([self.query(s, return_oov_flag) for s in surface_list])
        else:
            # TODO: maybe slow
            vecs = []
            flags = []
            for s in surface_list:
                v, oov_flag = self.query(s, return_oov_flag)
                vecs.append(v)
                flags.append(oov_flag)
            return np.array(vecs), flags


class Word2VecAPI(WordVectorizer):
    """
    Word2Vec API for OOV handling or others
    """
    def __init__(self, w2v, config=None, train_desc=None):
        """
        args:
            - w2v (Word2Vec or Word2VecKeyedVectors): trained word2vec
            - config (dict): configs for adhoc process such as centering etc...
            - train_desc (dict): Description. This contains info for `Training Word2Vec`
        """
        assert type(w2v) in [Word2Vec, KeyedVectors], "Invalid word2vec type: {}".format(type(w2v))
        self._w2v = w2v
        self._config = config if config is not None else {}
        self.train_desc = train_desc if train_desc is not None else {}
        self.postprocess()

    def postprocess(self):
        if 'post-process' in self._config:
            post_config = self._config["post-process"]
            if 'pca' in post_config:
                d = post_config["pca"]
                assert self._w2v.wv.vector_size > d, "dim should be lower than original"
                self.do_pca(d)
            if 'abtt' in post_config:
                self.do_all_but_the_top(post_config["abtt"])
        else:
            pass  # do nothing

    def do_pca(self, d):
        self._w2v.wv.vectors = pca(self._w2v.wv.vectors, d)
        self._w2v.wv.vector_size = d

    def do_all_but_the_top(self, d=None):
        if d == None:
            d = self._w2v.wv.vector_size // 100
        self._w2v.wv.vectors = all_but_the_top(self._w2v.wv.vectors, d)

    def _get_vec_with_oov(self, surface):
        if surface in self._w2v:
            return self._pick_vec(surface), False
        else:
            logger.warn("Out-of-vocab: surface={}".format(surface))
            return self._oov_vec(surface), True

    def _oov_vec(self, surface):
        return get_zero_vector(self._w2v.wv.vector_size)

    def _pick_vec(self, surface):
        return self._w2v[surface]

    def get_mean_vector(self, surfaces, ignore_oov=True):
        vecs, oovs = self.query_as_batch(surfaces, return_oov_flag=True)
        if ignore_oov:
            kvs = [not flag for flag in oovs]
            vecs = vecs[kvs]
        if all(oovs):
            logging.warn("given surfaces are all OOV: {}".format(surfaces))
            vecs = np.expand_dims(get_zero_vector(self._w2v.wv.vector_size),
                                  axis=0)
        return vecs.mean(axis=0)

    def cal_phrase_similarity(self, surfaces1, surfaces2):
        """
        calculate phrase similarity.
        currently, averaged phrase embedding is only available.
        """
        v1 = self.get_mean_vector(surfaces1, ignore_oov=True)
        v2 = self.get_mean_vector(surfaces2, ignore_oov=True)
        return cos_sim(v1, v2)


class Morph2vecAPI(WordVectorizer):
    def __init__(self):
        raise NotImplementedError("WIP")


def all_but_the_top(lookup_mat, d):
    """
    args:
        - lookup_mat (np.ndarray): postprocessed vectors, shape = (n_word, dim)
        - d (int): number of principal components
    """
    # centering
    center = lookup_mat.mean(axis=0)
    new_lookup_mat = lookup_mat - np.broadcast_to(center, lookup_mat.shape)

    # remove principal component
    pca = PCA(n_components=d, random_state=46)
    pca.fit(new_lookup_mat)
    sim = new_lookup_mat.dot(pca.components_.T) # shape = (n_word, d)
    new_lookup_mat -= new_lookup_mat.dot(pca.components_.T).dot(pca.components_)
    return new_lookup_mat


def pca(lookup_mat, d):
    pca = PCA(n_components=d, random_state=46)
    return pca.fit_transform(lookup_mat)


def build_w2v_api(w2v, config, w2v_desc):
    return Word2VecAPI(w2v=w2v, config=config, train_desc=w2v_desc)


def build_gensim_w2v(w2v_path, load_config, other_config):
    if load_config["w2v-fmt"] == False:
        w2v = Word2Vec.load(w2v_path)
    elif load_config["w2v-fmt"] == True:
        if load_config["fmt"] == "bin":
            w2v = KeyedVectors.load_word2vec_format(w2v_path, binary=True)
        elif load_config["fmt"] == "txt":
            w2v = KeyedVectors.load_word2vec_format(w2v_path, binary=False)
        else:
            raise ValueError("Invalid format: {}".format(load_config["fmt"]))
    else:
        raise ValueError("w2v-fmt should be bool: {}".format(load_config["w2v-fmt"]))
    return w2v
