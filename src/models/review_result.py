from dataclasses import dataclass

from src.models.issue import Issue, Severity


@dataclass(frozen=True)
class QualityScore:
    solid: int
    testability: int
    readability: int
    coverage_estimate: int


@dataclass(frozen=True)
class ReviewResult:
    verdict: str
    issues: list[Issue]
    score: QualityScore
    missing_tests: list[str]
    refactor_suggestion: str

    def count_critical(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == Severity.CRITICAL)
