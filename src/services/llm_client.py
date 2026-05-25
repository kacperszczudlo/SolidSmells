from typing import Protocol


class LlmClient(Protocol):
    def complete(self, *, system_instruction: str, user_prompt: str) -> str:
        """Zwraca surową odpowiedź tekstową LLM."""
        ...
