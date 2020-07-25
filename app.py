import os, datetime, shutil, sys, glob, json
from flask import Flask, render_template, redirect, request, url_for, session
from flask_wtf import FlaskForm
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.json_util import loads, dumps

import bcrypt

if os.path.exists("env.py"):
  import env 

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
app.config["MONGO_DBNAME"] = os.environ["MONGO_DBNAME"]
app.config["MONGO_URI"] = os.environ["MONGO_URI"]
mongo = PyMongo(app)

app.config['UPLOADED_IMAGES_DEST'] = 'static/img/users/'
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

# ====================================================================================
# ==== I N D E X =====================================================================
# TODO: Fix crash when user is removed from db but still in cache
@app.route('/')
def index():
	if "email" in session:
		try:
			activity_code = get_user_value('activity_code')
			return render_template(
			"index.html",
			have_user = check_for_user(),
			users=list(find_users()),
			activity = get_activity(activity_code),
			options = get_activity_options(activity_code),
			log_headers = get_log_headers(ObjectId(session['user_id'])),
			logs = list(get_log_entries(ObjectId(session['user_id']))),
			home_coords = get_home_position(),
			center_coords = get_center_coords(),
			coords = get_positions())
		except:
			session.clear()
			return render_template("login.html")	
	return render_template("login.html")

# ====================================================================================
# ==== G E T  C O N T E N T (Log headers and log entries) ============================

# ---- GET LOG HEADERS  ----
def get_log_headers(userId):
	return mongo.db.log_headers.find({"user_id" : userId}).sort("start_datetime",-1)

# ---- GET LOG ENTRIES   ----
def get_log_entries(userId):
	return mongo.db.logs.find({"user_id" : userId}).sort("datetime",-1)

# ====================================================================================
# ==== G E T  P O S I T I O N S  (for map markers) ===================================

# ---- Get position data sent to Google Maps script ----
def get_positions():
	pos_array = []
	for doc in mongo.db.logs.find({
		'user_id' : ObjectId(session['user_id']),
		'on_map' : True,
		'position.lat' : {'$ne' : ' -- '}, 
		'position.lng' : {'$ne' : ' -- '}
		}).sort("datetime",-1):
		position = doc['position']
		for pos in position:
			pos_array.append(pos)
	pos_array_json = json.dumps(pos_array)
	return pos_array_json

# ---- Get position for home port ----
def get_home_position():
	if "user_id" in session:
		home_pos = mongo.db.users.find_one({
			'_id' : ObjectId(session['user_id'])
		})['home_port_pos']
		home_pos = json.dumps(home_pos)
		return home_pos
	return [{"lat": "0.0", "lng": "0.0"}]

# ---- Log entry map switch control ----
@app.route('/map_switch/<log_id>', methods=["POST"])
def map_switch(log_id):
	log = mongo.db.logs.find_one( {'_id' : ObjectId(log_id)} )
	if log['on_map']:
		set_map = False
	else:
		set_map = True

	mongo.db.logs.update(
		{'_id' : ObjectId(log_id)},
		{'$set':{
			'on_map': set_map,
	}})
	return redirect(url_for("index"))

# ---- Journey map switch control (All logs) ----
@app.route('/map_switch_all/<journey_id>', methods=["POST"])
def map_switch_all(journey_id):
	log_header = mongo.db.log_headers.find_one({
		'_id' : ObjectId(journey_id) })
	
	
	if log_header['show_all']:
		show_all = False
	else:
		show_all = True

	mongo.db.log_headers.update(
		{'_id' : ObjectId(journey_id)},
		{'$set':{
			'show_all': show_all,
	}})
	switch_all_logs(journey_id, show_all)
	return redirect(url_for("index"))

def switch_all_logs(journey_id, set_map):	
	mongo.db.logs.update_many(
		{'head_id' : ObjectId(journey_id)},
		{'$set':{
			'on_map': set_map,
	}})


# ---- CENTER MAP POSITION COORDINATES ----------------------------------------------
def get_center_coords():
	if "user_id" in session:
		center_coords = mongo.db.users.find_one({'_id' : ObjectId(session['user_id'])})['center_map_pos']
		center_coords = json.dumps(center_coords)
		print(center_coords)
		return center_coords
	else:
		return [{"lat": "0.0", "lng": "0.0"}]

@app.route('/center_map/<log_id>', methods=['GET'])
def center_map(log_id):
	set_new_center(log_id)
	return redirect(url_for("index"))

# TODO: Fix center position function (current location, new log, edit log, delete log)
def set_new_center(log_id):
	log = mongo.db.logs.find_one( {'_id' : ObjectId(log_id)} )
	log_pos = log['position']
	mongo.db.users.update_one(
		{'_id' : ObjectId(session['user_id'])},
		{'$set':{
			'center_map_pos': log_pos}})

