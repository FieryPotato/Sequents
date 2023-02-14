import unittest

from unittest.mock import patch

import convert
from tree import Tree


class TestTreeMethods(unittest.TestCase):

    def test_tree_height(self) -> None:
        self.assertEqual(1, convert.string_to_tree('A; B').height())
        self.assertEqual(2, convert.string_to_tree('A & B; C').height())
        self.assertEqual(2, convert.string_to_tree('A; B & C').height())
        self.assertEqual(3, convert.string_to_tree('A & B; C & D').height())
        self.assertEqual(3, convert.string_to_tree('A & B; C v D').height())
        self.assertEqual(3, convert.string_to_tree('A v B; C & D').height())
        self.assertEqual(3, convert.string_to_tree('A; (A & B) & (C & D)').height())
        self.assertEqual(4, convert.string_to_tree('(A & B) & (C & D); A').height())
        self.assertEqual(3, convert.string_to_tree('(A v B) v (C v D); A').height())
        self.assertEqual(4, convert.string_to_tree('A; (A v B) v (C v D)').height())
        self.assertEqual(3, convert.string_to_tree('(A -> B) -> (C -> D); A').height())
        self.assertEqual(4, convert.string_to_tree('A; (A -> B) -> (C -> D)').height())

    def test_tree_width(self) -> None:

        atom = convert.string_to_tree('A; B')
        self.assertEqual(1, atom.width())

        with patch('settings.__Settings.get_rule', return_value='add'):
            two_parent = convert.string_to_tree('A; B & C')
            self.assertEqual(2, two_parent.width())

            two_then_one = convert.string_to_tree('A v B; ~ C')
            self.assertEqual(2, two_then_one.width())

            two_then_two = convert.string_to_tree('A v B; C & D')
            self.assertEqual(4, two_then_two.width())

            two_then_left_is_two = convert.string_to_tree('A v (B v C); ')
            self.assertEqual(3, two_then_left_is_two.width())

            one_then_two = convert.string_to_tree('A & B; C & D')
            self.assertEqual(2, one_then_two.width())

        with patch('settings.__Settings.get_rule', return_value='mul'):
            one_parent = convert.string_to_tree('A & B; C')
            self.assertEqual(1, one_parent.width())


