import unittest
from unittest.mock import patch

from proposition import Atom, Conjunction
from sequent import Sequent
from tree import Tree


class TestAtomic(unittest.TestCase):
    def test_tree_grows_atom_to_none(self) -> None:
        p = Atom('p')
        q = Atom('q')

        sequent = Sequent(ant=p, con=q)
        tree = Tree(sequent)
        tree.grow()
        expected = [None]
        self.assertEqual(expected, tree.branches)


class TestOneParentInvertible(unittest.TestCase):
    def test_left_and(self) -> None:
        with patch('rules.get_rule_setting', return_value='mul'):
            p = Atom('p')
            q = Atom('q')

            sequent = Sequent(
                ant=Conjunction(p, q),
                con=()
            )
            tree = Tree(sequent)
            tree.grow()
            actual = tree.branches

            parent_sequent = Sequent(
                ant=(p, q),
                con=()
            )
            parent_tree = Tree(parent_sequent)
            expected = [parent_tree]

            self.assertEqual(actual, expected)
            self.assertEqual([None], parent_tree.branches)