# ====================================================================================
# ==== C H A N G E  A C T I V I T Y ==================================================

# ---- Get activity by activity code ----
def get_activity(activity):
	if activity is not None:
		return mongo.db.activity_statuses.find_one({
			"activity_code" : activity})
	return "No activity set"

# ---- Get activity options  ----
def get_activity_options(activity):
	return mongo.db.activity_options.find({
		"show_on_status" : activity })

# ---- Change activity  ----
@app.route('/change_activity/<int:new_activity>')
def change_activity(new_activity):
	if new_activity == 2:
		return render_template(
			'newjourney.html',
			home_coords = get_home_position(),
			center_coords = get_center_coords(),
			coords = get_positions())
	if get_user_value('activity_code') == 2:
		close_journey()
	update_user_activity(new_activity)
	return redirect(url_for("index"))

# ====================================================================================
# ==== L O G  T Y P E S  =============================================================

# **** LOGTYPE: JOURNEY  *************************************************************

# ++++ LOG HEADER / JOURNEY ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ---- New Journey  ----
@app.route("/newjourney", methods=["POST", "GET"])
def newjourney():
	if request.method == "POST":
		close_journey()
		update_user_activity(2)
		header_index = mongo.db.log_headers.count() + 1
		log_headers = mongo.db.log_headers
		log_headers.insert({
			'user_id' : ObjectId(session['user_id']),
			'type' : 'Journey',
			'number' : header_index,
			'title' : request.form["title"],
			'description' : get_request_data(request.form["description"], " -- "),
			'start_location' : get_request_data(request.form["start_location"], " -- "),
			'end_location' : get_request_data(request.form["end_location"], " -- "),
			'distance' : get_request_data(request.form["distance"], " -- "),
			'start_datetime' : datetime.datetime.now(),
			'end_datetime' :  "Ongoing",
			'is_active' : True,
			'is_editable' : False,
			'show_all' : True })
		return redirect(url_for('index'))
	return render_template(
		'new_journey.html',
		home_coords = get_home_position(),
		center_coords = get_center_coords(),
		coords = get_positions())

# ---- Edit Journey Header  ----
@app.route('/edit_journey/<journey_id>', methods=['POST', 'GET'])
def edit_journey(journey_id):
	if request.method == 'POST':
		#TODO: Fix issue with editing date and time
		start_date = request.form["start_date"]
		start_time = request.form["start_time"]
		print('***********************************')
		print(start_date)
		print(start_time)
		print('***********************************')
		start_date = datetime.date(2020,6,15)
		start_time = datetime.time(9,0)
		start_datetime = datetime.datetime.combine(start_date,start_time)
		'''if request.form["end_date"] == "Ongoing" or request.form["end_time"] == "Ongoing":
			end_datetime = "Ongoing"
		else:
			end_date = request.form["end_date"]
			end_time = request.form["end_time"]
			end_datetime = datetime.datetime.combine(start_date, start_time)'''
		mongo.db.log_headers.update_one(
		{'_id' : ObjectId(journey_id)},
		{'$set':{
			'title': request.form['title'],
			'description' : get_request_data(request.form["description"], " -- "),
			'start_datetime' : start_datetime,
			'start_location' : get_request_data(request.form["start_location"], " -- "),
			'end_location' : get_request_data(request.form["end_location"], " -- "),
			'distance' : get_request_data(request.form["distance"], " -- "),
			'is_editable' : False }})
		return redirect(url_for('index'))
	this_journey = mongo.db.log_headers.find({'_id' : ObjectId(journey_id)})
	return render_template(
		"edit_journey.html", 
		journey_id=journey_id, 
		this_journey=this_journey,
		home_coords = get_home_position(),
		center_coords = get_center_coords(),
		coords = get_positions())

# ---- Delete Journey Header (and all it' contents) ----
@app.route('/delete_journey/<journey_id>', methods=['POST', 'GET'])
def delete_journey(journey_id):
	#TODO: Add function to remove any image files in the log_headers logs
	try:
		journey_img_dir = 'static/img/users/' + str(session['user_id'] + '/' + str(journey_id))
		shutil.rmtree(journey_img_dir)
		delete_it(journey_id)
		return redirect(url_for('index'))
	except OSError as e:
			print ("Error: %s - %s." % (e.filename, e.strerror))
			delete_it(journey_id)
			return redirect(url_for('index'))

def delete_it(journey_id):
	is_active = mongo.db.log_headers.find_one({'_id' :ObjectId(journey_id) })['is_active']
	if is_active:
		update_user_activity(0)
	mongo.db.logs.delete_many({'head_id' : ObjectId(journey_id)})
	mongo.db.log_headers.delete_one({'_id' :ObjectId(journey_id) })
	set_all_not_editable(session['user_id'])
	

