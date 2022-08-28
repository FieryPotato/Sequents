import unittest

from convert import deparenthesize, string_to_proposition, \
    string_to_sequent, find_connective
from proposition import Atom, Conditional, Conjunction, \
    Disjunction, Negation
from sequent import Sequent


class TestConvertProposition(unittest.TestCase):
    binary_connectives = ['and', 'or', 'implies', '&', 'v', '->']
    bin_test = ['the grass is green', 'the birds are singing']
    un_test = 'The cat is on the mat'
    atom = Atom(un_test)
    bin_atom_0 = Atom(bin_test[0])
    bin_atom_1 = Atom(bin_test[1])
    negation = Negation(atom)
    conjunction = Conjunction(bin_atom_0, bin_atom_1)
    conditional = Conditional(bin_atom_0, bin_atom_1)
    disjunction = Disjunction(bin_atom_0, bin_atom_1)
    comp_conj = Conjunction(conjunction, conjunction)
    comp_cond = Conditional(conditional, conditional)
    comp_disj = Disjunction(disjunction, disjunction)
    comp_neg = Negation(negation)

    def complex(self, connective: str) -> str:
        """
        Helper function to generate complex propositions.
        """
        string = '({g} {c} {b}) {c} ({g} {c} {b})'
        return string.format(g=self.bin_test[0], b=self.bin_test[1], c=connective)

    def test_atom_creation(self) -> None:
        strings = self.un_test, '(' + self.un_test + ')'
        for string in strings:
            expected = self.atom
            actual = string_to_proposition(string)
            with self.subTest(i=string):
                self.assertEqual(expected, actual)

    def test_binary_simple_no_parens_creation(self) -> None:
        props = [self.conjunction, self.disjunction, self.conditional] * 2
        c_w_spaces = [f' {c} ' for c in self.binary_connectives]
        tests = zip(c_w_spaces, props)
        for connective, expected in tests:
            string = connective.join(self.bin_test)
            actual = string_to_proposition(string)
            with self.subTest(i=connective):
                self.assertEqual(expected, actual)

    def test_binary_simple_parens_creation(self) -> None:
        props = [self.conjunction, self.disjunction, self.conditional] * 2
        c_w_spaces = [f' {c} ' for c in self.binary_connectives]
        tests = zip(c_w_spaces, props)
        for connective, expected in tests:
            string = '(' + connective.join(self.bin_test) + ')'
            actual = string_to_proposition(string)
            with self.subTest(i=connective):
                self.assertEqual(expected, actual)

    def test_binary_complex_creation(self) -> None:
        props = [self.comp_conj, self.comp_disj, self.comp_cond] * 2
        tests = zip(self.binary_connectives, props)
        for connective, expected in tests:
            string = self.complex(connective)
            actual = string_to_proposition(string)
            with self.subTest(i=connective):
                self.assertEqual(expected, actual)

    def test_negation_simple_no_parens_creation(self) -> None:
        for connective in ('not ', '~ '):
            string = connective + self.un_test
            expected = self.negation
            actual = string_to_proposition(string)
            with self.subTest(i=connective):
                self.assertEqual(expected, actual)

    def test_negation_simple_parens_creation(self) -> None:
        for connective in ('not ', '~ '):
            string = '(' + connective + self.un_test + ')'
            expected = self.negation
            actual = string_to_proposition(string)
            with self.subTest(i=connective):
                self.assertEqual(expected, actual)

    def test_negation_complex_creation(self) -> None:
        for connective in ('not', '~'):
            string = f'{connective} ({connective} {self.un_test})'
            expected = self.comp_neg
            actual = string_to_proposition(string)
            with self.subTest(i=connective):
                self.assertEqual(expected, actual)


