import unittest
from archive_pipeline.archive_logic import archive_old_cosmos_records

class TestArchive(unittest.TestCase):

    def test_archive_old_records(self):
        count = archive_old_cosmos_records()
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)

if __name__ == '__main__':
    unittest.main()
