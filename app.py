from flask import Flask, render_template, request
from flask_migrate import Migrate
from models import db, TokenBlocklist
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
migrate = Migrate(app, db)
db.init_app(app)



# Sending an email
# Flask mail configuration
app.config["MAIL_SERVER"]= 'smtp.gmail.com'
app.config["MAIL_PORT"]=587
app.config["MAIL_USE_TLS"]=True
app.config["MAIL_USE_SSL"]=False
app.config["MAIL_USERNAME"]="ashley.testingmoringa@gmail.com"
app.config["MAIL_PASSWORD"]= 'grst jjck zwug sbiz'
app.config["MAIL_DEFAULT_SENDER"]="ashley.testingmoringa@gmail.com"

mail = Mail(app)

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
app.register_blueprint(auth_bp)

# Callback function to check if a JWT exists in the database blocklist
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None

