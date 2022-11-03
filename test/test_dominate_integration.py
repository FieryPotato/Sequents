import unittest
from pathlib import Path

import convert

from HTML.HTML import HTML

MOCKS_DIR = Path('test/mocks/html')
OUTFILE = Path('test/mocks/html/out.html')


class TestDominateIntegration(unittest.TestCase):
    mocks = MOCKS_DIR
    out_file = OUTFILE

    def setUp(self) -> None:
        self.doc = HTML(self.out_file)
        self.doc.create_head()

    def tearDown(self) -> None:
        self.out_file.unlink(missing_ok=True)

    def test_head_is_created(self):
        self.doc.save()

        with open(self.mocks / 'create_head.html') as f:
            expected = f.readlines()

        with open(self.out_file) as f:
            actual = f.readlines()

        self.assertEqual(expected, actual)

    def test_typeset_atom(self) -> None:
        trees = [convert.string_to_tree('A; B')]
        self.doc.typeset(trees)

        with open(self.mocks / 'typeset' / 'atom.html') as f:
            expected = f.readlines()

        with open(self.out_file) as f:
            actual = f.readlines()

        self.assertEqual(expected, actual)



if __name__ == '__main__':
    unittest.main()