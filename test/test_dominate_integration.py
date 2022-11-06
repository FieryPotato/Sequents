import unittest
from pathlib import Path

import convert

from HTML.HTML import HTML
from HTML.utils import gridify, grid_to_dict

MOCKS_DIR = Path('test/mocks/html')
OUTFILE = Path('test/mocks/html/out.html')


class TestDominateIntegration(unittest.TestCase):
    mocks = MOCKS_DIR
    out_file = OUTFILE

    def setUp(self) -> None:
        self.doc = HTML(self.out_file)

    def tearDown(self) -> None:
        self.out_file.unlink(missing_ok=True)

    def test_head_is_created(self):
        self.doc.create_head()
        self.doc.save()

        with open(self.mocks / 'create_head.html') as f:
            expected = f.readlines()

        with open(self.out_file) as f:
            actual = f.readlines()

        self.assertEqual(expected, actual)

    def test_typeset_atom(self) -> None:
        tree = convert.string_to_tree('A; B')
        css_grid, objects_grid = gridify(tree)
        grid_dict = grid_to_dict(css_grid, objects_grid)
        
        e_title = '/* A; B */'
        e_template_areas = '_A6_B { grid-template-areas: \n'\
                           '  \'. ft\'\n'\
                           '  \'f ft\'\n'\
                           '  \'f .\'\n'\
                           '}'
        e_grid_area = [
            '._A6_B-f { grid-area: f; }',
            '._A6_B-ft { grid-area: ft; }',
        ]

        actual = self.doc.generate_tree_css(tree)
        expected = e_title, e_template_areas, e_grid_area

        # self.doc.save()

        # with open(self.mocks / 'typeset' / 'atom.html') as f:
        #     expected = f.readlines()

        # with open(self.out_file) as f:
        #     actual = f.readlines()
    
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
