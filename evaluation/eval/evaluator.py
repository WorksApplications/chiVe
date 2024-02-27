
import numpy as np
from scipy.stats import spearmanr
from sklearn.model_selection import cross_val_score, StratifiedKFold


class Evaluator():
    def __init__(self, dataset):
        self.dataset = dataset

    def predict_all(self, batchsize=1):
        for batch in self.dataset.batch_iter(batchsize=batchsize, rand_flg=False):
            for inst in batch:
                self._predict_one(inst)

    def run(self):
        self.predict_all()
        return self.get_eval_metric()

    def get_eval_metric(self):
        raise NotImplementedError()

    def _predict_one(self, inst):
        raise NotImplementedError()


class W2VSimilarityEvaluator(Evaluator):
    def __init__(self, dataset, w2v_api):
        super(W2VSimilarityEvaluator, self).__init__(dataset=dataset)
        self.w2v_api = w2v_api

    def get_eval_metric(self):
        # spearman corr
        human_scores = [
            b[0].gold for b in self.dataset.batch_iter(1, rand_flg=False)]
        auto_scores = [
            b[0].model_pred for b in self.dataset.batch_iter(1, rand_flg=False)]
        # assert all(human_scores), "Contain invalid gold data"
        # assert all(auto_scores), "Contain invalid prediction"
        corr = spearmanr(human_scores, auto_scores)[0]
        return corr

    def _predict_one(self, inst):
        e1, e2, gold_score = inst.get_content()
        pred = self.w2v_api.cal_phrase_similarity(e1, e2)
        inst.set_model_prediction(pred)


class ClassificationEvaluator(Evaluator):
    def __init__(self, dataset, w2v_api, clf):
        super(ClassificationEvaluator, self).__init__(dataset=dataset)
        self.w2v_api = w2v_api
        self.clf = clf

    def run_kfold(self, k=10):
        cv = get_sklearn_kfoldcv(k)
        txt_xs, ys = self.dataset.get_xys()
        xs = np.array([self.w2v_api.get_mean_vector(doc) for doc in txt_xs])
        scores = cross_val_score(self.clf, xs, ys, cv=cv)
        return {"scores": scores, "mean": np.mean(scores), "variance": np.var(scores)}


def get_sklearn_kfoldcv(n_splits, seed=46):
    return StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
