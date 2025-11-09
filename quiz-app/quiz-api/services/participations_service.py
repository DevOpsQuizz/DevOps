from db import SessionLocal
from models import *
from datetime import datetime
from flask import jsonify

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
    print("Questions fetched:", len(questions))
    print("Answers received:", len(answers))
    if len(answers) != len(questions):
        print("Mismatch in number of answers and questions")
        session.close()
        return jsonify({"error": "Le nombre de réponses ne correspond pas au nombre de questions du quiz."}), 400

    print('Calculating score...')
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
    return jsonify({"message": "La participation au quiz a été enregistrée", "playerName": playerName, "score": score}), 200

def get_leaderboard_data(page=1, limit=20):
    """
    Récupère le classement des participants avec pagination.
    :param page: Numéro de la page (1 par défaut).
    :param limit: Nombre de participants par page (20 par défaut).
    :return: Dictionnaire contenant les participants et le nombre total de pages.
    """
    session = SessionLocal()
    try:
        query = session.query(Participations).order_by(Participations.score.desc())
        total = query.count()
        participants = query.offset((page - 1) * limit).limit(limit).all()
        data = [
            {"id": p.id, "playerName": p.playerName, "score": p.score}
            for p in participants
        ]
        total_pages = (total + limit - 1) // limit
        return {"data": data, "totalPages": total_pages}
    finally:
        session.close()