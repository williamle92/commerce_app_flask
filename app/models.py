from operator import index
from app import db, login
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from flask_login import UserMixin

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150),nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    cart = db.relationship('Cart', backref='author', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password=generate_password_hash(password)
    

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User: {self.username}>'


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable= False)
    title = db.Column(db.String(50))
    description = db.Column(db.String(300))
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)

    def __init__(self, amount, title, description, user_id):
        self.amount = amount
        self.title = title
        self.description = description
        self.user_id = user_id

    def __repr__(self):
        return '<item {}>'.format(self.firstname)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)