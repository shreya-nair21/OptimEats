from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

# from routes.users import users_blueprint
from routes.business import  businesses_blueprint
# from routes.donation import handle_donation,get_business_donations
from models import db #MealClaimed, Meal,User,Donation

def create_app():
  app = Flask(__name__)
  #basic config
  app.config['SECRET_KEY'] = 'your_secret_key'
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///optimeat.db" 
  app.register_blueprint(businesses_blueprint)
  @app.route('/')
  def home():
    return render_template("home.html")
  
  @app.route('/donation',)
  def donation():
    return render_template("donations.html")
  
  @app.route('/business')
  def business():
    return render_template("business.html")
  
 
  return app

if __name__ == "__main__":
  app = create_app()
  db.init_app(app)
  app.run(debug=True)
