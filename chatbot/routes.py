from chatbot import app, db, bcrypt
from chatbot.chatutils import response
from chatbot.forms import LoginForm, RegistrationForm
from chatbot.models import User
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, login_required, logout_user
import logging

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')


# Function for the bot response
@app.route('/get-response')
def get_response():
    return response(request.args.get('msg'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash('Login successful', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Profile')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account has been successfully created. You are now able to log in', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', title='Register', form=form)
