from flask import Flask, render_template, session, jsonify, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os

from models import db, User, Business

from meals import meals_blueprint
from routes.business import businesses_blueprint
from routes.donation import donations_blueprint
from routes.users import users_blueprint

def create_app():
  app = Flask(__name__, template_folder='frontend', static_folder='frontend')

  #basic config
  app.config['SECRET_KEY'] = 'your_secret_key'
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///optimEat.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  CORS(app)
  db.init_app(app)

  #register all blueprints
  app.register_blueprint(meals_blueprint)
  app.register_blueprint(businesses_blueprint)
  app.register_blueprint(donations_blueprint)
  app.register_blueprint(users_blueprint)

  # Routes to serve HTML files
  @app.route('/')
  def home():
    return render_template('home.html')
  
  @app.route('/donations.html')
  def donation_page():
    return render_template('donations.html')
  
  @app.route('/business.html')
  def business_page():
    return render_template('business.html') 
  
  @app.route('/signup.html')
  def signup_page():
    return render_template('signup.html') 
  
  @app.route('/donor_dashboard.html')
  def donor_dashboard_page():
    return render_template('donor_dashboard.html')

  @app.route('/in_need.html')
  def in_need_page_route(): 
    return render_template('in_need.html')

  @app.route('/transparency.html')
  def transparency_page():
    return render_template('transparency.html')

  @app.route('/dashboard.html')
  def dashboard_page():
    return render_template('dashboard.html')

  # AUTHENTICATION ROUTES 
  @app.route('/api/auth/login', methods=['POST'])
  def login_user():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if user and user.password == data.get('password'): 
      session['user_id'] = user.id
      return jsonify({'message': 'Login successful', 'user': user.to_dict()}), 200
    return jsonify({'error': 'Invalid credentials'}), 401
    
  
  return app

if __name__ == "__main__":
  app = create_app()

  with app.app_context():
    db.create_all()
    print("Database tables created successfully")
    print("Server starting on http://localhost:5000")
  app.run(debug=True)
