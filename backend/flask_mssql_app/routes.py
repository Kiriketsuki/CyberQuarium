# routes.py
from flask import Blueprint, jsonify, request, make_response
from __init__ import db
from models import User, Animal, Egg
import re
import classes

main = Blueprint('main', __name__)

@main.route('/')
def hello():
    return 'Hello, World!'

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

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    # Check if user exists in the database and password matches
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        response = {"status": "success", "message": "User logged in successfully."}
        return jsonify(response)
    else:
        response = {"status": "error", "message": "Invalid email or password."}
        return jsonify(response)
    

@main.route('/api/user/<username>', methods=['GET'])
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'coins': user.coins
        })
    else:
        return jsonify({
            'error': 'User not found'
        }), 404


@main.route('/api/create_egg')
def create_egg():
    egg = classes.Egg()
    return jsonify({"rarity": egg.get_rarity(), "cost": egg.get_cost()})

@main.route('/api/buy_egg/<string:username>', methods=['POST'])
def buy_egg(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    egg_data = request.get_json()

    if user.coins < egg_data['cost']:
        return jsonify({"error": "Insufficient coins"}), 400

    # Subtract egg cost from user's coins
    user.coins -= egg_data['cost']

    # Create a new egg in the database
    new_egg = Egg(
        rarity=egg_data['rarity'],
        cost=egg_data['cost'],
        user_id=user.id
    )

    db.session.add(new_egg)
    db.session.commit()

    return jsonify(user.to_dict()), 200

# routes.py
@main.route('/api/user/<string:username>/eggs', methods=['GET'])
def get_eggs(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    eggs = [egg.to_dict() for egg in user.eggs]
    return jsonify(eggs), 200



# ?? helper functions

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

def is_strong_password(password):
    # At least 8 characters, with uppercase, lowercase, digit, and special character
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(password_regex, password)