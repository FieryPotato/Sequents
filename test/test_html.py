import unittest

from convert import string_to_tree, string_to_sequent
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
    def test_one(self) -> None:
        tree = string_to_tree('A; B')
        expected_css = [
            ['.', 'ft'],
            ['f', 'ft'],
            ['f', '.' ],
        ]

        seq = string_to_sequent('A; B')
        expected_objects = [
            [None, seq.tag()],
            [str(seq),  seq.tag()],
            [str(seq),  None]
        ]
        expected = expected_css, expected_objects
        actual = gridify(tree)
        self.assertEqual(expected, actual)



if __name__ == '__main__':
    unittest.main()
