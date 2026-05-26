import json
import unittest

from src.app_factory import create_app
from src.models.review_request import ReviewRequest
from src.services.prompt_builder import PromptBuilder
from src.services.response_parser import ResponseParser
from src.services.review_service import ReviewService

VALID_JSON = json.dumps(
    {
        "verdict": "OK — kod wymaga drobnych poprawek",
        "issues": [],
        "missing_tests": ["edge case"],
        "refactor_suggestion": "def f() -> None:\n    pass",
        "score": {
            "solid": 4,
            "testability": 4,
            "readability": 4,
            "coverage_estimate": 75,
        },
    }
)


class FakeLlmClient:
    def complete(self, *, system_instruction: str, user_prompt: str) -> str:
        return VALID_JSON


class TestIntegration(unittest.TestCase):

    def setUp(self):
        service = ReviewService(PromptBuilder(), FakeLlmClient(), ResponseParser())
        self.client = create_app(review_service=service).test_client()

    def test_should_return_full_review_json_from_api(self):
        response = self.client.post(
            "/api/review",
            json={"code": "def hello(): pass", "mode": "combined"},
        )

        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertEqual(body["verdict"], "OK — kod wymaga drobnych poprawek")
        self.assertEqual(body["score"]["solid"], 4)
        self.assertIn("edge case", body["missing_tests"][0])

    def test_should_reject_empty_code_without_calling_llm(self):
        response = self.client.post("/api/review", json={"code": "   "})

        self.assertEqual(response.status_code, 400)
        self.assertIn("required", response.get_json()["error"])
