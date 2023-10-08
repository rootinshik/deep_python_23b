import unittest
from unittest.mock import patch

from parse_json import parse_json


class TestParseJson(unittest.TestCase):
    def test_empty_json(self):
        json_str = "{}"
        required_fields = ["key1"]
        keywords = ["word2"]

        with patch("builtins.print") as mock_print:
            parse_json(json_str, required_fields, keywords, print)
            mock_print.assert_not_called()

    def test_empty_required_fields(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_fields = []
        keywords = ["word2"]

        with patch("builtins.print") as mock_print:
            parse_json(json_str, required_fields, keywords, print)
            mock_print.assert_not_called()

    def test_empty_keywords(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_fields = ["key1"]
        keywords = []

        with patch("builtins.print") as mock_print:
            parse_json(json_str, required_fields, keywords, print)
            mock_print.assert_not_called()

    def test_case_sensitive_required_fields(self):
        json_str = '{"Key1": "Word1 word2"}'
        required_fields = ["key1"]
        keywords = ["word2"]

        with patch("builtins.print") as mock_print:
            parse_json(json_str, required_fields, keywords, print)
            mock_print.assert_not_called()

    def test_case_insensitivity_keywords(self):
        json_str = '{"key1": "Word1 word2", ' \
                   '"key2": "worD2 Word3"}'
        required_fields = ["key1", "key2"]
        keywords = ["Word2", "wOrd3"]
        expected_output = [
            ("key1", "word2"),
            ("key2", "worD2"),
            ("key2", "Word3")
        ]

        print_args = []
        with patch("builtins.print",
                   side_effect=lambda *args: print_args.append(args)):
            parse_json(json_str, required_fields, keywords, print)
        self.assertEqual(print_args, expected_output)

    def test_keyword_in_two_string_required_fields_in_one(self):
        json_str = '{"key1": "Word1 word2", ' \
                   '"key2": "word2 word3"}'
        required_fields = ["key1"]
        keywords = ["word2"]
        expected_output = "key1", "word2"

        with patch("builtins.print") as mock_print:
            parse_json(json_str, required_fields, keywords, print)
            mock_print.assert_called_with(*expected_output)

    def test_parse_json_with_non_matching_keywords(self):
        json_str = '{"key1": "Word1 word2", ' \
                   '"key2": "word2 word3"}'
        required_fields = ["key1"]
        keywords = ["word3"]

        with patch("builtins.print") as mock_print:
            parse_json(json_str, required_fields, keywords, print)
            mock_print.assert_not_called()

    def test_missing_required_field(self):
        json_str = '{"key2": "word2 word3"}'
        required_fields = ["key1"]
        keywords = ["word2"]

        with patch("builtins.print") as mock_print:
            parse_json(json_str, required_fields, keywords, print)
            mock_print.assert_not_called()

    def test_required_fields_is_none(self):
        json_str = '{"key2": "word2 word3"}'
        required_fields = None
        keywords = ["word2"]

        with self.assertRaises(TypeError):
            parse_json(json_str, required_fields, keywords, print)

    def test_keywords_is_none(self):
        json_str = '{"key2": "word2 word3"}'
        required_fields = ["key1"]
        keywords = None

        with self.assertRaises(TypeError):
            parse_json(json_str, required_fields, keywords, print)

    def test_keyword_callback_is_none(self):
        json_str = '{"key2": "word2 word3"}'
        required_fields = ["key1"]
        keywords = ["word2"]

        with self.assertRaises(TypeError):
            parse_json(json_str, required_fields, keywords, None)

    def test_multiple_matches(self):
        json_str = '{"key1": "Word1 word3 word2", ' \
                   '"key2": "word2 word4"}'
        required_fields = ["key1", "key2"]
        keywords = ["word2", "word3"]
        expected_output = [
            ("key1", "word3"),
            ("key1", "word2"),
            ("key2", "word2")
        ]

        print_args = []
        with patch("builtins.print",
                   side_effect=lambda *args: print_args.append(args)):
            parse_json(json_str, required_fields, keywords, print)
        self.assertEqual(print_args, expected_output)

    def test_keyword_not_found(self):
        json_str = '{"key1": "Word1 word3", ' \
                   '"key2": "word4 word5", ' \
                   '"key3": "word2"}'
        required_fields = ["key1", "key2"]
        keywords = ["word2"]

        with patch("builtins.print") as mock_print:
            parse_json(json_str, required_fields, keywords, print)
            mock_print.assert_not_called()

    def test_multiple_keywords_in_one_string(self):
        json_str = '{"key1": "Word1 word2 word3", ' \
                   '"key2": "word3 word4 word2"}'
        required_fields = ["key1", "key2"]
        keywords = ["word2", "word3", "word42"]
        expected_output = [
            ("key1", "word2"),
            ("key1", "word3"),
            ("key2", "word3"),
            ("key2", "word2"),
        ]

        print_args = []
        with patch("builtins.print",
                   side_effect=lambda *args: print_args.append(args)):
            parse_json(json_str, required_fields, keywords, print)
        self.assertEqual(print_args, expected_output)

    def test_base_functionality(self):
        json_str = '{"key1": "Word1 word42 word3, word4", ' \
                   '"key2": "word3 word4 word42" ,' \
                   '"key3": "word42 word5 word12" , ' \
                   '"key4": "ord42 rd42 wrd42 d42 42"}'
        required_fields = ["key1", "key2", "key3", "key4"]
        keywords = ["word42"]
        expected_output = [
            ("key1", "word42"),
            ("key2", "word42"),
            ("key3", "word42"),
        ]

        print_args = []
        with patch("builtins.print",
                   side_effect=lambda *args: print_args.append(args)):
            parse_json(json_str, required_fields, keywords, print)
        self.assertEqual(print_args, expected_output)


if __name__ == "__main__":
    unittest.main()
