import mlcore.backend.util.checkpoint as checkpoint

class Processor:
    def __init__(self):
        self._checkpoint = False

    def set_attr(self, attr):
        pass

    def process(self, data):
        return data

    def execute(self, data):
        result = self.process(data)
        if self._checkpoint:
            path = checkpoint.get_checkpoint("model", self.get_class_name())
            result.to_csv(path)
        return result

    def get_class_name(self):
        return self.__class__.__name__


