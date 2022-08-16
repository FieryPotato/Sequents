import unittest

from src.proposition import Atom, Negation, Conjunction, \
    Conditional, Disjunction, tupseq


class TestProposition(unittest.TestCase):
    def test_equals(self) -> None:
        a1 = Atom('p1')
        a2 = Atom('p1')
        a3 = Atom('p2')
        self.assertEqual(a1, a2)
        self.assertNotEqual(a1, a3)


class TestAtom(unittest.TestCase):
    def setUp(self) -> None:
        self.a1 = Atom('p1')

    def test_atom_has_content(self) -> None:
        self.assertEqual(['p1'], self.a1.content)

    def test_putting_more_than_one_prop_in_atom_raises_value_error(self) -> None:
        with self.assertRaises(TypeError):
            Atom('p1', 'p2')

    def test_atom_complexity_is_0(self) -> None:
        self.assertEqual(0, self.a1.complexity)

    def test_atom_arity_is_1(self) -> None:
        self.assertEqual(1, self.a1.arity)

    def test_atom_is_hashable(self) -> None:
        a = {Atom('a'), Atom('b'), Atom('c')}
        b = {Atom('a'), Atom('b'), Atom('c')}
        self.assertEqual(a, b)

    def test_atom_is_immutable(self) -> None:
        with self.assertRaises(Exception):
            self.a1.prop = 'hello'


class TestNegation(unittest.TestCase):
    def setUp(self) -> None:
        self.a1 = Atom('p1')
        self.n1 = Negation(self.a1)
        self.n2 = Negation(self.n1)

    def test_creating_prop_with_string_raises_error(self) -> None:
        with self.assertRaises(TypeError):
            Negation('word')

    def test_putting_more_than_one_prop_in_negation_raises_value_error(self) -> None:
        with self.assertRaises(TypeError):
            Negation(self.a1, self.a1)

    def test_negation_arity_is_one(self) -> None:
        n = Negation(self.a1)
        self.assertEqual(1, n.arity)

    def test_negation_complexity_is_one_plus_content_complexity(self) -> None:
        self.assertEqual(1, self.n1.complexity)
        self.assertEqual(2, self.n2.complexity)

    def test_decomposed_negation_in_antecedent(self) -> None:
        actual = self.n1.decomposed('ant')
        expected = tupseq(con=(self.a1,)),
        self.assertEqual(actual, expected)

    def test_decomposed_negation_in_consequent(self) -> None:
        actual = self.n1.decomposed('con')
        expected = tupseq(ant=(self.a1,)),
        self.assertEqual(actual, expected)

    def test_negation_is_hashable(self) -> None:
        a = {Negation(Atom('a')), Negation(Atom('b')), Negation(Atom('c'))}
        b = {Negation(Atom('a')), Negation(Atom('b')), Negation(Atom('c'))}
        self.assertEqual(a, b)

    def test_negation_is_immutable(self) -> None:
        with self.assertRaises(Exception):
            self.n1.negatum = Atom('test')


class TestBinary(unittest.TestCase):
    def setUp(self) -> None:
        self.a1 = Atom('p1')
        self.a2 = Atom('p2')

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
            with self.subTest(i=prop):
                self.assertEqual(2, prop.arity)

    def test_creating_connective_with_improper_number_of_values_raises_value_error(self) -> None:
        for t in Conjunction, Disjunction, Conditional:
            with self.subTest(i=t):
                with self.assertRaises(TypeError):
                    t(self.a1)
                with self.assertRaises(TypeError):
                    t(self.a1, self.a2, self.a1)

    def test_creating_connective_with_improper_type_raises_type_error(self) -> None:
        for t in Conjunction, Disjunction, Conditional:
            with self.subTest(i=t):
                with self.assertRaises(TypeError):
                    t('oh no', 'errors')

    def test_complexity_is_one_plus_greatest_content_complexity(self) -> None:
        for propset in (self.conjunctions, self.conditionals, self.disjunctions):
            with self.subTest(i=propset):
                p1, p201, p211 = propset
                self.assertEqual(1, p1.complexity)
                self.assertEqual(2, p201.complexity)
                self.assertEqual(2, p211.complexity)

    def test_arity_is_2(self) -> None:
        for prop in self.cd1, self.cj1, self.dj1:
            with self.subTest(i=prop):
                self.assertEqual(2, prop.arity)

    def test_decompose_left_conjunction(self) -> None:
        expected = ((self.a1, self.a2), tuple()),
        self.assertEqual(expected, self.cj1.decomposed('ant'))

    def test_decompose_right_conjunction(self) -> None:
        expected = (tuple(), (self.a1,)), (tuple(), (self.a2,))
        self.assertEqual(expected, self.cj1.decomposed('con'))

    def test_decompose_left_disjunction(self) -> None:
        expected = ((self.a1,), tuple()), ((self.a2,), tuple())
        self.assertEqual(expected, self.dj1.decomposed('ant'))

    def test_decompose_right_disjunction(self) -> None:
        expected = (tuple(), (self.a1, self.a2)),
        self.assertEqual(expected, self.dj1.decomposed('con'))

    def test_decompose_left_conditional(self) -> None:
        expected = (tuple(), (self.a1,)), ((self.a2,), tuple())
        self.assertEqual(expected, self.cd1.decomposed('ant'))

    def test_decompose_right_conditional(self) -> None:
        expected = ((self.a1,), (self.a2,)),
        self.assertEqual(expected, self.cd1.decomposed('con'))

    def test_binaries_are_hashable(self) -> None:
        a = Atom('test')
        b = Atom('atom')
        for t in Conjunction, Disjunction, Conditional:
            with self.subTest(i=t):
                first = {t(a, a), t(b, b)}
                second = {t(a, a), t(b, b)}
                self.assertEqual(first, second)

    def test_binaries_are_immutable(self) -> None:
        for prop in self.cj1, self.cd1, self.dj1:
            with self.subTest(i=prop):
                with self.assertRaises(Exception):
                    prop.left = 'anything, really'


if __name__ == '__main__':
    unittest.main()
