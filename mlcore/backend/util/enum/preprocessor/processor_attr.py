from enum import Enum


class ProcessorAttr(Enum):
    '''
        Enum of attributes used for preprocessors
        Including:
            Target : names of the target columns for process
                     type : list
            Label : name of the label column of the data
                     type : string
            Start : used for down sampling. Marks the start index of the batch selected
                     type : int
            FeatureNum : used for feature selection. Identify the number of features remaining after selection
                     type : int
            Checkpoint : set if a processor needs checkpointing or not
                     type : boolean
    '''
    Target = "target"
    Label = "label"
    Start = "start"
    FeatureNum = "feature_num"
    Checkpoint = "checkpoint"
