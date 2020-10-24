from chatbot.config import Config
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
mail = Mail()

db = SQLAlchemy()
migrate = Migrate(db=db)

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    # Configurations:
    app = Flask(__name__)
    app.config.from_object(Config)

    bcrypt.init_app(app)
    mail.init_app(app)

    db.init_app(app)
    migrate.init_app(app)

    login_manager.init_app(app)

    from chatbot.errors.handlers import errors
    from chatbot.main.routes import main
    from chatbot.users.routes import users

    app.register_blueprint(errors)
    app.register_blueprint(main)
    app.register_blueprint(users)

    return app
