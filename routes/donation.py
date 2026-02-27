from flask import Blueprint, request, jsonify, session
from sqlalchemy import func, desc
from models import db, Donation, Business, User, Meal, MealClaimed
from utils.decorators import donor_required

donations_blueprint = Blueprint('donations', __name__)

# --- DONATION TRANSACTION ---

@donations_blueprint.route('/api/donations', methods=['POST'])
@donor_required
def handle_donation():
    """
    Handles a monetary donation transaction.
    1. Creates a Donation record.
    2. Atomically updates the target Business's balance.
    """
    data = request.get_json()
    
    # Required parameters
    donor_name = data.get('donor_name') or data.get('donorName')
    amount = data.get('amount') or data.get('donation')
    donation_type = data.get('type', 'money')
    business_id = data.get('business_id')
    user_id = data.get('user_id') # Optional

    meal = None
    if donation_type == 'food':
        meal_id = data.get('meal_id')
        quantity = int(data.get('quantity', 1))

        if meal_id:
             meal = Meal.query.get_or_404(meal_id)
             # Recalculate or override amount for food donation
             total_value = meal.price * quantity
             amount = total_value
        else:
             # Generic food donation without a specific meal attached
             amount = 0
    
    if donation_type == 'clothes':
        quantity = int(data.get('quantity', 1))
        amount = 0 # Clothes donations track quantity, not monetary value on balance
        
    
    if not donor_name:
         return jsonify({"error": "Missing required field: donor_name"}), 400

    try:
        amount = float(amount)
        if amount < 0:
            return jsonify({'error': 'Donation amount must be positive.'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid amount format'}), 400
        
    try:
        
        if not business_id:
             first_business = Business.query.first()
             if first_business:
                 business_id = first_business.id
             else:
                 return jsonify({'error': 'No businesses registered to receive donations.'}), 404

        business = Business.query.get(business_id)
        if not business:
            return jsonify({'error': 'Target business not found.'}), 404

        # Create Donation record
        new_donation = Donation(
            user_id=user_id,
            donor_name=donor_name,
            business_id=business_id,
            amount=amount,
            type=donation_type,
            meal_id=meal.id if meal else None,
            quantity=quantity if donation_type in ['food', 'clothes'] else 1
        )
        db.session.add(new_donation)

        # Update business balance (only adds value if amount > 0, e.g. money or valued food)
        business.balance += amount

        db.session.commit()
    
        return jsonify({
            "message": "Donation recorded and balance updated successfully.",
            "new_balance": business.balance,
            "donation_id": new_donation.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Donation transaction failed', 'details': str(e)}), 500

# --- READ (Get Donation History) ---

@donations_blueprint.route('/api/donations/business/<int:business_id>', methods=['GET'])
def get_business_donations(business_id):
    try:
       business = Business.query.get_or_404(business_id)
       donations = Donation.query.filter_by(business_id=business_id).order_by(Donation.timestamp.desc()).all()
    
       return jsonify({
        'success': True,
        'business_name': business.name,
        'total_donations': len(donations),
        'total_amount': sum(d.amount for d in donations),
        'donations': [d.to_dict() for d in donations]
    }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve donations', 'details': str(e)}), 500

@donations_blueprint.route('/api/donations/user/<int:user_id>', methods=['GET'])
@donor_required
def get_user_donations(user_id):
    if session.get('user_id') != user_id:
         return jsonify({'error': 'Unauthorized: Cannot view another donor history.'}), 403

    try:
       donations = Donation.query.filter_by(user_id=user_id).order_by(Donation.timestamp.desc()).all()
       return jsonify({
        'success': True,
        'total_donations': len(donations),
        'total_amount': sum(d.amount for d in donations),
        'donations': [d.to_dict() for d in donations]
    }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve donations', 'details': str(e)}), 500


@donations_blueprint.route('/api/transparency', methods=['GET'])
def transparency_report():
    total_donations = db.session.query(func.sum(Donation.amount)).scalar() or 0 
    
    # Existing 'meals_provided' counts claims (consumption). 
    # User might want "Meals Donated" (supply). I'll keep consumption as "provided" but add "donated" stats.
    # User Request: "Stat 1: Total Meals Donated. Stat 2: Total Clothes Donated."
    
    total_meals_donated = db.session.query(func.sum(Donation.quantity)).filter(Donation.type == 'food').scalar() or 0
    total_clothes_donated = db.session.query(func.sum(Donation.quantity)).filter(Donation.type == 'clothes').scalar() or 0
    
    total_meals_claimed = db.session.query(func.count(MealClaimed.id)).scalar() or 0
    active_businesses = Business.query.count()

    # top 5 donors
    top_donors = db.session.query(
        Donation.donor_name, func.sum(Donation.amount).label('total')
    ).group_by(Donation.donor_name).order_by(desc('total')).limit(5).all()


    return jsonify({
        'impact_summary': {
            'total_funds_raised': total_donations,
            'meals_donated': total_meals_donated,
            'clothes_donated': total_clothes_donated,
            'meals_provided': total_meals_claimed,
            'participating_businesses': active_businesses
        },
        'top_donors': [{'name': name, 'amount': amount} for name, amount in top_donors]
    })

