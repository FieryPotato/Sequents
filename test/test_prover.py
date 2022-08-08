import os
import unittest

from src.prover import Prover


EMPTY_TEST = 'test/io_testing/empty_test.txt'
TEST_FILE = 'test/io_testing/test_file.txt'

class TestProverIO(unittest.TestCase):
    def setUp(self) -> None:
        self.test_out = 'test_out.txt'
        self.prover = Prover()

    def tearDown(self) -> None:
        if os.path.exists(self.test_out):
            os.remove(self.test_out)

    def test_get_import_file_contents(self) -> None:
        for file in (EMPTY_TEST, TEST_FILE):
            self.prover.import_(file)
            with open(file) as f:
                expected_contents = f.readlines()
            self.assertEqual(expected_contents, self.prover.contents)

    def test_get_infile(self) -> None:
        self.prover.import_(EMPTY_TEST)
        self.assertEqual(EMPTY_TEST, self.prover.infile)

    def test_get_output_filename_during_import(self) -> None:
        suffix = '_result.json'
        out = EMPTY_TEST[:-4] + suffix
        self.prover.import_(EMPTY_TEST)
        self.assertEqual(out, self.prover.outfile)
    
    def test_custom_outfile_duringimport_(self) -> None:
        custom_out = 'results.json'
        self.prover.import_(EMPTY_TEST, outfile=custom_out)
        self.assertEqual(custom_out, self.prover.outfile)

    def test_save_file_to_correct_output(self) -> None:
        self.prover.outfile = self.test_out
        self.prover.export_()
        self.assertTrue(os.path.exists(self.test_out))

    def test_outfile_saves_prover_content(self) -> None:
        out_contents = "Testing output contents."
        self.prover.outfile = self.test_out
        self.prover.contents = out_contents
        self.prover.export_()
        with open(self.test_out, 'r') as file:
            self.assertEqual(file.read(), self.prover.contents)


if __name__ == '__main__':
    unittest.main()

