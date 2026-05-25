from dataclasses import asdict

from flask import Blueprint, jsonify, request

from src.models.review_request import ReviewMode, ReviewRequest
from src.services.response_parser import ParseError
from src.services.review_service import ReviewService


def create_blueprint(service: ReviewService) -> Blueprint:
    bp = Blueprint("review", __name__)

    @bp.post("/api/review")
    def review():
        data = request.get_json(silent=True) or {}
        code = data.get("code", "")
        if not code or not code.strip():
            return jsonify({"error": "code is required"}), 400
        try:
            req = ReviewRequest(
                code=code,
                language=data.get("language", "python"),
                mode=ReviewMode(data.get("mode", "combined")),
            )
            result = service.analyze(req)
            return jsonify(asdict(result)), 200
        except ParseError as e:
            return jsonify({"error": f"LLM returned malformed response: {e}"}), 502
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    return bp
