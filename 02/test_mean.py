import unittest
from unittest.mock import patch
import time
from mean import mean


class TestMeanDecorator(unittest.TestCase):
    def setUp(self) -> None:
        self._eps = 1e-3

    @staticmethod
    def find_calls_time_in_string(string: str) -> (int, float):
        num_calls = int(string.split()[7])
        mean_time = float(string.split()[4])
        return num_calls, mean_time

    def test_calls_to_mean_not_int(self):
        with self.assertRaises(ValueError):

            @mean("Что-то явно нехорошее")
            def sleep_func() -> None:
                time.sleep(1)

    def test_calls_to_mean_not_positive_int(self):
        with self.assertRaises(ValueError):

            @mean(-1)
            def sleep_func() -> None:
                time.sleep(1)

    def test_call_times_eq_call_to_mean(self):
        print_args = []
        with patch(
            "builtins.print", side_effect=lambda *args: print_args.append(*args)
        ):

            @mean(5)
            def sleep_function(time_to_sleep):
                time.sleep(time_to_sleep)

            for _ in range(5):
                sleep_function(0.1)

        num_calls, mean_time = TestMeanDecorator.find_calls_time_in_string(
            print_args[-1]
        )
        expected_calls, expected_mean = 5, 0.1
        self.assertEqual(num_calls, expected_calls)
        self.assertAlmostEqual(mean_time, expected_mean, delta=self.eps_)

        num_calls, mean_time = TestMeanDecorator.find_calls_time_in_string(
            print_args[0]
        )
        expected_calls, expected_mean = 1, 0.1
        self.assertEqual(num_calls, expected_calls)
        self.assertAlmostEqual(mean_time, expected_mean, delta=self.eps_)

    def test_call_times_le_call_to_mean(self):
        print_args = []
        with patch(
            "builtins.print", side_effect=lambda *args: print_args.append(*args)
        ):

            @mean(5)
            def sleep_function(time_to_sleep):
                time.sleep(time_to_sleep)

            for _ in range(3):
                sleep_function(0.1)

        num_calls, mean_time = TestMeanDecorator.find_calls_time_in_string(
            print_args[-1]
        )
        expected_calls, expected_mean = 3, 0.1
        self.assertEqual(num_calls, expected_calls)
        self.assertAlmostEqual(mean_time, expected_mean, delta=self.eps_)

    def test_call_times_ge_call_to_mean(self):
        print_args = []
        with patch(
            "builtins.print", side_effect=lambda *args: print_args.append(*args)
        ):

            @mean(3)
            def sleep_function(time_to_sleep):
                time.sleep(time_to_sleep)

            for _ in range(5):
                sleep_function(0.1)

        num_calls, mean_time = TestMeanDecorator.find_calls_time_in_string(
            print_args[-1]
        )
        expected_calls, expected_mean = 3, 0.1
        self.assertEqual(num_calls, expected_calls)
        self.assertAlmostEqual(mean_time, expected_mean, delta=self.eps_)

    def test_time_not_const(self):
        print_args = []
        with patch(
            "builtins.print", side_effect=lambda *args: print_args.append(*args)
        ):

            @mean(5)
            def sleep_function(time_to_sleep):
                time.sleep(time_to_sleep)

            for sleep_time in range(3, 6):
                sleep_function(sleep_time * 0.1)

        num_calls, mean_time = TestMeanDecorator.find_calls_time_in_string(
            print_args[-1]
        )
        expected_calls, expected_mean = 3, 0.4
        self.assertEqual(num_calls, expected_calls)
        self.assertAlmostEqual(mean_time, expected_mean, delta=self.eps_)


if __name__ == "__main__":
    unittest.main()
