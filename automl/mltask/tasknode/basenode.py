from automl.logger.logger import Logger
import datetime


class BaseNode:
    def __init__(self, node):
        self.id = node['id']
        self.type = node['type']
        self.desc = node['desc']
        self.indeg = 0
        self.inpath = []
        self.outpath = ''
        self.status = 0
        self.config = {}

    def set_config(self, config):
        if not config:
            return

    def run(self):
        msg = "node %s: %s has completed!" % (self.id, self.desc)
        print(msg)
        Logger.write_log(msg=msg)
        self.status = 2
