import tempfile
import unittest

import os
import requests

from automl import db
from automl.mldata.datacontroller import DataController
from filepath import data_dir

filename = ''
db.drop_all()
db.create_all()


class TestDataController(unittest.TestCase):
    def test_data_upload(self):
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv') as file:
            files = {'file': file}
            form = {
                'name': 'testname',
                'desc': 'testdesc'
            }
            global filename
            filename = file.name.split(os.sep)[-1]
            requests.post('http://127.0.0.1:9977/data/uploaddata', data=form, files=files)

    def test_get_dataset_count(self):
        self.assertEqual(DataController.get_dataset_count(), 1)

    def test_get_dataset_by_page(self):
        print(DataController.get_dataset_by_page(1))

    def test_get_all_dataset(self):
        print(DataController.get_all_datasets())

    def test_get_data_by_id(self):
        data = DataController.get_data_by_id(1)
        self.assertEqual(data.name, 'testname')
        self.assertEqual(data.desc, 'testdesc')
        self.assertEqual(data.path, os.path.join(data_dir, filename))

    def test_delete_dataset(self):
        DataController.delete_dataset(1)
        self.assertEqual(DataController.get_dataset_count(), 0)
        self.assertEqual(False, os.path.exists(os.path.join(data_dir, filename)))


if __name__ == '__main__':
    unittest.main()
