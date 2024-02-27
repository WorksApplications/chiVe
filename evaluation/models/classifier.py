
import logging
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sys import argv

logger = logging.getLogger(argv[0]).getChild(__file__)


def build_classifier(method, other_config):
    if method == "logreg":
        clf = LogisticRegression()
    elif method == "knn":
        clf = KNeighborsClassifier(n_neighbors=other_config["k"])
    else:
        raise ValueError("Invalid method: {}".format(method))
    return clf
