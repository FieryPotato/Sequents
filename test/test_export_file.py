import os
import unittest
import pickle

from proposition import *
from sequent import Sequent
from tree import Tree
from export_file import TreeExporter, PickleExporter


class TestExportTxtFile(unittest.TestCase):
    file = 'test/io_testing/export'
    p = Atom('p')
    q = Atom('q')
    n = Negation(p)
    cd = Conditional(p, q)
    cj = Conjunction(p, q)
    dj = Disjunction(p, q)

    def tearDown(self) -> None:
        if os.path.exists(self.file):
            os.remove(self.file)
        
    def test_saving_one_parent_rule_as_pickle(self) -> None:
        d = { 
            Sequent((),(self.cd,)):
                {Sequent((self.p,),(self.q,)): None}
        }
        tree = Tree.from_dict(d)
        exporter = TreeExporter(tree)
        actual = exporter.pickled()
        self.assertEqual(tree, pickle.loads(actual))

    def test_saving_tree_to_file(self) -> None:
        d_0 = {
            Sequent((),(self.cd,)):
                {Sequent((self.p,),(self.q,)): None}
        }
        t_0 = Tree.from_dict(d_0)

        d_1 = {
            Sequent((self.cd,),()):
                {
                    Sequent((),(self.p,)): None,
                    Sequent((self.q,),()): None
                }
        }
        t_1 = Tree.from_dict(d_1)
        tree_list = [t_0, t_1]
                        
        exporter = PickleExporter(self.file, tree_list)
        exporter.export()

        with open(self.file, 'rb') as f:
            actual = pickle.load(f)
        
        self.assertEqual(tree_list, actual)


if __name__ == '__main__':
    unittest.main()

