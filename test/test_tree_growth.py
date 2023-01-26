import unittest
from unittest.mock import patch

from proposition import Atom, Conjunction, Disjunction, Conditional, Negation, Universal, Existential
from sequent import Sequent
from tree import Tree, Branch


class TestAtomic(unittest.TestCase):
    def test_tree_grows_atom_to_none(self) -> None:
        p = Atom('p')
        q = Atom('q')

        sequent = Sequent(ant=p, con=q)
        tree = Tree(sequent)
        tree.grow()
        expected = (None,)
        self.assertEqual(expected, tree.branches)


class TestOneParentInvertible(unittest.TestCase):
    def test_left_mul_and(self) -> None:
        p = Atom('p')
        q = Atom('q')

        sequent = Sequent(
            ant=Conjunction(p, q),
            con=None
        )
        tree = Tree(sequent)
        with patch('settings.__Settings.get_rule', return_value='mul'):
            tree.grow()

        parent_sequent = Sequent(
            ant=(p, q),
            con=None
        )

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(len(tree.branches), 1)
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertEqual(len(tree.branches[0]), 1)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(parent_sequent, tree.branches[0][0].root)

    def test_right_mul_or(self) -> None:
        p = Atom('p')
        q = Atom('q')

        sequent = Sequent(
            ant=None,
            con=Disjunction(p, q)
        )
        tree = Tree(sequent)
        with patch('settings.__Settings.get_rule', return_value='mul'):
            tree.grow()

        parent_sequent = Sequent(
            ant=None,
            con=(p, q)
        )

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(len(tree.branches), 1)
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertEqual(len(tree.branches[0]), 1)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(parent_sequent, tree.branches[0][0].root)

    def test_right_mul_implies(self) -> None:
        p = Atom('p')
        q = Atom('q')

        sequent = Sequent(
            ant=None,
            con=Conditional(p, q)
        )
        tree = Tree(sequent)
        with patch('settings.__Settings.get_rule', return_value='mul'):
            tree.grow()

        parent_sequent = Sequent(
            ant=p,
            con=q
        )

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(len(tree.branches), 1)
        self.assertIsInstance(tree.branches[0], Branch)
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

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(len(tree.branches), 1)
        self.assertIsInstance(tree.branches[0], Branch)
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

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(len(tree.branches), 1)
        self.assertIsInstance(tree.branches[0], Branch)
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
        with patch('settings.__Settings.get_rule', return_value='add'):
            tree.grow()

        left_parent = Sequent(
            ant=None,
            con=p
        )
        right_parent = Sequent(
            ant=None,
            con=q
        )

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(len(tree.branches), 1)
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertEqual(len(tree.branches[0]), 2)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(left_parent, tree.branches[0][0].root)
        self.assertIsInstance(tree.branches[0][1], Tree)
        self.assertEqual(right_parent, tree.branches[0][1].root)

    def test_left_add_or(self):
        p = Atom('p')
        q = Atom('q')

        sequent = Sequent(
            ant=Disjunction(p, q),
            con=None
        )
        tree = Tree(sequent)
        with patch('settings.__Settings.get_rule', return_value='add'):
            tree.grow()

        left_parent = Sequent(
            ant=p,
            con=None
        )
        right_parent = Sequent(
            ant=q,
            con=None
        )

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(1, len(tree.branches))
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertEqual(len(tree.branches[0]), 2)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(left_parent, tree.branches[0][0].root)
        self.assertIsInstance(tree.branches[0][1], Tree)
        self.assertEqual(right_parent, tree.branches[0][1].root)

    def test_left_add_if(self):
        p = Atom('p')
        q = Atom('q')

        sequent = Sequent(
            ant=Conditional(p, q),
            con=None
        )
        tree = Tree(sequent)
        with patch('settings.__Settings.get_rule', return_value='add'):
            tree.grow()

        left_parent = Sequent(
            ant=None,
            con=p
        )
        right_parent = Sequent(
            ant=q,
            con=None
        )

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(1, len(tree.branches))
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertEqual(len(tree.branches[0]), 2)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(left_parent, tree.branches[0][0].root)
        self.assertIsInstance(tree.branches[0][1], Tree)
        self.assertEqual(right_parent, tree.branches[0][1].root)


