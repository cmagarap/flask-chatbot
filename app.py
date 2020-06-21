from chatutils import response
from flask import flash, Flask, redirect, render_template, request, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegistrationForm

# Configurations:
app = Flask(__name__)
app.config['SECRET_KEY'] = '15e0aecb49502bfb7c15d17e2a79509a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

tags = db.Table('tags',
                db.Column('name', db.String(100), unique=True),
                db.Column('pattern_id', db.Integer, db.ForeignKey('pattern.id')),
                db.Column('response_id', db.Integer, db.ForeignKey('response.id')))

class User(db.Model):
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


class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Label('{self.id}' ,'{self.name}')"


# App routes:
@app.route('/')
def index():
    return render_template('index.html')


# Function for the bot response
@app.route('/get-response')
def get_response():
    return response(request.args.get('msg'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login successful', 'success')
        return redirect(url_for('index'))

    return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account has been successfully created.', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', title='Register', form=form)


if __name__ == '__main__':
    app.run(debug=True)
