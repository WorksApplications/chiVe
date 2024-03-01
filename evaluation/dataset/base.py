
import numpy as np


class BaseDataset():
    def __init__(self, samples, name=None):
        _type = type(samples)
        assert _type == list or _type == np.ndarray, "Should be list or ndarray"
        self._samples = samples if type(samples) == np.ndarray else np.array(samples)
        self.name = name

    def __repr__(self):
        return "<{} name={}>".format(self.__class__.__name__, self.name)

    def __getitem__(self, item):
        return self._samples[item]

    def __len__(self):
        return len(self._samples)

    def split(self):
        raise NotImplementedError()

    def batch_iter(self, batchsize, rand_flg):
        assert batchsize > 0
        indices = np.random.permutation(len(self)) if rand_flg else np.arange(len(self))
        for start in range(0, len(self), batchsize):
            yield self[indices[start: start+batchsize]]

    def batch_iter_as_ndarray(self, batchsize, rand_flg):
        raise NotImplementedError("Not available")

    def get_basic_stats(self):
        raise NotImplementedError()

    def cal_stats(self):
        return {"n_sample": len(self._samples)}


class BaseInstance():
    def __init__(self):
        self.model_pred = None

    def get_content(self):
        raise NotImplementedError()

    def set_model_prediction(self, pred):
        self.model_pred = pred
