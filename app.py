import os
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

# ==== INDEX ====================================================================================================================================== 
@app.route('/')
def index():
    if "userName" in session:
      return render_template("index.html", users = mongo.db.users.find({"email" : session['userName']}))
    return render_template("login.html")

# ==== SIGNUP FORM AND DB INSERT (if not in session and user already exists) =======================================================================
# TODO: Fix issue with logged in users accessing this route    
@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
      users = mongo.db.users
      emailExist = users.find_one({"email" : request.form["email"]})

      if emailExist is None:
        password_hashed = bcrypt.hashpw(request.form["password"].encode("utf-8"), bcrypt.gensalt())
        users.insert({  'first_name' : request.form["first-name"], 
                        'last_name' : request.form["last-name"], 
                        'email' : request.form["email"], 
                        'password' : password_hashed
                    })
        session['userName'] = request.form["email"]
        return redirect(url_for("index"))
      
      return "already!!!"
    return render_template('signup.html')

# ==== LOG IN  =====================================================================================================================================
@app.route("/login", methods=["POST"])
def login():
	users = mongo.db.users
	validUser = users.find_one({"email" : request.form["email"]})
	if validUser:
		if bcrypt.hashpw(request.form["password"].encode("utf-8"), validUser['password']) == validUser['password']:
			session['userName'] = request.form["email"]
			return redirect(url_for("index"))
		return "wrong password"
	return "wrong username"

# ==== LOG OUT (Clear session vars) ================================================================================================================
@app.route("/logout")
def logout():
	session.clear()
	return redirect(url_for('index'))

# ==== APP.RUN =====================================================================================================================================
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=os.environ.get('PORT'),
        debug=True)
