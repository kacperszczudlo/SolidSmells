import unittest

from src.models.review_request import ReviewRequest, ReviewMode
from src.services.prompt_builder import PromptBuilder


class TestPromptBuilder(unittest.TestCase):

    def setUp(self):
        self.builder = PromptBuilder()

    def test_should_include_persona_in_system_instruction(self):
        sys_msg = self.builder.system_instruction()
        self.assertIn("Principal Python", sys_msg)

    def test_should_include_json_schema_request_in_system_instruction(self):
        sys_msg = self.builder.system_instruction()
        self.assertIn("JSON", sys_msg)

    def test_should_include_code_in_user_prompt(self):
        # Arrange
        req = ReviewRequest(code="def f(): pass")

        # Act
        prompt = self.builder.user_prompt(req)

        # Assert
        self.assertIn("def f(): pass", prompt)

    def test_should_include_mode_marker_in_user_prompt(self):
        req = ReviewRequest(code="x = 1", mode=ReviewMode.SOLID)
        prompt = self.builder.user_prompt(req)
        self.assertIn("SOLID", prompt)

    def test_should_include_javascript_language_in_user_prompt(self):
        # Arrange
        req = ReviewRequest(code="const x = 1;", language="javascript")

        # Act
        prompt = self.builder.user_prompt(req)

        # Assert
        self.assertIn("JavaScript", prompt)
        self.assertIn("const x = 1;", prompt)
