import json
import re

from src.models.issue import Issue, Severity
from src.models.review_result import QualityScore, ReviewResult

_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)


class ParseError(Exception):
    pass


def _strip_fences(raw: str) -> str:
    return _FENCE.sub("", raw).strip()


class ResponseParser:
    def parse(self, raw: str) -> ReviewResult:
        cleaned = _strip_fences(raw)
        if not cleaned:
            raise ParseError("Empty response from LLM")
        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise ParseError(f"Invalid JSON from LLM: {e}") from e
        return self._to_result(data)

    def _to_result(self, data: dict) -> ReviewResult:
        try:
            issues = [self._to_issue(item) for item in data.get("issues", [])]
            score_data = data["score"]
            score = QualityScore(
                solid=score_data["solid"],
                testability=score_data["testability"],
                readability=score_data["readability"],
                coverage_estimate=score_data["coverage_estimate"],
            )
            return ReviewResult(
                verdict=data["verdict"],
                issues=issues,
                missing_tests=data.get("missing_tests", []),
                refactor_suggestion=data.get("refactor_suggestion", ""),
                score=score,
            )
        except KeyError as e:
            raise ParseError(f"Missing field in LLM response: {e}") from e

    @staticmethod
    def _to_issue(item: dict) -> Issue:
        try:
            severity = Severity(item["severity"])
        except ValueError as e:
            raise ParseError(
                f"Invalid severity in LLM response: {item['severity']}"
            ) from e
        return Issue(
            severity=severity,
            category=item["category"],
            location=item["location"],
            problem=item["problem"],
            why_it_hurts=item["why_it_hurts"],
            fix=item["fix"],
        )
