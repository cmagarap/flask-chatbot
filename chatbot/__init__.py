from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


# Configurations:
app = Flask(__name__)
app.config['SECRET_KEY'] = '15e0aecb49502bfb7c15d17e2a79509a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from chatbot import routes