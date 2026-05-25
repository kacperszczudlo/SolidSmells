import unittest

from src.models.issue import Issue, Severity
from src.models.review_request import ReviewRequest, ReviewMode
from src.models.review_result import QualityScore, ReviewResult


class TestIssue(unittest.TestCase):

    def test_should_create_issue_with_all_fields(self):
        # Arrange
        severity, category = Severity.CRITICAL, "SOLID/SRP"
        location, problem = "calc.py:10", "Klasa robi za dużo"

        # Act
        issue = Issue(
            severity=severity,
            category=category,
            location=location,
            problem=problem,
            why_it_hurts="trudna w testach",
            fix="Extract Class",
        )

        # Assert
        self.assertEqual(issue.severity, Severity.CRITICAL)

    def test_should_raise_value_error_when_problem_is_empty(self):
        with self.assertRaises(ValueError):
            Issue(
                severity=Severity.WARNING,
                category="X",
                location="a.py:1",
                problem="",
                why_it_hurts="x",
                fix="y",
            )


class TestReviewResult(unittest.TestCase):

    def test_should_return_empty_issues_when_none_provided(self):
        # Arrange
        score = QualityScore(
            solid=5,
            testability=5,
            readability=5,
            coverage_estimate=90,
        )

        # Act
        result = ReviewResult(
            verdict="OK",
            issues=[],
            score=score,
            missing_tests=[],
            refactor_suggestion="",
        )

        # Assert
        self.assertEqual(result.issues, [])

    def test_should_count_critical_issues(self):
        # Arrange
        crit = Issue(
            severity=Severity.CRITICAL,
            category="X",
            location="a:1",
            problem="P",
            why_it_hurts="W",
            fix="F",
        )
        score = QualityScore(
            solid=3,
            testability=3,
            readability=3,
            coverage_estimate=50,
        )

        # Act
        result = ReviewResult(
            verdict="x",
            issues=[crit, crit],
            score=score,
            missing_tests=[],
            refactor_suggestion="",
        )

        # Assert
        self.assertEqual(result.count_critical(), 2)


class TestReviewRequest(unittest.TestCase):

    def test_should_default_to_combined_mode(self):
        req = ReviewRequest(code="print('x')")
        self.assertEqual(req.mode, ReviewMode.COMBINED)

    def test_should_raise_when_code_is_empty(self):
        with self.assertRaises(ValueError):
            ReviewRequest(code="")
