from flask import Blueprint, request, jsonify
from services.auth_service import admin_required
from services.participations import delete_all_participations, add_participation

participations_bp = Blueprint("participations", __name__, url_prefix="/participations")

@participations_bp.route("/all", methods=["DELETE"])
@admin_required
def delete_all_participations():
    return delete_all_participations()

@participations_bp.route("/add", methods=["POST"])
def create_participation():
    return add_participation()
