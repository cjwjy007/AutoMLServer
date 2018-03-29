from mlcore.backend.processors.combination_processor import CombinationProcessor
from mlcore.backend.processors.down_sample_processor import DownSampleProcessor
from mlcore.backend.processors.model_feature_selection_processor import ModelFeatureSelectionProcessor
from mlcore.backend.processors.normalize_processor import NormalizeProcessor
from mlcore.backend.processors.drop_processor import DropProcessor
from mlcore.backend.processors.fillna_processor import FillNaProcessor
from mlcore.backend.processors.one_hot_processor import OneHotProcessor
from mlcore.backend.util.enum.preprocessor.processor_type import ProcessorType
import pandas as pd


class DataPreprocess:
    def __init__(self):
        self.__processor = None
        self.__attr_dict = {}
        self.__processor_dict = {
            ProcessorType.Normalize.value: NormalizeProcessor(),
            ProcessorType.DownSample.value: DownSampleProcessor(),
            ProcessorType.ModelFeatureSelection.value: ModelFeatureSelectionProcessor(),
            ProcessorType.Drop.value: DropProcessor(),
            ProcessorType.FillNa.value: FillNaProcessor(),
            ProcessorType.Onehot.value: OneHotProcessor(),
            ProcessorType.Combination.value: CombinationProcessor()
        }

    def __set_processor(self, processor_name: str):
        self.__processor = self.__processor_dict.get(processor_name)

    def __set_attr(self, attr_dict: dict):
        self.__attr_dict = attr_dict

    def execute(self, data_source: str, data_sink: str, processor_name: str, attr: dict):
        self.__set_processor(processor_name)
        self.__set_attr(attr)
        self.__processor.set_attr(self.__attr_dict)
        if isinstance(data_source, list):
            input_data = []
            for ds in data_source:
                input_data.append(pd.read_csv(ds))
        else:
            input_data = pd.read_csv(data_source)
        output_data = self.__processor.execute(input_data)
        output_data.to_csv(data_sink, index=None)
