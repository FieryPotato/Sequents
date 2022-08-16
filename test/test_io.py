import os
import unittest

from src.file_io import TextImporter, get_importer


TEXT_FILE = 'test/io_testing/test_file.txt'
JSON_FILE = 'test/io_testing/test_file.json'
text_content = 'a bird in hand is worth two in the bush'
json_roots_only = {
        'A v B; A, B': {},
        'B, C; B & C': {},
        'C, C -> D; D': {},
        'E; E': {},
        }
json_tree = {
        'P, P -> Q; Q': {
            'P;P': {},
            'Q;Q': {}
            }
        }

class TestProverIO(unittest.TestCase):
    def setUp(self) -> None:
        with open(TEXT_FILE, 'w') as file:
            file.write(text_content)

    def tearDown(self) -> None:
        if os.path.exists(TEXT_FILE):
            os.remove(TEXT_FILE)

    def test_import_txt_file(self) -> None:
        importer = get_importer(TEXT_FILE)
        expected = TextImporter(TEXT_FILE)
        self.assertEqual(expected.__class__, importer.__class__)
        self.assertEqual(expected.path, importer.path)

    def test_import_lines(self) -> None:
        importer = TextImporter(TEXT_FILE)
        actual = importer.import_lines()
        expected = text_content.split('\n')
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()

