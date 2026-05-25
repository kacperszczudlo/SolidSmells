import unittest

from src.models.issue import Issue, Severity


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
