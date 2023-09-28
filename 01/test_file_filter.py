import unittest
from io import StringIO
from unittest import mock

from file_filter import FileFilter


class TestFileFilter(unittest.TestCase):
    def test_words_in_string(self):
        search_string = "а Роза упала на лапу Азора"
        words_to_find = [["роза"],
                         ["В", "порыве", "любви", "прошептала", "Аврора"]]

        result1 = FileFilter.words_in_string(search_string, words_to_find[0])
        result2 = FileFilter.words_in_string(search_string, words_to_find[1])
        self.assertEqual(result1, True)
        self.assertEqual(result2, False)

    def test_file_to_string_generator(self):
        input_data = "а\nроза \n упала"
        file_mock = StringIO(input_data)
        result = list(FileFilter.file_to_string_generator(file_mock))
        self.assertEqual(result, ["а", "роза", "упала"])

    @mock.patch(
        "file_filter.open",
        mock.mock_open(
            read_data="а Роза упала на лапу Азора \n"
                      "В порыве любви прошептала Аврора"
        ),
    )
    def test_find_in_file(self):
        result1 = ["а Роза упала на лапу Азора"]
        result2 = ["В порыве любви прошептала Аврора"]
        self.assertEqual(result1,
                         FileFilter.find_in_file("/dev/null", ["роза"]))
        self.assertEqual(result2,
                         FileFilter.find_in_file("/dev/null", ["Порыве"]))

        self.assertEqual([],
                         FileFilter.find_in_file("/dev/null", ["лю"]))

    def test_find_in_file_obj(self):
        input_data = "а Роза упала на лапу Азора"\
                     "\nВ порыве любви прошептала Аврора"
        file_mock = StringIO(input_data)
        result = FileFilter.find_in_file_obj(file_mock, ["роза", "упала"])
        self.assertEqual(result, ["а Роза упала на лапу Азора"])
