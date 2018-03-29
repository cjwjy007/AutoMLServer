from enum import Enum

import pandas as pd

from mlcore.backend.processors.processor import Processor


class CombinationProcessor(Processor):
    class CombinationAttrEnum(Enum):
        Strategy = "strategy"
        Key = "key"

    def __init__(self):
        Processor.__init__(self)
        self._strategy = None
        self._key = None

    def set_attr(self, attr):
        if self.CombinationAttrEnum.Strategy.value in attr:
            self._strategy = attr.get(self.CombinationAttrEnum.Strategy.value)
        if self.CombinationAttrEnum.Key.value in attr:
            self._key = attr.get(self.CombinationAttrEnum.Key.value)

    def process(self, data):
        if self._strategy == 'key':
            data = pd.merge(data[0], data[1], how='left', on=self._key)
        elif self._strategy == 'column':
            data = pd.concat([data[0], data[1]], axis=1)
        elif self._strategy == 'row':
            data = pd.concat([data[0], data[1]], axis=0)
        else:
            data = data[0]
        return data
