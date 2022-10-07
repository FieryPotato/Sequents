import unittest

from convert import string_to_tree
from html.utils import get_array


class TestHTMLArrayCreation(unittest.TestCase):
    def test_atom(self) -> None:
        t = string_to_tree('A; B')
        actual = get_array(t)
        expected = [
            ['.', '.'],
            ['.', '.'],
            ['.', '.'],
        ]
        self.assertEqual(expected, actual)

    def test_complexity_1(self) -> None:
        t_1 = string_to_tree('A & B; C')
        a_1 = get_array(t_1)
        e_1 = [
            ['.', '.'],
            ['.', '.'],
            ['.', '.'],
            ['.', '.'],
            ['.', '.'],
        ]
        self.assertEqual(e_1, a_1)

        t_2 = string_to_tree('A; B & C')
        a_2 = get_array(t_2)
        e_2 = [
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
        ]
        self.assertEqual(e_2, a_2)

    def test_complexity_2(self) -> None:
        t_1 = string_to_tree('A; B -> (C -> D)')
        a_1 = get_array(t_1)
        e_1 = [
            ['.', '.'],
            ['.', '.'],
            ['.', '.'],
            ['.', '.'],
            ['.', '.'],
            ['.', '.'],
            ['.', '.'],
        ]
        self.assertEqual(e_1, a_1)

        t_2 = string_to_tree('; A & (B v C)')
        a_2 = get_array(t_2)
        e_2 = [
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
        ]
        self.assertEqual(e_2, a_2)

        t_5 = string_to_tree('; A v (B & C)')
        a_5 = get_array(t_5)
        e_5 = [
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
        ]
        self.assertEqual(e_5, a_5)

        t_6 = string_to_tree('(A v B) v C; ')
        a_6 = get_array(t_6)
        e_6 = [
            ['.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.'],
        ]
        self.assertEqual(e_6, a_6)

        t_7 = string_to_tree('; A & (B & C)')
        a_7 = get_array(t_7)
        e_7 = [
            ['.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.'],
        ]
        self.assertEqual(e_7, a_7)

        t_8 = string_to_tree('A v B; C & D')
        a_8 = get_array(t_8)
        e_8 = [
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.']
        ]
        self.assertEqual(e_8, a_8)



if __name__ == '__main__':
    unittest.main()