class TestFindConnective(unittest.TestCase):
    def test_fc_returns_list_if_no_connective(self) -> None:
        string = 'anything'
        expected = ['anything']
        self.assertEqual(expected, find_connective(string))

    def test_fc_negation_atomic(self) -> None:
        for c in ('not', '~'):
            string = f'{c} the bird is in the bush'
            expected = [c, 'the bird is in the bush']
            with self.subTest(i=c):
                self.assertEqual(expected, find_connective(string))

    def test_fc_negation_nested(self) -> None:
        for c in ('not', '~'):
            string = f'{c} ({c} the bird is in the bush)'
            expected = [c, f'{c} the bird is in the bush']
            with self.subTest(i=c):
                self.assertEqual(expected, find_connective(string))

    def test_fc_binary_atomic(self) -> None:
        for c in ('and', '&', 'or', 'v', 'implies', '->'):
            string = f'the ball is red {c} the bat is blue'
            expected = ['the ball is red', c, 'the bat is blue']
            with self.subTest(i=c):
                self.assertEqual(expected, find_connective(string))

    def test_fc_binary_nested(self) -> None:
        for c in ('and', '&', 'or', 'v', 'implies', '->'):
            string = f'(word one {c} word two) {c} (word three {c} word four)'
            expected = [f'word one {c} word two', c, f'word three {c} word four']
            with self.subTest(i=c):
                self.assertEqual(expected, find_connective(string))


class TestDeparenthesize(unittest.TestCase):
    def test_single_set(self) -> None:
        s = '(words)'
        expected = 'words'
        actual = deparenthesize(s)
        self.assertEqual(expected, actual)

    def test_nested_set(self) -> None:
        s = '(nested (words))'
        expected = 'nested (words)'
        actual = deparenthesize(s)
        self.assertEqual(expected, actual)

    def test_double_nested_set(self) -> None:
        s = '((double nested))'
        expected = 'double nested'
        actual = deparenthesize(s)
        self.assertEqual(expected, actual)

    def test_disjoint_set(self) -> None:
        s = '(disjoint) -> (set)'
        self.assertEqual(s, deparenthesize(s))


class TestConvertSequent(unittest.TestCase):
    binaries = ['&', 'v', '->', 'and', 'or', 'implies']

    def test_atomic_1_1_sequent(self) -> None:
        string = 'antecedent one; consequent one'
        expected = Sequent(
            (Atom('antecedent one'),),
            (Atom('consequent one'),)
        )
        self.assertEqual(expected, string_to_sequent(string))

    def test_atomic_2_2_sequent(self) -> None:
        string = 'antecedent one, antecedent two; consequent one, consequent two'
        expected = Sequent(
            (Atom('antecedent one'), Atom('antecedent two')),
            (Atom('consequent one'), Atom('consequent two'))
        )
        self.assertEqual(expected, string_to_sequent(string))

    def test_negation_sequent(self) -> None:
        string = 'not one; ~ two'
        expected = Sequent((Negation(Atom('one')),), (Negation(Atom('two')),))
        self.assertEqual(expected, string_to_sequent(string))

    def test_binary_sequent(self) -> None:
        bare_string = 'left one {c} right one; left two {c} right two'
        types = (Conjunction, Disjunction, Conditional) * 2
        for connective, prop_type in zip(self.binaries, types):
            with self.subTest(i=connective):
                string = bare_string.format(c=connective)
                expected = Sequent(
                    (prop_type(Atom('left one'), Atom('right one')),),
                    (prop_type(Atom('left two'), Atom('right two')),)
                )
                self.assertEqual(expected, string_to_sequent(string))

    def test_convert_empty_antecedent(self) -> None:
        expected = Sequent((), (Atom('no antecedent'),))
        test_strings = '; no antecedent', ' ; no antecedent'
        for string in test_strings:
            with self.subTest(i=string):
                actual = string_to_sequent(string)
                self.assertEqual(expected, actual)

    def test_convert_empty_consequent(self) -> None:
        expected = Sequent((Atom('no consequent'),), ())
        test_strings = 'no consequent; ', 'no consequent;'
        for string in test_strings:
            with self.subTest(i=string):
                actual = string_to_sequent(string)
                self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
