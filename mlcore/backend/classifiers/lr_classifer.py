from mlcore.backend.classifiers.classifier import Classifier
from sklearn.linear_model import LogisticRegression


class LRClassifier(Classifier):
    def __init__(self, **kwargs):
        Classifier.__init__(self)
        self._clf = LogisticRegression(**kwargs)