import unittest

from proposition import Atom, Conjunction, Disjunction
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
        p = Atom('p')
        q = Atom('q')

        sequent = Sequent(
            ant=Conjunction(p, q),
            con=None
        )
        tree = Tree(sequent)
        tree.grow()

        parent_sequent = Sequent(
            ant=(p, q),
            con=None
        )

        assert isinstance(tree.branches, list)
        assert len(tree.branches) == 1
        assert isinstance(tree.branches[0], tuple)
        assert len(tree.branches[0]) == 1
        assert isinstance(tree.branches[0][0], Tree)
        assert parent_sequent == tree.branches[0][0].root

    def test_right_or(self) -> None:
        p = Atom('p')
        q = Atom('q')

        sequent = Sequent(
            ant=None,
            con=Disjunction(p, q)
        )
        tree = Tree(sequent)
        tree.grow()

        parent_sequent = Sequent(
            ant=None,
            con=(p, q)
        )

        assert isinstance(tree.branches, list)
        assert len(tree.branches) == 1
        assert isinstance(tree.branches[0], tuple)
        assert len(tree.branches[0]) == 1
        assert isinstance(tree.branches[0][0], Tree)
        assert parent_sequent == tree.branches[0][0].root
