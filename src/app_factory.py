from flask import Flask, render_template

from src.controllers.review_controller import create_blueprint
from src.services.prompt_builder import PromptBuilder
from src.services.response_parser import ResponseParser
from src.services.review_service import ReviewService


def create_app(review_service: ReviewService | None = None) -> Flask:
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    if review_service is None:
        from src.services.gemini_client import GeminiLlmClient

        review_service = ReviewService(
            PromptBuilder(),
            GeminiLlmClient(),
            ResponseParser(),
        )

    app.register_blueprint(create_blueprint(review_service))

    @app.get("/")
    def index():
        return render_template("index.html")

    return app
