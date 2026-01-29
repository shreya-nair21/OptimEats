from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from models import db, User, Business

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('type') # 'user' or 'business'

    if not email or not password or not user_type:
        return jsonify({'error': 'Email, password, and type are required'}), 400

    if user_type == 'user':
        user = User.query.filter_by(email=email).first()
        if user and user.password and check_password_hash(user.password, password):
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'id': user.id,
                'name': user.name,
                'type': 'user'
            }), 200
        elif user and not user.password: 
             # Fallback for old users without password or if logic was different
             # For now, require password
             return jsonify({'error': 'Invalid credentials'}), 401
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    elif user_type == 'business':
        business = Business.query.filter_by(email=email).first()
        if business and business.password and check_password_hash(business.password, password):
             return jsonify({
                'success': True,
                'message': 'Login successful',
                'id': business.id,
                'name': business.name,
                'type': 'business'
            }), 200
        else:
             return jsonify({'error': 'Invalid credentials'}), 401
    
    else:
        return jsonify({'error': 'Invalid user type'}), 400
