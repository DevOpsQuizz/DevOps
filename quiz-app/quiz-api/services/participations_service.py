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

def add_participation(playerName, answers):
    session = SessionLocal()
    latest_version = session.query(Versions).order_by(Versions.id.desc()).first()
    
    if not latest_version:
        new_version = Versions(date=datetime.utcnow())
        session.add(new_version)
        session.commit()
        latest_version = new_version.id
    else:
        latest_version = latest_version.id

    questions = session.query(Questions).filter_by(idVersions=latest_version).all()
    if len(answers) != len(questions):
        session.close()
        return jsonify({"error": "Le nombre de réponses ne correspond pas au nombre de questions du quiz."}), 400

    score = 0

    for idx in range(len(questions)):
        question = session.query(Questions).filter_by(idVersions=latest_version, position=idx + 1).first()
        possible_answers = session.query(Answers).filter_by(idQuestions=question.id).all()
        if possible_answers[answers[idx]-1].isCorrect:
                score += 1

    participation = Participations(
        playerName=playerName,
        score=score,
        date=datetime.utcnow(),
        answers=answers,  # tableau d'id réponses
        idVersions=latest_version
    )
    session.add(participation)
    session.commit()
    session.close()
    return jsonify({"message": "La participation au quiz a été enregistrée", "playerName": playerName, "score": score}), 201
