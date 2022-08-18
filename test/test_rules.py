import unittest

from src.proposition import Atom, Negation, Conditional, Conjunction,\
    Disjunction, Proposition
from src.sequent import Sequent
from src.rules import get_rule, LNeg, RNeg, MultLAnd, AddLAnd,\
    MultRAnd, AddRAnd, MultLOr, AddLOr, MultROr, AddROr, MultLIf,\
    AddLIf, MultRIf, AddRIf


class TestRules(unittest.TestCase):
    p = Atom("P")
    q = Atom("Q")
    n = Negation(p)
    cj = Conjunction(p, q)
    dj = Disjunction(p, q)
    cd = Conditional(p, q)

    def test_atomic_sequent_cant_decompose(self) -> None:
        for side in 'ant', 'con':
            with self.subTest(i=side):
                with self.assertRaises(Proposition.AtomicDecompositionError):
                    get_rule(self.p, side)

    def test_get_rules(self) -> None:
        expected_lst = [
            LNeg, LNeg, RNeg, RNeg, MultLAnd, AddLAnd, MultRAnd, 
            AddRAnd, MultLOr, AddLOr, MultROr, AddROr, MultLIf, 
            AddLIf, MultRIf, AddRIf
        ]
        
        tests = []
        for prop in (self.n, self.cj, self.dj, self.cd):
            for side in 'ant', 'con':
                for t in 'mul', 'add':
                    tests.append((prop, side, t))

        for expected, test in zip(expected_lst, tests):
            prop, side, t = test
            with self.subTest(i=[prop, side, t]):
                actual = get_rule(prop, side, t)
                self.assertEqual(expected, actual)



if __name__ == '__main__':
    unittest.main()

