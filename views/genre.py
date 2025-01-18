from models import db, Genre
from flask import Blueprint, jsonify, request


genre_bp = Blueprint("genre_bp", __name__)