class Pipeline:
    def __init__(self):
        self._pipeline_list = []

    def add(self,item):
        self._pipeline_list.append(item)

    def execute(self, data, execution_params):
        return data

    def _checkpoint(self):
        result = ''
        for item in self._pipeline_list:
            name = item.get_class_name()
            result = result + name + ' / '
        return result

