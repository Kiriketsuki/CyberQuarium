# models.py
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(80), unique=False, nullable=True)
    coins = db.Column(db.Float, default=100)
    session_id = db.Column(db.String(80), unique=True, nullable=True)

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
    image_url = db.Column(db.String, nullable=False)
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
            'image_url': self.image_url,
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
    
class MarketListing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    listing_name = db.Column(db.String(255), nullable=False)
    item_type = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    rarity = db.Column(db.String(255), nullable=False)
    yield_rate = db.Column(db.Float, nullable=True)
    sold = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<MarketListing {self.listing_name}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'item_id': self.item_id,
            'listing_name': self.listing_name,
            'item_type': self.item_type,
            'price': self.price,
            'name': self.name,
            'image': self.image,
            'rarity': self.rarity,
            'yield_rate': self.yield_rate,
            'sold': self.sold
        }