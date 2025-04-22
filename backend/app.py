import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user
import pymongo
from bson.objectid import ObjectId

# get env variables from .env
load_dotenv()

def create_app():
   """
   Create the Flask Application
   returns: app: the Flask application object
   """
   app = Flask(__name__)

   # set secret and auto reload templates
   app.secret_key = os.urandom(24)
   app.config["TEMPLATES_AUTO_RELOAD"] = True
   
   # set up for flask login
   login_manager = LoginManager()
   login_manager.init_app(app)
   login_manager.login_view = "index"

   cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
   db = cxn[os.getenv("MONGO_DBNAME")]

   # testing for mongoDB connection
   try:
      cxn.admin.command("ping")
      print(" * Connected to MongoDB")
   except Exception as e:
      print(" * Error connecting to MongodDB:", e)
   
   # class for user login
   class User(UserMixin):
      pass

   @login_manager.user_loader
   def user_loader(id):
      user_file = db.users.find_one({"_id": ObjectId(id)})
      if user_file:
         user = User()
         user.id = str(user_file["_id"])
         return user
      return None
   
   @app.route("/", methods=["GET","POST"])
   def index():
      """
      Route for home page, the login page
      """
      # if user logged in, redirect to home page
      if current_user.is_authenticated:
         return redirect(url_for("home"))
      
      # handle POST request
      if request.method == "POST":
         username = request.form.get("username").strip()
         password = request.form.get("password").strip()
         
         if username and password:
            document = db.users.find_one({"username": username})
            if document:
               # compare passwords
               if document["password"] == password:
                  user = User()
                  user.id = str(document["_id"])
                  login_user(user)
                  return redirect(url_for("home"))
               else:
                  return render_template("index.html", error="Incorrect Password. Try again.")
            else:
               return render_template("index.html", error="User not found. Create new account.")
         else:
            return render_template("index.html", error="All form fields are required.")
      
      # show login page for GET requests
      return render_template("index.html")
   
   @app.route("/register", methods=["GET","POST"])
   def register():
      """
      Route for user registration
      """
      # if user logged in, redirect to home page
      if current_user.is_authenticated:
         return redirect(url_for("home"))

      # handle POST request
      if request.method == "POST":
         username = request.form.get("username").strip()
         password = request.form.get("password").strip()
         confirm_password = request.form.get("confirm_password").strip()

         if username and password and confirm_password:
            if password == confirm_password:
               existing_user = db.users.find_one({"username": username})

               # handle if user already exists with username
               if existing_user:
                  return render_template("register.html", error="Username already exists.")
               
               # add new user
               user_doc = {"username": username, "password": password}
               added_user = db.users.insert_one(user_doc)

               # log new user
               user = User()
               user.id = str(added_user.inserted_id)
               login_user(user)
               return redirect(url_for("home"))
            else:
               # handle passwords not matching
               return render_template("register.html", error="Passwords do not match.")
         else:
            return render_template("register.html", error="All form fields are required.")
      
      # show register page for GET requests
      return render_template("register.html")
            
   @app.route("/logout")
   @login_required
   def logout():
      """
      Route for logging user out
      """
      logout_user()
      return redirect(url_for("index"))
   
   @app.route("/home")
   @login_required
   def home():
      """
      Route for app home page
      """
      pass

   @app.route("/meal-history")
   @login_required
   def meal_history():
      """
      Route for viewing meal history
      """
      pass

   @app.route("/add-meal")
   @login_required
   def add_meal():
      """
      Route for adding new meal to user's history
      """
      pass

   @app.route("/meal-summary")
   @login_required
   def meal_summary():
      """
      Route for viewing nutrition facts for a meal
      """
      pass

   @app.route("/meal-recommendations")
   @login_required
   def meal_recommendations():
      """
      Route for viewing recommended meals
      """
      pass



   
   return app


app = create_app()
if __name__ == "__main__":
   FLASK_PORT = os.getenv("FLASK_PORT", "5000")
   app.run(debug=True, host="0.0.0.0", port=int(FLASK_PORT))