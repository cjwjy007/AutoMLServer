import numpy as np
import pandas as pd
from mlcore.backend.processors.processor import Processor
from enum import Enum


class FillNaProcessor(Processor):

    def __init__(self):
        Processor.__init__(self)
        self._target = None
        self.delete_columns_name = []

    def set_attr(self, attr):
        pass

    def process(self, data):
        # data = data.fillna(method="pad")
        for col_name in data.columns:
            self._filling_column(data=data, col=col_name)

        data.drop(self.delete_columns_name, axis=1, inplace=True)
        return data

    def _filling_column(self, data, col=None):
        train_column = data[col]
        # not contain missing values
        if not train_column.isnull().any():
            return

        data_notnull = train_column[train_column.notnull()]
        # handle missing value
        while True:
            # categorical value
            if data_notnull.dtype is np.dtype(np.object):
                train_column.loc[train_column.isnull()] = 'nan_mark'
                break
            # numerical value
            else:
                # filling in the mean value or mode value
                # if True if random.randint(0, 1) == 0 else False:
                #     train_column.loc[train_column.isnull()] = data_notnull.mean()
                #
                # else:
                #     train_column.loc[train_column.isnull()] = data_notnull.mode()[0]
                average = train_column.mean()
                std = train_column.std()
                nan_count = train_column.isnull().sum()
                rand_input = np.random.randint(average - std,
                                               average + std, size=nan_count)
                train_column[np.isnan(train_column)] = rand_input
                break
