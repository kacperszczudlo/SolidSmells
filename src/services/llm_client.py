from typing import Protocol

from google import genai

from src.config import GEMINI_API_KEY, GEMINI_MODEL


class LlmClient(Protocol):
    def complete(self, *, system_instruction: str, user_prompt: str) -> str:
        """Zwraca surową odpowiedź tekstową LLM."""
        ...


class GeminiLlmClient:
    """Adapter dla google-genai SDK. Implementuje LlmClient (duck typing)."""

    def __init__(self, api_key: str = GEMINI_API_KEY, model: str = GEMINI_MODEL):
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set")
        self._client = genai.Client(api_key=api_key)
        self._model = model

    def complete(self, *, system_instruction: str, user_prompt: str) -> str:
        response = self._client.models.generate_content(
            model=self._model,
            contents=user_prompt,
            config={
                "system_instruction": system_instruction,
                "response_mime_type": "application/json",
                "temperature": 0.2,
            },
        )
        return response.text or ""
