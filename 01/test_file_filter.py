import unittest
from unittest import mock

from file_filter import FileFilter


class TestFileFilter(unittest.TestCase):
    def test_words_in_string(self):
        search_string = 'а Роза упала на лапу Азора'
        words_to_find = [['роза'], ['В', 'порыве', 'любви', 'прошептала', 'Аврора']]

        result1 = FileFilter.words_in_string(search_string, words_to_find[0])
        result2 = FileFilter.words_in_string(search_string, words_to_find[1])
        self.assertEqual(result1, True)
        self.assertEqual(result2, False)

    def test_file_to_string_generator(self):
        ...

    def test_find_in_file(self):
        ...

    def test_find_in_file_obj(self):
        ...
