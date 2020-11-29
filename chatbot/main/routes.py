from chatbot.chatutils import generate_response
from flask import Blueprint, render_template, request

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def index():
    return render_template('index.html', title='Home')


# Function for the bot response
@main.route('/get-response')
def get_response():
    return generate_response(request.args.get('msg'))
