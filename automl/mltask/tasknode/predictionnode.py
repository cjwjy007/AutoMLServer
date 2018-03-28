import datetime

from automl.mltask.tasknode.basenode import BaseNode
from mlcore.backend.classifier_test import ClassifierTest
from mlcore.backend.util.enum.classifier.classifier_attr import ClassifierAttr
from mlcore.backend.util.enum.classifier.classifier_type import ClassifierType


class PredictionNode(BaseNode):
    def __init__(self, node):
        super().__init__(node)

    def run(self):
        ds = ''
        ms = ''
        if len(self.inpath) >= 2:
            for ip in reversed(self.inpath):
                if ip.split('.')[-1] == 'csv' and not ds:
                    ds = ip
                elif ip.split('.')[-1] == 'model' and not ms:
                    ms = ip

        if ds and ms:
            self.inpath = [ds, ms]
            self.outpath = '{0}_{1}_{2}.csv'.format(ds.split('_')[0], self.desc, str(datetime.datetime.now()))
            data_classifier_test = ClassifierTest()
            attr = {ClassifierAttr.IsProb.value: False}
            data_classifier_test.execute(data_source=ds,
                                         model_source=ms,
                                         data_sink=self.outpath,
                                         classifier_name=ClassifierType.RandomForest.value,
                                         attr=attr)
        super().run()

    def set_config(self, config):
        super().set_config(config)
        self.config = config
