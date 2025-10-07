from flask import Blueprint, request, jsonify
from db import SessionLocal
from models import Participations
from services.participations import add_participation
participations_bp = Blueprint("participations", __name__, url_prefix="/api/participations")

@participations_bp.route("/add", methods=["POST"])
def create_participation():
    return add_participation()