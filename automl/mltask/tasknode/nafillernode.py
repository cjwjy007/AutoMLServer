import datetime

from automl.mltask.tasknode.basenode import BaseNode
from mlcore.backend.data_preprocess import DataPreprocess
from mlcore.backend.util.enum.preprocessor.processor_type import ProcessorType


class NAFillerNode(BaseNode):
    def __init__(self, node):
        super().__init__(node)

    def run(self):
        self.outpath = '{0}_{1}_{2}.csv'.format(self.inpath[0].split('_')[0], self.desc, str(datetime.datetime.now()))
        data_preprocess = DataPreprocess()
        attr = {}
        data_preprocess.execute(data_source=self.inpath[0],
                                data_sink=self.outpath,
                                processor_name=ProcessorType.FillNa.value, attr=attr)
        super().run()

    def set_config(self, config):
        super().set_config(config)
        self.config = config