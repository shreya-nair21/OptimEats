from flask import Flask, request, jsonify,Blueprint
from datetime import date
import os
from app import db 
from models import User, Business, Meal, MealClaimed, Donation

# Create a Blueprint instance for the user routes
users_blueprint = Blueprint('users', __name__)

# Define the maximum daily meals (plus dependents)
MEALS_PER_DEPENDENT = 2

# --- CRUD Operations for User ---

# CREATE (Register a New User) - Used for both regular users and initial business registration
@users_blueprint.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        new_user = User(
            # Default to regular user, will be linked to a business later for providers

            dependents=data.get('dependents', 0)
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create user', 'details': str(e)}), 400

# READ (Get a single User)
@users_blueprint.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

# UPDATE (Modify User Details, e.g., dependents)
@users_blueprint.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    try:
        if 'dependents' in data:
            user.dependents = data['dependents']
        
        db.session.commit()
        return jsonify(user.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update user', 'details': str(e)}), 400

# DELETE (Delete a User)
@users_blueprint.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    # The cascading rules defined in models should handle deletion of related records
    db.session.delete(user)
    db.session.commit()
    return '', 204

# --- MEAL CLAIMING  ---

@users_blueprint.route('/api/users/<int:user_id>/claim_meal', methods=['POST'])
def claim_meal(user_id):
    """
    Handles a user claiming a meal, checks daily limits, updates business balance, 
    and records the transaction atomically.
    """
    data = request.get_json()
    menu_id = data.get('menu_id')
    # force_claim = data.get('force_claim', False) 

    if not menu_id:
        return jsonify({"error": "Missing menu_id"}), 400

    # Start a database transaction for data integrity
    try:
        with db.session.begin_nested():
            user = User.query.get_or_404(user_id)
            menu_item = Menu.query.get_or_404(menu_id)
            business = Business.query.get_or_404(menu_item.business_id)

            # 1. ENFORCE DAILY MEAL LIMITS
            meal_cap = user.total_meals + (MEALS_PER_DEPENDENT * user.dependents)
            
            # Count meals claimed today by this user
            claimed_today = MealClaimed.query.filter_by(user_id=user_id)\
                                        .filter(db.cast(MealClaimed.timestamp, db.Date) == date.today())\
                                        .count()
            
            if claimed_today >= meal_cap:
                return jsonify({
                    "error": f"Daily meal limit reached. You (plus dependents) are limited to {meal_cap} meals.",
                    "claimed": claimed_today
                }), 403

            # 2. CHECK BUSINESS BALANCE
            meal_price = menu_item.price
            if business.balance < meal_price:
                return jsonify({
                    "error": f"Not enough balance for this meal: New Balance = {business.balance < meal_price}",
                }), 403
                # if not force_claim:
                #     # If not confirmed, ask the frontend to prompt the user
                #     new_balance = business.pay_forward_balance - meal_price
                #     return jsonify({
                #         "error": "Insufficient balance. Requires confirmation to proceed.",
                #         "current_balance": business.pay_forward_balance,
                #         "new_balance": new_balance,
                #         "confirmation_required": True
                #     }), 402 # 402 Payment Required status code
            
            # 3. EXECUTE TRANSACTION: CREATE RECORD AND UPDATE BALANCE
            
            # Create the claim record (Source Data)
            new_claim = MealClaimed(
                user_id=user_id, 
                business_id=business.id, 
                menu_id=menu_id,
                meal_price=meal_price
            )
            db.session.add(new_claim)
            
            # Update the balance (Derived Data)
            business.pay_forward_balance -= meal_price

        # Commit the main transaction
        db.session.commit()
        
        return jsonify({
            "message": "Meal claimed successfully",
            "new_balance": business.pay_forward_balance
        }), 201

    except Exception as e:
        # If any part of the transaction failed, this ensures everything is rolled back
        db.session.rollback()
        return jsonify({'error': 'Transaction failed', 'details': str(e)}), 500


donor_blueprint = Blueprint('donation', __name__)

@donor_blueprint.route('/api/donors', methods=['POST'])
def create_donor():
    data = request.get_json()
    new_donor = Donation(
        donation=data['donation'],
        user_id=data['user_id'],
        business_id = data['business_id']
    )
    db.session.add(new_donor)
    db.session.commit()
    return jsonify(new_donor.to_dict()), 201

   
# # READ all businesses
# @donor_blueprint.route('/api/donors', methods=['GET'])
# def get_donors():
#     donors = Donor.query.all()
#     return jsonify([donor.to_dict() for donor in donors])

# # READ a single business
# @donor_blueprint.route('/api/donors/<int:id>', methods=['GET'])
# def get_donor(id):
#     donor = Donor.query.get_or_404(id)
#     return jsonify(donor.to_dict())

# # UPDATE a business
# @donor_blueprint.route('/api/donors/<int:id>', methods=['PUT'])
# def update_donor(id):
#     donor = Donor.query.get_or_404(id)
#     data = request.get_json()
#     donor.name = data.get('name', donor.name)
#     donor.donation = data.get('donation', donor.donation)
#     donor.business_id = data.get('business_id', donor.business_id)
#     db.session.commit()
#     return jsonify(donor.to_dict())

