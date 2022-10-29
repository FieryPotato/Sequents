import unittest

from convert import string_to_tree, string_to_sequent, sequent_to_tree
from html.utils import get_array, gridify


class TestHTMLArrayCreation(unittest.TestCase):
    def test_atom(self) -> None:
        t = string_to_tree('A; B')
        actual = get_array(t, dtype=str)
        expected = [
            ['', ''],
            ['', ''],
            ['', ''],
        ]
        self.assertEqual(expected, actual)

    def test_complexity_1(self) -> None:
        t_1 = string_to_tree('A & B; C')
        a_1 = get_array(t_1, dtype=str)

        e_1 = [
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
        ]
        self.assertEqual(e_1, a_1)

        t_2 = string_to_tree('A; B & C')
        a_2 = get_array(t_2, dtype=str)

        e_2 = [
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
        ]
        self.assertEqual(e_2, a_2)

    def test_complexity_2(self) -> None:
        t_1 = string_to_tree('A; B -> (C -> D)')
        a_1 = get_array(t_1, dtype=str)

        e_1 = [
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
        ]
        self.assertEqual(e_1, a_1)

        t_2 = string_to_tree('; A & (B v C)')
        a_2 = get_array(t_2, dtype=str)

        e_2 = [
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
        ]
        self.assertEqual(e_2, a_2)

        t_5 = string_to_tree('; A v (B & C)')
        a_5 = get_array(t_5, dtype=str)

        e_5 = [
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
        ]
        self.assertEqual(e_5, a_5)

        t_6 = string_to_tree('(A v B) v C; ')
        a_6 = get_array(t_6, dtype=str)

        e_6 = [
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
        ]
        self.assertEqual(e_6, a_6)

        t_7 = string_to_tree('; A & (B & C)')
        a_7 = get_array(t_7, dtype=str)

        e_7 = [
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
        ]
        self.assertEqual(e_7, a_7)

        t_8 = string_to_tree('A v B; C & D')
        a_8 = get_array(t_8, dtype=str)

        e_8 = [
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '']
        ]
        self.assertEqual(e_8, a_8)


class TestGridification(unittest.TestCase):
    def test_atomic_gridify(self) -> None:
        string = 'A; B'
        seq = string_to_sequent(string)
        tree = sequent_to_tree(seq)
        expected_css = [
            ['.', 'ft'],
            ['f', 'ft'],
            ['f', '.' ],
        ]

        expected_objects = [str(seq), seq.tag()]
        expected = expected_css, expected_objects
        sub_test_strings = 'css', 'objects'
        actual = gridify(tree)
        for e, a, s in zip(expected, actual, sub_test_strings):
            with self.subTest(i=s):
                self.assertEqual(e, a)

    def test_c1_1p(self) -> None:
        string = '; A -> B'
        f = string_to_sequent(string)
        fm = string_to_sequent('A; B')
        tree = sequent_to_tree(f)
        expected_css = [
            ['.',  'fmt'],
            ['fm', 'fmt'],
            ['fm', 'ft'],
            ['f',  'ft'],
            ['f',  '.']
        ]
        expected_objects = [str(f), f.tag(), str(fm), fm.tag()]
        expected = expected_css, expected_objects
        sub_test_strings = 'css', 'objects'
        actual = gridify(tree)
        for e, a, s in zip(expected, actual, sub_test_strings):
            with self.subTest(i=s):
                self.assertEqual(e, a)

    def test_c1_2p(self) -> None:
        string = 'A -> B;'
        f = string_to_sequent(string)
        fl = string_to_sequent('; A')
        fr = string_to_sequent('B; ')
        tree = sequent_to_tree(f)
        expected_css = [
            ['.',  'flt', '.',  'frt'],
            ['fl', 'flt', 'fr', 'frt'],
            ['fl', '.',   'fr', 'ft'],
            ['f',  'f',   'f',  'ft'],
            ['f',  'f',   'f',  '.']
        ]
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
        string = 'A & B; A v B'
        f = string_to_sequent(string)
        fm = string_to_sequent('A, B; A v B')
        fmm = string_to_sequent('A, B; A, B')
        tree = sequent_to_tree(f)
        expected_css = [
            ['.', 'fmmt'],
            ['fmm', 'fmmt'],
            ['fmm', 'fmt'],
            ['fm', 'fmt'],
            ['fm', 'ft'],
            ['f', 'ft'],
            ['f', '.']
        ]
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
        string = 'A v B; A v B'
        f = string_to_sequent(string)
        fl = string_to_sequent('A; A v B')
        fr = string_to_sequent('B; A v B')
        flm = string_to_sequent('A; A, B')
        frm = string_to_sequent('B; A, B')
        tree = sequent_to_tree(f)
        expected_css = [
            ['.', 'flmt', '.', 'frmt'],
            ['flm', 'flmt', 'frm', 'frmt'],
            ['flm', 'flt', 'frm', 'frt'],
            ['fl' , 'flt', 'fr', 'frt'],
            ['fl', '.', 'fr', 'ft'],
            ['f', 'f', 'f', 'ft'],
            ['f', 'f', 'f', '.'],
        ]
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
        string = 'A & B; A & B'
        f = string_to_sequent(string)
        fm = string_to_sequent('A, B; A & B')
        fml = string_to_sequent('A, B; A')
        fmr = string_to_sequent('A, B; B')
        tree = sequent_to_tree(f)
        expected_css = [
            ['.', 'fmlt', '.', 'fmrt'],
            ['fml', 'fmlt', 'fmr', 'fmrt'],
            ['fml', '.', 'fmr','fmt'],
            ['fm', 'fm', 'fm', 'fmt'],
            ['fm', 'fm', 'fm', 'ft'],
            ['f', 'f', 'f', 'ft'],
            ['f', 'f', 'f', '.'],
        ]
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
        string = 'A v B; C & D'
        f = string_to_sequent(string)
        fl = string_to_sequent('A; C & D')
        fr = string_to_sequent('B; C & D')
        fll = string_to_sequent('A; C')
        flr = string_to_sequent('A; D')
        frl = string_to_sequent('B; C')
        frr = string_to_sequent('B; D')
        tree = string_to_tree(string)
        expected_css = [
            ['.',   'fllt', '.',   'flrt', '.',   'frlt', '.',   'frrt'],
            ['fll', 'fllt', 'flr', 'flrt', 'frl', 'frlt', 'frr', 'frrt'],
            ['fll', '.',    'flr', 'flt',  'frl', '.',    'frr', 'frt'],
            ['fl',  'fl',   'fl',  'flt',  'fr',  'fr',   'fr',  'frt'],
            ['fl',  'fl',   'fl',  '.',    'fr',  'fr',   'fr',  'ft'],
            ['f',   'f',    'f',   'f',    'f',   'f',    'f',   'ft'],
            ['f',   'f',    'f',   'f',    'f',   'f',    'f',   '.'],
        ]
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
        pass


if __name__ == '__main__':
    unittest.main()
