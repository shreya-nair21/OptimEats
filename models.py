from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.0)
    menu_items = db.relationship('Meal', backref='business', lazy=True)

    def __repr__(self):
        return f'<Business {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'menu_items': self.menu_items,
            'balance': self.balance
        }

class Users(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column (db.String(100), unique= True, nullable=False)
    total_meals = db.Column (db.Integer)
    __table_args__ = (
    CheckConstraint('total_meals <= 4 ', name='maximum_meals'),
    )
    dependants = db.Column (db.Integer)
    claimed_meals = db.relationship('MealClaimed', backref='claimer', lazy=True)
    # meal_collect = db.Column (db.String(100), unique= True, nullable=False)
    def to_dict(self):
        return {
            'id': self.id,
            'dependents': self.dependents
        }

class Donation(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    donation = db.Column(db.Float, default=0.0)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)

    def to_dict(self):
        return {
            'user_id': self.id,
            'name': self.name,
            'donation': self.donation,
            'business_id': self.business_id
        }


class MealClaimed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    
    def __repr__(self):
        return f'<MealClaimed ID: {self.id}>'
    
class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)