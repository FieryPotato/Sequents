import json
import os
import unittest

from src.file_io import TextImporter, JSONImporter, get_importer

text_content = 'a bird in hand is worth two in the bush; a bird in hand is worth two in the bush'
json_roots_only = {
    'A v B; A, B': {},
    'A, B; A v B': {},
    'B & C; B, C': {},
    'B, C; B & C': {},
    'C, C -> D; D': {},
    'D; C -> D, C': {},
    'E; E': {},
}
json_tree = {
    'A v B; A, B': {
        'A; A, B': {},
        'B; A, B': {}
    },
    'A, B; A v B': {
        'A, B; A, B': {}
    },
    'B & C; B, C': {
        'B, C; B, C': {}
    },
    'B, C; B & C': {
        'B, C; B': {},
        'B, C; C': {}

    },
    'C, C -> D; D': {
        'C; C': {},
        'D; D': {}
    },
    'D; C -> D, C': {
        'C, D; D, C': {}
    },
    'E; E': {},
}
json_universes = {
    'P & Q; R': [
        {'P; R': {}},
        {'Q; R': {}}
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

    def test_import_txt_file(self) -> None:
        importer = get_importer(self.file_path)
        expected = TextImporter(self.file_path)
        self.assertEqual(expected.__class__, importer.__class__)
        self.assertEqual(expected.path, importer.path)

    def test_import_lines(self) -> None:
        importer = TextImporter(self.file_path)
        actual = importer.import_lines()
        expected = text_content.split('\n')
        self.assertEqual(expected, actual)


class TestImportJson:
    file_path = 'test/io_testing/test_file.json'

    def tearDown(self) -> None:
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_import_json_roots(self) -> None:
        with open(self.file_path, 'w') as f:
            json.dump(f, json_roots_only)
        importer = JSONImporter(self.file_path)
        actual = importer.import_dict()
        expected = json_roots_only
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
