# routes.py
from flask import Blueprint, jsonify, request, make_response
from flask_jwt import jwt_required
from . import db
from .models import User, Animal, Egg, MarketListing
import re
from .animals import Animal as AnimalClass
from .animals import Egg as EggClass
from .animals import Breeder as BreederClass
import time
from .name_merger import merge_words
import uuid
import hashlib

main = Blueprint('main', __name__)

# route to view all users and all info


@main.route('/api/users')
def view_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username, 'email': user.email,
                  'password': user.password, "coin": user.coins} for user in users]
    return jsonify({'users': user_list})


@main.route("/api/listings")
def view_listings():
    listings = MarketListing.query.all()
    listing_list = [{'id': listing.id, 'item_id': listing.item_id,
                     'price': listing.price, 'username': listing.username} for listing in listings]
    return jsonify({'listings': listing_list})


@main.route('/register', methods=['POST'])
def register():
    user_credentials = request.get_json()

    email = user_credentials.get('email')
    password = user_credentials.get('password')
    confirmPassword = user_credentials.get('confirmPassword')

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
        response = {"status": "error",
                    "message": "User with this email address already exists."}
        return jsonify(response)

    # Perform user registration logic here
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    new_user = User(username=email.split(
        '@')[0], email=email, password=hashed_password)
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

    if not is_strong_password(password):
        response = {
            "status": "error",
            "message": "Try logging in with Google instead.",
        }
        return jsonify(response)

    # Check if user exists in the database and password matches
    user = User.query.filter_by(email=email).first()
    if user and user.password == hashlib.sha256(password.encode()).hexdigest():
        # Check if user has an active session stored in the database
        print(user.session_id == None)

        # Create a new session for the user
        session_id = generate_session_id()
        user.session_id = session_id
        db.session.commit()
        response = {"status": "success",
                    "message": "User logged in successfully.", "sessionID": session_id}
        return jsonify(response)
    else:
        response = {"status": "error", "message": "Invalid email or password."}
        return jsonify(response)


@main.route('/google', methods=['POST'])
def google():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')

    # Check if user exists in the database
    user = User.query.filter_by(email=email).first()
    if user:
        session_id = generate_session_id()
        user.session_id = session_id
        db.session.commit()
        response = {"status": "success",
                    "message": "User logged in successfully.", "sessionID": session_id}
        return jsonify(response)
    else:
        new_user = User(username=username, email=email)
        session_id = generate_session_id()
        new_user.session_id = session_id
        db.session.add(new_user)
        db.session.commit()
        response = {"status": "success",
                    "message": "User logged in successfully.", "sessionID": session_id}
        return jsonify(response)


@main.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    username = data.get('username')
    user = User.query.filter_by(username=username).first()
    if user:
        user.session_id = None
        db.session.commit()
        response = {"status": "success",
                    "message": "User logged out successfully."}
        return jsonify(response)
    else:
        response = {"status": "error", "message": "User not found."}
        return jsonify(response)

# Create an API endpoint which receives a username and sessionid and checks if the session is valid


@main.route('/api/session', methods=['POST'])
@jwt_required()
def check_session():
    data = request.get_json()
    username = data.get('username')
    sessionID = data.get('sessionid')
    if sessionID == None:
        response = {"status": "error", "message": "Session is invalid."}
        return jsonify(response)
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
@jwt_required()
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
@jwt_required()
def create_egg():
    egg = EggClass()
    return jsonify({"rarity": egg.get_rarity(), "cost": egg.get_cost()})


@main.route('/api/buy_egg/<string:username>', methods=['POST'])
@jwt_required()
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


