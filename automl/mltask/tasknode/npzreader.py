from automl.mldata.datacontroller import DataController
from automl.mltask.tasknode.basenode import BaseNode


class NPZReader(BaseNode):
    def __init__(self, node):
        super().__init__(node)

    def run(self):
        self.inpath = [DataController.get_datapath_by_id(self.config['dataId'])]
        self.outpath = self.inpath[0]
        super().run()

    def set_config(self, config):
        super().set_config(config)
        self.config = config
