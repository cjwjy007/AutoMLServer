import pandas as pd


class DataInput:
    def __init__(self):
        self.__data = None

    def __read(self, data_source):
        self.__data = pd.read_csv(data_source)

    def __write(self, data_sink):
        self.__data.to_csv(data_sink, index=None)

    def execute(self, data_source, data_sink):
        self.__read(data_source)
        self.__write(data_sink)