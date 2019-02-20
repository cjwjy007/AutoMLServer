from automl.errhandler.errhandler import ErrHandler
from automl.mltask.tasknode.binclabalnode import BinaryBalanceNode
from automl.mltask.tasknode.combinationnode import CombinationNode
from automl.mltask.tasknode.datanode import DataNode
from automl.mltask.tasknode.dlseqnode import DLSeqNode
from automl.mltask.tasknode.featselnode import FeatureSelectionNode
from automl.mltask.tasknode.nafillernode import NAFillerNode
from automl.mltask.tasknode.columnsfilternode import ColumnsFilterNode
from automl.mltask.tasknode.lrnode import LogisticRegressionNode
from automl.mltask.tasknode.npzreader import NPZReader
from automl.mltask.tasknode.onehotnode import OneHotNode
from automl.mltask.tasknode.predictionnode import PredictionNode
from automl.mltask.tasknode.rfnode import RandomForestNode


class NodeFactory:
    @staticmethod
    def get_node(node=None):
        try:
            if not node:
                return None
            elif node['type'] == 'model' and node['desc'] == 'DataInput':
                return DataNode(node=node)
            elif node['type'] == 'model' and node['desc'] == 'NPZReader':
                return NPZReader(node=node)
            elif node['type'] == 'multiinput_model' and node['desc'] == 'DataCombination':
                return CombinationNode(node=node)
            elif node['type'] == 'preprocessing' and node['desc'] == 'UnconcernedFilter':
                return ColumnsFilterNode(node=node)
            elif node['type'] == 'preprocessing' and node['desc'] == 'MissingValueFiller':
                return NAFillerNode(node=node)
            elif node['type'] == 'preprocessing' and node['desc'] == 'OneHotEncoder':
                return OneHotNode(node=node)
            elif node['type'] == 'preprocessing' and node['desc'] == 'FeatureSelection':
                return FeatureSelectionNode(node=node)
            elif node['type'] == 'preprocessing' and node['desc'] == 'BinClaBal':
                return BinaryBalanceNode(node=node)
            elif node['type'] == 'multiinput_predition' and node['desc'] == 'Prediction':
                return PredictionNode(node=node)
            elif node['type'] == 'alg' and node['desc'] == 'LogisticRegression':
                return LogisticRegressionNode(node=node)
            elif node['type'] == 'alg' and node['desc'] == 'RandomForest':
                return RandomForestNode(node=node)
            elif node['type'] == 'alg' and node['desc'] == 'Sequential':
                return DLSeqNode(node=node)
        except KeyError as e:
            ErrHandler.handle_err(e)
