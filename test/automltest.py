import unittest

from automl import db


def test_everything():
    path = './'
    discover = unittest.defaultTestLoader.discover(path, pattern='test*.py')
    runner = unittest.TextTestRunner()
    runner.run(discover)


if __name__ == '__main__':
    test_everything()
