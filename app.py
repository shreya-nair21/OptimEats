from flask import Flask
from models import MealClaimed, Menu
from routes.business import Business
from OptimEats.routes.donation import Donor
from routes.users import Users

def create_app():
  app = Flask(__name__)


  #basic config
  app.config['SECRET_KEY'] = 'your_secret_key'

  @app.route('/')
  def home():
    return "Flask backend setup successful!"
  
  return app

if __name__ == "__main__":
  app = create_app()
  app.run(debug=True)
