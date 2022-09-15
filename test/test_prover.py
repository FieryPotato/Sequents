import unittest

from proposition import Atom, Negation, Conjunction, Conditional,\
    Disjunction, Existential, Universal
from prover import Prover
from sequent import Sequent
from tree import Tree


class TestProverSolvesComplexity1(unittest.TestCase):
    names = {'sky', 'grass'}
    p = Atom('Blue<sky>')
    pg = Atom('Blue<grass>')
    p_ = Atom('Blue<x>')
    q = Atom('Green<grass>')
    qs = Atom('Green<sky>')
    q_ = Atom('Green<x>')
    land = Sequent((Conjunction(p, q),), ()) 
    rand = Sequent((), (Conjunction(p, q),))
    lor = Sequent((Disjunction(p, q),), ())
    ror = Sequent((), (Disjunction(p, q),))
    lif = Sequent((Conditional(p, q),), ())
    rif = Sequent((), (Conditional(p, q),))
    lneg = Sequent((Negation(p),), ())
    rneg = Sequent((), (Negation(p),))
    lexi = Sequent((Existential('x', p_),), ())
    rexi = Sequent((), (Existential('x', p_),))
    luni = Sequent((Universal('x', p_),), ())
    runi = Sequent((), (Universal('x', p_),))

    def do(self, root, branches) -> Prover:
        """Helper function that runs theactual test logic."""
        tree = Tree(
            root=root,
            is_grown=True,
            names=self.names
        )
        tree.branches.update(branches)
        p = Prover([root], names=self.names)
        p.run()
        
        # return expected, actual
        return [tree], p.forest

    def test_land(self) -> None:
        branches = {
            self.land: {
                Sequent((self.p, self.q), ()): None
            }
        }
        expected, actual = self.do(self.land, branches)
        self.assertEqual(expected, actual)

    def test_rand(self) -> None:
        branches = {
            self.rand: {
                Sequent((), (self.p,)): None,
                Sequent((), (self.q,)): None
            }
        }
        expected, actual = self.do(self.rand, branches)
        self.assertEqual(expected, actual)

    def test_lor(self) -> None:
        branches = {
            self.lor: {
                Sequent((self.p,), ()): None,
                Sequent((self.q,), ()): None
            }
        }
        expected, actual = self.do(self.lor, branches)
        self.assertEqual(expected, actual)

    def test_ror(self) -> None:
        branches = {
            self.ror: {
                Sequent((), (self.p, self.q)): None
            }
        }
        expected, actual = self.do(self.ror, branches)
        self.assertEqual(expected, actual)

    def test_lif(self) -> None:
        branches = {
            self.lif: {
                Sequent((), (self.p,)): None,
                Sequent((self.q,), ()): None
            }
        }
        expected, actual = self.do(self.lif, branches)
        self.assertEqual(expected, actual)

    def test_rif(self) -> None:
        branches = {
            self.rif: {
                Sequent((self.p,), (self.q,)): None
            }
        }
        expected, actual = self.do(self.rif, branches)
        self.assertEqual(expected, actual)

    def test_lneg(self) -> None:
        branches = {
            self.lneg: {
                Sequent((), (self.p,)): None
            }
        }
        expected, actual = self.do(self.lneg, branches)
        self.assertEqual(expected, actual)

    def test_rneg(self) -> None:
        branches = {
            self.rneg: {
                Sequent((self.p,), ()): None
            }
        }
        expected, actual = self.do(self.rneg, branches)
        self.assertEqual(expected, actual)

    def test_lexi(self) -> None:
        branches = {
            self.lexi: [
                {Sequent((self.p,), ()): None},
                {Sequent((self.pg,), ()): None}

            ]
        }        
        _, p = self.do(self.lexi, branches)
        s = lambda x: x.keys()
        expected = sorted(branches[self.lexi], key=s)
        actual = sorted(p[0].branches[self.lexi], key=s)
        self.assertEqual(expected, actual)

    def test_rexi(self) -> None:
        branches = {
            self.rexi: [
                {Sequent((), (self.p,)): None},
                {Sequent((), (self.pg,)): None}
            ]
        }
        _, p = self.do(self.rexi, branches)
        s = lambda x: x.keys()
        expected = sorted(branches[self.rexi], key=s)
        actual = sorted(p[0].branches[self.rexi], key=s)
        self.assertEqual(expected, actual)

    def test_luni(self) -> None:
        branches = {
            self.luni: [
                {Sequent((self.p,), ()): None},
                {Sequent((self.pg,), ()): None}
            ]
        }
        _, p = self.do(self.luni, branches)
        expected = sorted(branches[self.luni], key=lambda x: x.keys())
        actual = sorted(p[0].branches[self.luni], key=lambda x: x.keys())
        self.assertEqual(expected, actual)

    def test_runi(self) -> None:
        branches = {
            self.runi: [
                {Sequent((), (self.p,)): None},
                {Sequent((), (self.pg,)): None}
            ]
        }
        _, p = self.do(self.runi, branches)
        expected = sorted(branches[self.runi], key=lambda x: x.keys())
        actual = sorted(p[0].branches[self.runi], key=lambda x: x.keys())
        self.assertEqual(expected, actual)



if __name__ == '__main__':
    unittest.main()

