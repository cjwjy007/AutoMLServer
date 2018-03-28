import numpy as np
from mlcore.backend.processors.processor import Processor
from enum import Enum

class NormalizeProcessor(Processor):
    class NormalizeAttrEnum(Enum):
        Target = "target"

    def __init__(self):
        Processor.__init__(self)
        self._target = None

    def set_attr(self, attr):
        '''
            :param attr:
                attr dict needs:
                target : name of the target column (None for normalize all columns)
            :return:
        '''
        if self.NormalizeAttrEnum.Target.value in attr:
            self._target = attr.get(self.NormalizeAttrEnum.Target.value)

    def process(self, data):
        if self._target is None:
            data = data.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))
        else:
            data[self._target] = data[self._target].apply(lambda x: (x-np.min(x)) / (np.max(x) - np.min(x)))
        return data
