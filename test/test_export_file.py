import unittest

class TestExportFile(unittest.TestCase):
    def test_something(self) -> None:
        d = {
            Sequent(
                (),
                (Conditional(Atom('p'), (Atom('q')),),)
            ):
                Sequent(
                    (Atom('p'),), 
                    (Atom('q'),)): None
        }
        tree = Tree.from_dict(d)
        e = TreeExporter(tree)

if __name__ == '__main__':
    unittest.main()

