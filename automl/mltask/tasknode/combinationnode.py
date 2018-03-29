import datetime

from automl.mldata.datacontroller import DataController
from automl.mltask.tasknode.basenode import BaseNode
from mlcore.backend.data_preprocess import DataPreprocess
from mlcore.backend.util.enum.preprocessor.processor_type import ProcessorType


class CombinationNode(BaseNode):
    def __init__(self, node):
        super().__init__(node)

    def run(self):
        # transform maintable to inpath[0]
        mainpath = DataController.get_datapath_by_id(self.config.get('maintable'))
        if mainpath != self.inpath[0] and mainpath == self.inpath[1]:
            self.inpath[0], self.inpath[1] = self.inpath[1], self.inpath[0]
        self.outpath = '{0}_{1}_{2}.csv'.format(self.inpath[0].split('_')[0], self.desc, str(datetime.datetime.now()))
        data_preprocess = DataPreprocess()
        data_preprocess.execute(data_source=self.inpath,
                                data_sink=self.outpath,
                                processor_name=ProcessorType.Combination.value, attr=self.config)
        super().run()

    def set_config(self, config):
        super().set_config(config)
        self.config = config
