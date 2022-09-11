import unittest

from proposition import Atom, Negation, Conjunction, \
    Conditional, Disjunction, Universal, Existential


class TestProposition(unittest.TestCase):
    def test_equals(self) -> None:
        a1 = Atom('p1')
        a2 = Atom('p1')
        a3 = Atom('p2')
        self.assertEqual(a1, a2)
        self.assertNotEqual(a1, a3)

    def test_getitem(self) -> None:
        atom = Atom('p1')
        self.assertEqual('p1', atom[0])


class TestAtom(unittest.TestCase):
    def setUp(self) -> None:
        self.a1 = Atom('p1')

    def test_atom_has_content(self) -> None:
        self.assertEqual(('p1',), self.a1.content)

    def test_string(self) -> None:
        expected = 'p1'
        actual = str(self.a1)
        self.assertEqual(expected, actual)

    def test_putting_more_than_one_prop_in_atom_raises_value_error(self) -> None:
        with self.assertRaises(TypeError):
            Atom('p1', 'p2')

    def test_init_with_non_string_object_raises_typeerror(self) -> None:
        with self.assertRaises(TypeError):
            Atom(self.a1)

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

    def test_quantified_atom_has_names(self) -> None:
        tests = [
            Atom('Predicate<alice>'),
            Atom('TwoPlace<beth, carol>'),
            Atom('L<daisy, e, florence>')
        ]
        expected = [
            ('alice',),
            ('beth', 'carol'),
            ('daisy', 'florence')
        ]
        for t, e in zip(tests, expected):
            with self.subTest(i=t):
                self.assertEqual(e, t.names)

    def test_quantified_atom_has_variables(self) -> None:
        tests = [
            Atom('Predicate<a>'),
            Atom('Property<b, c>'),
            Atom('R<d, eleanor, f>')
        ]
        expected = [
            ('a',),
            ('b', 'c'),
            ('d', 'f')
        ]
        for t, e in zip(tests, expected):
            with self.subTest(i=t):
                self.assertEqual(e, t.unbound_variables)

    def test_instantiate_atom(self) -> None:
        tests = [
            Atom('Predicate<a>'),
            Atom('Property<b, c>'),
            Atom('Relation<diana, e, frieda>')
        ]
        variables = [
            'a',
            'c',
            'e'
        ]
        names = [
            'adrian',
            'clemence',
            'emma'
        ]
        expected = [
            Atom('Predicate<adrian>'),
            Atom('Property<b, clemence>'),
            Atom('Relation<diana, emma, frieda>')
        ]
        for t, v, n, e in zip(tests, variables, names, expected):
            with self.subTest(i=t):
                self.assertEqual(e, t.instantiate(v, n))


class TestNegation(unittest.TestCase):
    def setUp(self) -> None:
        self.a1 = Atom('p1')
        self.n1 = Negation(self.a1)
        self.n2 = Negation(self.n1)

    def test_string(self) -> None:
        expected_0 = '~ p1'
        expected_1 = '~ ~ p1'
        self.assertEqual(expected_0, str(self.n1))
        self.assertEqual(expected_1, str(self.n2))

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

    def test_negation_is_hashable(self) -> None:
        a = {Negation(Atom('a')), Negation(Atom('b')), Negation(Atom('c'))}
        b = {Negation(Atom('a')), Negation(Atom('b')), Negation(Atom('c'))}
        self.assertEqual(a, b)

    def test_negation_is_immutable(self) -> None:
        with self.assertRaises(Exception):
            self.n1.prop = Atom('test')

    def test_negation_has_names(self) -> None:
        tests = [
            Negation(Atom('A<alice>')),
            Negation(Atom('B<betty, charlie>')),
            Negation(Negation(Atom('D<edgar, falcon, gerry>')))
        ]
        expected = [
            ('alice',),
            ('betty', 'charlie'),
            ('edgar', 'falcon', 'gerry')
        ]
        for t, e in zip(tests, expected):
            with self.subTest(i=t):
               self.assertEqual(e, t.names)

    def test_negation_has_variables(self) -> None:
        tests = [
            Negation(Atom('A<alice>')),
            Negation(Atom('A<a>')),
            Negation(Negation(Atom('B<b, charlie, d>')))
        ]
        expected = [
            (),
            ('a',),
            ('b', 'd'),
        ]
        for t, e in zip(tests, expected):
            with self.subTest(i=t):
                self.assertEqual(e, t.unbound_variables)

    def test_instantiate_negation(self) -> None:
        tests = [
            Negation(Atom('A<a>')),
            Negation(Atom('B<betty, c>')),
            Negation(Negation(Atom('D<edward, f, georg>')))
        ]
        variables = [
            'a',
            'c',
            'f'
        ]
        names = [
            'alice',
            'charlie',
            'francis'
        ]
        expected = [
            Negation(Atom('A<alice>')),
            Negation(Atom('B<betty, charlie>')),
            Negation(Negation(Atom('D<edward, francis, georg>')))
        ]
        for t, v, n, e in zip(tests, variables, names, expected):
            with self.subTest(i=t):
                self.assertEqual(e, t.instantiate(v, n))


