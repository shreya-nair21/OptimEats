from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models import db, Business, Meal

businesses_blueprint = Blueprint('businesses', __name__)

# --- API Routes for CRUD Operations ---

# CREATE a new business
@businesses_blueprint.route('/api/businesses', methods=['POST'])
def create_business():
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({"error" : "Business name is required"}), 400
    
    try:
        new_business = Business(
            name=data.get('name'),
            contact=data.get('contact', ''),
            address=data.get('address', ''),
            email=data.get('email', ''), # Should be unique
            password=generate_password_hash(data['password']) if data.get('password') else None
        )
        db.session.add(new_business)
        db.session.commit()
        return jsonify(new_business.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create business", "details": str(e)}), 500

# READ all businesses
@businesses_blueprint.route('/api/businesses', methods=['GET'])
def get_businesses():
    businesses = Business.query.all()
    return jsonify([business.to_dict() for business in businesses])

# READ a single business
@businesses_blueprint.route('/api/businesses/<int:id>', methods=['GET'])
def get_business(id):
    business = Business.query.get_or_404(id)
    return jsonify(business.to_dict())

# UPDATE a business
@businesses_blueprint.route('/api/businesses/<int:id>', methods=['PUT'])
def update_business(id):
    business = Business.query.get_or_404(id)
    data = request.get_json()
    
    if 'name' in data: business.name = data['name']
    if 'contact' in data: business.contact = data['contact']
    if 'address' in data: business.address = data['address']
    if 'balance' in data: business.balance = data['balance']

    try:
        db.session.commit()
        return jsonify(business.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update business", "details": str(e)}), 500

# DELETE a business
@businesses_blueprint.route('/api/businesses/<int:id>', methods=['DELETE'])
def delete_business(id):
    business = Business.query.get_or_404(id)
    db.session.delete(business)
    db.session.commit()
    return '', 204

# --- MENU MANAGEMENT ---

@businesses_blueprint.route('/api/businesses/<int:business_id>/menu', methods=['POST'])
def add_menu_item(business_id):
    business = Business.query.get_or_404(business_id)
    data = request.get_json()

    if not data.get('name') or not data.get('price'):
        return jsonify({'error': 'Name and price are required'}), 400

    try:
        new_menu_item = Meal(
            name=data['name'],
            description=data.get('description'),
            price=float(data['price']),
            category=data.get('category'),
            available=data.get('available', True),
            business_id=business_id,
            image_url=data.get('image_url')
        )
        db.session.add(new_menu_item)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'New menu item added successfully',
            'meal': new_menu_item.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add menu item', 'details': str(e)}), 400

@businesses_blueprint.route('/api/businesses/<int:business_id>/menu', methods=['GET'])
def get_business_menu(business_id):
    try:
        business = Business.query.get_or_404(business_id)
        meals = Meal.query.filter_by(business_id=business_id).all()

        return jsonify({
            'success': True,
            'business_name': business.name,
            'total_items': len(meals),
            'menu': [m.to_dict() for m in meals]
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve menu', 'details': str(e)}), 500

@businesses_blueprint.route('/api/businesses/<int:business_id>/menu/<int:meal_id>', methods=['PUT'])
def update_menu_item(business_id, meal_id):
    meal = Meal.query.get_or_404(meal_id)
    if meal.business_id != business_id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    data = request.get_json()
    try:
        if 'name' in data: meal.name = data['name']
        if 'description' in data: meal.description = data['description']
        if 'price' in data: meal.price = float(data['price'])
        if 'category' in data: meal.category = data['category']
        if 'available' in data: meal.available = data['available']
        
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Menu item updated successfully',
            'meal': meal.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update menu item', 'details': str(e)}), 400

@businesses_blueprint.route('/api/businesses/<int:business_id>/menu/<int:meal_id>', methods=['DELETE'])
def delete_menu_item(business_id, meal_id):
    meal = Meal.query.get_or_404(meal_id)
    if meal.business_id != business_id:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({
            'success': True,
            'message':'Menu item deleted successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete menu item', 'details': str(e)}), 400





        
            


