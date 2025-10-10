from flask import Flask, request, jsonify
from flask_cors import CORS
from routes.meals import meals_blueprint
# from routes.business 
# from routes.donation 
# from routes.users 

def create_app():
  app = Flask(__name__)


  #basic config
  app.config['SECRET_KEY'] = 'your_secret_key'

  CORS(app)
  app.register_blueprint(meals_blueprint)
# test route
  @app.route('/')
  def home():
    return "Flask backend setup successful!"
  

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
  
  # Business registration
  @app.route('/api/businesses', methods=['POST'])
  def businesses():
    data = request.json
    print("Business registration received: ", data)
    return jsonify({"status" : "success" , "message" : "Business registered"})


  return app

if __name__ == "__main__":
  app = create_app()
  app.run(debug=True)
