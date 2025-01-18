from models import db, User
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash

user_bp = Blueprint("user_bp", __name__)
