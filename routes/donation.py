from flask import Blueprint, request, jsonify
from models import db, Donation, Business, User

donations_blueprint = Blueprint('donations', __name__)

# --- DONATION TRANSACTION ---

@donations_blueprint.route('/api/donations', methods=['POST'])
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
    business_id = data.get('business_id')
    user_id = data.get('user_id') # Optional
    
    if not donor_name or not amount:
        return jsonify({"error": "Missing required fields: donor_name, amount"}), 400

    try:
        amount = float(amount)
        if amount <= 0:
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
            amount=amount
        )
        db.session.add(new_donation)

        # Update business balance
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
def get_user_donations(user_id):
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

