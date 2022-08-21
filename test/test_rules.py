import unittest
from unittest.mock import patch

from proposition import Atom, Negation, Conditional, Conjunction, \
    Disjunction
from rules import get_decomposer
from sequent import Sequent


class TestRules(unittest.TestCase):
    p = Atom("P")
    q = Atom("Q")
    n = Negation(p)
    cj = Conjunction(p, q)
    dj = Disjunction(p, q)
    cd = Conditional(p, q)

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


if __name__ == '__main__':
    unittest.main()
