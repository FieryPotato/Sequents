import unittest
from unittest.mock import patch

from convert import string_to_tree, string_to_sequent, sequent_to_tree
from HTML.utils import get_array, gridify, grid_to_dict

STR_ATOM = 'A; B'
STR_1C_1P = '; A -> B'
STR_1C_2P = 'A -> B;'
STR_2C_1P_1P = 'A & B; A v B'
STR_2C_2P_1P = 'A v B; A v B'
STR_2C_1P_2P = 'A & B; A & B'
STR_2C_2P_2P = 'A v B; C & D'

CSS_ATOM = [
    ['.', 'ft'],
    ['f', 'ft'],
    ['f', '.'],
]
CSS_1C_1P = [
    ['.', 'fmt'],
    ['fm', 'fmt'],
    ['fm', 'ft'],
    ['f', 'ft'],
    ['f', '.']
]
CSS_1C_2P = [
    ['.', 'flt', '.', 'frt'],
    ['fl', 'flt', 'fr', 'frt'],
    ['fl', '.', 'fr', 'ft'],
    ['f', 'f', 'f', 'ft'],
    ['f', 'f', 'f', '.']
]
CSS_2C_1P_1P = [
    ['.', 'fmmt'],
    ['fmm', 'fmmt'],
    ['fmm', 'fmt'],
    ['fm', 'fmt'],
    ['fm', 'ft'],
    ['f', 'ft'],
    ['f', '.']
]
CSS_2C_2P_1P = [
    ['.', 'flmt', '.', 'frmt'],
    ['flm', 'flmt', 'frm', 'frmt'],
    ['flm', 'flt', 'frm', 'frt'],
    ['fl', 'flt', 'fr', 'frt'],
    ['fl', '.', 'fr', 'ft'],
    ['f', 'f', 'f', 'ft'],
    ['f', 'f', 'f', '.'],
]
CSS_2C_1P_2P = [
    ['.', 'fmlt', '.', 'fmrt'],
    ['fml', 'fmlt', 'fmr', 'fmrt'],
    ['fml', '.', 'fmr', 'fmt'],
    ['fm', 'fm', 'fm', 'fmt'],
    ['fm', 'fm', 'fm', 'ft'],
    ['f', 'f', 'f', 'ft'],
    ['f', 'f', 'f', '.'],
]
CSS_2C_2P_2P = [
    ['.', 'fllt', '.', 'flrt', '.', 'frlt', '.', 'frrt'],
    ['fll', 'fllt', 'flr', 'flrt', 'frl', 'frlt', 'frr', 'frrt'],
    ['fll', '.', 'flr', 'flt', 'frl', '.', 'frr', 'frt'],
    ['fl', 'fl', 'fl', 'flt', 'fr', 'fr', 'fr', 'frt'],
    ['fl', 'fl', 'fl', '.', 'fr', 'fr', 'fr', 'ft'],
    ['f', 'f', 'f', 'f', 'f', 'f', 'f', 'ft'],
    ['f', 'f', 'f', 'f', 'f', 'f', 'f', '.'],
]


class TestHTMLArrayCreation(unittest.TestCase):
    def test_atom(self) -> None:
        t = string_to_tree(STR_ATOM)  # A; B
        a = get_array(t, dtype=str)
        e = [
            ['', ''],
            ['', ''],
            ['', ''],
        ]
        self.assertEqual(e, a)

    @patch('settings.CONFIG_PATH', 'test/mocks/config_invertible_connective_types.json')
    def test_1c_1p(self) -> None:
        t = string_to_tree(STR_1C_1P)  # ; A -> B
        a = get_array(t, dtype=str)
        e = [
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
        ]
        self.assertEqual(e, a)

    def test_1c_2p(self) -> None:
        t = string_to_tree(STR_1C_2P)  # A -> B;
        a = get_array(t, dtype=str)

        e = [
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
        ]
        self.assertEqual(e, a)

    def test_c2_1_1(self) -> None:
        t = string_to_tree(STR_2C_1P_1P)  # A & B; A v B
        a = get_array(t, dtype=str)

        e = [
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
        ]
        self.assertEqual(e, a)

    def test_c2_2_1(self) -> None:
        t = string_to_tree(STR_2C_2P_1P)  # A v B; A v B
        a = get_array(t, dtype=str)

        e = [
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
        ]
        self.assertEqual(e, a)

    def test_c2_1_2(self) -> None:
        t = string_to_tree(STR_2C_1P_2P)  # A & B; A & B
        a = get_array(t, dtype=str)

        e = [
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
        ]
        self.assertEqual(e, a)

    def test_c2_2_2(self) -> None:
        t = string_to_tree('A v B; C & D')  # A v B; C & D
        a = get_array(t, dtype=str)

        e = [
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '']
        ]
        self.assertEqual(e, a)


