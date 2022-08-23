import unittest

from unittest.mock import patch

from proposition import Atom, Conjunction, Negation, Disjunction, Conditional
from sequent import Sequent
from tree import Tree


class TestTree(unittest.TestCase):
    p = Atom('p')
    q = Atom('q')
    n = Negation(p)
    cj = Conjunction(p, q)
    cd = Conditional(p, q)
    dj = Disjunction(p, q)

    def test_tree_has_root(self) -> None:
        sequent = Sequent((), ())
        tree = Tree(sequent)
        self.assertEqual(tree.root, sequent)
        self.assertEqual(tree.branches, {sequent: {}})

    def test_tree_starts_not_full(self) -> None:
        sequent = Sequent((self.p,), (self.q,))
        tree = Tree(sequent)
        self.assertFalse(tree.is_grown)

    def test_tree_grows_atom_to_none(self) -> None:
        sequent = Sequent((self.p,), (self.q,))
        tree = Tree(sequent)
        tree.grow()
        actual = tree.branches
        expected = {
            sequent: None
        }
        self.assertEqual(expected, actual)

    def test_tree_grows_one_parent_invertible_only(self) -> None:
        with patch('rules.get_rule_setting', return_value='mul'):
            sequent = Sequent((self.cj,), ())
            tree = Tree(sequent)
            tree.grow()
            actual = tree.branches
            expected = {
                sequent: {
                    Sequent((self.p, self.q), ()): None
                }
            }
            self.assertEqual(expected, actual)

    def test_tree_grows_two_parent_invertible_only(self) -> None:
        with patch('rules.get_rule_setting', return_value='add'):
            sequent = Sequent((self.dj,), ())
            tree = Tree(sequent)
            tree.grow()
            actual = tree.branches
            expected = {
                sequent: {
                    Sequent((self.p,), ()): None,
                    Sequent((self.q,), ()): None
    
                }
            }
            self.assertEqual(expected, actual)
    
    def test_tree_can_only_be_grown_once(self) -> None:
        sequent = Sequent((), ())
        tree = Tree(sequent)
        tree.grow()
        with self.assertRaises(Tree.TreeIsGrownError):
            tree.grow()

    def test_tree_grows_one_parent_non_invertible_only(self) -> None:
        with patch('rules.get_rule_setting', return_value='add'):
            sequent = Sequent((self.cj,), ())
            tree = Tree(sequent)
            tree.grow()
            expected = {
                sequent: [
                    {
                        Sequent((self.p,), ()): None,
                    },
                    {
                        Sequent((self.q,), ()): None,
                    }
                ]
            }
            actual = tree.branches
            self.assertEqual(expected, actual)
            
    def test_tree_grows_two_parent_non_invertible_only(self) -> None:
        with patch('rules.get_rule_setting', return_value='mul'):
            sequent = Sequent((self.dj,), (self.p,))
            tree = Tree(sequent)
            tree.grow()
            expected = {
                sequent: [
                    {
                        Sequent((self.p,), (self.p,)): None,
                        Sequent((self.q,), ()): None,
                    },
                    {
                        Sequent((self.p,), ()): None,
                        Sequent((self.q,), (self.p,)): None,
                    }
                ]
            }
            actual = tree.branches
            self.assertEqual(expected, actual)

    def test_tree_grows_one_parent_non_invertible_two_parent_invertible(self) -> None:
        with patch('rules.get_rule_setting', return_value='add'):
            sequent = Sequent((self.cj,), (self.cj,))
            tree = Tree(sequent)
            tree.grow()
            expected = {
                sequent: [
                    {
                        Sequent((self.p,), (self.cj,)): {
                            Sequent((self.p,), (self.p,)): None,
                            Sequent((self.p,), (self.q,)): None
                        },
                    },
                    {
                        Sequent((self.q,), (self.cj,)): {
                            Sequent((self.q,), (self.p,)): None,
                            Sequent((self.q,), (self.q,)): None
                        },
                    }
                ]
            }
            actual = tree.branches
            self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
