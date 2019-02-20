import numpy as np
import pandas as pd
from mlcore.backend.processors.processor import Processor
from enum import Enum
from sklearn import preprocessing


class OneHotProcessor(Processor):
    class OneHotAttrEnum(Enum):
        Target = "target"

    def __init__(self):
        Processor.__init__(self)
        self._target = None
        self.train_df = None

    def set_attr(self, attr):
        '''
            :param attr:
                attr dict needs:
                target : names of the target column (None for one-hot encode all columns)
            :return:
        '''
        if self.OneHotAttrEnum.Target.value in attr:
            self._target = attr.get(self.OneHotAttrEnum.Target.value)

    def process(self, data):
        # if self._target is None:
        #     data = pd.get_dummies(data)
        # else:
        #     data = pd.get_dummies(data, columns=self._target)
        # test if there are too many unique values,cast minority to MINORITY_MARK
        self.train_df = data
        return self.data_encode()

    def data_encode(self):
        print("---------Start data encoding---------")
        encoded_columns = pd.DataFrame()
        for col_name in self.train_df.columns:
            encoded_columns = self.column_encode(col=col_name, encoded_columns=encoded_columns)
        return encoded_columns

    def column_encode(self, col=None, encoded_columns=None):
        print("encoding {name}".format(name=col))
        train_column = self.train_df[col]
        encoded_column = None
        if train_column.dtype is np.dtype(np.object):
            while True:
                # test if there are too many unique values,cast minority to MINORITY_MARK
                train_column = self.minority_encode(train_column)
                # ont-hot encoder
                encoded_column = pd.get_dummies(train_column, prefix=train_column.name)
                break
        if encoded_column is not None:
            encoded_columns = pd.concat([encoded_columns, encoded_column], axis=1)
        else:
            encoded_columns = pd.concat([encoded_columns, train_column], axis=1)
        return encoded_columns

    def minority_encode(self, train_column):
        value_counts_dic = train_column.value_counts()
        if value_counts_dic.values.size > 100:
            min_value_counts = value_counts_dic[100]
            # LabelEncoder to accelerate the loop
            train_column = pd.Series(preprocessing.LabelEncoder().fit_transform(train_column),
                                     name=train_column.name)
            value_counts_dic = train_column.value_counts()
            print("column {name} is performing {times} times loop which may take a long time"
                  .format(name=train_column.name, times=len(train_column)))
            for idx, val in enumerate(train_column):
                if value_counts_dic[val] < min_value_counts:
                    train_column[idx] = -1

        return train_column
