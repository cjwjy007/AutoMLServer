import datetime
import time

from automl.errhandler.errhandler import ErrHandler
from automl.mltask.tasknode.basenode import BaseNode
from mlcore.backend.classifier_train import ClassifierTrain
from mlcore.backend.util.enum.classifier.classifier_attr import ClassifierAttr
from mlcore.backend.util.enum.classifier.classifier_type import ClassifierType


class LogisticRegressionNode(BaseNode):
    def __init__(self, node):
        super().__init__(node)

    def run(self):
        now = str(datetime.datetime.now())
        self.outpath = '{0}_{1}_{2}.model'.format(self.inpath[0].split('_')[0], self.desc, now)
        cv_sink = '{0}_{1}_{2}.csv'.format(self.inpath[0].split('_')[0], self.desc, now)
        data_classifier_train = ClassifierTrain()
        attr = {ClassifierAttr.Label.value: self.config['y']}
        data_classifier_train.execute(data_source=self.inpath[0],
                                      model_sink=self.outpath,
                                      cv_sink=cv_sink,
                                      classifier_name=ClassifierType.LogisticRegression.value,
                                      attr=attr,
                                      **self.config['param'])

        super().run()

    def set_config(self, config):
        super().set_config(config)
        self.config = config
        if not self.config.get('param'):
            self.config['param'] = {}
        else:
            if 'C' in self.config['param']:
                self.config['param']['C'] = float(self.config['param']['C'])