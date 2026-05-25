from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    NIT = "nit"


@dataclass(frozen=True)
class Issue:
    severity: Severity
    category: str
    location: str
    problem: str
    why_it_hurts: str
    fix: str

    def __post_init__(self) -> None:
        if not self.problem:
            raise ValueError("Issue.problem cannot be empty")
