from db import SessionLocal
from models import *
from flask import request, jsonify
from datetime import datetime

def delete_all_participations():
    session = SessionLocal()
    session.query(Participations).delete()
    session.commit()
    session.close()
    return jsonify({"message": "All participations deleted successfully"}), 204

def add_participation():
    data = request.get_json()
    session = SessionLocal()
    participation = Participations(
        playerName=data["playerName"],
        score=data["score"],
        date=datetime.utcnow(),
        answers=data["answers"],  # tableau d'id réponses
        idVersions=data["idVersions"]
    )
    session.add(participation)
    session.commit()
    session.close()
    return jsonify({"message": "Participation enregistrée"}), 201
