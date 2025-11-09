import hashlib
from flask import jsonify, request
from jwt_utils import build_token, decode_token
from functools import wraps

# md5("iloveflask") = d278077bbfe7285a144d4b5b11adb9cf
ADMIN_HASH_MD5 = "d278077bbfe7285a144d4b5b11adb9cf"


def handle_admin_login(payload):
    """
    Traite le login admin:
    - 200 {token} si OK, 400 si input invalide, 401 si accès non autorisé
    """

    password = str(payload.get("password") or "")
    if not password:
        return jsonify({"error": "Password required"}), 400

    provided_hash = hashlib.md5(password.encode("utf-8")).hexdigest()
    if provided_hash != ADMIN_HASH_MD5:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        token = build_token("quiz-app-admin")
        return jsonify({"token": token}), 200
    except Exception:
        return jsonify({"error": "Internal server error"}), 500
    


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get("Authorization"):
            return jsonify({"error": "Unauthorized"}), 401
        sub = decode_token(request.headers.get("Authorization").split("Bearer ")[-1])
        if sub == "quiz-app-admin":
            return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized"}), 401
    return decorated_function