import unittest

from descriptors import Probability
from descriptors import FootballMatchScore
from descriptors import LatexInLineMathEquation


class TestProbabilityDescriptor(unittest.TestCase):
    def test_probability_descriptor_valid(self):
        class SomeClass:
            probability = Probability()

        obj = SomeClass()
        obj.probability = 0.5
        self.assertEqual(obj.probability, 0.5)
        obj.probability = 0.3
        self.assertEqual(obj.probability, 0.3)

    def test_probability_descriptor_edge_cond(self):
        class SomeClass:
            probability = Probability()

        obj = SomeClass()
        obj.probability = 0
        self.assertEqual(obj.probability, 0)
        obj.probability = 1
        self.assertEqual(obj.probability, 1)

    def test_probability_descriptor_invalid_type(self):
        class SomeClass:
            probability = Probability()

        obj = SomeClass()
        with self.assertRaises(ValueError):
            obj.probability = "Вчера сходил на разводные мосты"

    def test_probability_descriptor_invalid_range(self):
        class SomeClass:
            probability = Probability()

        obj = SomeClass()

        with self.assertRaises(ValueError):
            obj.probability = 1.2

        with self.assertRaises(ValueError):
            obj.probability = -0.1

    def test_probability_descriptor_is_none(self):
        class SomeClass:
            probability = Probability()

        self.assertEqual(SomeClass.probability, None)


class TestLatexInLineMathEquationDescriptor(unittest.TestCase):
    def test_latex_descriptor_valid(self):
        class SomeClass:
            latex = LatexInLineMathEquation()

        obj = SomeClass()
        obj.latex = "$a + b$"
        self.assertEqual(obj.latex, "$a + b$")

    def test_latex_descriptor_invalid_format(self):
        class SomeClass:
            latex = LatexInLineMathEquation()

        obj = SomeClass()
        with self.assertRaises(ValueError):
            obj.latex = "a + b"

        with self.assertRaises(ValueError):
            obj.latex = "$a + b"

        with self.assertRaises(ValueError):
            obj.latex = "a + b$"

        for num in range(10):
            with self.assertRaises(ValueError):
                obj.latex = "$" * num

    def test_latex_descriptor_unclosed_brackets(self):
        class SomeClass:
            latex = LatexInLineMathEquation()

        obj = SomeClass()
        with self.assertRaises(ValueError):
            obj.latex = r"$\frac{a + b$"

    def test_latex_descriptor_is_none(self):
        class MyClass:
            latex = LatexInLineMathEquation()

        self.assertEqual(MyClass.latex, None)


class TestFootballMatchScoreDescriptor(unittest.TestCase):
    def test_score_descriptor_valid_list(self):
        class SomeClass:
            score = FootballMatchScore()

        obj = SomeClass()
        obj.score = [2, 1]
        self.assertEqual(obj.score, [2, 1])
        obj.score = [0, 0]
        self.assertEqual(obj.score, [0, 0])
        obj.score = [1, 2]
        self.assertEqual(obj.score, [1, 2])

        obj.score = (2, 1)
        self.assertEqual(obj.score, [2, 1])
        obj.score = (0, 0)
        self.assertEqual(obj.score, [0, 0])
        obj.score = (1, 2)

        self.assertEqual(obj.score, [1, 2])
        obj.score = {"Зенит": 7, "Спартак": 1}
        self.assertEqual(obj.score, [7, 1])
        obj.score = {"Сокол (Саратов)": 1, "Химки": 0}
        self.assertEqual(obj.score, [1, 0])
        obj.score = {"Динамо": 2, "ЦСКА": 1}
        self.assertEqual(obj.score, [2, 1])

    def test_score_descriptor_invalid_type(self):
        class MyClass:
            score = FootballMatchScore()

        obj = MyClass()
        with self.assertRaises(ValueError):
            obj.score = "Зенит обыграл спартак со счетом 7:1"

    def test_score_descriptor_invalid_length(self):
        class MyClass:
            score = FootballMatchScore()

        obj = MyClass()
        with self.assertRaises(ValueError):
            obj.score = [2]
        obj = MyClass()
        with self.assertRaises(ValueError):
            obj.score = {"Зенит": 0}
        obj = MyClass()
        with self.assertRaises(ValueError):
            obj.score = (1,)
        with self.assertRaises(ValueError):
            obj.score = [2, 4, 1]

    def test_score_descriptor_invalid_score_values(self):
        class MyClass:
            score = FootballMatchScore()

        obj = MyClass()
        with self.assertRaises(ValueError):
            obj.score = [2, -1]
        with self.assertRaises(ValueError):
            obj.score = [2.1, 2.19]

    def test_score_descriptor_is_none(self):
        class MyClass:
            score = FootballMatchScore()

        self.assertEqual(MyClass.score, None)


if __name__ == "__main__":
    unittest.main()
