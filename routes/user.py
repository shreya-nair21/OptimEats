from flask import Blueprint, request, jsonify
from datetime import date, datetime, time
from sqlalchemy import func
from models import db, User, Business, Meal, MealClaimed, Donation, SystemConfig, MEALS_PER_DEPENDENT

# Create a Blueprint instance for the user routes
user_blueprint = Blueprint('user', __name__)

# MEALS_PER_DEPENDENT is now improved if imported or defined here. 
# It was defined in class method before, but good to have as constant or from config
MEALS_PER_DEPENDENT = 2

# --- CRUD Operations for User ---

# CREATE (Register a New User)
@user_blueprint.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        # Basic validation
        if not data.get('name') or not data.get('email'):
             return jsonify({'error': 'Name and email are required'}), 400

        new_user = User(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone'),
            dependents=data.get('dependents', 0),
            password= data.get('password') 
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create user', 'details': str(e)}), 400

# READ (Get a single User)
@user_blueprint.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

# UPDATE (Modify User Details, e.g., dependents)
@user_blueprint.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    try:
        if 'dependents' in data:
            user.dependents = data['dependents']
        if 'phone' in data:
            user.phone = data['phone']
        
        db.session.commit()
        return jsonify(user.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update user', 'details': str(e)}), 400

# DELETE (Delete a User)
@user_blueprint.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return '', 204

# --- MEAL CLAIMING  ---

def check_emergency_mode():
    config = SystemConfig.query.filter_by(key='emergency_mode').first()
    return config and config.value.lower() == 'true'

@user_blueprint.route('/api/users/<int:user_id>/claim_meal', methods=['POST'])
def claim_meal(user_id):
    """
    Handles a user claiming a meal, checks daily limits, updates business balance, 
    and records the transaction atomically.
    """
    data = request.get_json()
    menu_id = data.get('menu_id')

    if not menu_id:
        return jsonify({"error": "Missing menu_id"}), 400

    try:
        user = User.query.get_or_404(user_id)
        
        is_emergency = check_emergency_mode()

        if is_emergency:
            meal_cap = (user.total_meals + (MEALS_PER_DEPENDENT * user.dependents)) * 2
        else:
            meal_cap = (user.total_meals + (MEALS_PER_DEPENDENT * user.dependents))

        with db.session.begin_nested(): 
            meal_item = Meal.query.get_or_404(menu_id) 
            business = Business.query.get_or_404(meal_item.business_id)

            # Count meals claimed today by this user
            today_start = datetime.combine(date.today(), time.min)
            claimed_today = MealClaimed.query.filter_by(user_id=user_id)\
                                        .filter(MealClaimed.timestamp >= today_start)\
                                        .count()
            
            if claimed_today >= meal_cap:
                return jsonify({
                    "error": f"Daily meal limit reached. You (plus dependents) are limited to {meal_cap} meals.",
                    "claimed": claimed_today
                }), 403

            # 2. CHECK BUSINESS BALANCE
            meal_price = meal_item.price
            if business.balance < meal_price:
                 return jsonify({
                    "error": "Business has insufficient balance.",
                    "business_balance": business.balance
                }), 403
            
            # 3. EXECUTE TRANSACTION
            new_claim = MealClaimed(
                user_id=user_id, 
                business_id=business.id, 
                menu_id=menu_id,
                meal_price=meal_price
            )
            db.session.add(new_claim)
            
            business.balance -= meal_price

        db.session.commit()
        
        return jsonify({
            "message": "Meal claimed successfully",
            "new_balance": business.balance
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Transaction failed', 'details': str(e)}), 500

# --- USER & DONOR HISTORY ---

@user_blueprint.route('/api/users/<int:user_id>/history', methods=['GET'])
def get_user_history(user_id):
    user = User.query.get_or_404(user_id)
    donations = Donation.query.filter_by(user_id=user_id).order_by(Donation.timestamp.desc()).all()
    claims = MealClaimed.query.filter_by(user_id=user_id).order_by(MealClaimed.timestamp.desc()).all()

    return jsonify({
        'user': user.name,
        'role': user.role,
        'donations': [d.to_dict() for d in donations],
        'claimed_meals': [c.to_dict() for c in claims]
    })
