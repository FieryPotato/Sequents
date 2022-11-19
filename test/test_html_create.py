import unittest

from pathlib import Path

import convert

from HTML.document import Builder


class TestBuilderMethods(unittest.TestCase):
    def test_grid_template_areas(self) -> None:
        template_areas = [
            ['.', 'flt', '.', 'frt'],
            ['fl', 'flt', 'fr', 'frt'],
            ['fl', '.', 'fr', 'ft'],
            ['f', 'f', 'f', 'ft'],
            ['f', 'f', 'f', '.']
        ]
        class_name = '_1A_or_B25_'

        grid_template_areas = Builder().grid_template_areas(template_areas, class_name)
        actual = [str(area) for area in grid_template_areas]
        expected = [
            '      ._1A_or_B25_ { grid-template-areas:\n',
            '        ". flt . frt"\n',
            '        "fl flt fr frt"\n',
            '        "fl . fr ft"\n',
            '        "f f f ft"\n',
            '        "f f f .";\n',
            '      }\n'
        ]

        self.assertEqual(expected, actual)

    def test_grid_area(self) -> None:
        class_name = '1A_and_B26_1A_or_B2'
        grid_dict = {
            '._1A_and_B26_1A_or_B2-f': '',
            '._1A_and_B26_1A_or_B2-ft': '',
            '._1A_and_B26_1A_or_B2-fm': '',
            '._1A_and_B26_1A_or_B2-fmt': '',
            '._1A_and_B26_1A_or_B2-fmm': '',
            '._1A_and_B26_1A_or_B2-fmmt': ''
        }

        expected = [
            '      ._1A_and_B26_1A_or_B2-f { grid-area: f; }\n',
            '      ._1A_and_B26_1A_or_B2-ft { grid-area: ft; }\n',
            '      ._1A_and_B26_1A_or_B2-fm { grid-area: fm; }\n',
            '      ._1A_and_B26_1A_or_B2-fmt { grid-area: fmt; }\n',
            '      ._1A_and_B26_1A_or_B2-fmm { grid-area: fmm; }\n',
            '      ._1A_and_B26_1A_or_B2-fmmt { grid-area: fmmt; }\n'
        ]

        actual = Builder().grid_area(grid_dict, class_name)
        self.assertEqual(expected, actual)

    def test_body_tree(self) -> None:
        f = 'A and B; A and B'
        ft = 'L&'
        fm = 'A, B; A and B'
        fmt = 'R&'
        fml = 'A, B; A'
        fmlt = 'Ax'
        fmr = 'A, B; B'
        fmrt = 'Ax'

        class_name = '_1A_and_B26_1A_and_B2'
        grid_dict = {
            '._1A_and_B26_1A_and_B2-f': f,
            '._1A_and_B26_1A_and_B2-ft': ft,
            '._1A_and_B26_1A_and_B2-fm': fm,
            '._1A_and_B26_1A_and_B2-fmt': fmt,
            '._1A_and_B26_1A_and_B2-fml': fml,
            '._1A_and_B26_1A_and_B2-fmlt': fmlt,
            '._1A_and_B26_1A_and_B2-fmr': fmr,
            '._1A_and_B26_1A_and_B2-fmrt': fmrt
        }

        expected = \
            '<div class="tree _1A_and_B26_1A_and_B2">\n' \
            '  <div class="cell _1A_and_B26_1A_and_B2-f">A &and; B &vdash; A &and; B</div>\n' \
            '  <div class="tag _1A_and_B26_1A_and_B2-ft">L&and;</div>\n' \
            '  <div class="cell _1A_and_B26_1A_and_B2-fm">A, B &vdash; A &and; B</div>\n' \
            '  <div class="tag _1A_and_B26_1A_and_B2-fmt">R&and;</div>\n' \
            '  <div class="cell _1A_and_B26_1A_and_B2-fml">A, B &vdash; A</div>\n' \
            '  <div class="tag _1A_and_B26_1A_and_B2-fmlt">Ax</div>\n' \
            '  <div class="cell _1A_and_B26_1A_and_B2-fmr">A, B &vdash; B</div>\n' \
            '  <div class="tag _1A_and_B26_1A_and_B2-fmrt">Ax</div>\n' \
            '</div>'

        body_tree = Builder().make_body_tree(grid_dict, class_name)
        actual = str(body_tree)

        self.assertEqual(expected, actual)


class TestCreate(unittest.TestCase):
    outfile = Path('test/mocks/html_result.html')

    def tearDown(self) -> None:
        self.outfile.unlink(missing_ok=True)

    def test_create_atomic(self) -> None:
        tree = convert.string_to_tree('A; B')
        document = Builder()
        document.build([tree])
        document.save(self.outfile)

        with open(self.outfile, 'r') as f:
            actual = f.readlines()

        with open('test/mocks/html/atom.html', 'r') as f:
            expected = f.readlines()

        self.assertEqual(expected, actual)

