import service.questions
from .questions import questions_bp, quiz_questions_bp
def register_blueprints(app):
    app.register_blueprint(questions_bp)
    app.register_blueprint(quiz_questions_bp)
