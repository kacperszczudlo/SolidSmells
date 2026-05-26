import json
import unittest
from unittest.mock import Mock

from src.models.review_request import ReviewRequest
from src.services.llm_client import LlmClient
from src.services.prompt_builder import PromptBuilder
from src.services.response_parser import ResponseParser
from src.services.review_service import ReviewService

VALID_JSON = json.dumps(
    {
        "verdict": "Wymaga refaktoryzacji",
        "issues": [],
        "missing_tests": [],
        "refactor_suggestion": "",
        "score": {
            "solid": 3,
            "testability": 3,
            "readability": 4,
            "coverage_estimate": 60,
        },
    }
)


class TestReviewService(unittest.TestCase):
    def test_should_call_llm_with_system_instruction_and_user_prompt(self):
        # Arrange
        mock_llm = Mock(spec=LlmClient)
        mock_llm.complete.return_value = VALID_JSON
        service = ReviewService(PromptBuilder(), mock_llm, ResponseParser())
        req = ReviewRequest(code="def f(): pass")

        # Act
        service.analyze(req)

        # Assert
        mock_llm.complete.assert_called_once()
        kwargs = mock_llm.complete.call_args.kwargs
        self.assertIn("Principal Python", kwargs["system_instruction"])
        self.assertIn("def f(): pass", kwargs["user_prompt"])

    def test_should_return_parsed_result_from_llm(self):
        mock_llm = Mock(spec=LlmClient)
        mock_llm.complete.return_value = VALID_JSON
        service = ReviewService(PromptBuilder(), mock_llm, ResponseParser())

        result = service.analyze(ReviewRequest(code="x = 1"))

        self.assertEqual(result.verdict, "Wymaga refaktoryzacji")
