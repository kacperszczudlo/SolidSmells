from dataclasses import dataclass
from enum import Enum


class ReviewMode(str, Enum):
    SOLID = "solid"
    SMELLS = "smells"
    COMBINED = "combined"


@dataclass(frozen=True)
class ReviewRequest:
    code: str
    language: str = "python"
    mode: ReviewMode = ReviewMode.COMBINED

    def __post_init__(self) -> None:
        if not self.code or not self.code.strip():
            raise ValueError("ReviewRequest.code cannot be empty")
