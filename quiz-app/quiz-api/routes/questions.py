from flask import Blueprint, request, jsonify
from services.questions_service import get_question_by_position, get_question_by_id, count_questions, create_question, update_question, delete_question, delete_all_questions
from services.auth_service import admin_required

questions_bp = Blueprint("questions", __name__, url_prefix="/questions")

@questions_bp.route("/", methods=["GET"])
def quiz_question():
    pos = request.args.get("position")
    if pos is None:
        return jsonify({"error": "Missing 'position' query parameter"}), 400
    try:
        position = int(pos)
    except ValueError:
        return jsonify({"error": "'position' must be an integer"}), 400
    return get_question_by_position(position)

@questions_bp.route("/", methods=["POST"])
@admin_required
def create_question_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    return create_question(data)


@questions_bp.route("/<int:question_id>", methods=["GET"])
def get_question_route(question_id):
    return get_question_by_id(question_id)

@questions_bp.route("/<int:question_id>", methods=["PUT"])
@admin_required
def update_question_route(question_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    return update_question(question_id, data)

@questions_bp.route("/<int:question_id>", methods=["DELETE"])
@admin_required
def delete_question_route(question_id):
    return delete_question(question_id)

@questions_bp.route("/all", methods=["DELETE"])
@admin_required
def delete_all_questions_route():
    return delete_all_questions()
