import datetime

from automl.mldata.datacontroller import DataController
from automl.mltask.tasknode.basenode import BaseNode
from filepath import result_dir
from mlcore.backend.data_input import DataInput


class DataNode(BaseNode):
    def __init__(self, node):
        super().__init__(node)

    def run(self):
        self.inpath = [DataController.get_datapath_by_id(self.config['dataId'])]
        self.outpath = "{0}/{1}_data_{2}.csv".format(result_dir, self.inpath[0].split('.')[-1],
                                                     str(datetime.datetime.now()))
        data_input = DataInput()
        data_input.execute(data_source=self.inpath[0],
                           data_sink=self.outpath)
        super().run()

    def set_config(self, config):
        super().set_config(config)
        self.config = config
