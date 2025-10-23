from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
from OptimEats.routes.meal import meals_blueprint
from models import db
from routes.business import businesses_blueprint
from routes.donation import donations_blueprint
from routes.user import user_blueprint, donor_blueprint

def create_app():
  app = Flask(__name__)
  #basic config
  app.config['SECRET_KEY'] = 'your_secret_key'
  app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  
  CORS(app)
  #registering all blueprints
  app.register_blueprint(meals_blueprint)
  app.register_blueprint(businesses_blueprint)
  app.register_blueprint(donations_blueprint)
  app.register_blueprint(user_blueprint)
  app.register_blueprint(donor_blueprint)

# Home page
  @app.route('/')
  def home():
    return render_template ('home.html')
    # return "Flask backend setup successful!"
  
# Money donation
  @app.route('/api/donations', methods=['POST'])
  def donations():
    data = request.json
    print("Money donation received: ", data)
    return jsonify({"status" : "success" , "message" : "Donation recorded"})
  
  # Food donation 
  @app.route('/api/food-donations', methods=['POST'])
  def food_donations():
    data = request.json
    print("Food donation received: ", data)
    return jsonify({"status" : "success" , "message" : "Food Donation recorded"})
  
  @app.route('/business')
  def business():
    return render_template("business.html")
  
 
  return app

if __name__ == "__main__":
  app = create_app()
  db.init_app(app)
  db.init_app(app)
  app.run(debug=True)
