import unittest
from unittest.mock import patch

from proposition import Atom, Negation, Conditional, Conjunction, \
    Disjunction, Universal, Existential
from rules import get_decomposer
from sequent import Sequent


class TestRules(unittest.TestCase):
    names = {'alpha', 'beta', 'gamma'}
    p = Atom('P')
    q = Atom('Q')
    x = Atom('P<x>')
    n = Negation(p)
    cj = Conjunction(p, q)
    dj = Disjunction(p, q)
    cd = Conditional(p, q)
    un = Universal('x', x)
    ex = Existential('x', x)

    def test_invertible_additive_decomposition(self) -> None:
        with patch('rules.get_rule_setting', return_value='add'):
            sequents = [
                Sequent((), (self.cj,)),  # RAND
                Sequent((self.dj,), ()),  # LOR
                Sequent((self.cd,), ()),  # LIF
            ]

            expected = [
                (Sequent((), (self.p,)), Sequent((), (self.q,))),  # RAND
                (Sequent((self.p,), ()), Sequent((self.q,), ())),  # LOR
                (Sequent((), (self.p,)), Sequent((self.q,), ())),  # LIF
            ]

            for s, e in zip(sequents, expected):
                with self.subTest(i=s):
                    decomposer = get_decomposer(s)
                    actual = decomposer.decompose()
                    self.assertEqual(e, actual)

    def test_invertible_multiplicative_decomposition(self) -> None:
        with patch('rules.get_rule_setting', return_value='mul'):
            sequents = [
                Sequent((self.n,), ()),   # LNEG
                Sequent((), (self.n,)),   # RNEG
                Sequent((self.cj,), ()),  # LAND
                Sequent((), (self.dj,)),  # ROR
                Sequent((), (self.cd,))   # RIF
            ]

            expected = [
                Sequent((), (self.p,)),         # LNEG
                Sequent((self.p,), ()),         # RNEG
                Sequent((self.p, self.q), ()),  # LAND
                Sequent((), (self.p, self.q)),  # ROR
                Sequent((self.p,), (self.q,))   # RIF
            ]

            for s, e in zip(sequents, expected):
                with self.subTest(i=s):
                    decomposer = get_decomposer(s)
                    actual = decomposer.decompose()
                    self.assertEqual(e, actual)

    def test_non_invertible_additive_decomposition(self) -> None:
        with patch('rules.get_rule_setting', return_value='add'):
            sequents = [
                Sequent((self.cj,), ()),  # LAND
                Sequent((), (self.dj,)),  # ROR
                Sequent((), (self.cd,))   # RIF
            ]

            expected = [
                [  # LAND
                    Sequent((self.p,), ()),
                    Sequent((self.q,), ())
                ],
                [  # ROR
                    Sequent((), (self.p,)),
                    Sequent((), (self.q,))
                ],
                [  # RIF
                    Sequent((self.p,), ()),
                    Sequent((), (self.q,))
                ]
            ]

            for s, e in zip(sequents, expected):
                with self.subTest(i=s):
                    decomposer = get_decomposer(s)
                    actual = decomposer.decompose()
                    self.assertEqual(e, actual)

    def test_non_invertible_multiplicative_decomposition(self) -> None:
        with patch('rules.get_rule_setting', return_value='mul'):
            sequents = [
                Sequent((self.p,), (self.cj,)),  # RAND
                Sequent((self.dj,), (self.p,)),  # LOR
                Sequent((self.cd,), (self.p,)),  # LIF
            ]

            expected = [
                [   # RAND
                    (
                        Sequent((self.p,), (self.p,)),
                        Sequent((), (self.q,))
                    ),
                    (
                        Sequent((), (self.p,)),
                        Sequent((self.p,), (self.q,))
                    )
                ],
                [   # LOR
                    (
                        Sequent((self.p,), (self.p,)),
                        Sequent((self.q,), ())
                    ),
                    (
                        Sequent((self.p,), ()),
                        Sequent((self.q,), (self.p,))
                    )
                ],
                [   # LIF
                    (
                        Sequent((), (self.p, self.p)),
                        Sequent((self.q,), ())
                    ),
                    (
                        Sequent((), (self.p,)),
                        Sequent((self.q,), (self.p,))
                    )
                ]
            ]

            for s, e in zip(sequents, expected):
                with self.subTest(i=s):
                    decomposer = get_decomposer(s)
                    actual = decomposer.decompose()
                    self.assertEqual(e, actual)

    def test_quantifier_decomposition(self) -> None:
        sequents = [  
            Sequent((self.un,), ()),  # LUni
            Sequent((), (self.un,)),  # RUni
            Sequent((self.ex,), ()),  # LExi
            Sequent((), (self.ex,)),  # RExi
        ]
        expected: list[list[Sequent]] = [
            [
                Sequent((Atom('P<alpha>'),), ()),
                Sequent((Atom('P<beta>'),), ()),
                Sequent((Atom('P<gamma>'),), ()),
            ],
            [
                Sequent((), (Atom('P<alpha>'),)),
                Sequent((), (Atom('P<beta>'),)),
                Sequent((), (Atom('P<gamma>'),)),
            ],
        ] * 2
        for s, e in zip(sequents, expected):
            with self.subTest(i=s):
                decomposer = get_decomposer(s, names=self.names)
                actual = decomposer.decompose()
                self.assertEqual(sorted(e), sorted(actual))


    def test_runi_instantiates_only_nonpresent_names(self):
        s1 = Sequent((Atom('T<beta>'),), (self.un,))
        expected: list[Sequent] = [
            Sequent((Atom('T<beta>'),), (Atom('P<alpha>'),)),
            Sequent((Atom('T<beta>'),), (Atom('P<gamma>'),))
        ]
        decomposer = get_decomposer(s1, names=self.names)
        actual = decomposer.decompose()
        self.assertEqual(sorted(expected), sorted(actual))

    def test_lexi_instantiates_only_nonpresent_names(self):
        s1 = Sequent((self.ex,), (Atom('T<gamma>'),))
        expected: list[Sequent] = [
            Sequent((Atom('P<alpha>'),), (Atom('T<gamma>'),)),
            Sequent((Atom('P<beta>'),), (Atom('T<gamma>'),))
        ]
        decomposer = get_decomposer(s1, names=self.names)
        actual = decomposer.decompose()
        self.assertEqual(sorted(expected), sorted(actual))



if __name__ == '__main__':
    unittest.main()
