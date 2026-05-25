from dataclasses import asdict

from flask import Blueprint, jsonify, request

from src.models.review_request import ReviewMode, ReviewRequest
from src.services.response_parser import ParseError
from src.services.review_service import ReviewService


def _parse_review_request(data: dict) -> ReviewRequest:
    code = data.get("code", "")
    if not code or not code.strip():
        raise ValueError("code is required")
    return ReviewRequest(
        code=code,
        language=data.get("language", "python"),
        mode=ReviewMode(data.get("mode", "combined")),
    )


def create_blueprint(service: ReviewService) -> Blueprint:
    bp = Blueprint("review", __name__)

    @bp.post("/api/review")
    def review():
        data = request.get_json(silent=True) or {}
        try:
            req = _parse_review_request(data)
            result = service.analyze(req)
            return jsonify(asdict(result)), 200
        except ParseError as e:
            return jsonify({"error": f"LLM returned malformed response: {e}"}), 502
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    return bp
