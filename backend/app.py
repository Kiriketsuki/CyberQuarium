from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from classes import Egg, Breeder

app = Flask(__name__)
cors = CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "Flask server is currently running on localhost:5000."


@app.route('/login', methods=['POST'])
def login():
    try:
        client = request.json
        client_username, client_password = client['username'], client['password']

        # Add Auth Logic

        return_json = {"success": True}

        return json.dumps(return_json), 200, {'Content-Type':'application/json'}
    
    except Exception as err:
        return jsonify({'error': err}), 500
    

@app.route('/signup', methods=['POST'])
def signup():
    try:
        new_client = request.json
        new_client_username, new_client_password = new_client['username'], new_client['password']

        # Add Auth Logic

        return_json = {"success": True}

        return json.dumps(return_json), 200, {'Content-Type':'application/json'}
    
    except Exception as err:
        return jsonify({'error': err}), 500
    

@app.route('/obtain-egg', methods=['POST'])
def obtain_egg():
    try:
        new_egg = Egg()

        return_json = {}

        return json.dumps(return_json), 200, {'Content-Type':'application/json'}
    
    except Exception as err:
        return jsonify({'error': err}), 500
    

@app.route('/hatch-egg', methods=['POST'])
def hatch_egg():
    try:
        target_egg = request.json
        egg_name = target_egg['name']

        # Find egg_name in db

        animal = egg.hatch()

        return_json = {}

        return json.dumps(return_json), 200, {'Content-Type':'application/json'}
    
    except Exception as err:
        return jsonify({'error': err}), 500
    

@app.route('/burn', methods=['POST'])
def burn():
    try:
        return_json = {}

        return json.dumps(return_json), 200, {'Content-Type':'application/json'}
    
    except Exception as err:
        return jsonify({'error': err}), 500
    

@app.route('/breed', methods=['POST'])
def breed():
    try:
        return_json = {}

        return json.dumps(return_json), 200, {'Content-Type':'application/json'}
    
    except Exception as err:
        return jsonify({'error': err}), 500