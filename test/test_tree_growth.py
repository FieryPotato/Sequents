import unittest

from proposition import Atom, Conjunction, Disjunction, Conditional, Negation
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

        self.assertIsInstance(tree.branches, list)
        self.assertEqual(len(tree.branches), 1)
        self.assertIsInstance(tree.branches[0], tuple)
        self.assertEqual(len(tree.branches[0]), 1)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(parent_sequent, tree.branches[0][0].root)

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

        self.assertIsInstance(tree.branches, list)
        self.assertEqual(len(tree.branches), 1)
        self.assertIsInstance(tree.branches[0], tuple)
        self.assertEqual(len(tree.branches[0]), 1)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(parent_sequent, tree.branches[0][0].root)

    def test_right_implies(self) -> None:
        p = Atom('p')
        q = Atom('q')

        sequent = Sequent(
            ant=None,
            con=Conditional(p, q)
        )
        tree = Tree(sequent)
        tree.grow()

        parent_sequent = Sequent(
            ant=p,
            con=q
        )

        self.assertIsInstance(tree.branches, list)
        self.assertEqual(len(tree.branches), 1)
        self.assertIsInstance(tree.branches[0], tuple)
        self.assertEqual(len(tree.branches[0]), 1)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(parent_sequent, tree.branches[0][0].root)

    def test_left_not(self) -> None:
        p = Atom('p')

        sequent = Sequent(
            ant=Negation(p),
            con=None
        )
        tree = Tree(sequent)
        tree.grow()

        parent_sequent = Sequent(
            ant=None,
            con=p
        )

        self.assertIsInstance(tree.branches, list)
        self.assertEqual(len(tree.branches), 1)
        self.assertIsInstance(tree.branches[0], tuple)
        self.assertEqual(len(tree.branches[0]), 1)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(parent_sequent, tree.branches[0][0].root)

    def test_right_not(self) -> None:
        p = Atom('p')

        sequent = Sequent(
            ant=None,
            con=Negation(p)
        )
        tree = Tree(sequent)
        tree.grow()

        parent_sequent = Sequent(
            ant=p,
            con=None
        )

        self.assertIsInstance(tree.branches, list)
        self.assertEqual(len(tree.branches), 1)
        self.assertIsInstance(tree.branches[0], tuple)
        self.assertEqual(len(tree.branches[0]), 1)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(parent_sequent, tree.branches[0][0].root)


class TestTwoParentInvertible(unittest.TestCase):
    def test_right_add_and(self):
        p = Atom('p')
        q = Atom('q')

        sequent = Sequent(
            ant=None,
            con=Conjunction(p, q)
        )
        tree = Tree(sequent)
        tree.grow()

        left_parent = Sequent(
            ant=None,
            con=p
        )
        right_parent = Sequent(
            ant=None,
            con=q
        )

        self.assertIsInstance(tree.branches, list)
        self.assertEqual(len(tree.branches), 1)
        self.assertIsInstance(tree.branches[0], tuple)
        self.assertEqual(len(tree.branches[0]), 2)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(left_parent, tree.branches[0][0].root)
        self.assertIsInstance(tree.branches[0][1], Tree)
        self.assertEqual(right_parent, tree.branches[0][1].root)
