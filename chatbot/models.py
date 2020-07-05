from chatbot import db, login_manager
from flask_login import UserMixin

tags = db.Table('tags',
                db.Column('name', db.String(100), unique=True),
                db.Column('pattern_id', db.Integer, db.ForeignKey('pattern.id')),
                db.Column('response_id', db.Integer, db.ForeignKey('response.id')))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Pattern(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    response = db.relationship('Response', secondary=tags, backref=db.backref('tags', lazy='dynamic'))

    def __repr__(self):
        return f"Pattern('{self.id}', '{self.name}')"


class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"Pattern('{self.id}', '{self.name}')"
