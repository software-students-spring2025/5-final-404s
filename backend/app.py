import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user
import pymongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from datetime import datetime, timezone
import requests
from recommend import recommend_meal

# function to get nutrition facts from api 
def get_nutrition_facts(food_name):
   """
   Given a food name use USDA api to get nutrition facts
   """
   key = os.getenv("FOOD_API_KEY")

   # send req and get data
   search_url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={key}&query={food_name}"
   search_response = requests.get(search_url)

   # handle errors
   if search_response.status_code != 200:
      return {
         "calories": 0,
         "protein": 0,
         "carbohydrates": 0,
         "fiber": 0,
         "calcium": 0
      } 
   search_data = search_response.json()

   # return default values when search not found
   if not search_data["foods"]:
      return {
         "calories": 0,
         "protein": 0,
         "carbohydrates": 0,
         "fiber": 0,
         "calcium": 0
      } 
   
   # get first food results
   fdc_id = search_data["foods"][0]["fdcId"]

   # use food id to make request
   food_url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}?api_key={key}"
   food_response = requests.get(food_url)

   # handle errors
   if food_response.status_code != 200:
      return {
         "calories": 0,
         "protein": 0,
         "carbohydrates": 0,
         "fiber": 0,
         "calcium": 0,
         
      } 
   food_data = food_response.json()

   # get nutrients for food and return values
   nutrients = food_data.get("labelNutrients", {})

   return {
      "calories": nutrients.get("calories", {}).get("value", 0),
      "protein": nutrients.get("protein", {}).get("value", 0),
      "carbohydrates": nutrients.get("carbohydrates", {}).get("value", 0),
      "fiber": nutrients.get("fiber", {}).get("value", 0),
      "calcium": nutrients.get("calcium", {}).get("value", 0),
   }

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
    def __init__(self, user_doc=None):
        if user_doc:
            self.id = str(user_doc["_id"])
            self.username = user_doc["username"]

   @login_manager.user_loader
   def user_loader(id):
      user_file = db.users.find_one({"_id": ObjectId(id)})
      if user_file:
         user = User()
         user.id = str(user_file["_id"])
         user.username = user_file["username"]
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
               if check_password_hash(document["password"], password):
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
   
   @app.route("/register", methods=["GET", "POST"])
   def register():
    if current_user.is_authenticated:
        print("✅ User is already authenticated, redirecting to /home")
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()

        print(f"🔹 Form submitted — username: {username}")

        # Validation
        if not (username and password and confirm_password):
            print("Missing fields")
            return render_template("register.html", error="All fields are required.")

        if password != confirm_password:
            print("Passwords do not match")
            return render_template("register.html", error="Passwords do not match.")

        if db.users.find_one({"username": username}):
            print("Username already exists")
            return render_template("register.html", error="Username already exists.")

        # Insert into MongoDB
        hashed_pw = generate_password_hash(password)
        result = db.users.insert_one({"username": username, "password": hashed_pw})
        print(f"User inserted with ID: {result.inserted_id}")

        user_doc = db.users.find_one({"_id": result.inserted_id})
        print(f"Retrieved user document: {user_doc is not None}")

        # Create User object
        user = User(user_doc)
        print("Created User object")

        # Log user in
        login_user(user)
        print("User logged in — redirecting to /home")

        return redirect(url_for("home"))

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
      # get user's most recent foods
      recent_meals = list(db.meals.find({
         "user_id": ObjectId(current_user.id)
      }).sort("added_at", -1))

      return render_template("home.html", meals = recent_meals)

   @app.route("/meal-history")
   @login_required
   def meal_history():
      """
      Route for viewing meal history
      """
      meals = list(db.meals.find({
         "user_id": ObjectId(current_user.id)
      }).sort("added_at", -1))
      return render_template("meal_history.html", meals=meals)

   @app.route("/add-meal", methods=["GET", "POST"])
   @login_required
   def add_meal():
      """
      Route for adding new meal to user's history
      """
      if request.method == "POST":
         # get meal data from form
         food_input = request.form.get("food_list").strip()
         meal_type = request.form.get("meal_type")
         date = request.form.get("date", datetime.now().strftime("%Y-%m-%d"))

         # split food input into list
         food_list = [food.strip() for food in food_input.split() if food.strip()]

         # initialze nutrition count for meal
         total_nutrition_facts = {
            "calories": 0,
            "protein": 0,
            "carbohydrates": 0,
            "fiber": 0,
            "calcium": 0
         }

         # get nutrition facts for each food item
         for food in food_list:
            nutrition_facts = get_nutrition_facts(food)
            total_nutrition_facts["calories"] += nutrition_facts["calories"]
            total_nutrition_facts["protein"] += nutrition_facts["protein"]
            total_nutrition_facts["carbohydrates"] += nutrition_facts["carbohydrates"]
            total_nutrition_facts["fiber"] += nutrition_facts["fiber"]
            total_nutrition_facts["calcium"] += nutrition_facts["calcium"]
         
         # insert meal to db 
         meal = {
            "user_id": ObjectId(current_user.id),
            "food_input": food_input,
            "foods": food_list,
            "meal_type": meal_type,
            "date": date,
            "nutrition": total_nutrition_facts,
            "added_at": datetime.now(timezone.utc)
         }
         meal_doc = db.meals.insert_one(meal).inserted_id
         return redirect(url_for("meal_summary", meal_id=str(meal_doc)))

      # handle GET requests
      return render_template("add_meal.html", date=datetime.now().strftime("%Y-%m-%d"))
        
   @app.route("/meal-summary/<meal_id>")
   @login_required
   def meal_summary(meal_id):
      """
      Route for viewing nutrition facts for a meal
      """
      # find meal from database
      try:
         meal = db.meals.find_one({
            "_id": ObjectId(meal_id),
            "user_id": ObjectId(current_user.id)
         })
      except:
         # return to home if error occurs
         return redirect(url_for("home"))

      # return to home if meal not found
      if not meal:
         return redirect(url_for("home"))

      recommendations = recommend_meal(meal["nutrition"])

      return render_template("meal_summary.html", meal=meal, recommendations=recommendations)

   return app


app = create_app()
if __name__ == "__main__":
   FLASK_PORT = os.getenv("FLASK_PORT", "8080")
   app.run(debug=True, host="0.0.0.0", port=int(FLASK_PORT))