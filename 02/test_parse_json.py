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

    def test_case_sensitive_keywords(self):
        json_str = '{"key1": "Word1 word2"}'
        required_fields = ["key1"]
        keywords = ["wOrd2"]

        with patch("builtins.print") as mock_print:
            parse_json(json_str, required_fields, keywords, print)
            mock_print.assert_not_called()

    def test_keyword_in_two_string_required_fields_in_one(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_fields = ["key1"]
        keywords = ["word2"]
        expected_output = "key1", "word2"

        with patch("builtins.print") as mock_print:
            parse_json(json_str, required_fields, keywords, print)
            mock_print.assert_called_with(*expected_output)

    def test_parse_json_with_non_matching_keywords(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
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


if __name__ == "__main__":
    unittest.main()