@main.route('/api/buy_listing/<string:username>', methods=['POST'])
@jwt_required()
def buy_listing(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    listing_data = request.get_json()

    if user.coins < listing_data['price']:
        return jsonify({"error": "Insufficient coins"}), 400

    # Subtract listing cost from user's coins
    user.coins -= listing_data['price']

    # Checl if egg or animal
    if listing_data['item_type'] == 'egg':
        item = Egg.query.filter_by(id=listing_data['item_id']).first()
    else:
        item = Animal.query.filter_by(id=listing_data['item_id']).first()

    if not item:
        return jsonify({"error": "Item not found"}), 404

    # Add listing cost to seller's coins
    seller = User.query.filter_by(id=listing_data['user_id']).first()
    seller.coins += listing_data['price']

    # Transfer item to buyer
    item.user_id = user.id

    if listing_data['item_type'] == 'egg':
        item.owner.eggs.remove(item)
        user.eggs.append(item)
    else:
        item.owner.animals.remove(item)
        user.animals.append(item)

    # Change listing status to sold
    listing = MarketListing.query.filter_by(id=listing_data['id']).first()
    listing.sold = True
    listing.status = 'Sold'
    # Commit changes to database
    db.session.commit()

    return jsonify(user.to_dict()), 200


@main.route('/api/user/<string:username>/eggs', methods=['GET'])
@jwt_required()
def get_eggs(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    eggs = [egg.to_dict() for egg in user.eggs]
    return jsonify(eggs), 200


@main.route('/api/user/<string:username>/animals', methods=['GET'])
@jwt_required()
def get_animals(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    animals = [animal.to_dict() for animal in user.animals]
    return jsonify(animals), 200


@main.route('/hatch', methods=['POST'])
@jwt_required()
def hatch():
    data = request.get_json()
    print(data)
    user = User.query.filter_by(username=data['user']['username']).first()
    egg = Egg.query.filter_by(id=data['egg']['id']).first()

    egg_rarity = egg.rarity
    egg_cost = egg.cost

    al_egg = EggClass(egg_rarity, egg_cost)
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


@main.route('/api/update_coins')
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
        breeder = BreederClass("breeder")
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


@main.route("/api/market_listing", methods=["POST"])
@jwt_required()
def list_on_market():
    data = request.get_json()
    user_id = data.get('user_id')
    username = User.query.filter_by(id=user_id).first().username
    item_id = data.get('item_id')
    listing_name = data.get('listing_name')
    item_type = data.get('item_type')
    price = data.get('price')

    if item_type == 'egg':
        item = Egg.query.filter_by(id=item_id, user_id=user_id).first()
    elif item_type == 'animal':
        item = Animal.query.filter_by(id=item_id, user_id=user_id).first()

    if not item:
        response = {"status": "error",
                    "message": "Item does not belong to user."}
        return jsonify(response)

    # Change the owner of the item to the escrow user
    escrow_user = User.query.filter_by(id=1).first()
    if item_type == 'egg':
        item.user_id = 1
        item.owner.eggs.remove(item)
        escrow_user.eggs.append(item)
        image = "https://ichef.bbci.co.uk/news/976/cpsprodpb/7614/production/_105482203__105172250_gettyimages-857294664.jpg"
        name = "Egg"
        yield_rate = 0
    elif item_type == 'animal':
        item.user_id = 1
        item.owner.animals.remove(item)
        escrow_user.animals.append(item)
        image = item.image_url
        name = item.name
        yield_rate = item.coin_yield

    rarity = item.rarity

    new_listing = MarketListing(
        user_id=user_id,
        username=username,
        image=image,
        name=name,
        item_id=item_id,
        listing_name=listing_name,
        item_type=item_type,
        price=price,
        rarity=rarity,
        yield_rate=yield_rate,
        status="Listed"
    )

    db.session.add(new_listing)
    db.session.commit()

    response = {"status": "success", "message": "Item listed on market."}
    return jsonify(response)


@main.route("/api/listings", methods=["GET"])
@jwt_required()
def get_listings():
    listings = MarketListing.query.all()
    listings = [listing.to_dict() for listing in listings]
    return jsonify(listings)


@main.route("/api/user_listings", methods=["POST"])
@jwt_required()
def get_user_listings():
    data = request.get_json()
    username = data.get('username')
    user = User.query.filter_by(username=username).first()
    if user:
        listings = MarketListing.query.filter_by(username=username).all()
        listings = [listing.to_dict() for listing in listings]
        return jsonify(listings)
    else:
        return jsonify({"status": "error", "message": "User not found."})


@main.route("/api/update_listing", methods=["POST"])
@jwt_required()
def update_listing():
    data = request.get_json()
    listing_id = data.get('id')
    listing_name = data.get('listing_name')
    price = data.get('price')

    listing = MarketListing.query.filter_by(id=listing_id).first()
    if listing:
        listing.listing_name = listing_name
        listing.price = price
        db.session.commit()
        return jsonify({"status": "success", "message": "Listing updated."})
    else:
        return jsonify({"status": "error", "message": "Listing not found."})


@main.route("/api/cancel_listing", methods=["POST"])
@jwt_required()
def cancel_listing():
    data = request.get_json()
    listing_id = data.get('id')
    user_id = data.get('user_id')
    listing = MarketListing.query.filter_by(id=listing_id).first()
    user = User.query.filter_by(id=user_id).first()

    if not listing:
        return jsonify({"status": "error", "message": "Listing not found."})

    if not user:
        return jsonify({"status": "error", "message": "User not found."})

    if listing.user_id != user_id:
        return jsonify({"status": "error", "message": "User does not own listing."})

    item_type = listing.item_type
    if item_type == 'egg':
        item = Egg.query.filter_by(id=listing.item_id).first()
    else:
        item = Animal.query.filter_by(id=listing.item_id).first()

    if item_type == 'egg':
        item.user_id = user_id
        item.owner.eggs.remove(item)
        user.eggs.append(item)
    elif item_type == 'animal':
        item.user_id = user_id
        item.owner.animals.remove(item)
        user.animals.append(item)

    listing.status = 'Cancelled'

    db.session.commit()
    return jsonify({"status": "success", "message": "Listing cancelled."})


@main.route("/api/animal", methods=["POST"])
@jwt_required()
def get_animal():
    data = request.get_json()
    animal_id = data.get('animal_id')
    animal = Animal.query.filter_by(id=animal_id).first()
    # find owner username
    username = User.query.filter_by(id=animal.user_id).first().username

    if animal:
        dict = animal.to_dict()
        dict['username'] = username
        return jsonify(dict)
    else:
        return jsonify({"status": "error", "message": "Animal not found."})


@main.route("/api/update_nickname", methods=["POST"])
@jwt_required()
def update_nickname():
    data = request.get_json()
    animal_id = data.get('animal_id')
    nickname = data.get('nickname')
    animal = Animal.query.filter_by(id=animal_id).first()
    if animal:
        animal.nickname = nickname
        db.session.commit()
        return jsonify({"status": "success", "message": "Nickname updated."})
    else:
        return jsonify({"status": "error", "message": "Animal not found."})

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
    animal = AnimalClass(rarity, species, name, coin_yield)
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
