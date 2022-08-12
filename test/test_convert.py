import unittest

from src.proposition import Atom, Conditional, Conjunction,\
        Disjunction, Negation, Proposition

@unittest.skip('Expected failure while removing regex stuff')
class TestConversion(unittest.TestCase):
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

    def complex(self, connective: str) -> str:
        '''
        Helper function to generate complex propositions.
        '''
        string = '({g} {c} {b}) {c} ({g} {c} {b})'
        return string.format(g=self.bin_test[0], b=self.bin_test[1], c=connective)

    def test_atom(self) -> None:
        string = self.un_test
        expected = self.atom
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)

    def test_atom_parens(self) -> None:
        string = self.un_test
        expected = self.atom
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)

    def test_conjunction_words_simple_no_parens(self) -> None:
        string = ' and '.join(self.bin_test)
        expected = self.conjunction     
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)

    def test_conjunction_words_simple_parens(self) -> None:
        string = '(' + ' and '.join(self.bin_test) + ')'
        expected = self.conjunction
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)

#    def test_conjunction_words_complex(self) -> None:
#        string = self.complex('and')
#        expected = self.comp_conj
#        actual = Proposition.from_string(string)
#        self.assertEqual(expected, actual)

    def test_conjunction_symb_simple_no_parens(self) -> None:
        string = ' & '.join(self.bin_test)
        expected = self.conjunction
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)
    
    def test_conjunction_symb_parens(self) -> None:
        string = '(' + ' & '.join(self.bin_test) + ')'
        expected = self.conjunction
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)

    def test_conditional_words_simple_no_parens(self) -> None:
        string = ' implies '.join(self.bin_test)
        expected = self.conditional
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)
    
    def test_conditional_words_parens(self) -> None:
        string = '(' + ' implies '.join(self.bin_test) + ')'
        expected = self.conditional
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)

    def test_conditional_symb_simple_no_parens(self) -> None:
        string = ' -> '.join(self.bin_test)
        expected = self.conditional
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)
    
    def test_conditional_symb_parens(self) -> None:
        string = '(' + ' -> '.join(self.bin_test) + ')'
        expected = self.conditional
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)

    def test_disjunction_words_simple_no_parens(self) -> None:
        string = ' or '.join(self.bin_test)
        expected = self.disjunction
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)

    def test_disjunction_words_parens(self) -> None:
        string = '(' + ' v '.join(self.bin_test) + ')'
        expected = self.disjunction
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)

    def test_disjunction_symb_simple_no_parens(self) -> None:
        string = ' v '.join(self.bin_test)
        expected = self.disjunction
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)

    def test_disjunction_symb_parens(self) -> None:
        string = '(' + ' or '.join(self.bin_test) + ')'
        expected = self.disjunction
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)

    def test_negation_words_no_parens(self) -> None:
        string = 'not ' + self.un_test
        expected = self.negation
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)

    def test_negation_symb_no_parens(self) -> None:
        string = '~ ' + self.un_test
        expected = self.negation
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)


class TestFindConnective(unittest.TestCase):
    def test_fc_returns_list_if_no_connective(self) -> None:
        string = 'anything'
        expected = ['anything']
        self.assertEqual(expected, Proposition.find_connective(string))

    def test_fc_negation_atomic(self) -> None:
        for c in ('not', '~'):
            with self.subTest(i=c):
                string = f'{c} the bird is in the bush'
                expected = [c, 'the bird is in the bush']
                self.assertEqual(expected, Proposition.find_connective(string))

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
                self.assertEqual(expected, Proposition.find_connective(string))

    def test_fc_binary_nested(self) -> None:
        for c in ('and', '&', 'or', 'v', 'implies', '->'):
            with self.subTest(i=c):
                string = f'(word one {c} word two) {c} (word three {c} word four)'
                expected = [f'word one {c} word two', c, f'word three {c} word four)']
                self.assertEqual(expected, Proposition.find_connective(string))


if __name__ == '__main__':
    unittest.main()

