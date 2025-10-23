# app.py
from flask import Blueprint,Flask, request, jsonify
import os
from models import db 
from models import Business, Meal # Import only the necessary models

# Create a Blueprint instance for the business routes
businesses_blueprint = Blueprint('businesses', __name__)

# --- API Routes for CRUD Operations ---

# CREATE a new business
@businesses_blueprint.route('/businesses/register', methods=['POST'])
def create_business():
    data = request.get_json()

    # Check for mandatory fields and handle missing data
    if not data or 'name' not in data:
        return jsonify({"error": "Missing JSON data or 'name' field"}), 400
    
    try:
        new_business = Business(
            name=data.get('name'),         
            contact=data.get('contact'),   
            address=data.get('address')    
        )
        
        db.session.add(new_business)
        db.session.commit()
        return jsonify(new_business.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Database error: {e}")
        return jsonify({"error": "Issue creating business in database", "details": str(e)}), 500

# READ all businesses
@businesses_blueprint.route('/businesses', methods=['GET'])
def get_businesses():
    businesses = Business.query.all()
    return jsonify([business.to_dict() for business in businesses])

# READ a single business
@businesses_blueprint.route('/businesses/<int:id>', methods=['GET'])
def get_business(id):
    business = Business.query.get_or_404(id)
    return jsonify(business.to_dict())

# UPDATE a business
@businesses_blueprint.route('/businesses/<int:id>', methods=['PUT'])
def update_business(id):
    business = Business.query.get_or_404(id)
    data = request.get_json()
    business.name = data.get('name', business.name)
    # business.meal_price = data.get('meal_price', business.meal_price)
    business.pay_forward_balance = data.get('pay_forward_balance', business.pay_forward_balance)
    db.session.commit()
    return jsonify(business.to_dict())

# DELETE a business
@businesses_blueprint.route('/businesses/<int:id>', methods=['DELETE'])
def delete_business(id):
    business = Business.query.get_or_404(id)
    db.session.delete(business)
    db.session.commit()
    return '', 204

@businesses_blueprint.route('/businesses/<int:business_id>/menu', methods=['POST'])
def add_menu_item(business_id):
    business = Business.query.get_or_404(business_id)
    data = request.get_json()
    try:
        new_menu_item = Meal(
            name=data['name'],
            price=data['price'],
            business_id=business_id
        )
        db.session.add(new_menu_item)
        db.session.commit()
        return jsonify(new_menu_item.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add menu item', 'details': str(e)}), 400
