import unittest

from src.sequent import Sequent
from src.proposition import *


class TestSequent(unittest.TestCase):
    def setUp(self) -> None:
        self.p = Atom("P")
        self.q = Atom("Q")
        self.n = Negation(self.p)
        self.cj = Conjunction(self.p, self.q)
        self.dj = Disjunction(self.p, self.q)
        self.cd = Conditional(self.p, self.q)

    def test_sequent_has_antecedent_and_consequent(self) -> None:
        s = Sequent([self.p], [self.q])
        self.assertEqual(self.p, s.ant[0])
        self.assertEqual(self.q, s.con[0])

    def test_sequent_equality(self) -> None:
        c = Conditional(self.p, self.p)
        d = Disjunction(self.p, self.p)
        atomic_a = Sequent([self.p], [self.p])
        atomic_b = Sequent([self.p], [self.p])
        self.assertEqual(atomic_a, atomic_b)
        self.assertNotEqual(atomic_a, ([self.p], [self.p]))

    def test_sequent_complexity(self) -> None:
        s_0 = Sequent([self.p], [self.q])
        self.assertEqual(0, s_0.complexity)
        s_1 = Sequent([self.n], [])
        self.assertEqual(1, s_1.complexity)
        s_2 = Sequent([self.n], [self.n])
        self.assertEqual(2, s_2.complexity)

    def test_atomic_sequent_cant_decompose(self) -> None:
        s = Sequent([self.p], [self.q])
        with self.assertRaises(Sequent.SequentIsAtomicError):
            s.decomposed()

    def test_decompose_lneg(self) -> None:
        s_0 = Sequent([self.n], [])
        expected_0 = [Sequent([], [self.p])]
        actual_0 = s_0.decomposed()
        self.assertEqual(expected_0, actual_0)
        
        s_1 = Sequent([self.n, self.q], [])
        expected_1 = [Sequent([self.q], [self.p])]
        actual_1 = s_1.decomposed()
        self.assertEqual(expected_1, actual_1)

    def test_decompose_rneg(self) -> None:
        s_0 = Sequent([], [self.n])
        expected_0 = [Sequent([self.p], [])]
        actual_0 = s_0.decomposed()
        self.assertEqual(expected_0, actual_0)
        
    def test_decompose_lcj(self) -> None:
        s = Sequent([self.cj], [])
        expected = [Sequent([self.p, self.q], [])]
        actual = s.decomposed()
        self.assertEqual(expected, actual)

    def test_decompose_rcj(self) -> None:
        s = Sequent([], [self.cj])
        expected = [Sequent([], [self.p]), Sequent([], [self.q])]
        actual = s.decomposed()
        self.assertEqual(expected, actual)
        
    def test_decompose_ldj(self) -> None:
        s = Sequent([self.dj], [])
        expected = [Sequent([self.p], []), Sequent([self.q], [])]
        actual = s.decomposed()
        self.assertEqual(expected, actual)

    def test_decompose_rdj(self) -> None:
        s = Sequent([], [self.dj])
        expected = [Sequent([], [self.p, self.q])]
        actual = s.decomposed()
        self.assertEqual(expected, actual)

    def test_decompose_lcd(self) -> None:
        s = Sequent([self.cd], [])
        expected = [Sequent([], [self.p]), Sequent([self.q], [])]
        self.assertEqual(expected, s.decomposed())

    def test_decompose_rcd(self) -> None:
        s = Sequent([], [self.cd])
        expected = [Sequent([self.p], [self.q])]
        self.assertEqual(expected, s.decomposed())
         
if __name__ == "__main__":
    unittest.main()

