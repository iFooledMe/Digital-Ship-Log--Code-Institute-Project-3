import os, datetime
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt

if os.path.exists("env.py"):
  import env 

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
app.config["MONGO_DBNAME"] = os.environ["MONGO_DBNAME"]
app.config["MONGO_URI"] = os.environ["MONGO_URI"]
mongo = PyMongo(app)

# ==== HELPER FUNCTION =======================================================
# ---- Get user in session  ----
def find_users():
	return mongo.db.users.find({
		"email" : session['session_id']})

# ---- Get a specified value from one user  ----
def get_user_value(key):
	return mongo.db.users.find_one({
		"email" : session['session_id']})[key]

# ==== INDEX ================================================================= 
@app.route('/')
def index():
	if "session_id" in session:
		print(get_user_value("_id"))
		return render_template(
			"index.html",
			users=find_users(),
			render_activity=get_activity(get_user_value("activity_code")),
			options=get_activity_options(get_user_value("activity_code")),
			journeys = get_journeys(get_user_value("_id"))  )
	return render_template("login.html")

# ==== ACTIVITY ==============================================================
# ---- Get activity by activity code ----
def get_activity(activity):
	if activity is not None:
		return mongo.db.activity_statuses.find_one({
			"status_code" : activity})['status_name']
	return "No activity set"

# ---- Get activity options  ----
def get_activity_options(activity):
	return mongo.db.activity_options.find({
		"show_on_status" : activity })

# ---- Change activity  ----
@app.route('/change_activity/<int:new_activity>')
def change_activity(new_activity):
	mongo.db.users.update(
		{"email" : session['session_id']},
		{"$set":{"activity_code":new_activity}})
	if new_activity == 2:
		return render_template("newjourney.html")
	return redirect(url_for("index"))

# ==== JOURNEYS  =============================================================
# ---- Get Journeys  ----
def get_journeys(userId):
	return mongo.db.journeys.find({
		"user_id" : str(userId)})

# ---- New Journey  ----
@app.route("/newjourney", methods=["POST", "GET"])
def newjourney():
	if request.method == "POST":
		journeys = mongo.db.journeys
		journeys.insert({
			'user_id' : str(get_user_value("_id")),
			'title' : request.form["title"],
			'description' : request.form["description"],
			'start_location' : request.form["start_location"],
			'end_location' : request.form["end_location"],
			'distance' : request.form["distance"],
			'start_datetime' : datetime.datetime.now(),
			'is_active' : True })
		return redirect(url_for("index"))
	return redirect(url_for("index"))

# ==== SIGNUP =================================================================
@app.route("/signup", methods=["POST", "GET"])
def signup():
	if request.method == "POST":
		users = mongo.db.users
		emailExist = users.find_one({"email": request.form["email"]})
		if emailExist is None:
			password_hashed = bcrypt.hashpw(request.form["password"].encode("utf-8"),bcrypt.gensalt())
			users.insert({
			'first_name' : request.form["first-name"],
			'last_name' : request.form["last-name"],
			'email' : request.form["email"],
			'password' : password_hashed,
			'activity_code' : 0 })
			session['session_id'] = request.form["email"]
			return redirect(url_for("index"))
		return render_template("signup.html", session_idExist = True)		
	elif "session_id" in session:
		return redirect(url_for("index")) 
	return render_template("signup.html")

# ==== LOG IN ================================================================
@app.route("/login", methods=["POST"])
def login():
	users = mongo.db.users
	validUser = users.find_one({"email" : request.form["email"]})
	renderBadLogin = render_template("login.html", badLogin = True)
	if validUser:
		if bcrypt.hashpw(
			request.form["password"].encode("utf-8"),
			validUser['password']) == validUser['password']:
				session['session_id'] = request.form["email"]
				return redirect(url_for("index"))
		return renderBadLogin
	return renderBadLogin

# ==== LOG OUT ===============================================================
@app.route("/logout")
def logout():
	session.clear()
	return redirect(url_for('index'))

# ==== APP.RUN ===============================================================
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=os.environ.get('PORT'),
        debug=True)
