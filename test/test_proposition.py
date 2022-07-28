import unittest

from src.proposition import Proposition, Atom, Negation, Conjunction, \
    Conditional, Disjunction


class TestProposition(unittest.TestCase):
    def test_equals(self) -> None:
        a1 = Atom("p1")
        a2 = Atom("p1")
        a3 = Atom("p2")
        self.assertEqual(a1, a2)
        self.assertNotEqual(a1, a3)

class TestAtom(unittest.TestCase):
    def setUp(self) -> None:
        self.a1 = Atom("p1")

    def test_atom_has_content(self) -> None:
        self.assertEqual(["p1"], self.a1.content)

    def test_putting_more_than_one_prop_in_atom_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            proposition = Atom("p1", "p2")
    
    def test_atom_complexity_is_0(self) -> None:
        self.assertEqual(0, self.a1.complexity)

    def test_atom_arity_is_1(self) -> None:
        self.assertEqual(1, self.a1.arity)
      
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

    def test_negation_decomposed_is_negatum(self) -> None:
        ant = ([], [self.a1]),
        con = ([self.a1], []),
        self.assertEqual(ant, self.n1.decomposed("ant"))
        self.assertEqual(con, self.n1.decomposed("con"))

class TestBinary(unittest.TestCase):
    def setUp(self) -> None:
        self.a1 = Atom("p1")
        self.a2 = Atom("p2")
        
        self.cj1 = Conjunction(self.a1, self.a2)
        self.cj2_0_1 = Conjunction(self.a1, self.cj1)
        self.cj2_1_1 = Conjunction(self.cj1, self.cj1)
        
        self.cd1 = Conditional(self.a1, self.a2)
        self.cd2_0_1 = Conditional(self.a1, self.cd1)
        self.cd2_1_1 = Conditional(self.cd1, self.cd1)
        
        self.dj1 = Disjunction(self.a1, self.a2)
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
        self.assertEqual(2, self.dj1.arity)

    def test_conditional_arity_is_2(self) -> None:
        self.assertEqual(2, self.cd1.arity)

    def test_conjunction_arity_is_2(self) -> None:
        self.assertEqual(2, self.cj1.arity)

    def test_decompose_left_conjunction(self) -> None:
        expected = ([self.a1, self.a2], []),
        self.assertEqual(expected, self.cj1.decomposed("ant"))

    def test_decompose_right_conjunction(self) -> None:
        expected = ([], [self.a1]), ([], [self.a2])
        self.assertEqual(expected, self.cj1.decomposed("con"))

    def test_decompose_left_disjunction(self) -> None:
        expected = ([self.a1], []), ([self.a2], [])
        self.assertEqual(expected, self.dj1.decomposed("ant"))

    def test_decompose_right_disjunction(self) -> None:
        expected = ([], [self.a1, self.a2]),
        self.assertEqual(expected, self.dj1.decomposed("con"))
    
    def test_decompose_left_conditional(self) -> None:
        expected = ([], [self.a1]), ([self.a2], [])
        self.assertEqual(expected, self.cd1.decomposed("ant"))

    def test_decompose_right_conditional(self) -> None:
        expected = ([self.a1], [self.a2]),
        self.assertEqual(expected, self.cd1.decomposed("con"))


if __name__ == "__main__":
    unittest.main()

