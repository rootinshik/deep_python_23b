import unittest

from custom_list import CustomList


class TestCustomList(unittest.TestCase):

    def test_addition(self):
        lst1 = CustomList([5, 1, 3, 7])
        lst2 = CustomList([1, 2, 7])
        result = lst1 + lst2
        self.assertEqual(result, CustomList([6, 3, 10, 7]))
        self.assertEqual(lst1, CustomList([5, 1, 3, 7]))
        self.assertEqual(lst2, CustomList([1, 2, 7]))

    def test_addition_with_different_lengths(self):
        lst1 = CustomList([5, 1, 3, 7])
        lst2 = CustomList([1])
        result = lst1 + lst2
        self.assertEqual(result, CustomList([6, 1, 3, 7]))
        self.assertEqual(lst1, CustomList([5, 1, 3, 7]))
        self.assertEqual(lst2, CustomList([1]))

    def test_addition_with_list(self):
        lst1 = CustomList([5, 1, 3, 7])
        lst2 = [1, 2, 7]
        result = lst1 + lst2
        self.assertEqual(result, CustomList([6, 3, 10, 7]))
        self.assertEqual(lst1, CustomList([5, 1, 3, 7]))
        self.assertEqual(lst2, [1, 2, 7])

    def test_subtraction(self):
        lst1 = CustomList([5, 1, 3, 6])
        lst2 = CustomList([5, 1, 3, 7])
        result = lst1 - lst2
        self.assertEqual(result, CustomList([0, 0, 0, -1]))
        self.assertEqual(lst1, CustomList([5, 1, 3, 6]))
        self.assertEqual(lst2, CustomList([5, 1, 3, 7]))

    def test_subtraction_with_different_lengths(self):
        lst1 = CustomList([5, 1, 3, 7])
        lst2 = CustomList([1])
        result = lst1 - lst2
        self.assertEqual(result, CustomList([4, 1, 3, 7]))
        self.assertEqual(lst1, CustomList([5, 1, 3, 7]))
        self.assertEqual(lst2, CustomList([1]))

    def test_subtraction_with_list(self):
        lst1 = CustomList([5, 1, 3, 7])
        lst2 = [1, 2, 7]
        result = lst1 - lst2
        self.assertEqual(result, CustomList([4, -1, -4, 7]))
        self.assertEqual(lst1, CustomList([5, 1, 3, 7]))
        self.assertEqual(lst2, [1, 2, 7])

    def test_equality(self):
        lst1 = CustomList([5, 1, 3, 7])
        lst2 = CustomList([1, 2, 7])
        self.assertEqual(lst1, lst1)
        self.assertEqual(lst2, lst2)
        self.assertEqual(lst1, CustomList([5, 1, 3, 7]))
        self.assertEqual(lst2, CustomList([1, 2, 7]))
        self.assertNotEqual(lst1, lst2)

    def test_comparison_operators(self):
        lst1 = CustomList([5, 1, 3, 7])
        lst2 = CustomList([1, 2, 7])
        self.assertTrue(lst1 > lst2)
        self.assertTrue(lst1 >= lst2)
        self.assertFalse(lst1 < lst2)
        self.assertFalse(lst1 <= lst2)
        self.assertTrue(lst1 <= CustomList([5, 1, 3, 7]))
        self.assertTrue(lst2 >= CustomList([1, 2, 7]))

    def test_subtraction_with_float_and_different_lengths(self):
        lst1 = CustomList([5.555, 1.555, 3.555])
        lst2 = [1.555, 2.555]
        result = lst1 - lst2
        self.assertAlmostEqual(result, CustomList([4.0, -1.0, 3.555]))
        self.assertEqual(lst1, CustomList([5.555, 1.555, 3.555]))
        self.assertEqual(lst2, [1.555, 2.555])

    def test_equality_with_float_and_different_lengths(self):
        lst1 = CustomList([2.555, 1.555, 3.555])
        lst2 = CustomList([1.555, 2.555, 7.555, 4.555])
        self.assertEqual(lst1, lst1)
        self.assertNotEqual(lst1, lst2)
        self.assertTrue(lst1 < lst2)
        self.assertTrue(lst1 <= lst2)
        self.assertFalse(lst1 > lst2)
        self.assertFalse(lst1 >= lst2)

    def test_str_representation(self):
        lst1 = CustomList([5, 1, 3, 7])
        self.assertEqual(str(lst1), "sum = 16, elements = [5, 1, 3, 7]")


if __name__ == '__main__':
    unittest.main()
