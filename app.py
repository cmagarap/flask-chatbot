from chatutils import response
from flask import flash, Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegistrationForm

# Configurations:
app = Flask(__name__)
app.config['SECRET_KEY'] = '15e0aecb49502bfb7c15d17e2a79509a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
db = SQLAlchemy(app)


# App routes:
@app.route("/")
def index():
    return render_template('index.html')


# Function for the bot response
@app.route("/get-response")
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


if __name__ == "__main__":
    app.run(debug=True)
