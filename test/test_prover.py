import os
import unittest

from src.prover import Prover


EMPTY_TEST = "test/io_testing/empty_test.txt"
TEST_FILE = "test/io_testing/test_file.txt"

class TestProver(unittest.TestCase):
    def setUp(self) -> None:
        self.prover = Prover()

    def test_get_import_file_contents(self) -> None:
        for file in (EMPTY_TEST, TEST_FILE):
            self.prover._import(file)
            with open(file) as f:
                expected_contents = f.readlines()
            self.assertEqual(expected_contents, self.prover.imported_contents)

    def test_get_import_filename(self) -> None:
        self.prover._import(EMPTY_TEST)
        self.assertEqual(EMPTY_TEST, self.prover.import_filename)

    def test_get_output_filename_during_import(self) -> None:
        suffix = "_result.json"
        out = EMPTY_TEST[:-4] + suffix
        self.prover._import(EMPTY_TEST)
        self.assertEqual(out, self.prover.outfile)
    
    def test_custom_outfile_during_import(self) -> None:
        custom_out = "results.json"
        self.prover._import(EMPTY_TEST, outfile=custom_out)
        self.assertEqual(custom_out, self.prover.outfile)


if __name__ == "__main__":
    unittest.main()

