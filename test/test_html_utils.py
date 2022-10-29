import unittest

from convert import string_to_tree, string_to_sequent, sequent_to_tree
from html.utils import get_array, gridify

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
     ['f', '.' ],
]
CSS_1C_1P = [
    ['.',  'fmt'],
    ['fm', 'fmt'],
    ['fm', 'ft'],
    ['f',  'ft'],
    ['f',  '.']
]
CSS_1C_2P = [
    ['.',  'flt', '.',  'frt'],
    ['fl', 'flt', 'fr', 'frt'],
    ['fl', '.',   'fr', 'ft'],
    ['f',  'f',   'f',  'ft'],
    ['f',  'f',   'f',  '.']
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
    ['fl' , 'flt', 'fr', 'frt'],
    ['fl', '.', 'fr', 'ft'],
    ['f', 'f', 'f', 'ft'],
    ['f', 'f', 'f', '.'],
]
CSS_2C_1P_2P = [
    ['.', 'fmlt', '.', 'fmrt'],
    ['fml', 'fmlt', 'fmr', 'fmrt'],
    ['fml', '.', 'fmr','fmt'],
    ['fm', 'fm', 'fm', 'fmt'],
    ['fm', 'fm', 'fm', 'ft'],
    ['f', 'f', 'f', 'ft'],
    ['f', 'f', 'f', '.'],
]
CSS_2C_2P_2P = [
    ['.',   'fllt', '.',   'flrt', '.',   'frlt', '.',   'frrt'],
    ['fll', 'fllt', 'flr', 'flrt', 'frl', 'frlt', 'frr', 'frrt'],
    ['fll', '.',    'flr', 'flt',  'frl', '.',    'frr', 'frt'],
    ['fl',  'fl',   'fl',  'flt',  'fr',  'fr',   'fr',  'frt'],
    ['fl',  'fl',   'fl',  '.',    'fr',  'fr',   'fr',  'ft'],
    ['f',   'f',    'f',   'f',    'f',   'f',    'f',   'ft'],
    ['f',   'f',    'f',   'f',    'f',   'f',    'f',   '.'],
]


class TestHTMLArrayCreation(unittest.TestCase):
    def test_atom(self) -> None:
        t = string_to_tree(STR_ATOM)
        a = get_array(t, dtype=str)
        e = [
            ['', ''],
            ['', ''],
            ['', ''],
        ]
        self.assertEqual(e, a)

    def test_1c_1p(self) -> None:
        t = string_to_tree(STR_1C_1P) 
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
        t = string_to_tree(STR_1C_2P)
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
        t = string_to_tree(STR_2C_1P_1P)
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
        t = string_to_tree(STR_2C_2P_1P)
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
        t = string_to_tree(STR_2C_1P_2P)
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
        t = string_to_tree('A v B; C & D')
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