class TestUniversal(unittest.TestCase):
    def test_arity_is_1(self) -> None:
        self.assertEqual(1, Universal.arity)
        
    def test_symb(self) -> None: 
        self.assertEqual('∀', Universal.symb)

    def test_var_and_prop(self) -> None:
        var = 'x'
        prop = Atom('P<x>')
        u1 = Universal('x', prop)
        self.assertEqual(var, u1.variable)
        self.assertEqual(prop, u1.prop)
        
    def test_universal_string(self) -> None:
        test = [
            Universal('a', Atom('P<a>')),
            Universal('b', Atom('P<alice, b>')),
            Universal('a', Universal('b', Atom('P<a, b>'))),
            Universal('x', Conditional(Atom('P<x>'), Atom('Q<x>')))
        ]
        expected = [
            '∀a P<a>',
            '∀b P<alice, b>',
            '∀a ∀b P<a, b>',
            '∀x (P<x> -> Q<x>)'
        ]
        for t, e in zip(test, expected):
            with self.subTest(i=t):
                self.assertEqual(e, str(t))

class TestExistential(unittest.TestCase):
    def test_arity_is_1(self) -> None:
        self.assertEqual(1, Existential.arity)

    def test_symb(self) -> None:
        self.assertEqual('∃', Existential.symb)

    def test_var_and_prop(self) -> None:
        var = 'x'
        prop = Atom('P<x>')
        e1 = Existential('x', prop)
        self.assertEqual(var, e1.variable)
        self.assertEqual(prop, e1.prop)

    def test_existential_string(self) -> None:
        test = [
            Existential('a', Atom('P<a>')),
            Existential('b', Atom('P<alice, b>')),
            Existential('a', Existential('b', Atom('P<a, b>'))),
            Existential('x', Conditional(Atom('P<x>'), Atom('Q<x>')))
        ]
        expected = [
            '∃a P<a>',
            '∃b P<alice, b>',
            '∃a ∃b P<a, b>',
            '∃x (P<x> -> Q<x>)'
        ]
        for t, e in zip(test, expected):
            with self.subTest(i=t):
                self.assertEqual(e, str(t))


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

    def test_conjunction_string(self) -> None:
        expecteds = [
            '(p1 & p2)',
            '(p1 & (p1 & p2))',
            '((p1 & p2) & (p1 & p2))'
        ]
        actuals = [
            self.cj1,
            self.cj2_0_1,
            self.cj2_1_1
        ]
        tests = zip(expecteds, actuals)
        for e, a in tests:
            with self.subTest(i=a):
                self.assertEqual(e, str(a))

    def test_disjunction_string(self) -> None:
        expecteds = [
            '(p1 v p2)',
            '(p1 v (p1 v p2))',
            '((p1 v p2) v (p1 v p2))'
        ]
        actuals = [
            self.dj1,
            self.dj2_0_1,
            self.dj2_1_1
        ]
        tests = zip(expecteds, actuals)
        for e, a in tests:
            with self.subTest(i=a):
                self.assertEqual(e, str(a))

    def test_conditional_string(self) -> None:
        expecteds = [
            '(p1 -> p2)',
            '(p1 -> (p1 -> p2))',
            '((p1 -> p2) -> (p1 -> p2))'
        ]
        actuals = [
            self.cd1,
            self.cd2_0_1,
            self.cd2_1_1
        ]
        tests = zip(expecteds, actuals)
        for e, a in tests:
            with self.subTest(i=a):
                self.assertEqual(e, str(a))

    def test_binary_names(self) -> None:
        classes = Conditional, Conjunction, Disjunction
        for cls in classes:
            tests = [
                cls(Atom('P<alice>'), Atom('Q<betty>')),
                cls(Negation(Atom('R<carol, destiny>')), Atom('S<eleanor, fancy>')),
            ]
            expected = [
                ('alice', 'betty'),
                ('carol', 'destiny', 'eleanor', 'fancy')
            ]
            for t, e in zip(tests, expected):
                with self.subTest(i=cls):
                    self.assertEqual(e, t.names)

    def test_binary_variables(self) -> None:
        classes = Conditional, Conjunction, Disjunction
        for cls in classes:
            tests = [
                cls(Atom('P<a>'), Atom('Q<b>')),
                cls(Negation(Atom('R<c, destiny>')), Atom('S<e, fancy>'))
            ]
            expected = [
                ('a', 'b'),
                ('c', 'e')
            ]
            for t, e in zip(tests, expected):
                with self.subTest(i=cls):
                    self.assertEqual(e, t.unbound_variables)

    def test_instantiate_binary(self) -> None:
        classes = Conditional, Conjunction, Disjunction
        for cls in classes:
            tests = [
                cls(Atom('P<a>'), Atom('Q<betty>')),
                cls(Atom('P<alice>'), Atom('Q<b>')),
                cls(Atom('P<a>'), Atom('Q<a>')),
                cls(Atom('P<alice>'), Atom('Q<a>')),
                cls(Negation(Atom('R<c, destiny>')), Atom('S<eleanor, c>'))
            ]
            variables = [
                'a',
                'b', 
                'a',
                'a',
                'c'
            ]
            names = [
                'alice',
                'betty',
                'alice', 
                'alice',
                'carol'
            ]
            expected = [
                cls(Atom('P<alice>'), Atom('Q<betty>')),
                cls(Atom('P<alice>'), Atom('Q<betty>')),
                cls(Atom('P<alice>'), Atom('Q<alice>')),
                cls(Atom('P<alice>'), Atom('Q<alice>')),
                cls(Negation(Atom('R<carol, destiny>')), Atom('S<eleanor, carol>'))
            ]
            for t, v, n, e in zip(tests, variables, names, expected):
                with self.subTest(i=t):
                    self.assertEqual(e, t.instantiate(v, n))
                


if __name__ == '__main__':
    unittest.main()
