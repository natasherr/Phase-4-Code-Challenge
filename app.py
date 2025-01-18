from flask import Flask, render_template, request
from flask_migrate import Migrate
from models import db, User, Book, Genre

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
migrate = Migrate(app, db)
db.init_app(app)

