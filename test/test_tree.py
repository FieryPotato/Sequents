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
        self.assertEqual(tree.branches, {sequent: None})

    def test_tree_starts_not_full(self) -> None:
        sequent = Sequent((self.p,), (self.q,))
        tree = Tree(sequent)
        self.assertFalse(tree.is_grown)

    def test_tree_can_only_be_grown_once(self) -> None:
        sequent = Sequent((), ())
        tree = Tree(sequent)
        tree.grow()
        with self.assertRaises(Tree.TreeIsGrownError):
            tree.grow()

    def test_tree_grows_atom_to_none(self) -> None:
        sequent = Sequent((self.p,), (self.q,))
        tree = Tree(sequent)
        tree.grow()
        actual = tree.branches
        expected = {
            sequent: None
        }
        self.assertEqual(expected, actual)

    def test_tree_grows_opi_only(self) -> None:
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

    def test_tree_grows_tpi_only(self) -> None:
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

    def test_tree_grows_opni_only(self) -> None:
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
            
    def test_tree_grows_tpni_only(self) -> None:
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
            
    def test_tree_grows_opi_opi(self) -> None:
        with patch('rules.get_rule_setting', return_value='mul'):
            sequent = Sequent((self.cj,), (self.dj,))
            tree = Tree(sequent)
            tree.grow()
            expected = {
                sequent: {
                    Sequent((self.p, self.q), (self.dj,)): {
                        Sequent((self.p, self.q), (self.p, self.q)): None
                    }
                }
            }
            actual = tree.branches
            self.assertEqual(expected, actual)

    def test_tree_grows_opi_tpi(self) -> None:
        s_e = ['mul', 'mul', 'add', 'add']
        with patch('rules.get_rule_setting', side_effect=s_e):
            sequent = Sequent((self.cj,), (self.cj,))
            tree = Tree(sequent)
            tree.grow()
            expected = {
                sequent: {
                    Sequent((self.p, self.q), (self.cj,)): {
                        Sequent((self.p, self.q), (self.p,)): None,
                        Sequent((self.p, self.q), (self.q,)): None
                    }
                }
            }
            actual = tree.branches
            self.assertEqual(expected, actual)

    def test_tree_grows_opi_opni(self) -> None:
        s_e = ['mul', 'mul', 'add', 'add']
        with patch('rules.get_rule_setting', side_effect=s_e):
            sequent = Sequent((self.cj,), (self.dj,))
            tree = Tree(sequent)
            tree.grow()
            expected = {
                sequent: {
                    Sequent((self.p, self.q), (self.dj,)): [
                        {Sequent((self.p, self.q), (self.p,)): None},
                        {Sequent((self.p, self.q), (self.q,)): None}
                    ]
                }
            }
            actual = tree.branches
            self.assertEqual(expected, actual)

    def test_tree_grows_opi_tpni(self) -> None:
        with patch('rules.get_rule_setting', return_value='mul'):
            sequent = Sequent((self.cj,), (self.cj,))
            tree = Tree(sequent)
            tree.grow()
            expected = {
                sequent: {
                    Sequent((self.p, self.q), (self.cj,)): [
                        {
                            Sequent((self.p, self.q), (self.p,)): None,
                            Sequent((), (self.q,)): None
                        },
                        {
                            Sequent((self.p,), (self.p,)): None,
                            Sequent((self.q,), (self.q,)): None
                        },
                        {
                            Sequent((self.q,), (self.p,)): None,
                            Sequent((self.p,), (self.q,)): None
                        },
                        {
                            Sequent((), (self.p,)): None,
                            Sequent((self.p, self.q), (self.q,)): None
                        },
                    ]
                }
            }
            actual = tree.branches
            self.assertEqual(expected, actual)

    def test_tree_grows_tpi_opi(self) -> None:
        s_e = ['add', 'add', 'mul', 'mul', 'mul', 'mul']
        with patch('rules.get_rule_setting', side_effect=s_e):
            sequent = Sequent((self.dj,), (self.dj,))
            tree = Tree(sequent)
            tree.grow()
            expected = {
                sequent: {
                    Sequent((self.p,), (self.dj,)): {
                        Sequent((self.p,), (self.p, self.q)): None
                    },
                    Sequent((self.q,), (self.dj,)): {
                        Sequent((self.q,), (self.p, self.q)): None
                    }
                }
            }
            actual = tree.branches
            self.assertEqual(expected, actual)

    def test_tree_grows_tpi_tpi(self) -> None:
        s_e = ['add', 'add', 'add', 'add', 'add', 'add']
        with patch('rules.get_rule_setting', side_effect=s_e):
            sequent = Sequent((self.dj,), (self.cj,))
            tree = Tree(sequent)
            tree.grow()
            expected = {
                sequent: {
                    Sequent((self.p,), (self.cj,)): {
                        Sequent((self.p,), (self.p,)): None,
                        Sequent((self.p,), (self.q,)): None
                    },
                    Sequent((self.q,), (self.cj,)): {
                        Sequent((self.q,), (self.p,)): None,
                        Sequent((self.q,), (self.q,)): None
                    }
                }
            }
            actual = tree.branches
            self.assertEqual(expected, actual)

    def test_tree_grows_tpi_opni(self) -> None:
        s_e = ['add', 'add', 'add', 'add', 'add', 'add']
        with patch('rules.get_rule_setting', side_effect=s_e):
            sequent = Sequent((self.dj,), (self.dj,))
            tree = Tree(sequent)
            tree.grow()
            expected = {
                sequent: {
                    Sequent((self.p,), (self.dj,)): [
                        {Sequent((self.p,), (self.p,)): None},
                        {Sequent((self.p,), (self.q,)): None}
                    ],
                    Sequent((self.q,), (self.dj,)): [
                        {Sequent((self.q,), (self.p,)): None},
                        {Sequent((self.q,), (self.q,)): None}
                    ],
                }
            }
            actual = tree.branches
            self.assertEqual(expected, actual)

    def test_tree_grows_tpi_tpni(self) -> None:
        s_e = ['add', 'add', 'mul', 'mul', 'mul', 'mul']
        with patch('rules.get_rule_setting', side_effect=s_e):
            sequent = Sequent((self.dj,), (self.cj,))
            tree = Tree(sequent)
            tree.grow()
            expected = {
                sequent: {
                    Sequent((self.p,), (self.cj,)): [
                        {
                            Sequent((self.p,), (self.p,)): None,
                            Sequent((), (self.q,)): None,
                        },
                        {
                            Sequent((), (self.p,)): None,
                            Sequent((self.p,), (self.q,)): None,
                        }
                    ],
                    Sequent((self.q,), (self.cj,)): [
                        {
                            Sequent((self.q,), (self.p,)): None,
                            Sequent((), (self.q,)): None,
                        },
                        {
                            Sequent((), (self.p,)): None,
                            Sequent((self.q,), (self.q,)): None,
                        }
                    ]
                }
            }
            actual = tree.branches
            self.assertEqual(expected, actual)

    def test_tree_grows_opni_opi(self) -> None:
        s_e = ['add', 'add', 'mul', 'mul', 'mul', 'mul']
        with patch('rules.get_rule_setting', side_effect=s_e):
            sequent = Sequent((self.cj,), (self.dj,))
            tree = Tree(sequent)
            tree.grow()
            expected = {
                sequent: [
                    {
                        Sequent((self.p,), (self.dj,)): {
                            Sequent((self.p,), (self.p, self.q)): None
                        }
                    },
                    {
                        Sequent((self.q,), (self.dj,)): {
                            Sequent((self.q,), (self.p, self.q)): None
                        },
                    }
                ]
            }
            actual = tree.branches
            self.assertEqual(expected, actual)

    def test_tree_grows_opni_tpi(self) -> None:
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

    def test_tree_grows_opni_opni(self) -> None:
        with patch('rules.get_rule_setting', return_value='add'):
            sequent = Sequent((self.cj,), (self.dj,))
            tree = Tree(sequent)
            tree.grow()
            expected = {
                sequent: [
                    {
                        Sequent((self.p,), (self.dj,)): [
                            {
                                Sequent((self.p,), (self.p,)): None
                            },
                            {
                                Sequent((self.p,), (self.q,)): None
                            }
                        ]
                    },
                    {
                        Sequent((self.q,), (self.dj,)): [
                            {
                                Sequent((self.q,), (self.p,)): None
                            },
                            {
                                Sequent((self.q,), (self.q,)): None
                            }
                        ]
                    }
                ]
            }
            actual = tree.branches
            self.assertEqual(expected, actual)

    def test_tree_grows_opni_tpni(self) -> None:
        s_e = ['add', 'add', 'mul', 'mul', 'mul', 'mul']
        with patch('rules.get_rule_setting', side_effect=s_e):
            sequent = Sequent((self.cj,), (self.cj,))
            tree = Tree(sequent)
            tree.grow()
            expected = {
                sequent: [
                    {
                        Sequent((self.p,), (self.cj,)): [
                            {
                                Sequent((self.p,), (self.p,)): None,
                                Sequent((), (self.q,)): None
                            },
                            {
                                Sequent((), (self.p,)): None,
                                Sequent((self.p,), (self.q,)): None
                            }
                        ]
                    },
                    {
                        Sequent((self.q,), (self.cj,)): [
                            {
                                Sequent((self.q,), (self.p,)): None,
                                Sequent((), (self.q,)): None
                            },
                            {
                                Sequent((), (self.p,)): None,
                                Sequent((self.q,), (self.q,)): None
                            }
                        ]
                    }
                ]
            }
            actual = tree.branches
            self.assertEqual(expected, actual)

    def test_tree_grows_tpni_opi(self) -> None:
        with patch('rules.get_rule_setting', return_value='mul'):
            sequent = Sequent((self.dj,), (self.dj,))
            tree = Tree(sequent)
            tree.grow()
            expected = {
                sequent: [
                    {
                        Sequent((self.p,), (self.dj,)): {
                            Sequent((self.p,), (self.p, self.q)): None
                        },
                        Sequent((self.q,), ()): None
                    },
                    {
                        Sequent((self.p,), ()): None,
                        Sequent((self.q,), (self.dj,)): {
                            Sequent((self.q,), (self.p, self.q)): None
                        },
                    }
                ]
            }
            actual = tree.branches
            self.assertEqual(expected, actual)

    def test_tree_grows_tpni_tpi(self) -> None:
        s_e = ['mul', 'mul', 'add', 'add', 'add', 'add']
        with patch('rules.get_rule_setting', side_effect=s_e):
            sequent = Sequent((self.dj,), (self.cj,))
            tree = Tree(sequent)
            tree.grow()
            expected = {
                sequent: [
                    {
                        Sequent((self.p,), (self.cj,)):
                            {
                                Sequent((self.p,), (self.p,)): None,
                                Sequent((self.p,), (self.q,)): None
                            },
                        Sequent((self.q,), ()): None
                    },
                    {
                        Sequent((self.p,), ()): None,
                        Sequent((self.q,), (self.cj,)):
                            {
                                Sequent((self.q,), (self.p,)): None,
                                Sequent((self.q,), (self.q,)): None
                            }
                    }
                ]
            }
            actual = tree.branches
            self.assertEqual(expected, actual)

    def test_tree_grows_tpni_opni(self) -> None:
        pass

    def test_tree_grows_tpni_tpni(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
