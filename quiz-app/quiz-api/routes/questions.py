from flask import Blueprint
from services.questions import get_question_by_position, count_questions, create_question

questions_bp = Blueprint("questions", __name__, url_prefix="/questions")

@questions_bp.route("/quiz", methods=["GET"])
def quiz_question():
    return get_question_by_position()

@questions_bp.route("/count", methods=["GET"])
def quiz_count():
    return count_questions()

@questions_bp.route("/", methods=["POST"])
def create_question_route():
    return create_question()