class TestTreeSplitting(unittest.TestCase):
    def test_atomic_tree_is_no_op(self) -> None:
        atom = convert.string_to_tree('A; B')
        result = atom.split()

        self.assertEqual(1, len(result))
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], Tree)

    def test_invertible_one_parent_is_no_op(self) -> None:
        invertible = convert.string_to_tree('~ A; B')
        result = invertible.split()

        self.assertEqual(1, len(result))
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], Tree)

        expected_parent = convert.string_to_sequent('; B, A')
        actual_parent = result[0].branches[0][0]
        self.assertEqual(expected_parent, actual_parent.root)

    def test_invertible_two_parent_is_no_op(self) -> None:
        with patch('settings.__Settings.get_rule', return_value='add'):
            invertible = convert.string_to_tree('A v B; C')
            result = invertible.split()

        self.assertEqual(1, len(result))
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], Tree)

        left_parent = convert.string_to_sequent('A; C')
        actual_left = result[0].branches[0][0]
        self.assertEqual(left_parent, actual_left.root)

        right_parent = convert.string_to_sequent('B; C')
        actual_right = result[0].branches[0][1]
        self.assertEqual(right_parent, actual_right.root)

    def test_height_two_one_parent_invertible_split(self) -> None:
        invertible = convert.string_to_tree('~ A; ~ B')
        result = invertible.split()

        self.assertEqual(1, len(result))
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], Tree)

        intermediate_parent = convert.string_to_sequent('; ~ B, A')
        actual_intermediate = result[0].branches[0][0]
        self.assertIsInstance(actual_intermediate, Tree)
        self.assertEqual(intermediate_parent, actual_intermediate.root)
        self.assertEqual(1, len(actual_intermediate.branches))

        final_parent = convert.string_to_sequent('B; A')
        actual_final = result[0].branches[0][0].branches[0][0]
        self.assertIsInstance(actual_final, Tree)
        self.assertEqual(final_parent, actual_final.root)
        self.assertEqual(1, len(actual_final.branches))

    def test_height_two_two_parent_invertible_split(self) -> None:
        with patch('settings.__Settings.get_rule', return_value='add'):
            invertible = convert.string_to_tree('A v B; C & D')
            result = invertible.split()

        self.assertEqual(1, len(result))
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], Tree)

        intermediate_left = convert.string_to_sequent('A; C & D')
        actual_left = result[0].branches[0][0]
        self.assertEqual(intermediate_left, actual_left.root)
        self.assertEqual(1, len(actual_left.branches))

        intermediate_right = convert.string_to_sequent('B; C & D')
        actual_right = result[0].branches[0][1]
        self.assertEqual(intermediate_right, actual_right.root)
        self.assertEqual(1, len(actual_right.branches))

        final_ll = convert.string_to_sequent('A; C')
        actual_ll = result[0].branches[0][0].branches[0][0]
        self.assertEqual(final_ll, actual_ll.root)
        self.assertEqual(1, len(actual_ll.branches))

        final_lr = convert.string_to_sequent('A; D')
        actual_lr = result[0].branches[0][0].branches[0][1]
        self.assertEqual(final_lr, actual_lr.root)
        self.assertEqual(1, len(actual_lr.branches))

        final_rl = convert.string_to_sequent('B; C')
        actual_rl = result[0].branches[0][1].branches[0][0]
        self.assertEqual(final_rl, actual_rl.root)
        self.assertEqual(1, len(actual_rl.branches))

        final_rr = convert.string_to_sequent('B; D')
        actual_rr = result[0].branches[0][1].branches[0][1]
        self.assertEqual(final_rr, actual_rr.root)
        self.assertEqual(1, len(actual_rr.branches))

    def test_non_invertible_one_parent(self) -> None:
        tree = convert.string_to_tree(
            'forallx (P<x>); ', names={'alice', 'bob'}
        )
        result = sorted(tree.split())

        self.assertEqual(2, len(result))
        self.assertIsInstance(result, list)

        parent_0 = convert.string_to_sequent('P<alice>; ')
        self.assertIsInstance(result[0], Tree)
        self.assertEqual(1, len(result[0].branches))
        self.assertEqual(result[0].branches[0][0].root, parent_0)

        parent_1 = convert.string_to_sequent('P<bob>; ')
        self.assertIsInstance(result[1], Tree)
        self.assertEqual(1, len(result[1].branches))
        self.assertEqual(result[1].branches[0][0].root, parent_1)

    def test_non_invertible_then_non_invertible_one_parent(self) -> None:
        with patch('settings.__Settings.get_rule', return_value='add'):
            tree = convert.string_to_tree('A & B; C v D')
            result = tree.split()

        self.assertEqual(4, len(result))

        expected_acd = convert.string_to_sequent('A; C v D')
        actual_acd = result[0].branches[0][0]
        self.assertIsInstance(actual_acd, Tree)
        self.assertEqual(expected_acd, actual_acd.root)
        expected_acd_ac = convert.string_to_sequent('A; C')
        actual_acd_ac = result[0].branches[0][0].branches[0][0]
        self.assertIsInstance(actual_acd_ac, Tree)
        self.assertEqual(expected_acd_ac, actual_acd_ac.root)

        actual_acd_ = result[1].branches[0][0]
        self.assertIsInstance(actual_acd_, Tree)
        self.assertEqual(expected_acd, actual_acd_.root)
        expected_acd_ad = convert.string_to_sequent('A; D')
        actual_acd_ad = result[1].branches[0][0].branches[0][0]
        self.assertIsInstance(actual_acd_ad, Tree)
        self.assertEqual(expected_acd_ad, actual_acd_ad.root)

        expected_bcd = convert.string_to_sequent('B; C v D')
        actual_bcd = result[2].branches[0][0]
        self.assertIsInstance(actual_bcd, Tree)
        self.assertEqual(expected_bcd, actual_bcd.root)
        expected_bcd_bc = convert.string_to_sequent('B; C')
        actual_bcd_bc = result[2].branches[0][0].branches[0][0]
        self.assertIsInstance(actual_bcd_bc, Tree)
        self.assertEqual(expected_bcd_bc, actual_bcd_bc.root)

        actual_bcd_ = result[3].branches[0][0]
        self.assertIsInstance(actual_bcd_, Tree)
        self.assertEqual(expected_bcd, actual_bcd_.root)
        expected_bcd_bd = convert.string_to_sequent('B; D')
        actual_bcd_bd = result[3].branches[0][0].branches[0][0]
        self.assertIsInstance(actual_bcd_bd, Tree)
        self.assertEqual(expected_bcd_bd, actual_bcd_bd.root)

    def test_non_invertible_then_non_invertible_two_parent(self) -> None:
        with patch('settings.__Settings.get_rule', return_value='mul'):
            tree = convert.string_to_tree('A v B; C & D')
            result = tree.split()

        self.assertEqual(4, len(result))

        _0_expected_l = convert.string_to_sequent('A; C & D')
        _0_actual_l = result[0].branches[0][0]
        self.assertEqual(_0_expected_l, _0_actual_l.root)
        _0_expected_ll = convert.string_to_sequent('A; C')
        _0_actual_ll = result[0].branches[0][0].branches[0][0]
        self.assertEqual(_0_expected_ll, _0_actual_ll.root)
        _0_expected_lr = convert.string_to_sequent('; D')
        _0_actual_lr = result[0].branches[0][0].branches[0][1]
        self.assertEqual(_0_expected_lr, _0_actual_lr.root)
        _0_expected_r = convert.string_to_sequent('B; ')
        _0_actual_r = result[0].branches[0][1]
        self.assertEqual(_0_expected_r, _0_actual_r.root)

        _1_expected_l = convert.string_to_sequent('A; C & D')
        _1_actual_l = result[1].branches[0][0]
        self.assertEqual(_1_expected_l, _1_actual_l.root)
        _1_expected_ll = convert.string_to_sequent('; C')
        _1_actual_ll = result[1].branches[0][0].branches[0][0]
        self.assertEqual(_1_expected_ll, _1_actual_ll.root)
        _1_expected_lr = convert.string_to_sequent('A; D')
        _1_actual_lr = result[1].branches[0][0].branches[0][1]
        self.assertEqual(_1_expected_lr, _1_actual_lr.root)
        _1_expected_r = convert.string_to_sequent('B; ')
        _1_actual_r = result[1].branches[0][1]
        self.assertEqual(_1_expected_r, _1_actual_r.root)

        _2_expected_l = convert.string_to_sequent('A; ')
        _2_actual_l = result[2].branches[0][0]
        self.assertEqual(_2_expected_l, _2_actual_l.root)
        _2_expected_r = convert.string_to_sequent('B; C & D')
        _2_actual_r = result[2].branches[0][1]
        self.assertEqual(_2_expected_r, _2_actual_r.root)
        _2_expected_rl = convert.string_to_sequent('B; C')
        _2_actual_rl = result[2].branches[0][1].branches[0][0]
        self.assertEqual(_2_expected_rl, _2_actual_rl.root)
        _2_expected_rr = convert.string_to_sequent('; D')
        _2_actual_rr = result[2].branches[0][1].branches[0][1]
        self.assertEqual(_2_expected_rr, _2_actual_rr.root)

        _3_expected_l = convert.string_to_sequent('A; ')
        _3_actual_l = result[3].branches[0][0]
        self.assertEqual(_3_expected_l, _3_actual_l.root)
        _3_expected_r = convert.string_to_sequent('B; C & D')
        _3_actual_r = result[3].branches[0][1]
        self.assertEqual(_3_expected_r, _3_actual_r.root)
        _3_expected_rl = convert.string_to_sequent('; C')
        _3_actual_rl = result[3].branches[0][1].branches[0][0]
        self.assertEqual(_3_expected_rl, _3_actual_rl.root)
        _3_expected_rr = convert.string_to_sequent('B; D')
        _3_actual_rr = result[3].branches[0][1].branches[0][1]
        self.assertEqual(_3_expected_rr, _3_actual_rr.root)



if __name__ == '__main__':
    unittest.main()
