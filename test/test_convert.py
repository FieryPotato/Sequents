import unittest

from src.convert import Convert
from src.proposition import Atom, Conditional, Conjunction,\
        Disjunction, Negation

class TestConvert(unittest.TestCase):
    test_words = ['the grass is green', 'the birds are singing']
    conjunction = Conjunction(Atom('the grass is green'), Atom('the birds are singing'))   
    conditional = Conditional(Atom('the grass is green'), Atom('the birds are singing'))
    disjunction = Disjunction(Atom('the grass is green'), Atom('the birds are singing'))   

    def test_atom(self):
        string = 'The cat is on the mat'
        expected = Atom('The cat is on the mat')
        actual = Convert(string).to_proposition()
        self.assertEqual(expected, actual)

    def test_conjunction_words_simple_no_parens(self):
        string = ' and '.join(self.test_words)
        expected = self.conjunction     
        actual = Convert(string).to_proposition()
        self.assertEqual(expected, actual)

    def test_conjunction_symb_simple_no_parens(self):
        string = ' & '.join(self.test_words)
        expected = self.conjunction
        actual = Convert(string).to_proposition()
        self.assertEqual(expected, actual)

    def test_conditional_words_simple_no_parens(self):
        string = 'if {} then {}'.format(*self.test_words)
        expected = self.conditional
        actual = Convert(string).to_proposition()
        self.assertEqual(expected, actual)

    def test_conditional_symb_simple_no_parens(self):
        string = ' -> '.join(self.test_words)
        expected = self.conditional
        actual = Convert(string).to_proposition()
        self.assertEqual(expected, actual)

    def test_disjunction_words_simple_no_parens(self):
        string = ' or '.join(self.test_words)
        expected = self.disjunction
        actual = Convert(string).to_proposition()
        self.assertEqual(expected, actual)

    def test_disjunction_symb_simple_no_parens(self):
        string = ' v '.join(self.test_words)
        expected = self.disjunction
        actual = Convert(string).to_proposition()
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()