class TestOneParentNonInvertible(unittest.TestCase):
    def test_left_universal_with_no_names(self):
        uni = Universal('x', Atom('P<x>'))
        sequent = Sequent(
            ant=uni,
            con=None
        )
        tree = Tree(sequent)
        tree.grow()

        prop = Atom('P<NONE>')
        parent = Sequent(
            ant=prop,
            con=None
        )

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(1, len(tree.branches))
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertEqual(len(tree.branches[0]), 1)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(parent, tree.branches[0][0].root)

    def test_left_universal_with_two_names(self):
        uni = Universal('x', Atom('P<x, alice>'))
        sequent = Sequent(
            ant=uni,
            con=None
        )
        tree = Tree(sequent, names={'robert'})
        tree.grow()

        p_1 = Atom('P<alice, alice>')
        p_2 = Atom('P<robert, alice>')
        parents = {
            Sequent(
                ant=parent,
                con=None
            )
            for parent in (p_1, p_2)
        }
        leaves = {branch[0].root for branch in tree.branches}

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(2, len(tree.branches))
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertIsInstance(tree.branches[1], Branch)
        self.assertEqual(len(tree.branches[0]), 1)
        self.assertEqual(len(tree.branches[1]), 1)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertIsInstance(tree.branches[1][0], Tree)
        self.assertEqual(leaves, parents)

    def test_left_universal_with_tree_name(self):
        uni = Universal('x', Atom('P<x>'))
        sequent = Sequent(
            ant=uni,
            con=None
        )
        tree = Tree(sequent, names={'alice'})
        tree.grow()

        prop = Atom('P<alice>')
        parent = Sequent(
            ant=prop,
            con=None
        )

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(1, len(tree.branches))
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertEqual(len(tree.branches[0]), 1)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(parent, tree.branches[0][0].root)

    def test_right_universal_with_no_names(self):
        uni = Universal('x', Atom('P<x>'))
        sequent = Sequent(
            ant=None,
            con=uni,
        )
        tree = Tree(sequent)
        tree.grow()

        prop = Atom('P<NONE>')
        parent = Sequent(
            ant=None,
            con=prop,
        )

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(1, len(tree.branches))
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertEqual(len(tree.branches[0]), 1)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(parent, tree.branches[0][0].root)

    def test_right_universal_with_self_name(self):
        uni = Universal('x', Atom('P<x, robert>'))
        sequent = Sequent(
            ant=None,
            con=uni
        )
        tree = Tree(sequent)
        tree.grow()

        prop = Atom('P<NONE, robert>')
        parent = Sequent(
            ant=None,
            con=prop,
        )

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(1, len(tree.branches))
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertEqual(len(tree.branches[0]), 1)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(parent, tree.branches[0][0].root)

    def test_right_universal_with_two_names(self):
        uni = Universal('x', Atom('P<x, alice>'))
        sequent = Sequent(
            ant=None,
            con=uni,
        )
        tree = Tree(sequent, names={'robert'})
        tree.grow()

        prop = Atom('P<robert, alice>')
        parent = Sequent(
            ant=None,
            con=prop
        )

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(1, len(tree.branches))
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertEqual(len(tree.branches[0]), 1)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(parent, tree.branches[0][0].root)

    def test_left_existential_with_no_names(self):
        exi = Existential('x', Atom('P<x>'))
        sequent = Sequent(
            ant=exi,
            con=None
        )
        tree = Tree(sequent)
        tree.grow()

        prop = Atom('P<NONE>')
        parent = Sequent(
            ant=prop,
            con=None
        )

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(1, len(tree.branches))
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertEqual(len(tree.branches[0]), 1)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(parent, sorted(tree.branches[0])[0].root)

    def test_left_existential_with_two_names(self):
        exi = Existential('x', Atom('P<x, alice>'))
        sequent = Sequent(
            ant=exi,
            con=None
        )
        tree = Tree(sequent, names={'robert'})
        tree.grow()

        p_1 = Atom('P<alice, alice>')
        p_2 = Atom('P<robert, alice>')
        parents = {
            Sequent(
                ant=parent,
                con=None
            )
            for parent in (p_1, p_2)
        }
        leaves = {branch[0].root for branch in tree.branches}

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(2, len(tree.branches))
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertIsInstance(tree.branches[1], Branch)
        self.assertEqual(len(tree.branches[0]), 1)
        self.assertEqual(len(tree.branches[1]), 1)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertIsInstance(tree.branches[1][0], Tree)
        self.assertEqual(leaves, parents)

    def test_left_existential_with_three_names(self):
        exi = Existential('x', Atom('P<x>'))
        sequent = Sequent(
            ant=exi,
            con=None
        )
        tree = Tree(sequent, names={'alice'})
        tree.grow()

        prop = Atom('P<alice>')
        parent = Sequent(
            ant=prop,
            con=None
        )

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(1, len(tree.branches))
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertEqual(len(tree.branches[0]), 1)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(parent, tree.branches[0][0].root)

    def test_right_existential_with_no_names(self):
        exi = Existential('x', Atom('P<x>'))
        sequent = Sequent(
            ant=None,
            con=exi
        )
        tree = Tree(sequent)
        tree.grow()

        prop = Atom('P<NONE>')
        parent = Sequent(
            ant=None,
            con=prop
        )

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(1, len(tree.branches))
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertEqual(len(tree.branches[0]), 1)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(parent, sorted(tree.branches[0])[0].root)

    def test_right_existential_with_two_names(self):
        exi = Existential('x', Atom('P<x, alice>'))
        sequent = Sequent(
            ant=None,
            con=exi
        )
        tree = Tree(sequent, names={'robert'})
        tree.grow()

        p_1 = Atom('P<alice, alice>')
        p_2 = Atom('P<robert, alice>')
        parents = {
            Sequent(
                ant=None,
                con=parent
            )
            for parent in (p_1, p_2)
        }
        leaves = {branch[0].root for branch in tree.branches}

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(2, len(tree.branches))
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertIsInstance(tree.branches[1], Branch)
        self.assertEqual(len(tree.branches[0]), 1)
        self.assertEqual(len(tree.branches[1]), 1)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertIsInstance(tree.branches[1][0], Tree)
        self.assertEqual(leaves, parents)

    def test_right_existential_with_tree_name(self):
        exi = Existential('x', Atom('P<x>'))
        sequent = Sequent(
            ant=None,
            con=exi
        )
        tree = Tree(sequent, names={'alice'})
        tree.grow()

        prop = Atom('P<alice>')
        parent = Sequent(
            ant=None,
            con=prop
        )

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(1, len(tree.branches))
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertEqual(len(tree.branches[0]), 1)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(parent, tree.branches[0][0].root)

    def test_left_add_and(self):
        p = Atom('p')
        q = Atom('q')

        sequent = Sequent(
            ant=Conjunction(p, q),
            con=None
        )
        tree = Tree(sequent)
        with patch('settings.__Settings.get_rule', return_value='add'):
            tree.grow()

        p1 = Sequent(
            ant=p,
            con=None
        )
        p2 = Sequent(
            ant=q,
            con=None,
        )

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(len(tree.branches), 2)
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertIsInstance(tree.branches[1], Branch)
        self.assertEqual(len(tree.branches[0]), 1)
        self.assertEqual(len(tree.branches[1]), 1)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertIsInstance(tree.branches[1][0], Tree)
        self.assertEqual(p1, tree.branches[0][0].root)
        self.assertEqual(p2, tree.branches[1][0].root)

    def test_right_add_or(self):
        p = Atom('p')
        q = Atom('q')

        sequent = Sequent(
            ant=None,
            con=Disjunction(p, q),
        )
        tree = Tree(sequent)
        with patch('settings.__Settings.get_rule', return_value='add'):
            tree.grow()

        p1 = Sequent(
            ant=None,
            con=p
        )
        p2 = Sequent(
            ant=None,
            con=q,
        )

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(len(tree.branches), 2)
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertIsInstance(tree.branches[1], Branch)
        self.assertEqual(len(tree.branches[0]), 1)
        self.assertEqual(len(tree.branches[1]), 1)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertIsInstance(tree.branches[1][0], Tree)
        self.assertEqual(p1, tree.branches[0][0].root)
        self.assertEqual(p2, tree.branches[1][0].root)

    def test_right_add_if(self):
        p = Atom('p')
        q = Atom('q')

        sequent = Sequent(
            ant=None,
            con=Conditional(p, q),
        )
        tree = Tree(sequent)
        with patch('settings.__Settings.get_rule', return_value='add'):
            tree.grow()

        p1 = Sequent(
            ant=None,
            con=p
        )
        p2 = Sequent(
            ant=q,
            con=None,
        )

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(len(tree.branches), 2)
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertIsInstance(tree.branches[1], Branch)
        self.assertEqual(len(tree.branches[0]), 1)
        self.assertEqual(len(tree.branches[1]), 1)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertIsInstance(tree.branches[1][0], Tree)
        self.assertEqual(p1, tree.branches[0][0].root)
        self.assertEqual(p2, tree.branches[1][0].root)


