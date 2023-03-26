import unittest

from sequent import Sequent
from proposition import Atom, Negation, Conjunction, Disjunction, Conditional


class TestSequent(unittest.TestCase):
    p = Atom("p")
    q = Atom("q")
    n = Negation(p)
    cj = Conjunction(p, q)
    dj = Disjunction(p, q)
    cd = Conditional(p, q)
    propositions = p, n, cj, dj, cd

    def test_sequent_has_antecedent_and_consequent(self) -> None:
        s = Sequent((self.p,), (self.q,))
        self.assertEqual(self.p, s.ant[0])
        self.assertEqual(self.q, s.con[0])

    def test_sequent_string(self) -> None:
        s_0 = Sequent((self.p,), (self.q,))
        self.assertEqual('p; q', str(s_0))
        s_1 = Sequent((self.cj, self.dj), (self.cd, self.n))
        string = '(p & q), (p v q); (p -> q), ~ p'
        self.assertEqual(string, str(s_1))
        s_2 = Sequent(
            (
                Conjunction(
                    Disjunction(
                        self.p, 
                        self.q
                    ), 
                    self.p
                ),
            ), 
            (
                Negation(
                    Conditional(
                        self.q, 
                        self.n
                    )
                ),
            )
        )
        string = '((p v q) & p); ~ (q -> ~ p)'
        self.assertEqual(string, str(s_2))

    def test_equality(self) -> None:
        c = Conditional(self.p, self.p)
        d = Disjunction(self.p, self.p)
        atomic_a = Sequent((self.p,), (self.p,))
        atomic_b = Sequent((self.p,), (self.p,))
        self.assertEqual(atomic_a, atomic_b)
        self.assertNotEqual(atomic_a, ((self.p,), (self.p,)))
        self.assertNotEqual(c, d)

    def test_complexity(self) -> None:
        s_0 = Sequent((self.p,), (self.q,))
        self.assertEqual(0, s_0.complexity)
        s_1 = Sequent((self.n,), ())
        self.assertEqual(1, s_1.complexity)
        s_2 = Sequent((self.n,), (self.n,))
        self.assertEqual(2, s_2.complexity)

    def test_first_complex_prop(self) -> None:
        s_0 = Sequent((self.p, self.q, self.n), (self.dj, self.cj))
        expected = self.n, 'ant', 2
        actual = s_0.first_complex_prop()
        self.assertEqual(expected, actual)
        
        s_1 = Sequent((self.p, self.q), (self.q, self.cj, self.dj))
        expected = self.cj, 'con', 1
        actual = s_1.first_complex_prop()
        self.assertEqual(expected, actual)

    def test_atomic_first_complex_prop(self) -> None:
        s = Sequent((self.p,), (self.q,))
        expected = None
        actual = s.first_complex_prop()
        self.assertEqual(expected, actual)

    def test_possible_mix_parents(self) -> None:
        s_0 = Sequent((self.p,), (self.q,))
        expected = [
            (Sequent((self.p,), (self.q,)), Sequent((), ())),
            (Sequent((self.p,), ()), Sequent((), (self.q,))),
            (Sequent((), (self.q,)), Sequent((self.p,), ())),
            (Sequent((), ()), Sequent((self.p,), (self.q,)))
        ]
        self.assertEqual(expected, s_0.possible_mix_parents())

        s_1 = Sequent((self.p, self.q), (self.cj, self.cd))
        expected = [
            (Sequent((self.p, self.q), (self.cj, self.cd)), Sequent((), ())),
            (Sequent((self.p, self.q), (self.cj,)), Sequent((), (self.cd,))),
            (Sequent((self.p, self.q), (self.cd,)), Sequent((), (self.cj,))),
            (Sequent((self.p, self.q), ()), Sequent((), (self.cj, self.cd))),
            (Sequent((self.p,), (self.cj, self.cd)), Sequent((self.q,), ())),
            (Sequent((self.p,), (self.cj,)), Sequent((self.q,), (self.cd,))),
            (Sequent((self.p,), (self.cd,)), Sequent((self.q,), (self.cj,))),
            (Sequent((self.p,), ()), Sequent((self.q,), (self.cj, self.cd))),
            (Sequent((self.q,), (self.cj, self.cd)), Sequent((self.p,), ())),
            (Sequent((self.q,), (self.cj,)), Sequent((self.p,), (self.cd,))),
            (Sequent((self.q,), (self.cd,)), Sequent((self.p,), (self.cj,))),
            (Sequent((self.q,), ()), Sequent((self.p,), (self.cj, self.cd))),
            (Sequent((), (self.cj, self.cd)), Sequent((self.p, self.q), ())),
            (Sequent((), (self.cj,)), Sequent((self.p, self.q), (self.cd,))),
            (Sequent((), (self.cd,)), Sequent((self.p, self.q), (self.cj,))),
            (Sequent((), ()), Sequent((self.p, self.q), (self.cj, self.cd))),
        ]
        self.assertEqual(expected, s_1.possible_mix_parents())


    def test_is_atomic(self) -> None:
        a = Sequent((self.p,), (self.q,))
        self.assertTrue(a.is_atomic)

        c = Sequent((self.n,), (self.q,))
        self.assertFalse(c.is_atomic)


    def test_sequent_has_names(self) -> None:
        names = {'alice', 'betty', 'clarice'}
        a = Atom('P<alice>')
        b = Atom('Q<betty, clarice>')
        s0 = Sequent((a,), (b,))
        self.assertEqual(names, s0.names)
        
        s1 = Sequent((a, b), (a, b))
        self.assertEqual(names, s1.names)

    def test_sequent_is_sortable(self) -> None:
        s1 = Sequent((self.p,), (self.q,))
        s2 = Sequent((self.q,), (self.p,))
        self.assertTrue(s1 > s2 or s1 < s2)

    def test_sequent_tag(self) -> None:
        sequents = [
            Sequent((self.p,), (self.q,)),
            Sequent((self.n,), ()),
            Sequent((), (self.n,)),
            Sequent((self.cj,), ()),
            Sequent((), (self.cj,)),
            Sequent((self.cd,), ()),
            Sequent((), (self.cd,)),
            Sequent((self.dj,), ()),
            Sequent((), (self.dj,)),
        ]   
        expected = [
            'Ax',
            'L~',
            'R~',
            'L&',
            'R&',
            'L->',
            'R->',
            'Lv',
            'Rv',
        ]
        for s, e in zip(sequents, expected):
            self.assertEqual(e, s.tag())


if __name__ == '__main__':
    unittest.main()

