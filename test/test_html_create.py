import os
import unittest

from html.HTML import HTML


def cleanup(filename) -> None:
    if os.path.exists(filename):
        os.remove(filename)
    

class TestCreate(unittest.TestCase):
    def test_create_document(self) -> None:
        expected_file_path = "test/mocks/html_bare_expected.html"
        with open(expected_file_path) as f:
            expected = f.readlines()
        expected[-1] = expected[-1][:-1]  # the document has a trailing \n
        actual_file_path = "test/mocks/html_bare_actual.html"
        with HTML(actual_file_path, title='TestDoc') as doc:
            pass
        with open(actual_file_path) as f:
            actual = f.readlines()
        self.assertEqual(expected, actual)
        cleanup(actual_file_path)


