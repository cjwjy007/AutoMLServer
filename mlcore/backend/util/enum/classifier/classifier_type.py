from enum import Enum


class ClassifierType(Enum):
    '''
        Enum for names of the classifiers
        Including:
            RandomForest : random forest classifier
                           need attr : Label, RequireTune(default False), TuneParams, IsProb(default True),
                                       Checkpoint(default False), RestorePath
            LogisticRegression : logistic regression classifier
                           need attr : Label, RequireTune(default False), TuneParams, IsProb(default True),
                                       Checkpoint(default False), RestorePath
            XGBoost : xgboost classifier
                           need attr : Label, RequireTune(default False), TuneParams, IsProb(default True),
                                       Checkpoint(default False), RestorePath
    '''
    RandomForest = "random_forest"
    LogisticRegression = "logistic_regression"
    XGBoost = "xgboost"
