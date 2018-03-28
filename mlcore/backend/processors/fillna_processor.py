import numpy as np
import pandas as pd
from mlcore.backend.processors.processor import Processor
from enum import Enum

class FillNaProcessor(Processor):

    def __init__(self):
        Processor.__init__(self)
        self._target = None

    def set_attr(self, attr):
        pass

    def process(self, data):
        data = data.fillna(method="pad")
        return data