class TestGridification(unittest.TestCase):
    def test_atomic_gridify(self) -> None:
        string = STR_ATOM  # A; B
        seq = string_to_sequent(string)
        tree = sequent_to_tree(seq)
        expected_css = CSS_ATOM
        expected_objects = [str(seq), seq.tag()]
        expected = expected_css, expected_objects
        sub_test_strings = 'css', 'objects'
        actual = gridify(tree)
        for e, a, s in zip(expected, actual, sub_test_strings):
            with self.subTest(i=s):
                self.assertEqual(e, a)

    def test_c1_1p(self) -> None:
        string = STR_1C_1P  # ; A -> B
        f = string_to_sequent(string)
        fm = string_to_sequent(STR_ATOM)
        tree = sequent_to_tree(f)
        expected_css = CSS_1C_1P
        expected_objects = [str(f), f.tag(), str(fm), fm.tag()]
        expected = expected_css, expected_objects
        sub_test_strings = 'css', 'objects'
        actual = gridify(tree)
        for e, a, s in zip(expected, actual, sub_test_strings):
            with self.subTest(i=s):
                self.assertEqual(e, a)

    def test_c1_2p(self) -> None:
        string = STR_1C_2P  # A -> B;
        f = string_to_sequent(string)
        fl = string_to_sequent('; A')
        fr = string_to_sequent('B; ')
        tree = sequent_to_tree(f)
        expected_css = CSS_1C_2P
        expected_objects = [
            str(f), f.tag(), str(fl), fl.tag(), str(fr), fr.tag()
        ]
        expected = expected_css, expected_objects
        actual = gridify(tree)
        sub_test_strings = 'css', 'objects'
        for e, a, s in zip(expected, actual, sub_test_strings):
            with self.subTest(i=s):
                self.assertEqual(e, a)

    def test_c2_1_1(self) -> None:
        string = STR_2C_1P_1P  # A & B; A v B
        f = string_to_sequent(string)
        fm = string_to_sequent('A, B; A v B')
        fmm = string_to_sequent('A, B; A, B')
        tree = sequent_to_tree(f)
        expected_css = CSS_2C_1P_1P
        expected_objects = [
            str(f), f.tag(), str(fm), fm.tag(), str(fmm), fmm.tag()
        ]
        expected = expected_css, expected_objects
        actual = gridify(tree)
        sub_test_strings = 'css', 'objects'
        for e, a, s in zip(expected, actual, sub_test_strings):
            with self.subTest(i=s):
                self.assertEqual(e, a)

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
            str(f), f.tag(), str(fl), fl.tag(),
            str(flm), flm.tag(), str(fr), fr.tag(), str(frm), frm.tag()
        ]
        expected = expected_css, expected_objects
        actual = gridify(tree)
        sub_test_strings = 'css', 'objects'
        for e, a, s in zip(expected, actual, sub_test_strings):
            with self.subTest(i=s):
                self.assertEqual(e, a)

    def test_c2_1_2(self) -> None:
        string = STR_2C_1P_2P  # 'A & B; A & B'
        f = string_to_sequent(string)
        fm = string_to_sequent('A, B; A & B')
        fml = string_to_sequent('A, B; A')
        fmr = string_to_sequent('A, B; B')
        tree = sequent_to_tree(f)
        expected_css = CSS_2C_1P_2P
        expected_objects = [
            str(f), f.tag(), str(fm), fm.tag(), str(fml), fml.tag(),
            str(fmr), fmr.tag()
        ]
        expected = expected_css, expected_objects
        actual = gridify(tree)
        sub_test_strings = 'css', 'objects'
        for e, a, s in zip(expected, actual, sub_test_strings):
            with self.subTest(i=s):
                self.assertEqual(e, a)

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
            str(f), f.tag(), str(fl), fl.tag(), str(fll), fll.tag(), 
            str(flr), flr.tag(), str(fr), fr.tag(), str(frl), 
            frl.tag(), str(frr), frr.tag()
        ]
        expected = expected_css, expected_objects
        actual = gridify(tree)
        sub_test_strings = 'css', 'objects'
        for e, a, s in zip(expected, actual, sub_test_strings):
            with self.subTest(i=s):
                self.assertEqual(e, a)


    def test_lopsided_left_tree(self) -> None:
        string = '(A v B) v C;'
        f = string_to_sequent(string)
        fl = string_to_sequent('A v B;')
        fr = string_to_sequent('C;')
        fll = string_to_sequent('A;')
        flr = string_to_sequent('B;')
        tree = string_to_tree(string)
        expected_css = [
            ['.',   'fllt', '.',   'flrt', '.',  '.'],
            ['fll', 'fllt', 'flr', 'flrt', '.',  '.'],
            ['fll', '.',    'flr', 'flt',  '.',  'frt'],
            ['fl',  'fl',   'fl',  'flt',  'fr', 'frt'],
            ['fl',  'fl',   'fl',  '.',    'fr', 'ft'],
            ['f',   'f',    'f',   'f',    'f',  'ft'],
            ['f',   'f',    'f',   'f',    'f',  '.']
        ]
        expected_objects = [
            str(f), f.tag(), str(fl), fl.tag(), str(fll), fll.tag(), 
            str(flr), flr.tag(), str(fr), fr.tag(),

        ]
        expected = expected_css, expected_objects
        actual = gridify(tree)
        sub_test_strings = 'css', 'objects'
        for e, a, s in zip(expected, actual, sub_test_strings):
            with self.subTest(i=s):
                self.assertEqual(e, a)


    def test_lopsided_right_tree(self) -> None:
        string = '; A & (B & C)'
        f = string_to_sequent(string)
        fl = string_to_sequent('; A')
        fr = string_to_sequent('; (B & C)')
        frl = string_to_sequent('; B')
        frr = string_to_sequent('; C')
        tree = string_to_tree(string)
        expected_css = [
            ['.',   '.',   '.',   'frlt', '.',    'frrt'],
            ['.',   '.',   'frl', 'frlt', 'frr',  'frrt'],
            ['.',   'flt', 'frl', '.' ,   'frr',  'frt'],
            ['fl',  'flt', 'fr',  'fr',   'fr',   'frt'],
            ['fl',  '.',   'fr',  'fr',   'fr',   'ft'],
            ['f',   'f',   'f',   'f',    'f',    'ft'],
            ['f',   'f',   'f',   'f',    'f',    '.']
        ]
        expected_objects = [
            str(f), f.tag(), str(fl), fl.tag(), str(fr), fr.tag(),
            str(frl), frl.tag(), str(frr), frr.tag()
        ]
        expected = expected_css, expected_objects
        actual = gridify(tree)
        sub_test_strings = 'css', 'objects'
        for e, a, s in zip(expected, actual, sub_test_strings):
            with self.subTest(i=s):
                self.assertEqual(e, a)


class TestGridToTree(unittest.TestCase):
    def test_atomic_tree(self) -> None:
        string = STR_ATOM
        tree = string_to_tree(string)
        


if __name__ == '__main__':
    unittest.main()
