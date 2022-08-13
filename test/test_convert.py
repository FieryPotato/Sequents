import unittest

from src.proposition import Atom, Conditional, Conjunction,\
        Disjunction, Negation
from src.convert import deparenthesize, string_to_proposition, find_connective

class TestConversion(unittest.TestCase):
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
        '''
        Helper function to generate complex propositions.
        '''
        string = '({g} {c} {b}) {c} ({g} {c} {b})'
        return string.format(g=self.bin_test[0], b=self.bin_test[1], c=connective)

    def test_atom(self) -> None:
        string = self.un_test
        expected = self.atom
        actual = string_to_proposition(string)
        self.assertEqual(expected, actual)

    def test_atom_parens(self) -> None:
        string = '(' + self.un_test + ')'
        expected = self.atom
        actual = string_to_proposition(string)
        self.assertEqual(expected, actual)

    def test_binary_simple_no_parens(self) -> None:
        props = [self.conjunction, self.disjunction, self.conditional] * 2
        c_w_spaces = [f' {c} ' for c in self.binary_connectives]
        tests = zip(c_w_spaces, props)
        for connective, expected in tests:
            with self.subTest(i=connective):
                string = connective.join(self.bin_test)
                actual = string_to_proposition(string)
                self.assertEqual(expected, actual)

    def test_binary_simple_parens(self) -> None:
        props = [self.conjunction, self.disjunction, self.conditional] * 2
        c_w_spaces = [f' {c} ' for c in self.binary_connectives]
        tests = zip(c_w_spaces, props)
        for connective, expected in tests:
            with self.subTest(i=connective):
                string = '(' + connective.join(self.bin_test) + ')'
                actual = string_to_proposition(string)
                self.assertEqual(expected, actual)

    def test_binary_complex(self) -> None:
        props = [self.comp_conj, self.comp_disj, self.comp_cond] * 2
        tests = zip(self.binary_connectives, props)
        for connective, expected in tests:
            with self.subTest(i=connective):
                string = self.complex(connective)
                actual = string_to_proposition(string)
                self.assertEqual(expected, actual)

    def test_negation_simple_no_parens(self) -> None:
        for connective in ('not ', '~ '):
            with self.subTest(i=connective):
                string = connective + self.un_test
                expected = self.negation
                actual = string_to_proposition(string)
                self.assertEqual(expected, actual)

    def test_negation_simple_parens(self) -> None:
        for connective in ('not ', '~ '):
            with self.subTest(i=connective):
                string = '(' + connective + self.un_test + ')'
                expected = self.negation
                actual = string_to_proposition(string)
                self.assertEqual(expected, actual)

    def test_negation_complex(self) -> None:
        for connective in ('not', '~'):
            with self.subTest(i=connective):
                string = f'{connective} ({connective} {self.un_test})'
                expected = self.comp_neg
                actual = string_to_proposition(string)
                self.assertEqual(expected, actual)


class TestFindConnective(unittest.TestCase):
    def test_fc_returns_list_if_no_connective(self) -> None:
        string = 'anything'
        expected = ['anything']
        self.assertEqual(expected, find_connective(string))

    def test_fc_negation_atomic(self) -> None:
        for c in ('not', '~'):
            with self.subTest(i=c):
                string = f'{c} the bird is in the bush'
                expected = [c, 'the bird is in the bush']
                self.assertEqual(expected, find_connective(string))

    def test_fc_negation_nested(self) -> None:
        for c in ('not', '~'):
            with self.subTest(i=c):
                string = f'{c} ({c} the bird is in the bush)'
                expected = [c, f'{c} the bird is in the bush']

    def test_fc_binary_atomic(self) -> None:
        for c in ('and', '&', 'or', 'v', 'implies', '->'):
            with self.subTest(i=c):
                string = f'the ball is red {c} the bat is blue'
                expected = ['the ball is red', c, 'the bat is blue']
                self.assertEqual(expected, find_connective(string))

    def test_fc_binary_nested(self) -> None:
        for c in ('and', '&', 'or', 'v', 'implies', '->'):
            with self.subTest(i=c):
                string = f'(word one {c} word two) {c} (word three {c} word four)'
                expected = [f'word one {c} word two', c, f'word three {c} word four']
                self.assertEqual(expected, find_connective(string))


class test_deparenthesize(unittest.TestCase):
    def test_single_set(self):
        s = '(words)'
        expected = 'words'
        actual = deparenthesize(s)
        self.assertEqual(expected, actual)
    
    def test_nested_set(self):
        s = '(nested (words))'
        expected = 'nested (words)'
        actual = deparenthesize(s)
        self.assertEqual(expected, actual)

    def test_double_nested_set(self):
        s = '((double nested))'
        expected ='double nested'
        actual = deparenthesize(s)
        self.assertEqual(expected, actual)

    def test_disjoint_set(self):
        s = '(disjoint) -> (set)'
        self.assertEqual(s, deparenthesize(s))


if __name__ == '__main__':
    unittest.main()

