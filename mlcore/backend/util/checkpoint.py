import mlcore.backend.configs.paths as paths
import time


def get_checkpoint(type, name):
    time_str = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
    HOME = paths.CHECKPOINT_ROOT
    type_dict = {"data" : "data",
                 "model": "model",
                 "preprocess_pipeline": "data",
                 "classifier_pipeline": "model"}
    suffix_dict = {"data" : ".csv",
                   "model": ".model",
                   "preprocess_pipeline": ".txt",
                   "classifier_pipeline": ".txt"}
    folder = type_dict.get(type)
    suffix = suffix_dict.get(type)
    path = HOME + "/checkpoint/" + folder + "/" + time_str + "_" + name + suffix
    return path

