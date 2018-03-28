from mlcore.backend.classifiers.lr_classifer import LRClassifier
from mlcore.backend.classifiers.rf_classifier import RFClassifier
from mlcore.backend.classifiers.xgb_classifier import XgbClassifier
from mlcore.backend.util.enum.classifier.classifier_type import ClassifierType
import pandas as pd


class ClassifierTrain:
    def __init__(self):
        self.__classifier = None
        self.__attr_dict = {}

    def __set_classifer(self, classifier_name, **kwargs):
        if classifier_name == ClassifierType.RandomForest.value:
            self.__classifier = RFClassifier(**kwargs)
        elif classifier_name == ClassifierType.LogisticRegression.value:
            self.__classifier = LRClassifier(**kwargs)
        elif classifier_name == ClassifierType.XGBoost.value:
            self.__classifier = XgbClassifier(**kwargs)

    def __set_attr(self, attr_dict, model_sink):
        self.__attr_dict = attr_dict
        self.__attr_dict["checkpoint"] = True
        self.__attr_dict["checkpoint_path"] = model_sink

    def execute(self, data_source, model_sink, cv_sink, classifier_name, attr, **kwargs):
        self.__set_classifer(classifier_name, **kwargs)
        self.__set_attr(attr, model_sink)
        self.__classifier.set_attr(self.__attr_dict)
        input_data = pd.read_csv(data_source)
        cv_result = self.__classifier.train(input_data)
        with open(cv_sink, "w", encoding="utf8") as cv_file:
            cv_file.write('cross_validation\n')
            for result in cv_result:
                cv_file.write(str(result))
                cv_file.write("\n")
