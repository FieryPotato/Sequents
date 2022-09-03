import os
import unittest
import pickle

from proposition import Atom, Negation, Conditional, Conjunction,\
    Disjunction
from sequent import Sequent
from tree import Tree, tree_from_dict
from export_file import PickleExporter


class TestExportFile(unittest.TestCase):
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
        
    def test_saving_tree_to_file(self) -> None:
        d_0 = {
            Sequent((),(self.cd,)):
                {Sequent((self.p,),(self.q,)): None}
        }
        t_0 = tree_from_dict(d_0)

        d_1 = {
            Sequent((self.cd,),()):
                {
                    Sequent((),(self.p,)): None,
                    Sequent((self.q,),()): None
                }
        }
        t_1 = tree_from_dict(d_1)
        tree_list = [t_0, t_1]
                        
        exporter = PickleExporter(self.file)
        exporter.export(tree_list)

        with open(self.file, 'rb') as f:
            actual = pickle.load(f)
        
        self.assertEqual(tree_list, actual)



if __name__ == '__main__':
    unittest.main()

