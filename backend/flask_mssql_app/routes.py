# routes.py
from flask import Blueprint, jsonify, request, make_response
from __init__ import db
from models import User, testing
import re

main = Blueprint('main', __name__)

@main.route('/')
def hello():
    return 'Hello, World!'

@main.route('/api/testing', methods=['POST'])
def post_testing():
    data = request.get_json()
    new_testing = testing(message=data['message'])
    db.session.add(new_testing)
    db.session.commit()
    return jsonify({'message': 'New user created'})

@main.route("/api/view_testings")
def view_testings():
    testings = testing.query.all()
    testing_list = [{'id': testing.id, 'message': testing.message} for testing in testings]
    return jsonify({'testings': testing_list})

# route to view all users and all info
@main.route('/api/view_users')
def view_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username, 'email': user.email, 'password': user.password} for user in users]
    return jsonify({'users': user_list})

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    confirmPassword = data.get('confirmPassword')

    if not is_valid_email(email):
        response = {"status": "error", "message": "Invalid email address."}
        return jsonify(response)

    if not is_strong_password(password):
        response = {
            "status": "error",
            "message": "Password must be at least 8 characters long, with at least one uppercase letter, one lowercase letter, one digit, and one special character.",
        }
        return jsonify(response)

    if password != confirmPassword:
        response = {"status": "error", "message": "Passwords do not match."}
        return jsonify(response)

    # Check if user already exists in the database
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        response = {"status": "error", "message": "User with this email address already exists."}
        return jsonify(response)

    # Perform user registration logic here
    new_user = User(username=email.split('@')[0], email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    message = "User registered successfully."
    response = {"status": "success", "message": message}
    return jsonify(response)


# ?? helper functions

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

def is_strong_password(password):
    # At least 8 characters, with uppercase, lowercase, digit, and special character
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(password_regex, password)