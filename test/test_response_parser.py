import json
import unittest

from src.services.response_parser import ParseError, ResponseParser

VALID = {
    "verdict": "OK",
    "issues": [],
    "missing_tests": [],
    "refactor_suggestion": "",
    "score": {
        "solid": 5,
        "testability": 5,
        "readability": 5,
        "coverage_estimate": 90,
    },
}


class TestResponseParser(unittest.TestCase):

    def setUp(self):
        self.parser = ResponseParser()

    def test_should_parse_valid_response(self):
        result = self.parser.parse(json.dumps(VALID))
        self.assertEqual(result.verdict, "OK")

    def test_should_strip_markdown_fences(self):
        wrapped = "```json\n" + json.dumps(VALID) + "\n```"
        result = self.parser.parse(wrapped)
        self.assertEqual(result.verdict, "OK")
