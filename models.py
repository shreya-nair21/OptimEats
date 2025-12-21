from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from datetime import datetime

db = SQLAlchemy()

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    contact = db.Column(db.String(100), nullable=False) 
    address = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=True) 
    balance = db.Column(db.Float, default=0.0)
    
    # Relationships
    menu_items = db.relationship('Meal', backref='business', lazy=True)
    donations_received = db.relationship('Donation', backref='business', lazy=True)
    meals_claimed = db.relationship('MealClaimed', backref='business', lazy=True)

    def __repr__(self):
        return f'<Business {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'contact': self.contact,
            'address': self.address,
            'email': self.email,
            'balance': self.balance,
            'menu_items': [meal.to_dict() for meal in self.menu_items]
        }

class User(db.Model):
    __tablename__ = 'user' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=True) 
    phone = db.Column(db.String(20), unique=True, nullable=True)
    total_meals = db.Column(db.Integer, default=2)
    dependents = db.Column(db.Integer, default=0)

    __table_args__ = (
        CheckConstraint('total_meals <= 4 ', name='maximum_meals'),
    )
    
    donations_made = db.relationship('Donation', backref='donor', lazy=True)
    claimed_meals = db.relationship('MealClaimed', backref='claimer', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'
    
    def get_daily_meal_limit(self):
        MEALS_PER_DEPENDENT = 2
        return self.total_meals + (MEALS_PER_DEPENDENT * self.dependents)

    def to_dict(self):
        return {
            'id': self.id,
            'name' : self.name,
            'email' : self.email,
            'phone' : self.phone,
            'total_meals' : self.total_meals,
            'daily_limit' : self.get_daily_meal_limit(),
            'dependents': self.dependents
        }

Users = User 

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) 
    donor_name = db.Column(db.String(100), nullable=False) 
    amount = db.Column(db.Float, default=0.0)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Donation ${self.amount} to Business {self.business_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'donor_name': self.donor_name,
            'amount': self.amount,
            'business_id': self.business_id,
            'timestamp': self.timestamp.isoformat()
        }

class MealClaimed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('meal.id'), nullable=False) 
    meal_price = db.Column(db.Float, nullable=False) 
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    
    def __repr__(self):
        return f'<MealClaimed ID: {self.id} User: {self.user_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'business_id': self.business_id,
            'menu_id': self.menu_id,
            'meal_price': self.meal_price,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
    
class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=True)
    available = db.Column(db.Boolean, default=True) 
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<Meal {self.name} - ${self.price}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'available': self.available,
            'business_id': self.business_id,
            'image_url': self.image_url
        }
