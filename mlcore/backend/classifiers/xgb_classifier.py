from xgboost.sklearn import XGBClassifier
from mlcore.backend.classifiers.classifier import Classifier

class XgbClassifier(Classifier):
    def __init__(self, **kwargs):
        Classifier.__init__(self)
        self._clf = XGBClassifier(**kwargs)