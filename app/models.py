from operator import index
from flask import current_app, session
from sqlalchemy.orm import backref
from app import db, login, app
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from flask_login import UserMixin

@login.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150),nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password=generate_password_hash(password)
    
    def is_authenticated(self):
        return True

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User: {self.username}>'


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable= False)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300))


    def __repr__(self):
        return f'<Item {self.title} {self.amount} >'



class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantity= db.Column(db.Integer, nullable=False)
    info_id = db.Column(db.Integer, db.ForeignKey('info.id'))
    usershipping = db.Column(db.Integer, db.ForeignKey('usershipping.id'))

    def __repr__(self):
        return f"Cart Item('{self.quantity}')" 

class Info(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    address = db.Column(db.String(100), nullable = False)
    country = db.Column(db.String(20), nullable = False)
    city = db.Column(db.String(50), nullable = False)
    zipcode = db.Column(db.String(100), nullable = False)
    phone = db.Column(db.String(15), nullable = False)
    cartitems = db.relationship("Cart", backref="cart", lazy = 'dynamic')
    order_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    total = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"Infor('{self.firstname}', '{self.address}','{self.phone}')"