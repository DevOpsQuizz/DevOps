from flask import Blueprint, request, jsonify
from services.auth_service import admin_required
from services.participations_service import delete_all_participations, add_participation

participations_bp = Blueprint("participations", __name__, url_prefix="/participations")

@participations_bp.route("/all", methods=["DELETE"])
@admin_required
def delete_participations():
    return delete_all_participations()

@participations_bp.route("/", methods=["POST"])
def create_participation():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    return add_participation(
        playerName=data["playerName"],
        answers=data["answers"]
    )