import unittest

from src.proposition import Atom, Conditional, Conjunction,\
        Disjunction, Negation, Proposition

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

    def test_atom(self):
        string = self.un_test
        expected = self.atom
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)

    def test_atom_parens(self):
        string = self.un_test
        expected = self.atom
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)

    def test_conjunction_words_simple_no_parens(self):
        string = ' and '.join(self.bin_test)
        expected = self.conjunction     
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)

    def test_conjunction_words_simple_parens(self):
        string = '(' + ' and '.join(self.bin_test) + ')'
        expected = self.conjunction
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)

    def test_conjunction_symb_simple_no_parens(self):
        string = ' & '.join(self.bin_test)
        expected = self.conjunction
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)
    
    def test_conjunction_symb_parens(self):
        string = '(' + ' & '.join(self.bin_test) + ')'
        expected = self.conjunction
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)

    def test_conditional_words_simple_no_parens(self):
        string = ' implies '.join(self.bin_test)
        expected = self.conditional
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)
    
    def test_conditional_words_parens(self):
        string = '(' + ' implies '.join(self.bin_test) + ')'
        expected = self.conditional
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)

    def test_conditional_symb_simple_no_parens(self):
        string = ' -> '.join(self.bin_test)
        expected = self.conditional
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)
    
    def test_conditional_symb_parens(self):
        string = '(' + ' -> '.join(self.bin_test) + ')'
        expected = self.conditional
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)

    def test_disjunction_words_simple_no_parens(self):
        string = ' or '.join(self.bin_test)
        expected = self.disjunction
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)

    def test_disjunction_words_parens(self):
        string = '(' + ' v '.join(self.bin_test) + ')'
        expected = self.disjunction
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)

    def test_disjunction_symb_simple_no_parens(self):
        string = ' v '.join(self.bin_test)
        expected = self.disjunction
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)

    def test_disjunction_symb_parens(self):
        string = '(' + ' or '.join(self.bin_test) + ')'
        expected = self.disjunction
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)

    def test_negation_words_no_parens(self):
        string = 'not ' + self.un_test
        expected = self.negation
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)

    def test_negation_symb_no_parens(self) -> None:
        string = '~ ' + self.un_test
        expected = self.negation
        actual = Proposition.from_string(string)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()

