import datetime

from sklearn.neighbors import NearestNeighbors
import pandas as pd

from automl.mltask.tasknode.basenode import BaseNode
from mlcore.backend.data_input import DataInput
from mlcore.backend.data_preprocess import DataPreprocess
from mlcore.backend.util.enum.preprocessor.processor_type import ProcessorType


class BinaryBalanceNode(BaseNode):
    def __init__(self, node):
        super().__init__(node)

    def run(self):
        self.outpath = '{0}_{1}_{2}.csv'.format(self.inpath[0].split('_')[0], self.desc, str(datetime.datetime.now()))
        data_input = DataInput()
        data_input.execute(data_source=self.inpath[0],
                           data_sink=self.outpath)
        super().run()

    def set_config(self, config):
        super().set_config(config)
        self.config = config
        # sample 1nn point

    def sample_1nn(self, sample_n=5, major=None, minor=None):
        print("---------dealing imbalance data---------")
        major_df = self.train_df.ix[self.train_y == major]
        minor_df = self.train_df.ix[self.train_y == minor]
        major_df.drop(self.train_y.name, axis=1, inplace=True)
        minor_df.drop(self.train_y.name, axis=1, inplace=True)
        nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(minor_df.values)
        dis_dic = pd.DataFrame(index=range(len(major_df.columns)), columns=['id', 'distance'])
        for idx in range(len(major_df)):
            distance, indices = nbrs.kneighbors(major_df.iloc[idx].values.reshape(1, -1))
            dis_dic.ix[idx, 'id'] = major_df.index[idx]
            dis_dic.ix[idx, 'distance'] = distance[0][0]
        dis_dic = dis_dic.sort_values(by='distance', axis=0, ascending=True).reset_index(drop=True)
        index_to_drop = dis_dic.ix[sample_n:, 'id'].values
        return index_to_drop

    def transform_imbalance_data(self):
        values_y = self.train_y.value_counts()
        values_size = values_y.size
        min_balance_percentage_name = None
        min_value_count = values_y[0]
        for idx, val in enumerate(values_y):
            balance_percentage = val / (self.train_y.size / values_size)
            if balance_percentage < 0.2 and val <= min_value_count:
                min_balance_percentage_name = idx
                min_value_count = val
        # data is balanced
        if min_balance_percentage_name is None:
            return
        # balance data
        # if min_value_count > 10000 oversample column to min_value_count
        # if min_value_count < 10000 oversample column to 1.5 * min_value_count
        if values_size == 2:
            major, major_value = None, None
            minor, minor_value = None, None
            for idx, val in enumerate(values_y):
                if idx is not min_balance_percentage_name:
                    major, major_value = idx, val
                else:
                    minor, minor_value = idx, val
            index_to_drop = self.sample_1nn(sample_n=minor_value, major=major, minor=minor).astype(int)
            self.train_df.drop(index_to_drop, inplace=True)
            self.train_df.reset_index(drop=True, inplace=True)
        else:
            if min_value_count < 10000:
                min_value_count = int(min_value_count * 1.5)

            for idx, val in enumerate(values_y):
                if idx is not min_balance_percentage_name:
                    if val > min_value_count:
                        index_to_drop = self.train_y.ix[self.train_y == idx].sample(n=val - min_value_count,
                                                                                    random_state=7).index
                        self.train_df.drop(index_to_drop, inplace=True)
                        self.train_df.reset_index(drop=True, inplace=True)