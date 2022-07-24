import unittest

from src.proposition import Proposition, Atom, Negation, Conjunction, \
    Conditional, Disjunction


class TestAtom(unittest.TestCase):
    def test_atom_has_content(self) -> None:
        a = Atom("p1")
        self.assertEqual(["p1"], a.content)

    def test_putting_more_than_one_prop_in_atom_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            proposition = Atom("p1", "p2")
    
    def test_atom_complexity_is_0(self) -> None:
        atom = Atom("p1")
        self.assertEqual(0, atom.complexity)

    def test_atom_arity_is_1(self) -> None:
        atom = Atom("p1")
        self.assertEqual(1, atom.arity)
       

class TestUnary(unittest.TestCase):
    def setUp(self) -> None:
        self.a1 = Atom("p1")
        self.n1 = Negation(self.a1)
        self.n2 = Negation(self.n1)
        
    def test_putting_more_than_one_prop_in_negation_raises_vaule_error(self) -> None:
        with self.assertRaises(ValueError):
            n = Negation(self.a1, self.a1)

    def test_negation_arity_is_one(self) -> None:
        n = Negation(self.a1)
        self.assertEqual(1, n.arity)

    def test_negation_complexity_is_one_plus_content_complexity(self) -> None:
        self.assertEqual(1, self.n1.complexity)
        self.assertEqual(2, self.n2.complexity)


class TestBinary(unittest.TestCase):
    def setUp(self) -> None:
        self.a1 = Atom("p1")
        
        self.cj1 = Conjunction(self.a1, self.a1)
        self.cj2_0_1 = Conjunction(self.a1, self.cj1)
        self.cj2_1_1 = Conjunction(self.cj1, self.cj1)
        
        self.cd1 = Conditional(self.a1, self.a1)
        self.cd2_0_1 = Conditional(self.a1, self.cd1)
        self.cd2_1_1 = Conditional(self.cd1, self.cd1)
        
        self.dj1 = Disjunction(self.a1, self.a1)
        self.dj2_0_1 = Disjunction(self.a1, self.dj1)
        self.dj2_1_1 = Disjunction(self.dj1, self.dj1)
        
        self.conjunctions = [
                self.cj1, self.cj2_0_1, self.cj2_1_1
        ]
        self.conditionals = [
                self.cd1, self.cd2_0_1, self.cd2_1_1
        ]
        self.disjunctions = [
                self.dj1, self.dj2_0_1, self.dj2_1_1
        ]

    def test_arity_is_2(self) -> None:
        for prop in (self.cj1, self.cd1, self.dj1): 
            self.assertEqual(2, prop.arity)
   
    def test__complexity_is_one_plus_greatest_content_complexity(self) -> None:
        for propset in (self.conjunctions, self.conditionals, self.disjunctions):
            p1, p201, p211 = propset
            self.assertEqual(1, p1.complexity)
            self.assertEqual(2, p201.complexity)
            self.assertEqual(2, p211.complexity)


    def test_disjunction_arity_is_2(self) -> None:
        self.assertEqual(2, self.cd1.arity)


if __name__ == "__main__":
    unittest.main()

