from flask import Flask, render_template, request
from flask_migrate import Migrate
from models import db, User, Book, Genre
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
migrate = Migrate(app, db)
db.init_app(app)

# JWT
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

jwt = JWTManager(app)
# Initializing the jwt
jwt.init_app(app)



# Import all functions in the views folder
from views import *

app.register_blueprint(user_bp)
app.register_blueprint(genre_bp)
app.register_blueprint(book_bp)