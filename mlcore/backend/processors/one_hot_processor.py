import numpy as np
import pandas as pd
from mlcore.backend.processors.processor import Processor
from enum import Enum

class OneHotProcessor(Processor):
    class OneHotAttrEnum(Enum):
        Target = "target"

    def __init__(self):
        Processor.__init__(self)
        self._target = None

    def set_attr(self, attr):
        '''
            :param attr:
                attr dict needs:
                target : names of the target column (None for one-hot encode all columns)
            :return:
        '''
        if self.OneHotAttrEnum.Target.value in attr:
            self._target = attr.get(self.OneHotAttrEnum.Target.value)

    def process(self, data):
        if self._target is None:
            data = pd.get_dummies(data)
        else:
            data = pd.get_dummies(data, columns=self._target)
        return data
