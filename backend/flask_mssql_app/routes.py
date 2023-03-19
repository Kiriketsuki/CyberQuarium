# routes.py
from flask import Blueprint, jsonify, request, make_response
from __init__ import db
from models import User, Animal, Egg
import re
import classes as animal_logic
import time
from apscheduler.schedulers.background import BackgroundScheduler
from name_merger import merge_words
import config
import uuid
import hashlib

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
    session_id = generate_session_id()
    new_user.session_id = session_id
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
        # Check if user has an active session stored in the database
        print(user.session_id == None)

        # Create a new session for the user
        session_id = generate_session_id()
        user.session_id = session_id
        db.session.commit()
        response = {"status": "success", "message": "User logged in successfully.", "sessionID": session_id}
        return jsonify(response)
    else:
        response = {"status": "error", "message": "Invalid email or password."}
        return jsonify(response)
    
# Create an API endpoint which receives a username and sessionid and checks if the session is valid
@main.route('/api/session', methods=['POST'])
def check_session():
    data = request.get_json()
    username = data.get('username')
    sessionID = data.get('sessionid')
    print(sessionID)
    # Check if user exists in the database
    user = User.query.filter_by(username=username).first()
    if user:
        # Check if session ID matches the one stored in the database
        print(user.session_id)
        if user.session_id == sessionID:
            response = {"status": "success", "message": "Session is valid."}
            return jsonify(response)
        
    response = {"status": "error", "message": "Session is invalid."}
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
    egg = animal_logic.Egg()
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

@main.route('/api/user/<string:username>/eggs', methods=['GET'])
def get_eggs(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    eggs = [egg.to_dict() for egg in user.eggs]
    return jsonify(eggs), 200

@main.route('/api/user/<string:username>/animals', methods=['GET'])
def get_animals(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    animals = [animal.to_dict() for animal in user.animals]
    return jsonify(animals), 200

@main.route('/hatch', methods=['POST'])
def hatch():
    data = request.get_json()
    print(data)
    user = User.query.filter_by(username=data['user']['username']).first()
    egg = Egg.query.filter_by(id=data['egg']['id']).first()

    egg_rarity = egg.rarity
    egg_cost = egg.cost

    al_egg = animal_logic.Egg(egg_rarity, egg_cost)
    animal = al_egg.hatch()

    if not user or not egg:
        return jsonify({"error": "User or egg not found"}), 404

    
    # Delete the egg and add the new animal to the database
    db.session.delete(egg)
    animal = animal_class_to_model(animal, user.id)
    db.session.add(animal)
    db.session.commit()

    # Return the animal's information
    return jsonify(animal.to_dict()), 200


@main.route('/api/update-coins')
def update_coins():
    current_time = time.time()
    animals = Animal.query.all()
    
    for animal in animals:
        elapsed_time = current_time - animal.dob
        elapsed_minutes = elapsed_time // 60
        animal.coins_yielded = elapsed_minutes * animal.coin_yield / 60
        db.session.commit()
    
    return {'status': 'success'}, 200

@main.route('/api/burn_animal', methods=['POST'])
def burn_animal():
    get_coin_update()
    data = request.json
    animal_id = data['animal_id']
    user_id = data['user_id']

    # Find the animal in question
    animal = Animal.query.filter_by(id=animal_id, user_id=user_id).first()

    if animal:
        # Find the user
        user = User.query.filter_by(id=user_id).first()
        yielded = 0
        if user:
            # Add the amount of coins yielded to the coin total of the user
            user.coins += animal.coins_yielded
            yielded = animal.coins_yielded
            # Remove the animal from the database
            db.session.delete(animal)
            db.session.commit()

            return jsonify({'status': 'success', 'message': f'Animal burned successfully. You have gained {yielded} coins, and have a total of {user.coins}'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'User not found.'}), 404
    else:
        return jsonify({'status': 'error', 'message': 'Animal not found.'}), 404

@main.route('/api/breed_animals', methods=['POST'])
def breed_animals():
    animal_id_1 = request.json.get('animal_id_1')
    animal_id_2 = request.json.get('animal_id_2')
    user_id = request.json.get('user_id')

    # Retrieve the animals from the database
    animal1 = Animal.query.get(animal_id_1)
    animal2 = Animal.query.get(animal_id_2)

    if animal1 and animal2:
        animal_1 = animal_model_to_class(animal1)
        animal_2 = animal_model_to_class(animal2)

        new_name = merge_words(animal_1.name, animal_2.name)

        # Breed the animals
        breeder = animal_logic.Breeder("breeder")
        breeder.add_animal(animal_1)
        breeder.add_animal(animal_2)
        new_animal = breeder.breed(animal1.id, animal2.id)

        # Add the new animal to the database
        new_animal = animal_class_to_model(new_animal, user_id)
        new_animal.name = new_name
        db.session.add(new_animal)

        # Remove the old animals from the database
        db.session.delete(animal1)
        db.session.delete(animal2)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Animals bred successfully', 'animal': new_animal.to_dict()}), 200
    else:
        return jsonify({'status': 'error', 'message': 'One or more animals not found.'}), 404

# ?? helper functions

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

def is_strong_password(password):
    # At least 8 characters, with uppercase, lowercase, digit, and special character
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(password_regex, password)

def animal_class_to_model(animal_class, user_id):
    return Animal(
        dob=animal_class.dob,
        image_url=animal_class.get_image(),
        rarity=animal_class.get_rarity(),
        species=animal_class.get_species(),
        name=animal_class.get_name(),
        coin_yield=animal_class.get_yield(),
        coins_yielded=animal_class.coins_yielded,
        user_id=user_id,
    )

def animal_model_to_class(animal_model):
    return create_animal(
        animal_model.id,
        animal_model.dob,
        animal_model.rarity,
        animal_model.species,
        animal_model.name,
        animal_model.coin_yield,
        animal_model.coins_yielded,
    )

def create_animal(id, dob, rarity, species, name, coin_yield, coins_yielded):
    animal = animal_logic.Animal(rarity, species, name, coin_yield)
    animal.id = id
    animal.dob = dob
    animal.coins_yielded = coins_yielded
    return animal


def get_coin_update():
    current_time = time.time()
    animals = Animal.query.all()
    
    for animal in animals:
        elapsed_time = current_time - animal.dob
        elapsed_minutes = elapsed_time // 60
        animal.coins_yielded = elapsed_minutes * animal.coin_yield / 60
        db.session.commit()


def generate_session_id():
    """
    Generate a secure and unique session ID
    """
    # Generate a random UUID as the session ID
    session_id = str(uuid.uuid4())
    
    # Generate a hash of the session ID using SHA-256 for added security
    hash_object = hashlib.sha256(session_id.encode())
    hash_hex = hash_object.hexdigest()
    
    # Return the hashed session ID
    return hash_hex

scheduler = BackgroundScheduler()
scheduler.add_job(func=update_coins, trigger="interval", minutes=5)
scheduler.start()