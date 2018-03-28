import unittest

from automl.mlcomp.compcontroller import CompController


class TestCompController(unittest.TestCase):
    def test_get_data_columns(self):
        test_param1 = {
            'graph_id': 'test',
            'node_id': 'd1565430'
        }
        test_param2 = {
            'graph_id': 'test',
            'node_id': '02f747c9'
        }
        test_result1 = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare',
                        'Cabin', 'Embarked']
        test_result2 = ['PassengerId', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin',
                        'Embarked']
        self.assertEqual(test_result1, CompController.get_data_columns(**test_param1))
        self.assertEqual(test_result2, CompController.get_data_columns(**test_param2))

    def test_get_data_columns_detail(self):
        test_param1 = {
            'graph_id': 'test',
            'node_id': 'bdda524d',
            'col_name': 'Survived',
        }
        test_param2 = {
            'graph_id': 'test',
            'node_id': '9e32bd30',
            'col_name': 'PassengerId'
        }
        test_result1 = {'count': 891.0, 'mean': 0.3838383838383838, 'std': 0.4865924542648585, 'min': 0.0, '25%': 0.0,
                        '50%': 0.0, '75%': 1.0, 'max': 1.0}
        test_result2 = {'count': 418.0, 'mean': 1100.5, 'std': 120.81045760473994, 'min': 892.0, '25%': 996.25,
                        '50%': 1100.5, '75%': 1204.75, 'max': 1309.0}
        self.assertEqual(test_result1, CompController.get_data_columns_detail(**test_param1))
        self.assertEqual(test_result2, CompController.get_data_columns_detail(**test_param2))

    def test_get_config(self):
        test_param1 = {
            'graph_id': 'test',
            'node_id': 'd1565430'
        }
        test_param2 = {
            'graph_id': 'test',
            'node_id': '02f747c9'
        }
        test_result1 = {
            "strategy": "columns",
            "columns": [
                "Pclass",
                "Sex",
                "Embarked"
            ]
        }
        test_result2 = {
            'columns': [
                {
                    "key": "0",
                    "label": "PassengerId"
                },
                {
                    "key": "2",
                    "label": "Name"
                },
                {
                    "key": "7",
                    "label": "Ticket"
                },
                {
                    "key": "9",
                    "label": "Cabin"
                }
            ]
        }

        CompController.set_config(config=test_result1, **test_param1)
        CompController.set_config(config=test_result2, **test_param2)
        self.assertEqual(test_result1, CompController.get_config(**test_param1))
        self.assertEqual(test_result2, CompController.get_config(**test_param2))


if __name__ == '__main__':
    unittest.main()
