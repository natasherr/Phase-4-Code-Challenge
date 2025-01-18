from models import db, Book
from flask import Blueprint, jsonify, request

book_bp = Blueprint("book_bp", __name__)