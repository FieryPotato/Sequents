import unittest

from unittest.mock import patch

from convert import dict_to_tree, tree_to_dict, string_to_tree, \
    string_to_sequent, sequent_to_tree
from proposition import Atom, Conjunction, Negation, Disjunction, Conditional
from sequent import Sequent
from tree import Tree, split_tree


class TestTreeMethods(unittest.TestCase):
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

    def test_tree_height(self) -> None:
        strings = 'A; B', 'A v B; C', 'A v B; C v D'
        expected = 1,      2,          3
        with patch('rules.get_rule_setting', return_value='add'):
            for s, e in zip(strings, expected):
                with self.subTest(i=s):
                    actual = string_to_tree(s).height()
                    self.assertEqual(e, actual)

    def test_tree_width(self) -> None:
        with patch('rules.get_rule_setting', return_value='add'):
            t_1 = string_to_tree('A; B')
            self.assertEqual(1, t_1.width())

            t_2 = string_to_tree('A; B & C')
            self.assertEqual(2, t_2.width())

        with patch('rules.get_rule_setting', return_value='mul'):
            t_1_ = string_to_tree('A & B; C')
            self.assertEqual(1, t_1_.width())


class TestTreeGrowth(unittest.TestCase):
    p = Atom('p')
    q = Atom('q')
    n = Negation(p)
    cj = Conjunction(p, q)
    cd = Conditional(p, q)
    dj = Disjunction(p, q)

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
        s_e = ['mul', 'mul', 'add', 'add', 'add', 'add']
        with patch('rules.get_rule_setting', side_effect=s_e):
            sequent = Sequent((self.dj,), (self.dj,))
            tree = Tree(sequent)
            tree.grow()
            expected = {
                sequent: [
                    {
                        Sequent((self.p,), (self.dj,)): [
                            {
                                Sequent((self.p,), (self.p,)): None,
                            },
                            {
                                Sequent((self.p,), (self.q,)): None,
                            }
                        ],
                        Sequent((self.q,), ()): None,
                    },
                    {
                        Sequent((self.p,), ()): None,
                        Sequent((self.q,), (self.dj,)): [
                            {
                                Sequent((self.q,), (self.p,)): None,
                            },
                            {
                                Sequent((self.q,), (self.q,)): None,
                            }
                        ]
                    }
                ]
            }
            actual = tree.branches
            self.assertEqual(expected, actual)

    def test_tree_grows_tpni_tpni(self) -> None:
        with patch('rules.get_rule_setting', return_value='mul'):
            sequent = Sequent((self.dj,), (self.cj,))
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
                        ],
                        Sequent((self.q,), ()): None
                    },
                    {
                        Sequent((self.p,), ()): None,
                        Sequent((self.q,), (self.cj,)): [
                            {
                                Sequent((self.q,), (self.p,)): None,
                                Sequent((), (self.q,)): None
                            },
                            {
                                Sequent((), (self.p,)): None,
                                Sequent((self.q,), (self.q,)): None
                            }
                        ],
                    }
                ]
            }
            actual = tree.branches
            self.assertEqual(expected, actual)

    def test_from_dict(self) -> None:
        test = {
            Sequent((self.n, self.cj), (self.cd, self.n)): {
                Sequent((self.cj,), (self.cd, self.n, self.p)): {
                    Sequent((self.p, self.q), (self.cd, self.n, self.p)): {
                        Sequent((self.p, self.q, self.p), (self.n, self.p, self.q)): {
                            Sequent((self.p, self.q, self.p, self.p), (self.p, self.q)): None
                        }
                    }
                }
            }
        }
        tree = dict_to_tree(test)
        self.assertEqual(tree.branches, test)

    def test_to_dict_atomic(self) -> None:
        test = {
            Sequent((self.p,), (self.q,)): None
        }
        tree = dict_to_tree(test)
        expected = {
            'p; q': None
        }
        actual = tree_to_dict(tree)
        self.assertEqual(expected, actual)

    def test_to_dict_c_1_opi(self) -> None:
        test = {
            Sequent((self.p, self.n), ()): {
                Sequent((self.p,), (self.p,)): None
            }
        }
        tree = dict_to_tree(test)
        expected = {
            'p, ~ p; ': {
                'p; p': None
            }
        }
        actual = tree_to_dict(tree)
        self.assertEqual(expected, actual)

    def test_to_json_c_1_tpi(self) -> None:
        test = {
            Sequent((self.cd,), ()): {
                Sequent((), (self.p,)): None,
                Sequent((self.q,), ()): None
            }
        }
        tree = dict_to_tree(test)
        expected = {
            '(p -> q); ': {
                '; p': None,
                'q; ': None
            }
        }
        actual = tree_to_dict(tree)
        self.assertEqual(expected, actual)

    def test_to_json_c_1_opni(self) -> None:
        test = {
            Sequent((self.cj,), ()): [
                {Sequent((self.p,), ()): None},
                {Sequent((self.q,), ()): None}
            ]
        }
        tree = dict_to_tree(test)
        expected = {
            '(p & q); ': [
                {'p; ': None},
                {'q; ': None}
            ]
        }
        actual = tree_to_dict(tree)
        self.assertEqual(expected, actual)

    def test_to_json_c_1_tpni(self) -> None:
        test = {
            Sequent((self.p,), (self.dj,)): [
                {
                    Sequent((self.p,), (self.p,)): None,
                    Sequent((), (self.q,)): None
                },
                {
                    Sequent((), (self.p,)): None,
                    Sequent((self.p,), (self.q,)): None
                }
            ]
        }
        tree = dict_to_tree(test)
        expected = {
            'p; (p v q)': [
                {
                    'p; p': None,
                    '; q': None
                },
                {   
                    '; p': None,
                    'p; q': None
                }
            ]
        }
        actual = tree_to_dict(tree)
        self.assertEqual(expected, actual)

    def test_tree_can_have_names(self) -> None:
        names = {'alpha', 'beta', 'gamma'}
        tree = Tree(Sequent((), ()), names=names)
        self.assertEqual(names, tree.names)

    def test_tree_knows_how_many_leaves_it_has(self) -> None:
        strings = [
            "A v B; A v B",
            "A & B; A v B",
            "A v B; A & B",
            "A -> B, A; B"
        ]
        leaf_numbers = 2, 1, 4, 2
        pairs = zip(strings, leaf_numbers)
        for s, l in pairs:
            with self.subTest(i=s):
                t = string_to_tree(s)
                self.assertEqual(l, t.width())


class TestTreeSplitting(unittest.TestCase):
    maxDiff=None
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


if __name__ == '__main__':
    unittest.main()
