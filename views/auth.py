from models import db, User
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from models import TokenBlocklist
from flask_jwt_extended import get_jwt


auth_bp = Blueprint("auth_bp", __name__)

# LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data['email']
    password = data['email']

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        # Creating a token and associating it with the user id
        access_token = create_access_token(identity=user.id)
        return jsonify({"Access Token": access_token}), 200

    else:
        return jsonify({"error": "Either email/password is incorrect"}), 404
    

# Getting the current user
@auth_bp.route("/current_user", methods=["GET"])
# Pass it before any route that you want to be protected
@jwt_required()
def current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }
    return jsonify({"user": user_data}), 200



# Endpoint for revoking the current users access token. Saved the unique
# identifier (jti) for the JWT into our database.
@auth_bp.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return jsonify({"success":"Logged out successfully"})