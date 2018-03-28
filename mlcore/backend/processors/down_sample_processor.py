import numpy as np
from mlcore.backend.processors.processor import Processor
from enum import Enum


class DownSampleProcessor(Processor):
    class DownSampleAttrEnum(Enum):
        Label = "label"
        Start = "start"
        Checkpoint = "checkpoint"

    def __init__(self):
        Processor.__init__(self)
        self._start = 0
        self._label = None

    def set_attr(self, attr):
        '''
        :param attr:
            attr dict needs:
                label: name of the label column
                start: start index for down sampling
        :return:
        '''
        if self.DownSampleAttrEnum.Label.value in attr:
            self._label = attr.get(self.DownSampleAttrEnum.Label.value)
        if self.DownSampleAttrEnum.Start.value in attr:
            self._start = attr.get(self.DownSampleAttrEnum.Start.value)
        if self.DownSampleAttrEnum.Checkpoint.value in attr:
            checkpoint = attr.get(self.DownSampleAttrEnum.Checkpoint.value)
            self._checkpoint = checkpoint
        self.set_attr(attr)

    def process(self, data):
        data_0 = data[data[self._label] == 0]
        data_1 = data[data[self._label] == 1]
        length_0 = data_0.shape[0]
        length_1 = data_1.shape[0]
        if length_0 > length_1:
            end = self._start + length_1
            if end > length_0:
                end = length_0
            data_0_downsample = data_0.iloc[self._start:end]
            data_result = data_1.append(data_0_downsample)
            length = data_result.shape[0]
            result_list = np.arange(length)
            np.random.shuffle(result_list)
            data_result = data_result.iloc[result_list]
        else:
            end = self._start + length_0
            if end > length_1:
                end = length_1
            data_1_downsample = data_1.iloc[self._start:end]
            data_result = data_0.append(data_1_downsample)
            length = data_result.shape[0]
            result_list = np.arange(length)
            np.random.shuffle(result_list)
            data_result = data_result.iloc[result_list]
        return data_result
