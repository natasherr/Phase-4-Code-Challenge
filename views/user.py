from models import db, User
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from flask_mail import Message
from app import mail,app
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint("user_bp", __name__)


# FETCH USERS
@user_bp.route("/users")
def fetch_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin
            })
        
    return jsonify(user_list)

# FETCH USER BY ID
@user_bp.route("/users/<int:user_id>")
def fetch_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin
            })
    else:
        return jsonify({"error": "User not found"})

# ADD USERS
@user_bp.route("/user/add", methods=["POST"])
def add_user():
    data = request.get_json()

    username = data['username']   
    email = data['email']
    password = generate_password_hash(data['password'])
    is_admin = (data['is_admin'])

    check_username = User.query.filter_by(username=username).first()
    check_email = User.query.filter_by(email=email).first()

    if check_username or check_email:
        return jsonify({"error":"Username/email already exists"})
    
    else:
        new_user = User(username=username, email=email, password=password, is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()

        try:
            msg = Message(
                subject="Test Mail",
                sender=app.config["MAIL_DEFAULT_SENDER"],
                recipients=[email],
                body="This is a test mail sent from a Flask Application."
            )
            mail.send(msg)
            return jsonify({"success": "User created successfully"})

        except Exception as e:
            return jsonify({"error":f"Failed to send mail: {str(e)}"})


# Update User
@user_bp.route("/users", methods=["PATCH"])
@jwt_required()
def update_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user:
        data = request.get_json()

        username = data.get('username', user.username)   
        email = data.get('email', user.email)
        password = generate_password_hash(data.get('password', user.password))
        is_admin = data.get('is_admin', user.is_admin)

        check_username = User.query.filter_by(username=username and id!= user.id).first()
        check_email = User.query.filter_by(email=email and id!= user.id).first()

        if check_username or check_email:
            return jsonify({"error":"Username/email already exists"})
        
        else:
            user.username = username
            user.email = email
            user.password = password

            db.session.commit()
            return jsonify({"success": "Profile updated successfully"})
    
    else:
        return jsonify({"error": "User does not exist!!"})
    
    


# DELETE USER
@user_bp.route("/users", methods=["DELETE"])
@jwt_required()
def delete_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"success": "Account deleted successfully"})
    
    else:
        return jsonify({"error": "The user you are trying to delete does not exist!!"})
