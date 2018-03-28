from util.pipeline import Pipeline
from util.factory import Factory


class Module:
    def __init__(self):
        self._pipeline = Pipeline()
        self._factory = Factory()
        self._execution_params = {}

    def set_execution_params(self, execution_params):
        self._execution_params = execution_params

    def add(self, name, attr):
        item = self._factory.produce(name, attr)
        self._pipeline.add(item)

    def execute(self, data):
        return self._pipeline.execute(data, self._execution_params)
