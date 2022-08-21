import unittest

from src.proposition import Atom, Negation, Conditional, Conjunction,\
    Disjunction, Proposition
from src.sequent import Sequent
from src.rules import get_decomposer

class TestRules(unittest.TestCase):
    p = Atom("P")
    q = Atom("Q")
    n = Negation(p)
    cj = Conjunction(p, q)
    dj = Disjunction(p, q)
    cd = Conditional(p, q)

    def test_invertible_decomposition(self) -> None:
        sequents = [
            Sequent((self.n,), tuple()),   # LNEG
            Sequent(tuple(), (self.n,)),   # RNEG
            Sequent((self.cj,), tuple()),  # LAND
            Sequent(tuple(), (self.cj,)),  # RAND
            Sequent((self.dj,), tuple()),  # LOR
            Sequent(tuple(), (self.dj,)),  # ROR
            Sequent((self.cd,), tuple()),  # LIF
            Sequent(tuple(), (self.cd,))   # RIF
        ]

        expected = [
            Sequent(tuple(), (self.p,)),                                 # LNEG
            Sequent((self.p,), tuple()),                                 # RNEG
            Sequent((self.p, self.q), tuple()),                          # LAND
            (Sequent(tuple(), (self.p,)), Sequent(tuple(), (self.q,))),  # RAND
            (Sequent((self.p,), tuple()), Sequent((self.q,), tuple())),  # LOR
            Sequent(tuple(), (self.p, self.q)),                          # ROR
            (Sequent(tuple(), (self.p,)), Sequent((self.q,), tuple())),  # LIF
            (Sequent((self.p,), (self.q,)))                              # RIF
        ]

        for s, e in zip(sequents, expected):
            with self.subTest(i=s):
                decomposer = get_decomposer(s)
                actual = decomposer.decompose()
                self.assertEqual(e, actual)


if __name__ == '__main__':
    unittest.main()

