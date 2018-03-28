from enum import Enum


class ClassifierAttr(Enum):
    '''
        Enums for attributes used for classifiers
        Including:
            Label : the name of the label column of the data
                    type : string
            RequireTune : if a param tuning is needed when training
                    type : boolean
            TuneParams : the params tuning dictionary
                    type : dict
            IsProb : if the result is a probability or not
                    type : boolean
            Checkpoint : if the model needs checkpointing or not
                    type : boolean
            RestorePath : the path used when restoring the model
                    type : string
            CVPath : the path used when outputting cross validation result
                    type : string
    '''
    Label = 'label'
    RequireTune = "require_tune"
    TuneParams = "tune_params"
    IsProb = "is_prob"
    Checkpoint = "checkpoint"
    CheckpointPath = "checkpoint_path"
    RestorePath = "restore_path"
    CVPath = "cv_path"