class TestHTMLification(unittest.TestCase):
    def test_atom(self) -> None:
        seq = string_to_sequent(STR_ATOM)  # A; B
        tree = sequent_to_tree(seq)
        expected_css = CSS_ATOM
        expected_objects = [
            [None, seq.tag()],
            [seq.long_string, seq.tag()],
            [seq.long_string, None]
        ]
        expected = expected_css, expected_objects

        # Test gridification 
        sub_test_strings = 'css', 'objects'
        actual = gridify(tree)
        for e, a, s in zip(expected, actual, sub_test_strings):
            with self.subTest(i=f'grid: {s}'):
                self.assertEqual(e, a)

        # Test output dict
        with self.subTest(i='output dict'):
            e = {
                'root': 'A &vdash; B',
                '._A6_B-f': seq.long_string,
                '._A6_B-ft': seq.tag()
            }
            self.assertEqual(e, grid_to_dict(*expected))


    def test_c1_1p(self) -> None:
        string = STR_1C_1P  # ; A -> B
        f = string_to_sequent(string)
        fm = string_to_sequent(STR_ATOM)
        tree = sequent_to_tree(f)
        expected_css = CSS_1C_1P
        expected_objects = [
            [None, fm.tag()],
            [fm.long_string, fm.tag()],
            [fm.long_string, f.tag()],
            [f.long_string, f.tag()],
            [f.long_string, None]
        ]
        expected = expected_css, expected_objects

        # Test gridification
        sub_test_strings = 'css', 'objects'
        actual = gridify(tree)
        for e, a, s in zip(expected, actual, sub_test_strings):
            with self.subTest(i=f'grid: {s}'):
                self.assertEqual(e, a)

        # Test output dict
        with self.subTest(i='output dict'):
            e = {
                'root': ' &vdash; (A &rarr; B)',
                '._6_1A_implies_B2-f': f.long_string,
                '._6_1A_implies_B2-ft': f.tag(),
                '._6_1A_implies_B2-fm': fm.long_string,
                '._6_1A_implies_B2-fmt': fm.tag()
            }
            self.assertEqual(e, grid_to_dict(*expected))

    def test_c1_2p(self) -> None:
        string = STR_1C_2P  # A -> B;
        f = string_to_sequent(string)
        fl = string_to_sequent('; A')
        fr = string_to_sequent('B; ')
        tree = sequent_to_tree(f)
        expected_css = CSS_1C_2P
        expected_objects = [
            [None, fl.tag(), None, fr.tag()],
            [fl.long_string, fl.tag(), fr.long_string, fr.tag()],
            [fl.long_string, None, fr.long_string, f.tag()],
            [f.long_string, f.long_string, f.long_string, f.tag()],
            [f.long_string, f.long_string, f.long_string, None]
        ]
        expected = expected_css, expected_objects

        # Test gridification
        actual = gridify(tree)
        sub_test_strings = 'css', 'objects'
        for e, a, s in zip(expected, actual, sub_test_strings):
            with self.subTest(i=f'grid: {s}'):
                self.assertEqual(e, a)

        # Test output dict
        with self.subTest(i='output dict'):
            e = {
                'root': '(A &rarr; B) &vdash; ',
                '._1A_implies_B26-f': f.long_string,
                '._1A_implies_B26-ft': f.tag(),
                '._1A_implies_B26-fl': fl.long_string,
                '._1A_implies_B26-flt': fl.tag(),
                '._1A_implies_B26-fr': fr.long_string,
                '._1A_implies_B26-frt': fr.tag()
            }
            self.assertEqual(e, grid_to_dict(*expected))

    def test_c2_1_1(self) -> None:
        string = STR_2C_1P_1P  # A & B; A v B
        f = string_to_sequent(string)
        fm = string_to_sequent('A, B; A v B')
        fmm = string_to_sequent('A, B; A, B')
        tree = sequent_to_tree(f)
        expected_css = CSS_2C_1P_1P
        expected_objects = [
            [None, fmm.tag()],
            [fmm.long_string, fmm.tag()],
            [fmm.long_string, fm.tag()],
            [fm.long_string, fm.tag()],
            [fm.long_string, f.tag()],
            [f.long_string, f.tag()],
            [f.long_string, None]
        ]
        expected = expected_css, expected_objects

        # Test gridification 
        actual = gridify(tree)
        sub_test_strings = 'css', 'objects'
        for e, a, s in zip(expected, actual, sub_test_strings):
            with self.subTest(i=f'grid: {s}'):
                self.assertEqual(e, a)

        # Test output dict
        with self.subTest(i='output dict'):
            e = {
                'root': '(A &and; B) &vdash; (A &or; B)',
                '._1A_and_B26_1A_or_B2-f': f.long_string,
                '._1A_and_B26_1A_or_B2-ft': f.tag(),
                '._1A_and_B26_1A_or_B2-fm': fm.long_string,
                '._1A_and_B26_1A_or_B2-fmt': fm.tag(),
                '._1A_and_B26_1A_or_B2-fmm': fmm.long_string,
                '._1A_and_B26_1A_or_B2-fmmt': fmm.tag()
            }
            self.assertEqual(e, grid_to_dict(*expected))

    def test_c2_2_1(self) -> None:
        string = STR_2C_2P_1P  # A v B; A v B
        f = string_to_sequent(string)
        fl = string_to_sequent('A; A v B')
        fr = string_to_sequent('B; A v B')
        flm = string_to_sequent('A; A, B')
        frm = string_to_sequent('B; A, B')
        tree = sequent_to_tree(f)
        expected_css = CSS_2C_2P_1P
        expected_objects = [
            [None, flm.tag(), None, frm.tag()],
            [flm.long_string, flm.tag(), frm.long_string, frm.tag()],
            [flm.long_string, fl.tag(), frm.long_string, fr.tag()],
            [fl.long_string, fl.tag(), fr.long_string, fr.tag()],
            [fl.long_string, None, fr.long_string, f.tag()],
            [f.long_string, f.long_string, f.long_string, f.tag()],
            [f.long_string, f.long_string, f.long_string, None]
        ]
        expected = expected_css, expected_objects

        # Test gridification
        actual = gridify(tree)
        sub_test_strings = 'css', 'objects'
        for e, a, s in zip(expected, actual, sub_test_strings):
            with self.subTest(i=f'grid: {s}'):
                self.assertEqual(e, a)

        # Test output dict
        with self.subTest(i='output dict'):
            e = {
                'root': '(A &or; B) &vdash; (A &or; B)',
                '._1A_or_B26_1A_or_B2-f': f.long_string,
                '._1A_or_B26_1A_or_B2-ft': f.tag(),
                '._1A_or_B26_1A_or_B2-fl': fl.long_string,
                '._1A_or_B26_1A_or_B2-flt': fl.tag(),
                '._1A_or_B26_1A_or_B2-fr': fr.long_string,
                '._1A_or_B26_1A_or_B2-frt': fr.tag(),
                '._1A_or_B26_1A_or_B2-flm': flm.long_string,
                '._1A_or_B26_1A_or_B2-flmt': flm.tag(),
                '._1A_or_B26_1A_or_B2-frm': frm.long_string,
                '._1A_or_B26_1A_or_B2-frmt': frm.tag(),
            }
            self.assertEqual(e, grid_to_dict(*expected))

    def test_c2_1_2(self) -> None:
        string = STR_2C_1P_2P  # 'A & B; A & B'
        f = string_to_sequent(string)
        fm = string_to_sequent('A, B; A & B')
        fml = string_to_sequent('A, B; A')
        fmr = string_to_sequent('A, B; B')
        tree = sequent_to_tree(f)
        expected_css = CSS_2C_1P_2P
        expected_objects = [
            [None, fml.tag(), None, fmr.tag()],
            [fml.long_string, fml.tag(), fmr.long_string, fmr.tag()],
            [fml.long_string, None, fmr.long_string, fm.tag()],
            [fm.long_string, fm.long_string, fm.long_string, fm.tag()],
            [fm.long_string, fm.long_string, fm.long_string, f.tag()],
            [f.long_string, f.long_string, f.long_string, f.tag()],
            [f.long_string, f.long_string, f.long_string, None]
        ]
        expected = expected_css, expected_objects

        # Test gridification
        actual = gridify(tree)
        sub_test_strings = 'css', 'objects'
        for e, a, s in zip(expected, actual, sub_test_strings):
            with self.subTest(i=f'grid: {s}'):
                self.assertEqual(e, a)

        # Test output dict
        with self.subTest(i='output dict'):
            e = {
                'root': '(A &and; B) &vdash; (A &and; B)',
                '._1A_and_B26_1A_and_B2-f': f.long_string,
                '._1A_and_B26_1A_and_B2-ft': f.tag(),
                '._1A_and_B26_1A_and_B2-fm': fm.long_string,
                '._1A_and_B26_1A_and_B2-fmt': fm.tag(),
                '._1A_and_B26_1A_and_B2-fml': fml.long_string,
                '._1A_and_B26_1A_and_B2-fmlt': fml.tag(),
                '._1A_and_B26_1A_and_B2-fmr': fmr.long_string,
                '._1A_and_B26_1A_and_B2-fmrt': fmr.tag(),
            }
            self.assertEqual(e, grid_to_dict(*expected))

    def test_c2_2_2(self) -> None:
        string = STR_2C_2P_2P  # 'A v B; C & D'
        f = string_to_sequent(string)
        fl = string_to_sequent('A; C & D')
        fr = string_to_sequent('B; C & D')
        fll = string_to_sequent('A; C')
        flr = string_to_sequent('A; D')
        frl = string_to_sequent('B; C')
        frr = string_to_sequent('B; D')
        tree = string_to_tree(string)
        expected_css = CSS_2C_2P_2P
        expected_objects = [
            [None, fll.tag(), None, flr.tag(), None, frl.tag(), None, frr.tag()],
            [fll.long_string, fll.tag(), flr.long_string, flr.tag(), frl.long_string, frl.tag(), frr.long_string,
             frr.tag()],
            [fll.long_string, None, flr.long_string, fl.tag(), frl.long_string, None, frr.long_string, fr.tag()],
            [fl.long_string, fl.long_string, fl.long_string, fl.tag(), fr.long_string, fr.long_string, fr.long_string,
             fr.tag()],
            [fl.long_string, fl.long_string, fl.long_string, None, fr.long_string, fr.long_string, fr.long_string,
             f.tag()],
            [f.long_string, f.long_string, f.long_string, f.long_string, f.long_string, f.long_string, f.long_string,
             f.tag()],
            [f.long_string, f.long_string, f.long_string, f.long_string, f.long_string, f.long_string, f.long_string,
             None],
        ]
        expected = expected_css, expected_objects

        # Test gridification
        actual = gridify(tree)
        sub_test_strings = 'css', 'objects'
        for e, a, s in zip(expected, actual, sub_test_strings):
            with self.subTest(i=f'grid: {s}'):
                self.assertEqual(e, a)

        # Test output dict
        with self.subTest(i='output_dict'):
            e = {
                'root': '(A &or; B) &vdash; (C &and; D)',
                '._1A_or_B26_1C_and_D2-f': f.long_string,
                '._1A_or_B26_1C_and_D2-ft': f.tag(),
                '._1A_or_B26_1C_and_D2-fl': fl.long_string,
                '._1A_or_B26_1C_and_D2-flt': fl.tag(),
                '._1A_or_B26_1C_and_D2-fll': fll.long_string,
                '._1A_or_B26_1C_and_D2-fllt': fll.tag(),
                '._1A_or_B26_1C_and_D2-flr': flr.long_string,
                '._1A_or_B26_1C_and_D2-flrt': flr.tag(),
                '._1A_or_B26_1C_and_D2-fr': fr.long_string,
                '._1A_or_B26_1C_and_D2-frt': fr.tag(),
                '._1A_or_B26_1C_and_D2-frl': frl.long_string,
                '._1A_or_B26_1C_and_D2-frlt': frl.tag(),
                '._1A_or_B26_1C_and_D2-frr': frr.long_string,
                '._1A_or_B26_1C_and_D2-frrt': frr.tag(),
            }
            self.assertEqual(e, grid_to_dict(*expected))

    def test_lopsided_tree(self) -> None:
        self.maxDiff = None
        string = '(A v B) v C;'
        f = string_to_sequent(string)
        fl = string_to_sequent('A v B;')
        fr = string_to_sequent('C;')
        fll = string_to_sequent('A;')
        flr = string_to_sequent('B;')
        tree = string_to_tree(string)
        expected_css = [
            ['.', 'fllt', '.', 'flrt', '.', '.'],
            ['fll', 'fllt', 'flr', 'flrt', '.', '.'],
            ['fll', '.', 'flr', 'flt', '.', 'frt'],
            ['fl', 'fl', 'fl', 'flt', 'fr', 'frt'],
            ['fl', 'fl', 'fl', '.', 'fr', 'ft'],
            ['f', 'f', 'f', 'f', 'f', 'ft'],
            ['f', 'f', 'f', 'f', 'f', '.']
        ]
        expected_objects = [
            [None, fll.tag(), None, flr.tag(), None, None],
            [fll.long_string, fll.tag(), flr.long_string, flr.tag(), None, None],
            [fll.long_string, None, flr.long_string, fl.tag(), None, fr.tag()],
            [fl.long_string, fl.long_string, fl.long_string, fl.tag(), fr.long_string, fr.tag()],
            [fl.long_string, fl.long_string, fl.long_string, None, fr.long_string, f.tag()],
            [f.long_string, f.long_string, f.long_string, f.long_string, f.long_string, f.tag()],
            [f.long_string, f.long_string, f.long_string, f.long_string, f.long_string, None]
        ]
        expected = expected_css, expected_objects

        # Test gridification
        actual = gridify(tree)
        sub_test_strings = 'css', 'objects'
        for e, a, s in zip(expected, actual, sub_test_strings):
            with self.subTest(i=f'grid: {s}'):
                self.assertEqual(e, a)

        # Test output dict
        with self.subTest(i='output dict'):
            e = {
                'root': '((A &or; B) &or; C) &vdash; ',
                '._11A_or_B2_or_C26-f': f.long_string,
                '._11A_or_B2_or_C26-ft': f.tag(),
                '._11A_or_B2_or_C26-fl': fl.long_string,
                '._11A_or_B2_or_C26-flt': fl.tag(),
                '._11A_or_B2_or_C26-fll': fll.long_string,
                '._11A_or_B2_or_C26-fllt': fll.tag(),
                '._11A_or_B2_or_C26-flr': flr.long_string,
                '._11A_or_B2_or_C26-flrt': flr.tag(),
                '._11A_or_B2_or_C26-fr': fr.long_string,
                '._11A_or_B2_or_C26-frt': fr.tag(),
            }
            self.assertEqual(e, grid_to_dict(*expected))


if __name__ == '__main__':
    unittest.main()
