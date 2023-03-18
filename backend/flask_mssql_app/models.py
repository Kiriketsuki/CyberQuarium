# models.py
from __init__ import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    coins = db.Column(db.Float, default=100)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'coins': self.coins
        }

    # Relationships
    animals = db.relationship('Animal', backref='owner', lazy=True)
    eggs = db.relationship('Egg', backref='owner', lazy=True)

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dob = db.Column(db.Float, nullable=False)
    rarity = db.Column(db.String, nullable=False)
    species = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    coin_yield = db.Column(db.Float, nullable=False)
    coins_yielded = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'dob': self.dob,
            'rarity': self.rarity,
            'species': self.species,
            'name': self.name,
            'coin_yield': self.coin_yield,
            'coins_yielded': self.coins_yielded
        }

class Egg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rarity = db.Column(db.String, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'rarity': self.rarity,
            'cost': self.cost
        }