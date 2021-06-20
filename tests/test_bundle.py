import os
import unittest
import filecmp
from shutil import rmtree
from dogsbody.bundle import create_bundle, extract_bundle


class TestCreateExtract(unittest.TestCase):

    DATA = {
        'data': os.path.join(os.path.dirname(__file__), 'data'),
        'source': os.path.join(os.path.dirname(__file__), 'test_source'),
        'output': os.path.join(os.path.dirname(__file__), 'data', 'output'),
        'filename': os.path.join(os.path.dirname(__file__), 'data', 'test.zip'),
    }

    def setUp(self):
        os.makedirs(self.DATA['data'])

    def tearDown(self):
        rmtree(self.DATA['data'])

    def test_basic(self):
        create_bundle(self.DATA['source'], self.DATA['filename'], '1234')
        extract_bundle(self.DATA['filename'], self.DATA['output'], '1234')

        common = ['main.sh', 'readme.txt']
        result, _, _ = filecmp.cmpfiles(self.DATA['source'], self.DATA['output'], common)
        self.assertEqual(result, common)


if __name__ == '__main__':
    unittest.main()
