from flask import Blueprint, request, jsonify
from app import db 
from models import Donation, Business # Need Donation model for record and Business for balance update

# Create a Blueprint instance for the donations routes
donations_blueprint = Blueprint('donations', __name__)

# --- DONATION TRANSACTION (The Core Logic) ---

@donations_blueprint.route('/api/donations', methods=['POST'])
def handle_donation():
    """
    Handles a monetary donation transaction.
    1. Creates a Donation record (Source of Truth).
    2. Atomically updates the target Business's pay_forward_balance.
    """
    data = request.get_json()
    
    # Required parameters for a successful donation
    amount = data.get('donation')
    business_id = data.get('business_id')
    
    # Optional: user_id is included if the donor is logged in
    user_id = data.get('user_id') 

    if not amount or not business_id or amount <= 0:
        return jsonify({"error": "Invalid donation amount or missing business ID."}), 400

    # Start a database transaction for data integrity
    try:
        # Use begin_nested to ensure atomicity
        with db.session.begin_nested():
            # 1. Find the business (must exist to receive a donation)
            business = Business.query.get(business_id)
            if not business:
                return jsonify({'error': 'Target business not found.'}), 404

            # 2. Create the Donation record (Source Data)
            new_donation = Donation(
                user_id=user_id,
                business_id=business_id,
                donation=amount
            )
            db.session.add(new_donation)

            # 3. Update the business's balance
            business.balance += amount

        # Commit the main transaction
        db.session.commit()
        
        return jsonify({
            "message": "Donation recorded and balance updated successfully.",
            "new_balance": business.balance,
            "donation_id": new_donation.id
        }), 201

    except Exception as e:
        # If anything goes wrong, roll back the transaction
        db.session.rollback()
        return jsonify({'error': 'Donation transaction failed', 'details': str(e)}), 500

# --- READ (Get Donation History for a Business) ---

@donations_blueprint.route('/api/donations/business/<int:business_id>', methods=['GET'])
def get_business_donations(business_id):
    """Retrieves all donation records for a specific business."""
    # Note: Using .all() here is fine for a demo, but should be paginated in a real app.
    donations = Donation.query.filter_by(business_id=business_id).order_by(Donation.timestamp.desc()).all()
    
    return jsonify([donation.to_dict() for donation in donations])

# --- NEW ROUTE: GET PRIORITY BUSINESSES (Negative Balance First) ---

@donations_blueprint.route('/api/businesses/priority', methods=['GET'])
def get_priority_businesses():
    """
    Retrieves all businesses, ordered by the lowest (most negative) pay_forward_balance 
    to show donors which businesses are in deficit and need priority.
    """
    # Order by balance ascending (lowest balance first). 
    # This places the most negative balances at the top.
    businesses = Business.query.order_by(Business.pay_forward_balance.asc()).all()
    
    return jsonify([business.to_dict() for business in businesses])
