import numpy as np
import pandas as pd
from mlcore.backend.processors.processor import Processor
from enum import Enum

class DropProcessor(Processor):
    class DropAttrEnum(Enum):
        Target = "target"

    def __init__(self):
        Processor.__init__(self)
        self._target = None

    def set_attr(self, attr):
        '''
            :param attr:
                attr dict needs:
                target : names of the target column (None for drop all columns)
            :return:
        '''
        if self.DropAttrEnum.Target.value in attr:
            self._target = attr.get(self.DropAttrEnum.Target.value)

    def process(self, data):
        if self._target is None:
            data = pd.DataFrame()
        else:
            data = data.drop(self._target, axis=1)
        return data
