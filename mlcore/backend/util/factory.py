class Factory:
    def __init__(self):
        self._factory_index = {}

    def produce(self, name, attr):
        item = self._factory_index.get(name)
        item.set_attr(attr)
        return item
