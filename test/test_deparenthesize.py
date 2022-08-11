import unittest

from src.proposition import deparenthesize


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

