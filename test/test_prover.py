import os
import unittest

from src.file_io import import_file


TEST_FILE = 'test/io_testing/test_file.txt'
text_content = """atomic antecedent; atomic consequent
not negated antecedent; not negated consequent
~ negated premise; ~ negated conclusion
left ant con and right ant con; left con con and right con con
i realized & almost too late; that conditionals & also shorten to con
i'll have to or do something about it; before reaching or those symbols
maybe i'll be able v to have a work around; that lets me not v repeat propositional content
oh I guess i've implies been doing that; even though this implies will be awful to test
conditional antecedent premise -> conditional consequent premise; conditional antecedent conclusion -> conditional consequent conclusion
not (nested or (propositional and content)); ~ (nested v (propositional & content))"""


class TestProverIO(unittest.TestCase):
    def setUp(self) -> None:
        with open(TEST_FILE, 'w') as file:
            file.write(text_content)

   def tearDown(self) -> None:
       if os.exists(TEST_FILE):
           os.remove(TEST_FILE)

    def test_import_txt_file(self) -> None:
        pass
        


if __name__ == '__main__':
    unittest.main()

