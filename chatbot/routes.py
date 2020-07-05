from chatbot import app
from chatbot.chatutils import response
from chatbot.forms import LoginForm, RegistrationForm
from chatbot.models import User
from flask import flash, redirect, render_template, request, url_for


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
