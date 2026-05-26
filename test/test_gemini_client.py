import unittest
from unittest.mock import Mock, patch

from src.services.gemini_client import GeminiLlmClient


class TestGeminiLlmClient(unittest.TestCase):
    def test_should_raise_when_api_key_is_empty(self):
        with self.assertRaises(ValueError) as ctx:
            GeminiLlmClient(api_key="")
        self.assertIn("GEMINI_API_KEY", str(ctx.exception))

    @patch("src.services.gemini_client.genai.Client")
    def test_should_return_text_from_generate_content(self, mock_client_cls):
        mock_response = Mock()
        mock_response.text = '{"verdict":"OK","issues":[]}'
        mock_client_cls.return_value.models.generate_content.return_value = (
            mock_response
        )

        client = GeminiLlmClient(api_key="test-key", model="gemini-3.5-flash")
        result = client.complete(
            system_instruction="system",
            user_prompt="user",
        )

        self.assertEqual(result, '{"verdict":"OK","issues":[]}')
        mock_client_cls.return_value.models.generate_content.assert_called_once()
