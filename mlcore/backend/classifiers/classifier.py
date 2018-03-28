from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib
import mlcore.backend.util.checkpoint as checkpoint
from sklearn.model_selection import cross_val_score
from mlcore.backend.util.enum.preprocessor.processor_attr import ProcessorAttr
import numpy as np
from mlcore.backend.util.enum.classifier.classifier_attr import ClassifierAttr

class Classifier:
    def __init__(self):
        self._clf = None
        self._label = None
        self._require_tune = False
        self._tune_params = None
        self._is_prob = True
        self._checkpoint = True
        self._checkpoint_path = None
        self._cv_path = None

    def set_specific_attr(self, attr):
        pass

    def set_attr(self, attr):
        if ClassifierAttr.Label.value in attr:
            label = attr.get(ClassifierAttr.Label.value)
            self._label = label
        if ClassifierAttr.RequireTune.value in attr:
            require_tune = attr.get(ClassifierAttr.RequireTune.value)
            self._require_tune = require_tune
        if ClassifierAttr.TuneParams.value in attr:
            tune_params = attr.get(ClassifierAttr.TuneParams.value)
            self._tune_params = tune_params
        if ClassifierAttr.IsProb.value in attr:
            is_prob = attr.get(ClassifierAttr.IsProb.value)
            self._is_prob = is_prob
        if ClassifierAttr.Checkpoint.value in attr:
            checkpoint = attr.get(ClassifierAttr.Checkpoint.value)
            self._checkpoint = checkpoint
        if ClassifierAttr.CheckpointPath.value in attr:
            checkpoint_path = attr.get(ClassifierAttr.CheckpointPath.value)
            self._checkpoint_path = checkpoint_path
        if ClassifierAttr.RestorePath.value in attr:
            restore_path = attr.get(ClassifierAttr.RestorePath.value)
            self._clf = joblib.load(restore_path)
        if ClassifierAttr.CVPath.value in attr:
            self._cv_path = attr.get(ClassifierAttr.CVPath.value)
        self.set_specific_attr(attr)

    def train(self, data):
        target = self._label
        X = np.array(data.drop([target],axis=1))
        y = np.array(data[target]).reshape(-1)
        if self._require_tune:
            self.param_tuning(data)
        self._clf.fit(X, y)
        if self._checkpoint:
            if self._checkpoint_path is None:
                path = checkpoint.get_checkpoint("model", self.get_class_name())
            else:
                path = self._checkpoint_path
            joblib.dump(self._clf, path)
        return self.cross_validation(data)

    def param_tuning(self, data):
        target = self._label
        X = np.array(data.drop([target], axis=1))
        y = np.array(data[target]).reshape(-1)
        grid = GridSearchCV(self._clf, cv=5, n_jobs=2, param_grid=self._tune_params)
        grid.fit(X, y)
        self._clf = grid.best_estimator_

    def cross_validation(self, data):
        target = self._label
        X = np.array(data.drop([target], axis=1))
        y = np.array(data[target]).reshape(-1)
        return cross_val_score(self._clf, X, y, cv=5)

    def predict(self,data):
        is_prob = self._is_prob
        if is_prob:
            result = self._clf.predict_proba(data)[:,1]
        else:
            result = self._clf.predict(data)
        return result

    def get_class_name(self):
        return self.__class__.__name__
