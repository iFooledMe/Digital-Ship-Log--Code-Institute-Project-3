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

# ==== HELPER FUNCTIONS ======================================================
# ---- Get user in session  ----
def find_users():
	return mongo.db.users.find({
		"email" : session['email']})

# ---- Get a specified value from one user  ----
def get_user_value(key):
	return mongo.db.users.find_one({
		"email" : session['email']})[key]

# ---- Get _id when user logs in or register  ----
def get_user_id(email):
	return mongo.db.users.find_one({
		"email" : email})["_id"]

# ---- Set session variables ----
def set_session_vars(email):
	session['email'] = email
	session['user_id'] = str(get_user_id(email))

# ---- Update User activity code ----
def update_user_activity(new_activity):
	mongo.db.users.update(
		{"email" : session['email']},
		{"$set":{"activity_code":new_activity}})

# ==== INDEX ================================================================= 
@app.route('/')
def index():
	if "email" in session:
		activity_code = get_user_value('activity_code')
		return render_template(
			"index.html",
			users=find_users(),
			activity = get_activity_name(activity_code),
			options = get_activity_options(activity_code),
			log_headers = get_log_header(session['user_id']))
	return render_template("login.html")

# ==== ACTIVITY ==============================================================
# ---- Get activity by activity code ----
def get_activity_name(activity):
	if activity is not None:
		return mongo.db.activity_statuses.find_one({
			"activity_code" : activity})['activity_name']
	return "No activity set"

# ---- Get activity options  ----
def get_activity_options(activity):
	return mongo.db.activity_options.find({
		"show_on_status" : activity })

# ---- Change activity  ----
@app.route('/change_activity/<int:new_activity>')
def change_activity(new_activity):
	if new_activity == 2:
		return render_template("newjourney.html")
	update_user_activity(new_activity)
	return redirect(url_for("index"))

# ==== LOG HEADERS  =============================================================
# ---- Get Log Headers  ----
def get_log_header(userId):
	return mongo.db.log_headers.find({
		"user_id" : userId})

# ==== LOGTYPE: JOURNEY  =============================================================

# ---- New Journey  ----
@app.route("/newjourney", methods=["POST", "GET"])
def newjourney():
	if request.method == "POST":
		close_journey()
		update_user_activity(2)
		log_headers = mongo.db.log_headers
		log_headers.insert({
			'user_id' : str(get_user_value("_id")),
			'type' : "Journey",
			'title' : request.form["title"],
			'description' : request.form["description"],
			'start_location' : request.form["start_location"],
			'end_location' : request.form["end_location"],
			'distance' : request.form["distance"],
			'start_datetime' : datetime.datetime.now(),
			'end_datetime' : "",
			'is_active' : True })
		return redirect(url_for('index'))
	return redirect(url_for('index'))

# ---- Close active Journey before creating a new ----
def close_journey():
	find_journey = {'user_id' : session['user_id'], 'type' : 'Journey', 'is_active' : True}
	update_values = {'$set': {'end_datetime' : datetime.datetime.now(), 'is_active' : False} }
	mongo.db.log_headers.update_one(find_journey, update_values)

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
			set_session_vars(request.form['email'])
			return redirect(url_for("index"))
		return render_template("signup.html", emailExist = True)		
	elif "email" in session:
		return redirect(url_for("index")) 
	return render_template("signup.html")

# ==== LOG IN ================================================================
@app.route('/login', methods=['POST'])
def login():
	users = mongo.db.users
	validUser = users.find_one({'email' : request.form['email']})
	renderBadLogin = render_template('login.html', badLogin = True)
	if validUser:
		if bcrypt.hashpw(
			request.form['password'].encode('utf-8'),
			validUser['password']) == validUser['password']:
			set_session_vars(request.form['email'])
			return redirect(url_for('index'))
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
