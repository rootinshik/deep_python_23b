import unittest

from custom_list import CustomList


class CustomAssertions:
    def assertCustomListEqual(self, lst1: CustomList, lst2: CustomList):
        if len(lst1) != len(lst2):
            raise AssertionError("Lists not same size")
        if not all(a == b for a, b in zip(lst1, lst2)):
            raise AssertionError("Lists not equal")


class TestCustomList(unittest.TestCase, CustomAssertions):
    def test_addition(self):
        lst1 = CustomList([5, 1, 3, 7])
        lst2 = CustomList([1, 2, 7])

        result1 = lst1 + lst2

        self.assertCustomListEqual(result1, CustomList([6, 3, 10, 7]))
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 7]))
        self.assertCustomListEqual(lst2, CustomList([1, 2, 7]))

        self.assertEqual(type(lst1), CustomList)
        self.assertEqual(type(lst2), CustomList)
        self.assertEqual(type(result1), CustomList)

        result2 = lst2 + lst1

        self.assertCustomListEqual(result2, CustomList([6, 3, 10, 7]))
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 7]))
        self.assertCustomListEqual(lst2, CustomList([1, 2, 7]))

        self.assertEqual(type(lst1), CustomList)
        self.assertEqual(type(lst2), CustomList)
        self.assertEqual(type(result2), CustomList)

    def test_addition_with_different_len(self):
        lst1 = CustomList([5, 1, 3, 7])
        lst2 = CustomList([1])

        result1 = lst1 + lst2
        self.assertCustomListEqual(result1, CustomList([6, 1, 3, 7]))
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 7]))
        self.assertCustomListEqual(lst2, CustomList([1]))

        self.assertEqual(type(lst1), CustomList)
        self.assertEqual(type(lst2), CustomList)
        self.assertEqual(type(result1), CustomList)

        result2 = lst2 + lst1

        self.assertCustomListEqual(result2, CustomList([6, 1, 3, 7]))
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 7]))
        self.assertCustomListEqual(lst2, CustomList([1]))

        self.assertEqual(type(lst1), CustomList)
        self.assertEqual(type(lst2), CustomList)
        self.assertEqual(type(result2), CustomList)

    def test_addition_with_list(self):
        lst1 = CustomList([5, 1, 3, 7])
        lst2 = [1, 2, 7, 7]

        result1 = lst1 + lst2

        self.assertCustomListEqual(result1, CustomList([6, 3, 10, 14]))
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 7]))
        self.assertEqual(lst2, [1, 2, 7, 7])

        self.assertEqual(type(lst1), CustomList)
        self.assertEqual(type(lst2), list)
        self.assertEqual(type(result1), CustomList)

        result2 = lst2 + lst1

        self.assertCustomListEqual(result2, CustomList([6, 3, 10, 14]))
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 7]))
        self.assertEqual(lst2, [1, 2, 7, 7])

        self.assertEqual(type(lst1), CustomList)
        self.assertEqual(type(lst2), list)
        self.assertEqual(type(result2), CustomList)

    def test_addition_with_list_with_different_len(self):
        lst1 = CustomList([5, 1, 3, 7])
        lst2 = [1, 2]

        result1 = lst1 + lst2

        self.assertCustomListEqual(result1, CustomList([6, 3, 3, 7]))
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 7]))
        self.assertEqual(lst2, [1, 2])

        self.assertEqual(type(lst1), CustomList)
        self.assertEqual(type(lst2), list)
        self.assertEqual(type(result1), CustomList)

        result2 = lst2 + lst1

        self.assertCustomListEqual(result2, CustomList([6, 3, 3, 7]))
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 7]))
        self.assertEqual(lst2, [1, 2])

        self.assertEqual(type(lst1), CustomList)
        self.assertEqual(type(lst2), list)
        self.assertEqual(type(result2), CustomList)

    def test_subtraction(self):
        lst1 = CustomList([5, 1, 3, 6])
        lst2 = CustomList([5, 1, 3, 7])

        result1 = lst1 - lst2

        self.assertCustomListEqual(result1, CustomList([0, 0, 0, -1]))
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 6]))
        self.assertCustomListEqual(lst2, CustomList([5, 1, 3, 7]))

        self.assertEqual(type(lst1), CustomList)
        self.assertEqual(type(lst2), CustomList)
        self.assertEqual(type(result1), CustomList)

        result2 = lst2 - lst1

        self.assertCustomListEqual(result2, CustomList([0, 0, 0, 1]))
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 6]))
        self.assertCustomListEqual(lst2, CustomList([5, 1, 3, 7]))

        self.assertEqual(type(lst1), CustomList)
        self.assertEqual(type(lst2), CustomList)
        self.assertEqual(type(result2), CustomList)

    def test_subtraction_with_different_lengths(self):
        lst1 = CustomList([5, 1, 3, 6])
        lst2 = CustomList([5, 1])

        result1 = lst1 - lst2

        self.assertCustomListEqual(result1, CustomList([0, 0, 3, 6]))
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 6]))
        self.assertCustomListEqual(lst2, CustomList([5, 1]))

        self.assertEqual(type(lst1), CustomList)
        self.assertEqual(type(lst2), CustomList)
        self.assertEqual(type(result1), CustomList)

        result2 = lst2 - lst1

        self.assertCustomListEqual(result2, CustomList([0, 0, -3, -6]))
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 6]))
        self.assertCustomListEqual(lst2, CustomList([5, 1]))

        self.assertEqual(type(lst1), CustomList)
        self.assertEqual(type(lst2), CustomList)
        self.assertEqual(type(result2), CustomList)

    def test_subtraction_with_list(self):
        lst1 = CustomList([5, 1, 3, 6])
        lst2 = [0, 1, 0, 15]

        result1 = lst1 - lst2

        self.assertCustomListEqual(result1, CustomList([5, 0, 3, -9]))
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 6]))
        self.assertEqual(lst2, [0, 1, 0, 15])

        self.assertEqual(type(lst1), CustomList)
        self.assertEqual(type(lst2), list)
        self.assertEqual(type(result1), CustomList)

        result2 = lst2 - lst1

        self.assertCustomListEqual(result2, CustomList([-5, 0, -3, 9]))
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 6]))
        self.assertEqual(lst2, [0, 1, 0, 15])

        self.assertEqual(type(lst1), CustomList)
        self.assertEqual(type(lst2), list)
        self.assertEqual(type(result2), CustomList)

    def test_subtraction_with_list_with_different_len(self):
        lst1 = CustomList([5, 1, 3, 6])
        lst2 = [0, 1]

        result1 = lst1 - lst2

        self.assertCustomListEqual(result1, CustomList([5, 0, 3, 6]))
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 6]))
        self.assertEqual(lst2, [0, 1])

        self.assertEqual(type(lst1), CustomList)
        self.assertEqual(type(lst2), list)
        self.assertEqual(type(result1), CustomList)

        result2 = lst2 - lst1

        self.assertCustomListEqual(result2, CustomList([-5, 0, -3, -6]))
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 6]))
        self.assertEqual(lst2, [0, 1])

        self.assertEqual(type(lst1), CustomList)
        self.assertEqual(type(lst2), list)
        self.assertEqual(type(result2), CustomList)

    def test_equality(self):
        lst1 = CustomList([5, 1, 3, 7])
        lst2 = CustomList([1, 2, 7])
        lst3 = CustomList([5, 11])

        self.assertCustomListEqual(lst1, lst1)
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 7]))

        self.assertCustomListEqual(lst2, lst2)
        self.assertCustomListEqual(lst2, CustomList([1, 2, 7]))

        self.assertCustomListEqual(lst3, lst3)
        self.assertCustomListEqual(lst3, CustomList([5, 11]))

        self.assertNotEqual(lst1, lst2)
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 7]))
        self.assertCustomListEqual(lst2, CustomList([1, 2, 7]))

        self.assertEqual(lst1, lst3)
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 7]))
        self.assertCustomListEqual(lst3, CustomList([5, 11]))

        self.assertNotEqual(lst3, lst2)
        self.assertCustomListEqual(lst2, CustomList([1, 2, 7]))
        self.assertCustomListEqual(lst3, CustomList([5, 11]))

    def test_comparison_operators(self):
        lst1 = CustomList([5, 1, 3, 7])
        lst2 = CustomList([1, 2, 7])

        self.assertTrue(lst1 > lst2)
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 7]))
        self.assertListEqual(lst2, CustomList([1, 2, 7]))

        self.assertTrue(lst1 >= lst2)
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 7]))
        self.assertListEqual(lst2, CustomList([1, 2, 7]))

        self.assertFalse(lst1 < lst2)
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 7]))
        self.assertListEqual(lst2, CustomList([1, 2, 7]))

        self.assertFalse(lst1 <= lst2)
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 7]))
        self.assertListEqual(lst2, CustomList([1, 2, 7]))

        self.assertTrue(lst1 <= CustomList([5, 1, 3, 7]))
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 7]))
        self.assertListEqual(lst2, CustomList([1, 2, 7]))

        self.assertTrue(lst2 >= CustomList([1, 2, 7]))
        self.assertCustomListEqual(lst1, CustomList([5, 1, 3, 7]))
        self.assertListEqual(lst2, CustomList([1, 2, 7]))

    def test_subtraction_with_float_and_different_lengths(self):
        lst1 = CustomList([5.555, 1.555, 3.555])
        lst2 = [1.555, 2.555]
        result = lst1 - lst2
        self.assertEqual(result, CustomList([4.0, -1.0, 3.555]))
        self.assertCustomListEqual(lst1, CustomList([5.555, 1.555, 3.555]))
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


if __name__ == "__main__":
    unittest.main()
