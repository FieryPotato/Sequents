import unittest

from unittest.mock import patch

import convert
from convert import dict_to_tree, string_to_tree, \
    string_to_sequent, sequent_to_tree
from proposition import Atom, Conjunction, Negation, Disjunction, Conditional
from sequent import Sequent
from tree import Tree, split_tree


class TestTreeMethods(unittest.TestCase):

    def test_tree_height(self) -> None:
        self.assertEqual(1, string_to_tree('A; B').height())
        self.assertEqual(2, string_to_tree('A & B; C').height())
        self.assertEqual(2, string_to_tree('A; B & C').height())
        self.assertEqual(3, string_to_tree('A & B; C & D').height())
        self.assertEqual(3, string_to_tree('A & B; C v D').height())
        self.assertEqual(3, string_to_tree('A v B; C & D').height())
        self.assertEqual(3, string_to_tree('A; (A & B) & (C & D)').height())
        self.assertEqual(4, string_to_tree('(A & B) & (C & D); A').height())
        self.assertEqual(3, string_to_tree('(A v B) v (C v D); A').height())
        self.assertEqual(4, string_to_tree('A; (A v B) v (C v D)').height())
        self.assertEqual(3, string_to_tree('(A -> B) -> (C -> D); A').height())
        self.assertEqual(4, string_to_tree('A; (A -> B) -> (C -> D)').height())

    def test_tree_width(self) -> None:

        t_1 = string_to_tree('A; B')
        self.assertEqual(1, t_1.width())

        with patch('settings.__Settings.get_rule', return_value='add'):
            t_2 = string_to_tree('A; B & C')
            self.assertEqual(2, t_2.width())

        with patch('settings.__Settings.get_rule', return_value='mul'):
            t_1_ = string_to_tree('A & B; C')
            self.assertEqual(1, t_1_.width())


class TestTreeSplitting(unittest.TestCase):
    def test_complexity_0_tree(self) -> None:
        t = string_to_tree('A; A')
        self.assertEqual([t], split_tree(t))

    def test_c1_1pi(self) -> None:
        s = string_to_sequent('A & B; A, B')
        expected = [dict_to_tree({
            s: {string_to_sequent('A, B; A, B'): None}
        })]
        with patch('rules.get_rule_setting', return_value='mul'):
            tree = sequent_to_tree(s)
            actual = split_tree(tree)
            self.assertEqual(expected, actual)

    def test_c1_2pi(self) -> None:
        s = string_to_sequent('A, B; A & B')
        expected = [dict_to_tree({
            s: {string_to_sequent('A, B; A'): None,
                string_to_sequent('A, B; B'): None
                }
        })]
        with patch('rules.get_rule_setting', return_value='add'):
            t = sequent_to_tree(s)
            actual = split_tree(t)
            self.assertEqual(expected, actual)

    def test_c1_1pni(self) -> None:
        e_branch_a = {
            Sequent((Conjunction(Atom('A'), Atom('B')),), (Atom('A'), Atom('B'))):
                {Sequent((Atom('A'),), (Atom('A'), Atom('B'))): None}
        }
        e_branch_b = {
            Sequent((Conjunction(Atom('A'), Atom('B')),), (Atom('A'), Atom('B'))):
                {Sequent((Atom('B'),), (Atom('A'), Atom('B'))): None}
        }
        with patch('rules.get_rule_setting', return_value='add'):
            tree = string_to_tree('A & B; A, B')
            expected = [e_branch_a, e_branch_b]
            split = split_tree(tree)
            actual = [t.branches for t in split]
            self.assertEqual(expected, actual)

    def test_c1_2pni(self) -> None:
        root = string_to_sequent('A, B; C & D')
        a = {
            root: {
                string_to_sequent('A, B; C'): None,
                string_to_sequent('; D'): None
            }
        }
        b = {
            root: {
                string_to_sequent('A; C'): None,
                string_to_sequent('B; D'): None
            }
        }
        c = {
            root: {
                string_to_sequent('B; C'): None,
                string_to_sequent('A; D'): None
            }
        }
        d = {
            root: {
                string_to_sequent('; C'): None,
                string_to_sequent('A, B; D'): None
            }
        }
        expected = [a, b, c, d]
        with patch('rules.get_rule_setting', return_value='mul'):
            tree = sequent_to_tree(root)
            split = split_tree(tree)
            actual = [t.branches for t in split]
            self.assertEqual(expected, actual)

    def test_1pni_then_2pi_split(self) -> None:
        string = 'A & C, A -> B; B'
        root = convert.string_to_sequent(string)
        a = {
            root: {
                convert.string_to_sequent('A, A -> B; B'): {
                    convert.string_to_sequent('A, A; A'): None,
                    convert.string_to_sequent('A, B; B'): None
                }
            }
        }
        b = {
            root: {
                convert.string_to_sequent('C, A -> B; B'): {
                    convert.string_to_sequent('C, A; A'): None,
                    convert.string_to_sequent('C, B; B'): None
                }
            }

        }
        expected = [a, b]
        with patch('rules.get_rule_setting', return_value='add'):
            tree = convert.sequent_to_tree(root)
            split = split_tree(tree)
            actual = [t.branches for t in split]
            self.assertEqual(expected, actual)

    def test_quantified_split(self) -> None:
        string = 'Human<socrates>, forallx (Human<x> -> Mortal<x>); Mortal<socrates>'
        root = string_to_sequent(string)
        tree = string_to_tree(string)
        split = split_tree(tree)
        actual = [t.branches for t in split]
        a = {
            root: {
                string_to_sequent('Human<socrates>, Human<socrates> -> Mortal<socrates>; Mortal<socrates>'): {
                    string_to_sequent('Human<socrates>; Mortal<socrates>, Human<socrates>'): None,
                    string_to_sequent('Human<socrates>, Mortal<socrates>; Human<socrates>'): None
                }
            }

        }
        expected = [a]
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