# ---- Close active Journey before creating a new ----
def close_journey():
	find_journey = {
		'user_id' : ObjectId(session['user_id']),
		'type' : 'Journey', 'is_active' : True}
	update_values = {'$set': {
		'end_datetime' : datetime.datetime.now(),
		'is_active' : False} }
	mongo.db.log_headers.update_one(find_journey, update_values)

# ---- Set a logheader and it's sub sug entries to a editable state ----
@app.route("/set_editable/<journey_id>")
def set_editable(journey_id):
	find_journey = {'_id' : ObjectId(journey_id)}
	is_editable = mongo.db.log_headers.find_one(find_journey)['is_editable']
	if is_editable:
		update_values = {'$set': {'is_editable' : False } }
	else:
		update_values = {'$set': {'is_editable' : True } }
	set_all_not_editable(session['user_id'])
	mongo.db.log_headers.update_one(find_journey, update_values)
	return redirect(url_for('index'))

# ++++ LOG ENTRIES ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ---- New Journey Log Entry ----
@app.route("/newlog/<journey_id>", methods=["POST", "GET", 'request.files or none'])
def newlog(journey_id):
	if request.method == "POST":
		log_number = mongo.db.logs.find({"head_id" : ObjectId(journey_id)}).count() + 1
		try:
			save_folder = str(session['user_id'] + '/' + str(journey_id)) + '/' + str(log_number)
			image = images.save(request.files['image'], save_folder)
			img_url = "../static/img/users/" + str(image)
		except:
			img_url = "None"

		mongo.db.logs.insert_one({
			'user_id' : ObjectId(session['user_id']),
			'head_id' : ObjectId(journey_id),
			'log_number' : log_number,
			'type' : 'journey_log',
			'datetime' : datetime.datetime.now(),
			'edit_date' : "",
			'title' : request.form["title"],
			'note' : request.form["note"],
			'img_url' : img_url,
			'img_cap' : request.form["img_cap"],
			'weather' : get_request_data(request.form["weather"], " -- "),
			'temp' : get_request_data(request.form["temp"], " -- "),
			'air_pressure' : get_request_data(request.form["air_pressure"], " -- "),
			'wind_dir' : get_request_data(request.form["wind_dir"], " -- "),
			'wind_speed' : get_request_data(request.form["wind_speed"], " -- "),
			'activity' : get_request_data(request.form["activity"], " -- "),
			'heading' : get_request_data(request.form["heading"], " -- "),
			'speed' : get_request_data(request.form["speed"], " -- "),
			'location' : get_request_data(request.form["location"], " -- "),
			'position' : 
				[{
				'lat' : get_request_data(request.form["latitude"], " -- "),
				'lng' : get_request_data(request.form["longitude"], " -- ")
				}],
			'on_map': True
			})
		if len(request.form["latitude"]) != 0 and len(request.form["longitude"]) != 0:
			log = mongo.db.logs.find_one({
				'head_id' : ObjectId(journey_id),
				'log_number' : log_number })
			log_id = log['_id']
			set_new_center(log_id)

		return redirect(url_for('index'))
	weather_options = mongo.db.weather_options.find()
	wind_directions = mongo.db.wind_dir_options.find()
	activity_options = mongo.db.sub_activity_options.find()
	return render_template(
		'new_journey_log.html', 
		journey_id = journey_id, 
		weather_options = weather_options,
		wind_directions = wind_directions,
		activity_options = activity_options,
		home_coords = get_home_position(),
		center_coords = get_center_coords(),
		coords = get_positions())

# ---- Edit Journey Log Entry ---- 
@app.route('/edit_log/<journey_id>/<log_id>', methods=['POST', 'GET'])
def edit_log(journey_id, log_id):
	if request.method == 'POST':
		try:
			save_folder = str(session['user_id'] + '/' + str(journey_id)) + '/' + str(log_number)
			image = images.save(request.files['image'], save_folder)
			img_url = "../static/img/users/" + str(image)
		except:
			img_url = "none"
		mongo.db.logs.update(
		{'_id' : ObjectId(log_id)},
		{'$set':{
			'title': request.form['title'],
			'note' : get_request_data(request.form["note"], " -- "),
			'img_url' : img_url,
			'img_cap' : request.form["img_cap"],
			'weather' : get_request_data(request.form["weather"], " -- "),
			'temp' : get_request_data(request.form["temp"], " -- "),
			'air_pressure' : get_request_data(request.form["air_pressure"], " -- "),
			'wind_dir' : get_request_data(request.form["wind_dir"], " -- "),
			'wind_speed' : get_request_data(request.form["wind_speed"], " -- "),
			'activity' : get_request_data(request.form["activity"], " -- "),
			'heading' : get_request_data(request.form["heading"], " -- "),
			'speed' : get_request_data(request.form["speed"], " -- "),
			'location' : get_request_data(request.form["location"], " -- "),
			'position' : 
				[{
				'lat' : get_request_data(request.form["latitude"], " -- "),
				'lng' : get_request_data(request.form["longitude"], " -- ")
				}]
			}})
		if len(request.form["latitude"]) != 0 and len(request.form["longitude"]) != 0:
			log = mongo.db.logs.find_one({
				'_id' : ObjectId(log_id) })
			log_id = log['_id']
			set_new_center(log_id)
		return redirect(url_for('index'))
	weather_options = mongo.db.weather_options.find()
	wind_directions = mongo.db.wind_dir_options.find()
	activity_options = mongo.db.sub_activity_options.find()
	this_log = mongo.db.logs.find({'_id' : ObjectId(log_id)})
	return render_template(
		"edit_journey_log.html", 
		log_id=log_id,
		journey_id = journey_id, 
		this_log=this_log,
		weather_options = weather_options,
		wind_directions = wind_directions,
		activity_options = activity_options,
		home_coords = get_home_position(),
		center_coords = get_center_coords(),
		coords = get_positions())

