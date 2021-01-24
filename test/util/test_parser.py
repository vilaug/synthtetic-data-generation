import pathlib
import sys
import unittest

src_dir = "/workdir"
sys.path.insert(1, src_dir)

from src.util.parser import Parser  # noqa: E402


class ParserTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_parse_args(self):
        parsed_args = self.parser.parse_args(['-m', 'HDPE', '-p', '100', '-c', '1',
                                              '-i', '1', '-b', 'background', '-o', 'images'])
        self.assertEqual(parsed_args.materials, ['HDPE'])

    def test_exception_1(self):
        self.assertRaises(OSError, lambda: self.parser.parse_args(['-m', 'HDPE', 'PET', '-p', '100',
                                                                   '-c', '1', '-i', '1', '-b',
                                                                   'background', '-o', 'images']))

    def test_exception_2(self):
        self.assertRaises(OSError, lambda: self.parser.parse_args(['-m', 'HDPE', '-p', '80', '-c',
                                                                   '1', '-i', '1', '-b',
                                                                   'background', '-o', 'images']))

    def test_yaml(self):
        data = self.parser.parse_long_term_configuration(pathlib.Path(
            src_dir + r"/test/util/test.yaml"))
        self.assertEqual(data, {'key1': {'key1.1': 'stringvalue'},
                                'key2': {'key2.1': 1, 'key2.2': [1, 2, 3]}})


if __name__ == '__main__':
    unittest.main(argv=sys.argv[0:1])
