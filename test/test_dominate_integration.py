import unittest
from pathlib import Path

from HTML.HTML import HTML

MOCKS_DIR = Path('test/mocks/html')
OUTFILE = Path('test/mocks/html/out.html')


class MyTestCase(unittest.TestCase):
    mocks = MOCKS_DIR
    out_file = OUTFILE

    def tearDown(self) -> None:
        OUTFILE.unlink(missing_ok=True)

    def test_something(self):
        doc = HTML(self.out_file)
        doc.create_head()
        doc.save()

        with open(self.mocks / 'create_head.html') as f:
            expected = f.readlines()

        with open(self.out_file) as f:
            actual = f.readlines()

        self.assertEqual(expected, actual)



if __name__ == '__main__':
    unittest.main()