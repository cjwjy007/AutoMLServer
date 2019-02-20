from mlcore.backend.classifiers.lr_classifer import LRClassifier
from mlcore.backend.classifiers.rf_classifier import RFClassifier
from mlcore.backend.classifiers.xgb_classifier import XgbClassifier
from mlcore.backend.util.enum.classifier.classifier_type import ClassifierType
import pandas as pd
from sklearn.externals import joblib


class ClassifierTest:
    def __init__(self):
        self.__classifier = None
        self.__attr_dict = {}
        self.__classifier_dict = {
            ClassifierType.RandomForest.value: RFClassifier(),
            ClassifierType.LogisticRegression.value: LRClassifier(),
            ClassifierType.XGBoost.value: XgbClassifier()
        }

    def __set_classifer(self, classifier_name):
        self.__classifier = self.__classifier_dict[classifier_name]

    def __set_attr(self, attr_dict, model_source):
        self.__attr_dict = attr_dict
        self.__attr_dict["checkpoint"] = True
        self.__attr_dict["restore_path"] = model_source

    def execute(self, data_source, model_source, data_sink, classifier_name, attr):
        self.__set_classifer(classifier_name)
        self.__set_attr(attr, model_source)
        self.__classifier.set_attr(self.__attr_dict)
        input_data = pd.read_csv(data_source)
        columns_mask = self._ClassifierTest__classifier._clf.columns_mask
        input_data = input_data[columns_mask]
        if "restore_path" in self.__attr_dict:
            self.__classifier = joblib.load(self.__attr_dict["restore_path"])
        result = self.__classifier.predict(input_data.as_matrix())
        input_data["RESULT"] = result
        output_data = input_data["RESULT"]
        output_data.to_csv(data_sink, index=None, header=True)
