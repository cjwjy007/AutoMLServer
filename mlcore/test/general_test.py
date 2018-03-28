from mlcore.backend.data_input import DataInput
from mlcore.backend.data_preprocess import DataPreprocess
from mlcore.backend.classifier_train import ClassifierTrain
from mlcore.backend.classifier_test import ClassifierTest
from mlcore.backend.result_merge import ResultMerge
from mlcore.backend.util.enum.classifier.classifier_type import ClassifierType
from mlcore.backend.util.enum.classifier.classifier_attr import ClassifierAttr
from mlcore.backend.util.enum.preprocessor.processor_type import ProcessorType
from mlcore.backend.util.enum.preprocessor.processor_attr import ProcessorAttr

data_input = DataInput()
data_preprocess = DataPreprocess()
data_classifier_train = ClassifierTrain()
data_classifier_test = ClassifierTest()
result_merge = ResultMerge()
###  INPUT DATA ###
data_input.execute(data_source="../data/train/Titanic_data.csv",
                   data_sink="../data/train/train_output.csv")

### DATA PREPROCESS ###
attr = {ProcessorAttr.Target.value: ["PassengerId", "Name", "Ticket", "Cabin"]}
data_preprocess.execute(data_source="../data/train/train_output.csv",
                        data_sink="../data/train/train_preprocess_drop.csv",
                        processor_name=ProcessorType.Drop.value, attr=attr)
data_preprocess.execute(data_source="../data/test/test.csv",
                        data_sink="../data/test/test_preprocess_drop.csv",
                        processor_name=ProcessorType.Drop.value, attr=attr)

attr = {}
data_preprocess.execute(data_source="../data/train/train_preprocess_drop.csv",
                        data_sink="../data/train/train_preprocess_fillna.csv",
                        processor_name=ProcessorType.FillNa.value, attr=attr)
data_preprocess.execute(data_source="../data/test/test_preprocess_drop.csv",
                        data_sink="../data/test/test_preprocess_fillna.csv",
                        processor_name=ProcessorType.FillNa.value, attr=attr)

attr = {ProcessorAttr.Target.value: ["Pclass", "Sex", "Embarked"]}
data_preprocess.execute(data_source="../data/train/train_preprocess_fillna.csv",
                        data_sink="../data/train/train_preprocess_onehot.csv",
                        processor_name=ProcessorType.Onehot.value, attr=attr)
data_preprocess.execute(data_source="../data/test/test_preprocess_fillna.csv",
                        data_sink="../data/test/test_preprocess_onehot.csv",
                        processor_name=ProcessorType.Onehot.value, attr=attr)

attr = {ProcessorAttr.Target.value: ["Fare", "Age", "SibSp", "Parch"]}
data_preprocess.execute(data_source="../data/train/train_preprocess_onehot.csv",
                        data_sink="../data/train/train_preprocess_normalize.csv",
                        processor_name=ProcessorType.Normalize.value, attr=attr)
data_preprocess.execute(data_source="../data/test/test_preprocess_onehot.csv",
                        data_sink="../data/test/test_preprocess_normalize.csv",
                        processor_name=ProcessorType.Normalize.value, attr=attr)

### DATA_TRAIN ###
attr = {ClassifierAttr.Label.value: "Survived"}
data_classifier_train.execute(data_source="../data/train/train_preprocess_normalize.csv",
                              model_sink="../model/RFmodel.model",
                              cv_sink="../data/train/train_cv_RF.csv",
                              classifier_name=ClassifierType.RandomForest.value,
                              attr=attr,
                              n_estimators=20)

attr = {ClassifierAttr.Label.value: "Survived"}
data_classifier_train.execute(data_source="../data/train/train_preprocess_normalize.csv",
                              model_sink="../model/LRmodel.model",
                              cv_sink="../data/train/train_cv_LR.csv",
                              classifier_name=ClassifierType.LogisticRegression.value,
                              attr=attr)

attr = {ClassifierAttr.Label.value: "Survived"}
data_classifier_train.execute(data_source="../data/train/train_preprocess_normalize.csv",
                              model_sink="../model/XGBmodel.model",
                              cv_sink="../data/train/train_cv_XGB.csv",
                              classifier_name=ClassifierType.XGBoost.value,
                              attr=attr)

### DATA TEST ###
attr = {ClassifierAttr.IsProb.value: False}
data_classifier_test.execute(data_source="../data/test/test_preprocess_normalize.csv",
                             model_source="../model/RFmodel.model",
                             data_sink="../data/result/result_RF.csv",
                             classifier_name=ClassifierType.RandomForest.value,
                             attr=attr)

attr = {ClassifierAttr.IsProb.value: False}
data_classifier_test.execute(data_source="../data/test/test_preprocess_normalize.csv",
                             model_source="../model/LRmodel.model",
                             data_sink="../data/result/result_LR.csv",
                             classifier_name=ClassifierType.RandomForest.value,
                             attr=attr)

attr = {ClassifierAttr.IsProb.value: False}
data_classifier_test.execute(data_source="../data/test/test_preprocess_normalize.csv",
                             model_source="../model/XGBmodel.model",
                             data_sink="../data/result/result_XGB.csv",
                             classifier_name=ClassifierType.XGBoost.value,
                             attr=attr)

### MERGE RESULT ###
result_list = ["../data/result/result_RF.csv",
               "../data/result/result_LR.csv",
               "../data/result/result_XGB.csv"]
result_merge.execute(source_data_list=result_list,
                     data_sink="../data/result/result_final.csv",
                     type="bagging")
