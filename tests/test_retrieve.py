import unittest
from retrieval_layer.helper import fetch_data

class TestRetrieve(unittest.TestCase):

    def test_fetch_cosmos(self):
        data = fetch_data(source='cosmos')
        self.assertIsInstance(data, list)

    def test_fetch_archive(self):
        data = fetch_data(source='archive')
        self.assertIsInstance(data, list)

    def test_invalid_source(self):
        with self.assertRaises(ValueError):
            fetch_data(source='badsource')

if __name__ == '__main__':
    unittest.main()
