import pandas as pd
import numpy as np


class ResultMerge:
    def __init__(self):
        self.__result_array = None
        self.__result = None

    def __bagging(self):
        result = []
        for i in range(self.__result_array.shape[1]):
            result.append(np.argmax(np.bincount(self.__result_array[:, i])))
        self.__result = pd.DataFrame(np.array(result))

    def __averaging(self):
        result = np.mean(self.__result_array, axis=0)
        self.__result = pd.DataFrame(np.array(result))

    def __get_result_array(self, source_data_list):
        result = []
        self.__result = pd.read_csv(source_data_list[0])
        for path in source_data_list:
            data = np.array(pd.read_csv(path)).reshape(-1)
            result.append(data)
        self.__result_array = np.array(result)

    def execute(self, source_data_list, data_sink, type):
        self.__get_result_array(source_data_list)
        if type == "bagging":
            self.__bagging()
        if type == "averaging":
            self.__averaging()
        self.__result.to_csv(data_sink, index=None)



