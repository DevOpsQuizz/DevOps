from flask import Blueprint, jsonify
from services.quiz_service import get_quiz_info

quiz_info_bp = Blueprint("quiz-info", __name__, url_prefix="/quiz-info")

@quiz_info_bp.route("/", methods=["GET"])
def quiz_info():
    return get_quiz_info()