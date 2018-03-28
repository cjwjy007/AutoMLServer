from mlcore.backend.processors.processor import Processor
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import GradientBoostingClassifier
from enum import Enum


class ModelFeatureSelectionProcessor(Processor):
    class ModelFeatureSelectionAttrEnum(Enum):
        Label = "label"

    def __init__(self):
        Processor.__init__(self)
        self._label = None
        self._selected_feature = None

    def set_attr(self, attr):
        '''
        :param attr:
         attr dict needs:
            label : name of the label column
        :return:
        '''

        if self.ModelFeatureSelectionAttrEnum.Label.value in attr:
            self._label = attr.get(self.ModelFeatureSelectionAttrEnum.Label.value)


    def process(self, data):
        X = data.drop([self._label],axis=1)
        y = data[self._label]
        if self._selected_feature is None:
            mask = SelectFromModel(GradientBoostingClassifier()).fit(X,y).get_support()
            self._selected_feature = mask
            data = data.iloc[:,self._selected_feature]
        else:
            data = data.iloc[:,self._selected_feature]
        return data