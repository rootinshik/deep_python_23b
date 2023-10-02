import unittest
from unittest import mock

from find_in_file import find_in_file


class TestFileFilter(unittest.TestCase):
    @mock.patch(
        "find_in_file.open",
        mock.mock_open(
            read_data="а Роза упала на лапу Азора \n"
                      "В порыве любви прошептала Аврора"
        ),
    )
    def test_one_word_in_one_line(self):
        words_to_find = ["роза"]
        result = list(find_in_file(file="/dev/null",
                                   words_to_find=words_to_find))
        self.assertEqual(result, ["а Роза упала на лапу Азора"])

    @mock.patch(
        "find_in_file.open",
        mock.mock_open(
            read_data="а Роза упала на лапу Азора \n"
                      "В порыве любви прошептала Аврора"
        ),
    )
    def test_two_words_in_one_line(self):
        words_to_find = ["роза", "УПАЛА"]
        result = list(find_in_file(file="/dev/null",
                                   words_to_find=words_to_find))
        self.assertEqual(result, ["а Роза упала на лапу Азора"])

    @mock.patch(
        "find_in_file.open",
        mock.mock_open(
            read_data="а Роза упала на лапу Азора \n"
                      "В порыве любви прошептала Аврора"
        ),
    )
    def test_two_words_in_two_lines(self):
        words_to_find = ["А", "роза", "УПАЛА", "аврора"]
        result = list(find_in_file(file="/dev/null",
                                   words_to_find=words_to_find))
        self.assertEqual(result, ["а Роза упала на лапу Азора",
                                  "В порыве любви прошептала Аврора"])

    @mock.patch(
        "find_in_file.open",
        mock.mock_open(
            read_data="а Роза упала на лапу Азора \n"
                      "В порыве любви прошептала Аврора"
        ),
    )
    def test_zero_words_match(self):
        words_to_find = ["роз"]
        result = list(find_in_file(file="/dev/null",
                                   words_to_find=words_to_find))
        self.assertEqual(result, [])

    @mock.patch(
        "find_in_file.open",
        mock.mock_open(
            read_data="а Роза упала на лапу Азора \n"
                      "В порыве любви прошептала Аврора"
        ),
    )
    def test_no_words_to_find(self):
        words_to_find = []
        result = list(find_in_file(file="/dev/null",
                                   words_to_find=words_to_find))
        self.assertEqual(result, [])

    @mock.patch("find_in_file.open", mock.mock_open(read_data=""))
    def test_empty_file(self):
        words_to_find = ["аврора"]
        result = list(find_in_file(file="/dev/null",
                                   words_to_find=words_to_find))
        self.assertEqual(result, [])

    @mock.patch(
        "find_in_file.open",
        mock.mock_open(
            read_data="а Роза упала на лапу Азора \n"
                      "В порыве любви прошептала Аврора"
        ),
    )
    def test_case_sens_words(self):
        words_to_find = ["РОЗА", "в"]
        result = list(find_in_file(file="/dev/null",
                                   words_to_find=words_to_find))
        self.assertEqual(result, ["а Роза упала на лапу Азора",
                                  "В порыве любви прошептала Аврора"])

    @mock.patch(
        "find_in_file.open",
        mock.mock_open(
            read_data="а Роза упала на лапу Азора \n"
                      "В порыве любви прошептала Аврора"
        ),
    )
    def test_word_equal_file(self):
        words_to_find = ["а Роза упала на лапу Азора"]
        result = list(find_in_file(file="/dev/null",
                                   words_to_find=words_to_find))
        self.assertEqual(result, [])

    @mock.patch(
        "find_in_file.open",
        mock.mock_open(
            read_data="а Роза упала на лапу Азора \n"
                      "В порыве любви прошептала Аврора"
        ),
    )
    def test_gen(self):
        words_to_find = ["роза"]
        gen = find_in_file(file="/dev/null",
                           words_to_find=words_to_find)
        self.assertEqual(next(gen), "а Роза упала на лапу Азора")
        with self.assertRaises(StopIteration):
            next(gen)

    @mock.patch(
        "find_in_file.open",
        mock.mock_open(
            read_data="а Роза упала на лапу Азора \n"
                      "В порыве любви прошептала Аврора"
        ),
    )
    def test_empty_word(self):
        words_to_find = [""]
        result = list(find_in_file(file="/dev/null",
                                   words_to_find=words_to_find))
        self.assertEqual(result, [])

    def test_not_file_as_input(self):
        words_to_find = ["роза"]
        gen = find_in_file(file=42,
                           words_to_find=words_to_find)
        with self.assertRaises(AttributeError):
            next(gen)

    # Тест для генератора
