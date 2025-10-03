from flask import Blueprint, request, jsonify
from db import SessionLocal
from models import Questions

questions_bp = Blueprint("questions", __name__, url_prefix="/api/questions")

quiz_questions_bp = Blueprint("quiz_questions", __name__, url_prefix="/api/questions")

