from flask import Blueprint, request, jsonify
from app import db 
from models import Meal, Business

# Create a Blueprint instance for the meals routes
meals_blueprint = Blueprint('meals', __name__)

# --- GET ALL AVAILABLE MEALS ---
@meals_blueprint.route('/api/meals', methods=['GET'])
def get_all_meals():
    """
    Retrieves all available meals from all businesses.
    Returns meal details including business info and pricing.
    """
    try:
        meals = Meal.query.all()
        
        meals_data = []
        for meal in meals:
            business = Business.query.get(meal.business_id)
            meals_data.append({
                'id': meal.id,
                'name': meal.name,
                'price': meal.price,
                'business_id': meal.business_id,
                'business_name': business.name if business else 'Unknown',
                'business_balance': business.balance if business else 0
            })
        
        return jsonify({
            'success': True,
            'total_meals': len(meals_data),
            'meals': meals_data
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch meals', 'details': str(e)}), 500


# --- GET MEALS BY BUSINESS ---
@meals_blueprint.route('/api/meals/business/<int:business_id>', methods=['GET'])
def get_business_meals(business_id):
    """
    Retrieves all meals offered by a specific business.
    """
    try:
        business = Business.query.get_or_404(business_id)
        meals = Meal.query.filter_by(business_id=business_id).all()
        
        meals_data = [
            {
                'id': meal.id,
                'name': meal.name,
                'price': meal.price,
                'business_name': business.name,
                'business_balance': business.balance
            }
            for meal in meals
        ]
        
        return jsonify({
            'success': True,
            'business_name': business.name,
            'total_meals': len(meals_data),
            'meals': meals_data
        }), 200
    except Exception as e:
        return jsonify({'error': 'Business not found or failed to fetch meals', 'details': str(e)}), 500


# --- GET MEALS WITH AVAILABLE BALANCE (For "In Need" Dashboard) ---
@meals_blueprint.route('/api/meals/available', methods=['GET'])
def get_available_meals():
    """
    Retrieves meals from businesses that have positive balance 
    (i.e., businesses that can fulfill meal claims).
    Useful for the "In Need" dashboard to show which meals can be claimed.
    """
    try:
        # Get all businesses with positive balance
        available_businesses = Business.query.filter(Business.balance > 0).all()
        
        meals_data = []
        for business in available_businesses:
            meals = Meal.query.filter_by(business_id=business.id).all()
            for meal in meals:
                meals_data.append({
                    'id': meal.id,
                    'name': meal.name,
                    'price': meal.price,
                    'business_id': business.id,
                    'business_name': business.name,
                    'business_balance': business.balance,
                    'can_claim': business.balance >= meal.price
                })
        
        return jsonify({
            'success': True,
            'total_available_meals': len(meals_data),
            'meals': meals_data
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch available meals', 'details': str(e)}), 500