# ---- Delete Journey Log Entry ---- 
@app.route('/delete_log/<journey_id>/<log_id>/<log_number>', methods=['POST', 'GET'])
def delete_log(journey_id, log_id, log_number):
	try:
		journey_img_dir = 'static/img/users/' + str(session['user_id'] + '/' + str(journey_id) + '/' + str(log_number))
		shutil.rmtree(journey_img_dir)
		delete_log(log_id)
		return redirect(url_for('index'))
	except OSError as e:
			print ("Error: %s - %s." % (e.filename, e.strerror))
			delete_log(log_id)
			return redirect(url_for('index'))

def delete_log(log_id):
	mongo.db.logs.delete_one({'_id' : ObjectId(log_id)})
	set_all_not_editable(session['user_id'])
	return redirect(url_for('index'))

# ====================================================================================
# ==== U S E R  A U T H E N T I C A T I O N  / R E G I S T R A T I O N ===============

# **** SIGNUP ************************************************************************
@app.route("/signup", methods=["POST", "GET"])
def signup():
	if request.method == "POST":
		users = mongo.db.users
		emailExist = users.find_one({"email": request.form["email"]})
		if emailExist is None:
			password_hashed = bcrypt.hashpw(request.form["password"].encode("utf-8"),bcrypt.gensalt())
			users.insert_one({
			'first_name' : request.form["first-name"],
			'last_name' : request.form["last-name"],
			'email' : request.form["email"],
			'password' : password_hashed,
			'activity_code' : 0,
			'home_port_name' : request.form["home-port-name"],
			'home_port_pos' : 
				[{
				'lat' : request.form["latitude"],
				'lng' : request.form["longitude"]
				}],
			'center_map_pos' : 
				[{
				'lat' : request.form["latitude"],
				'lng' : request.form["longitude"]
				}]
			 })
			set_session_vars(request.form['email'])
			mongo.db.check_for_user.update_one(
				{'_id' : ObjectId('5f1c6c41464dab8a7c623f9b')},
				{'$set':{ 'have_user': True }})
			return redirect(url_for("index"))
		return render_template("signup.html", emailExist = True)		
	elif "email" in session:
		return redirect(url_for("index")) 
	return render_template("signup.html")

# **** LOG IN ****************************************************************************
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
			set_all_not_editable(session['user_id'])
			mongo.db.check_for_user.update_one(
				{'_id' : ObjectId('5f1c6c41464dab8a7c623f9b')},
				{'$set':{'have_user': True }})
			return redirect(url_for('index'))
		return renderBadLogin
	return renderBadLogin

# **** LOG OUT ***************************************************************************
@app.route("/logout")
def logout():
	session.clear()
	mongo.db.check_for_user.update_one(
		{'_id' : ObjectId('5f1c6c41464dab8a7c623f9b')},
		{'$set':{'have_user': False }})
	return redirect(url_for('index'))

# ====================================================================================
# ==== H E L P E R  F U N C T I O N S ================================================
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

def get_request_data(request_data, empty_string_text):
	if request_data == "":
		return empty_string_text
	return request_data
	
def set_all_not_editable(user_id):
	mongo.db.log_headers.update_many(
		{'user_id' : ObjectId(user_id)},
		{'$set': {'is_editable' : False } })

def check_for_user():
	have_user = mongo.db.check_for_user.find_one(
		{'_id' : ObjectId('5f1c6c41464dab8a7c623f9b')})['have_user']
	return have_user

# ====================================================================================
# ==== A P P . R U N =================================================================
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=os.environ.get('PORT'),
        debug=True)
# TODO: Set deubug=False before submition