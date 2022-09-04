import json
import os
import unittest

from import_file import TextImporter, JSONImporter, ByteImporter, get_importer
from proposition import Atom, Negation, Conjunction, Disjunction, Conditional

text_content = 'a bird in hand is worth two in the bush; a bird in hand is worth two in the bush'

json_roots_only = {
    'A v B; A, B': None,
    'A, B; A v B': None,
    'B & C; B, C': None,
    'B, C; B & C': None,
    'C, C -> D; D': None,
    'D; C -> D, C': None,
    'E; E': None,
}

json_tree = {
    'A v B; A, B': {
        'A; A, B': None,
        'B; A, B': None
    },
    'A, B; A v B': {
        'A, B; A, B': None
    },
    'B & C; B, C': {
        'B, C; B, C': None
    },
    'B, C; B & C': {
        'B, C; B': None,
        'B, C; C': None

    },
    'C, C -> D; D': {
        'C; C': None,
        'D; D': None
    },
    'D; C -> D, C': {
        'C, D; D, C': None
    },
    'E; E': None,
}

json_universes = {
    'P & Q; R': [
        {'P; R': None},
        {'Q; R': None}
    ]
}


class TestImportText(unittest.TestCase):
    file_path = 'test/io_testing/test_file.txt'

    def setUp(self) -> None:
        with open(self.file_path, 'w') as file:
            file.write(text_content)

    def tearDown(self) -> None:
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_get_text_importer(self) -> None:
        importer = get_importer(self.file_path)
        expected = TextImporter(self.file_path)
        self.assertEqual(expected.__class__, importer.__class__)
        self.assertEqual(expected.path, importer.path)

    def test_import_lines(self) -> None:
        importer = TextImporter(self.file_path)
        actual = importer.import_()
        expected = text_content.split('\n')
        self.assertEqual(expected, actual)

    def test_importing_incorrect_file_extension_causes_exception(self) -> None:
        with self.assertRaises(KeyError):
            importer = get_importer('test.tar.gz')


class TestImportJson(unittest.TestCase):
    file_path = 'test/io_testing/test_file.json'

    def tearDown(self) -> None:
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_get_json_importer(self) -> None:
        importer = get_importer(self.file_path)
        expected = JSONImporter(self.file_path)
        self.assertEqual(expected.__class__, importer.__class__)
        self.assertEqual(expected.path, importer.path)

    def test_import_json_roots(self) -> None:
        # setUp
        with open(self.file_path, 'w') as f:
            json.dump(json_roots_only, f)
        # Test
        importer = JSONImporter(self.file_path)
        actual = importer.import_()
        expected = json_roots_only
        self.assertEqual(expected, actual)

    def test_import_whole_json(self) -> None:
        # setUp
        with open(self.file_path, 'w') as f:
            json.dump(json_tree, f)
        # Test
        importer = JSONImporter(self.file_path)
        actual = importer.import_()
        expected = json_tree
        self.assertEqual(expected, actual)


class TestImportBytes(unittest.TestCase):
    file_path = 'test/io_testing/byte_test'

    def test_import_bytes_trees(self) -> None:
        importer = ByteImporter(self.file_path)
        actual = importer.import_()
        self.assertEqual(type(actual), list)
        self.assertEqual(len(actual), 2)
        for tree in actual:
            self.assertEqual(str(type(tree)), '<class \'tree.Tree\'>')

    def test_get_bytes_importer(self) -> None:
        importer = get_importer(self.file_path)
        expected = ByteImporter(self.file_path)
        self.assertEqual(expected.__class__, importer.__class__)
        self.assertEqual(expected.path, importer.path)

if __name__ == '__main__':
    unittest.main()
