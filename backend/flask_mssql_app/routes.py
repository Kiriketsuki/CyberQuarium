# routes.py
from flask import Blueprint, jsonify, request, make_response
from __init__ import db
from models import User, testing

main = Blueprint('main', __name__)

@main.route('/')
def hello():
    return 'Hello, World!'

@main.route('/api/users')
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
    return jsonify({'users': user_list})

@main.route('/api/test')
def test():
    return jsonify({'message': 'Test'})

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
