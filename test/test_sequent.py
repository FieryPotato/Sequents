import unittest

from src.sequent import Sequent
from src.proposition import *


class TestSequent(unittest.TestCase):
    p = Atom("P")
    q = Atom("Q")
    n = Negation(p)
    cj = Conjunction(p, q)
    dj = Disjunction(p, q)
    cd = Conditional(p, q)

    def test_sequent_has_antecedent_and_consequent(self) -> None:
        s = Sequent((self.p,), (self.q,))
        self.assertEqual(self.p, s.ant[0])
        self.assertEqual(self.q, s.con[0])

    def test_sequent_equality(self) -> None:
        c = Conditional(self.p, self.p)
        d = Disjunction(self.p, self.p)
        atomic_a = Sequent((self.p,), (self.p,))
        atomic_b = Sequent((self.p,), (self.p,))
        self.assertEqual(atomic_a, atomic_b)
        self.assertNotEqual(atomic_a, ((self.p,), (self.p,)))
        self.assertNotEqual(c, d)

    def test_sequent_complexity(self) -> None:
        s_0 = Sequent((self.p,), (self.q,))
        self.assertEqual(0, s_0.complexity)
        s_1 = Sequent((self.n,), ())
        self.assertEqual(1, s_1.complexity)
        s_2 = Sequent((self.n,), (self.n,))
        self.assertEqual(2, s_2.complexity)


if __name__ == '__main__':
    unittest.main()

