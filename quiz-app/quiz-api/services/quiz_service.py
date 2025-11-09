from db import SessionLocal
from models import Questions, Participations
from flask import jsonify

def get_quiz_info():
    session = SessionLocal()
    try:
        # Les questions
        questions = session.query(Questions).all()
        size = len(questions)
        print("Quiz size:", size)

        # Participations
        participations = session.query(Participations).all()
        scores = [
            {
                "playerName": p.playerName,
                "score": p.score,
                "date": p.date.isoformat() if p.date else None
            }
            for p in participations
        ]

        return jsonify({
            "size": size,
            "scores": scores
        }), 200
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
    finally:
        session.close()