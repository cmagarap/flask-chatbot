from chatbot import app, bcrypt, db, mail
from chatbot.chatutils import response
from chatbot.forms import LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm
from chatbot.models import User
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, login_required, logout_user
from flask_mail import Message
import logging
import os

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


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, click the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email and no changes will be made.
    '''
    
    mail.send(msg)


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RequestResetForm()
    app.logger.info(f"'email {os.environ.get('EMAIL_USER')}'")
    app.logger.info(f"'password {os.environ.get('EMAIL_PASS')}'")
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))

    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated. You are now able to log in', 'success')
        return redirect(url_for('index'))
    return render_template('reset_password.html', titl='Reset Password', form=form)
