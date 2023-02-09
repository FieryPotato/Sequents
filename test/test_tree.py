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

    # def test_non_invertible_then_invertible(self) -> None:
    #     tree = convert.string_to_tree('A & B; A & B')
    #     result = split_tree(tree)

    #     self.assertEqual(2, len(result))


    # def test_non_invertible_then_non_invertible(self) -> None:
    #     tree = convert.string_to_tree('A & B; C v D')

    #     with patch('settings.__Settings.get_rule', return_value='add'):
    #         tree.grow()

    #     result = split_tree(tree)

    #     self.assertEqual(4, len(result))

    #     ACD_parent = convert.string_to_sequent('A; C v D')
    #     AC_parent = convert.string_to_sequent('A; C')
    #     AD_parent = convert.string_to_sequent('A; D')

    #     BCD_parent = convert.string_to_sequent('B; C v D')
    #     BC_parent = convert.string_to_sequent('B; C')
    #     BD_parent = convert.string_to_sequent('B; D')



if __name__ == '__main__':
    unittest.main()
