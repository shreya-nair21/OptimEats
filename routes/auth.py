from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from models import db, User, Business
import os
import requests

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

# --- PASSWORD RESET FLOW ---

def send_reset_email(to_email, reset_link):
    """
    Sends an email via SendGrid API if the key is present.
    If no key is found, it safely prints the link to the console for testing.
    """
    api_key = os.getenv('SENDGRID_API_KEY')
    if api_key:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            "personalizations": [{"to": [{"email": to_email}]}],
            "from": {"email": "noreply@optimeats.com"},
            "subject": "OptimEats - Password Reset",
            "content": [{"type": "text/html", "value": f"<p>Hello,</p><p>Please click the link below to reset your password:</p><p><a href='{reset_link}'>{reset_link}</a></p><p>If you did not request this, please ignore this email.</p>"}]
        }
        try:
            requests.post('https://api.sendgrid.com/v3/mail/send', headers=headers, json=data)
            print(f"Sent real email via SendGrid to {to_email}")
        except Exception as e:
            print(f"Failed to send email: {e}")
    else:
        # Fallback for local testing without an API key
        print("\n" + "="*50)
        print(f"MOCK API EMAIL TO: {to_email}")
        print(f"SUBJECT: OptimEats - Password Reset")
        print(f"LINK: {reset_link}")
        print("Note: Provide SENDGRID_API_KEY in .env to send real emails.")
        print("="*50 + "\n")

@auth_blueprint.route('/api/auth/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
        
    # Check both tables
    account_type = None
    if User.query.filter_by(email=email).first():
        account_type = 'user'
    elif Business.query.filter_by(email=email).first():
        account_type = 'business'
        
    if not account_type:
        # For security, don't reveal if account exists or not
        return jsonify({'message': 'If an account exists, a reset link has been sent.'}), 200
        
    # Generate token
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = s.dumps({'email': email, 'type': account_type}, salt='password-reset-salt')
    
    reset_link = f"http://localhost:5000/reset_password.html?token={token}"
    send_reset_email(email, reset_link)
    
    return jsonify({'message': 'If an account exists, a reset link has been sent.'}), 200

@auth_blueprint.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('password')
    
    if not token or not new_password:
        return jsonify({'error': 'Token and new password are required'}), 400
        
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        # Verify token expires in 1 hour (3600 seconds)
        data = s.loads(token, salt='password-reset-salt', max_age=3600)
        email = data.get('email')
        account_type = data.get('type')
    except SignatureExpired:
        return jsonify({'error': 'The password reset link has expired.'}), 400
    except BadSignature:
        return jsonify({'error': 'Invalid password reset token.'}), 400
        
    hashed_password = generate_password_hash(new_password)
    
    if account_type == 'user':
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = hashed_password
            db.session.commit()
            return jsonify({'message': 'Password updated successfully.'}), 200
    elif account_type == 'business':
        business = Business.query.filter_by(email=email).first()
        if business:
            business.password = hashed_password
            db.session.commit()
            return jsonify({'message': 'Password updated successfully.'}), 200
            
    return jsonify({'error': 'Account not found.'}), 404
