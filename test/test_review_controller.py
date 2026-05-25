import unittest
from unittest.mock import Mock

from src.app_factory import create_app
from src.models.review_result import QualityScore, ReviewResult
from src.services.review_service import ReviewService


class TestReviewController(unittest.TestCase):

    def setUp(self):
        self.service = Mock(spec=ReviewService)
        self.service.analyze.return_value = ReviewResult(
            verdict="OK",
            issues=[],
            missing_tests=[],
            refactor_suggestion="",
            score=QualityScore(
                solid=5,
                testability=5,
                readability=5,
                coverage_estimate=80,
            ),
        )
        self.app = create_app(review_service=self.service)
        self.client = self.app.test_client()

    def test_should_return_400_when_code_is_missing(self):
        response = self.client.post("/api/review", json={})
        self.assertEqual(response.status_code, 400)

    def test_should_return_200_with_result_on_valid_request(self):
        response = self.client.post("/api/review", json={"code": "x = 1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["verdict"], "OK")

    def test_should_pass_mode_to_service(self):
        self.client.post("/api/review", json={"code": "x=1", "mode": "solid"})
        called_with = self.service.analyze.call_args.args[0]
        self.assertEqual(called_with.mode.value, "solid")

    def test_should_return_502_when_llm_response_is_malformed(self):
        from src.services.response_parser import ParseError

        self.service.analyze.side_effect = ParseError("Invalid JSON from LLM")
        response = self.client.post("/api/review", json={"code": "x = 1"})
        self.assertEqual(response.status_code, 502)
        self.assertIn("malformed", response.get_json()["error"])
