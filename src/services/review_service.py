from src.models.review_request import ReviewRequest
from src.models.review_result import ReviewResult
from src.services.llm_client import LlmClient
from src.services.prompt_builder import PromptBuilder
from src.services.response_parser import ResponseParser


class ReviewService:
    def __init__(
        self,
        builder: PromptBuilder,
        llm: LlmClient,
        parser: ResponseParser,
    ):
        self._builder = builder
        self._llm = llm
        self._parser = parser

    def analyze(self, request: ReviewRequest) -> ReviewResult:
        raw = self._llm.complete(
            system_instruction=self._builder.system_instruction(),
            user_prompt=self._builder.user_prompt(request),
        )
        return self._parser.parse(raw)
