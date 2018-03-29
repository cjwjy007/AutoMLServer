from enum import Enum


class ProcessorType(Enum):
    '''
        Enum of different types of preprocessors
        Including:
            DownSample : do a down sample process
                         need attr : Label, Start(default 0), Checkpoint(default False)
            ModelFeatureSelection : do a feature selection process using a GBDT model
                         need attr : Label, Checkpoint(default False)
            Normalize : do a normalize process
                         need attr : Target, Checkpoint(default False)
    '''
    DownSample = "down_sample"
    ModelFeatureSelection = "model_feature_selection"
    Normalize = "normalize"
    Drop = "drop"
    FillNa = "fillna"
    Onehot = "onehot"
    Combination = 'combination'

