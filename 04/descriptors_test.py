import unittest

from descriptors import Probability, FootballMatchScore

import unittest


class TestProbabilityDescriptor(unittest.TestCase):
    def test_valid_probability(self):
        class Event:
            probability = Probability()

        event = Event()
        event.probability = 0.5
        self.assertEqual(event.probability, 0.5)

    def test_invalid_probability(self):
        class Event:
            probability = Probability()

        event = Event()
        with self.assertRaises(ValueError):
            event.probability = 1.5


class TestFootballMatchScoreDescriptor(unittest.TestCase):
    def test_valid_scores(self):
        class Match:
            score = FootballMatchScore()

        match = Match()
        match.score = [2, 1]
        self.assertEqual(match.score, [2, 1])

    def test_invalid_scores(self):
        class Match:
            score = FootballMatchScore()

        match = Match()
        with self.assertRaises(ValueError):
            match.score = [2, "1"]


if __name__ == "__main__":
    unittest.main()