class TestTwoParentNonInvertible(unittest.TestCase):
    def test_right_mul_and_only(self):
        p = Atom('p')
        q = Atom('q')

        sequent = Sequent(
            ant=None,
            con=Conjunction(p, q)
        )
        tree = Tree(sequent)
        with patch('settings.__Settings.get_rule', return_value='mul'):
            tree.grow()

        left_parent = Sequent(
            ant=None,
            con=p
        )
        right_parent = Sequent(
            ant=None,
            con=q
        )

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(len(tree.branches), 1)
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertEqual(len(tree.branches[0]), 2)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(left_parent, tree.branches[0][0].root)
        self.assertIsInstance(tree.branches[0][1], Tree)
        self.assertEqual(right_parent, tree.branches[0][1].root)

    def test_right_mul_and_with_propositions(self):
        p, q, r, s = (Atom(c) for c in 'pqrs')

        sequent = Sequent(
            ant=r,
            con=(Conjunction(p, q), s)
        )
        tree = Tree(sequent)
        with patch('settings.__Settings.get_rule', return_value='mul'):
            tree.grow()

        l0 = Sequent(ant=r, con=(p, s))
        r0 = Sequent(ant=None, con=q)

        l1 = Sequent(ant=r, con=p)
        r1 = Sequent(ant=None, con=(q, s))

        l2 = Sequent(ant=None, con=(p, s))
        r2 = Sequent(ant=r, con=q)

        l3 = Sequent(ant=None, con=p)
        r3 = Sequent(ant=r, con=(q, s))

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(len(tree.branches), 4)
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertEqual(len(tree.branches[0]), 2)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(l0, tree.branches[0][0].root)
        self.assertIsInstance(tree.branches[0][1], Tree)
        self.assertEqual(r0, tree.branches[0][1].root)
        self.assertEqual(len(tree.branches[1]), 2)
        self.assertIsInstance(tree.branches[1][0], Tree)
        self.assertEqual(l1, tree.branches[1][0].root)
        self.assertIsInstance(tree.branches[1][1], Tree)
        self.assertEqual(r1, tree.branches[1][1].root)
        self.assertEqual(len(tree.branches[2]), 2)
        self.assertIsInstance(tree.branches[2][0], Tree)
        self.assertEqual(l2, tree.branches[2][0].root)
        self.assertIsInstance(tree.branches[2][1], Tree)
        self.assertEqual(r2, tree.branches[2][1].root)
        self.assertEqual(len(tree.branches[3]), 2)
        self.assertIsInstance(tree.branches[3][0], Tree)
        self.assertEqual(l3, tree.branches[3][0].root)
        self.assertIsInstance(tree.branches[3][1], Tree)
        self.assertEqual(r3, tree.branches[3][1].root)

    def test_left_mul_or_only(self):
        p = Atom('p')
        q = Atom('q')

        sequent = Sequent(
            ant=Disjunction(p, q),
            con=None
        )
        tree = Tree(sequent)
        with patch('settings.__Settings.get_rule', return_value='mul'):
            tree.grow()

        left_parent = Sequent(
            ant=p,
            con=None
        )
        right_parent = Sequent(
            ant=q,
            con=None
        )

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(len(tree.branches), 1)
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertEqual(len(tree.branches[0]), 2)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(left_parent, tree.branches[0][0].root)
        self.assertIsInstance(tree.branches[0][1], Tree)
        self.assertEqual(right_parent, tree.branches[0][1].root)

    def test_left_mul_or_with_propositions(self):
        p, q, r, s = (Atom(c) for c in 'pqrs')

        sequent = Sequent(
            ant=(Disjunction(p, q), s),
            con=r
        )
        tree = Tree(sequent)
        with patch('settings.__Settings.get_rule', return_value='mul'):
            tree.grow()

        l0 = Sequent(ant=(p, s), con=r)
        r0 = Sequent(ant=q, con=None)

        l1 = Sequent(ant=(p, s), con=None)
        r1 = Sequent(ant=q, con=r)

        l2 = Sequent(ant=p, con=r)
        r2 = Sequent(ant=(q, s), con=None)

        l3 = Sequent(ant=p, con=None)
        r3 = Sequent(ant=(q, s), con=r)

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(len(tree.branches), 4)
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertEqual(len(tree.branches[0]), 2)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(l0, tree.branches[0][0].root)
        self.assertIsInstance(tree.branches[0][1], Tree)
        self.assertEqual(r0, tree.branches[0][1].root)
        self.assertEqual(len(tree.branches[1]), 2)
        self.assertIsInstance(tree.branches[1][0], Tree)
        self.assertEqual(l1, tree.branches[1][0].root)
        self.assertIsInstance(tree.branches[1][1], Tree)
        self.assertEqual(r1, tree.branches[1][1].root)
        self.assertEqual(len(tree.branches[2]), 2)
        self.assertIsInstance(tree.branches[2][0], Tree)
        self.assertEqual(l2, tree.branches[2][0].root)
        self.assertIsInstance(tree.branches[2][1], Tree)
        self.assertEqual(r2, tree.branches[2][1].root)
        self.assertEqual(len(tree.branches[3]), 2)
        self.assertIsInstance(tree.branches[3][0], Tree)
        self.assertEqual(l3, tree.branches[3][0].root)
        self.assertIsInstance(tree.branches[3][1], Tree)
        self.assertEqual(r3, tree.branches[3][1].root)

    def test_left_mul_if_only(self):
        p = Atom('p')
        q = Atom('q')

        sequent = Sequent(
            ant=Conditional(p, q),
            con=None
        )
        tree = Tree(sequent)
        with patch('settings.__Settings.get_rule', return_value='mul'):
            tree.grow()

        left_parent = Sequent(
            ant=None,
            con=p
        )
        right_parent = Sequent(
            ant=q,
            con=None
        )

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(len(tree.branches), 1)
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertEqual(len(tree.branches[0]), 2)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(left_parent, tree.branches[0][0].root)
        self.assertIsInstance(tree.branches[0][1], Tree)
        self.assertEqual(right_parent, tree.branches[0][1].root)

    def test_left_mul_if_with_propositions(self):
        p, q, r, s = (Atom(c) for c in 'pqrs')

        sequent = Sequent(
            ant=(Conditional(p, q), s),
            con=r
        )
        tree = Tree(sequent)
        with patch('settings.__Settings.get_rule', return_value='mul'):
            tree.grow()

        l0 = Sequent(ant=s, con=(p, r))
        r0 = Sequent(ant=q, con=None)

        l1 = Sequent(ant=s, con=p)
        r1 = Sequent(ant=q, con=r)

        l2 = Sequent(ant=None, con=(p, r))
        r2 = Sequent(ant=(q, s), con=None)

        l3 = Sequent(ant=None, con=p)
        r3 = Sequent(ant=(q, s), con=r)

        self.assertIsInstance(tree.branches, tuple)
        self.assertEqual(len(tree.branches), 4)
        self.assertIsInstance(tree.branches[0], Branch)
        self.assertEqual(len(tree.branches[0]), 2)
        self.assertIsInstance(tree.branches[0][0], Tree)
        self.assertEqual(l0, tree.branches[0][0].root)
        self.assertIsInstance(tree.branches[0][1], Tree)
        self.assertEqual(r0, tree.branches[0][1].root)
        self.assertEqual(len(tree.branches[1]), 2)
        self.assertIsInstance(tree.branches[1][0], Tree)
        self.assertEqual(l1, tree.branches[1][0].root)
        self.assertIsInstance(tree.branches[1][1], Tree)
        self.assertEqual(r1, tree.branches[1][1].root)
        self.assertEqual(len(tree.branches[2]), 2)
        self.assertIsInstance(tree.branches[2][0], Tree)
        self.assertEqual(l2, tree.branches[2][0].root)
        self.assertIsInstance(tree.branches[2][1], Tree)
        self.assertEqual(r2, tree.branches[2][1].root)
        self.assertEqual(len(tree.branches[3]), 2)
        self.assertIsInstance(tree.branches[3][0], Tree)
        self.assertEqual(l3, tree.branches[3][0].root)
        self.assertIsInstance(tree.branches[3][1], Tree)
        self.assertEqual(r3, tree.branches[3][1].root)
