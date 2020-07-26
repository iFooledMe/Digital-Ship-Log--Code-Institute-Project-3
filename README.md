# YOUR DIGITAL LOG BOOK
<img src="static/img/logo.png">

## AN INTERACTIVE LOG BOOK FOR YOUR BOAT
### A Code Institute Student Project
<hr>
<br>

<a href="https://ship-log-app.herokuapp.com/" target="_blank">Find the latest deployed version of this app at Heroku following this link</a>

## SUMMARY

This project aims to create a digital interactive log book for recreational boats and ships. As tradition on the seas offer, for recreational sailors often these logs are done in a physical logbook by pen and paper. In such a logbook normally the ship's captain enters a log daily, reporting navigational information such as heading, speed. Weather information such as wind direction, wind speed, weather conditions etc. Also there are usually  some notes about important events happening onboard the ship, like accidents, if something needs to be repaired, if the ship got new provisions, entered dock for unload, load etc. In the professional merchant fleet such log entries are mandatory and part of the international regulations. But for recreational ships and boats it is not. While many boat owners keep such a logbook in their ship/boat, often they mostly stay in a drawer collecting dust.
<br>

<em><strong>“Your Digital Log Book” is a web-application where recreational skippers can keep their ships logs digitally. Maybe not so much for the importance of such logs, but more as a collection of memories from different Journeys made in the past from notes, uploaded images, navigation- and weather data and plotted map positions. At least such digital logs won’t collect any dust.</strong></em>

## FEATURES

### Start and Login
The index page where users can sign in or click on any of the links to the sign up page.
<img src="static/img/readme/1.png">

### Sign up
The signup page where new users register. As seen in the image below there is an input control to check for existing email-addresses in the database, as the email addresses are used as usernames. A successful sign up creates a hashed binary password in the database. Other input controls are done directly in the html forms.
<img src="static/img/readme/3.png">

 ### Users personal log page
Successful log in or new registration redirects to the users personal log page. At the top of the page the users get the information that they currently are logged in with the email address they just submitted either in the log in or in the sign up form. The “door/arrow” icon to the right of the username/email address let the users sign out from the current session.
 <img src="static/img/readme/4.png">
Below the navbar to the left the user receives a welcome message, information about their current activity (“No/Other activity”, “At home port” or “On journey”) and some information about their last log entry. The user changes activity or starts a new journey from the dropdown menu below the welcome/status information window.

As seen in the example above, this user has currently yet no journeys or log entries created.

To the right a map (Google maps) is centered on a new marker marking the user's home port just submitted from the sign in form.

### Create a new Journey
A Journey is a kind of header or container of log entries for a particular journey. The journey header must have a title but all other fields in the form are optional, where the user can submit more details about the journey to be started.
 <img src="static/img/readme/5.png">

 ### Journey ongoing
 When the new journey is created it now shows in the users personal logs page. The current activity in the welcome/activity window has now changed to “On Journey”.
  <img src="static/img/readme/6.png">
  During this day-trip the user can now add new log entries to this journey by clicking the “New log” button at the bottom of the header window.

### New log entry
When creating a new log a log title and description is mandatory (if not what’s the point?). Besides those fields the user can optionally add an image and image capture to the log entry (in this release just one image per entry), and also weather and trip data.
  <img src="static/img/readme/7.png">

  ### The new log entry added to the journey
  The log just created is now added as a collapsible element below the header. There is no limit to how many log entries can be added to a journey. As seen in the image all the data just submitted is presented to the user.
<img src="static/img/readme/8.png">

The new log entry is also presented in the map where a new marker for the log (if coordinates are given) is created and centered upon. Only the most recent log marker in the map has this yellow form. On the right of each header (both journey header and log entry header) there is a switch where either all map markers for the journey, or just one individual log entry marker, can be switched on and off from the map. The marker icon to the left of this switch is used to center on that particular marker in the map.
<img src="static/img/readme/9.png">
A journey can be ended from the “Change activity” dropdown menu.
<img src="static/img/readme/10.png">

Each journey header is created within one single accordion element, and within each log header the logentries are collapsible elements, allowing a very compact overview if many journeys and logs are created.
<img src="static/img/readme/11.png">

### Edit Journeys and log entries
Each Journey header has this edit icon. Clicking it opens up an edit menu for both the header itself and for all of the log entries within that journey.
<img src="static/img/readme/12.png">
<img src="static/img/readme/13.png">

The edit button opens form to update either the journey header data or the data in a single log entry.
<img src="static/img/readme/14.png">
<img src="static/img/readme/15.png">

And the trash can icons remove either a single log entry or a complete journey with all its contents. In both cases a modal is popped open where the user get a warning about deletion and an opportunity to revert the deletion. 

<img src="static/img/readme/16.png">

## USER STORIES

### USER AUTHENTICATION
As a user i wish to...
- #1 - create a new account
- #2 - Login to my personal account
- #3 - Logout from my account
- #4 - Recieve information if I do something not authorized

### USABILITY
As a user I wish to...
- #5 - Create one or many new journeys
  (Title, description, from where, to where, expected distance)
- #6 - Within each journey create log entries
  (Title, note, image, weather data, trip data)
- #7 - See my log entries on a map
- #8 - See my home port in the map
- #9 - Be able to edit, or delete journeys and log entries as I see fit
- #10 - Store my data persistently so that they are accessible when I get back to the site next time

### INFORMATION
As a visitor I wish to…
- #11 - Get information on how to use the features
- #12 - Get general information about what the app is about

## TECHNOLOGIES USED
- HTML 5
- CSS 3 (Bootstrap 4.5.0, Popper 16.0, bootstrap-extension 4.6.1, mdbootstrap 4.19.1, fontawesome 5.13.1)
- JAVASCRIPT (JQuery 3.5.1, popper 1.16.0, bootstrap 4.5.0, bootstrap-extension 4.6.1, mdbootstrap 4.19.1)
- Python 3.8.5
- MongoDB 
- MongoDB Atlas for cloud storage
- Google Maps Javascript API
- Google Fonts
- Font Awesome
- GitHub for version control
- Heroku for deployment
- Visual Studio Code 1.46.1 as IDE
- Google Chrome 84.0.4147.89 (and development tool)
- GIMP 2.10.14 for image manipulation

### DATABASE STRUCTURE

#### Database model
The main collections in the application are:
- users (storing user data)
- log_headers (storing journey header data)
- logs (storing individual log data)

These 3 collections are interconnected with their respective ObjectId.
In the lowest level a log object is connected with a specific log_header and user with the "user_id = user._id" and "head_id = log_headers._id"

<img src="static/img/readme/db_model.png">

The following collections are hard coded and keep data for various options used in menus:
- check_for_user (check if there is a user signed in)
- activity_options (used for change activity dropdown options)
- activity_statuses (used for "Current activity" in the Welcome/Activity window)
- weather_options (used for the various weather options available creating or updating a log entry)
- wind_dir_options (used for the various wind direction options available creating or updating a log entry)
- wind_dir_options (used for the various sub activity options available creating or updating a log entry)

<img src="static/img/readme/db_1.png">
<img src="static/img/readme/db_2.png">
<img src="static/img/readme/db_3.png">
<img src="static/img/readme/db_4.png">
<img src="static/img/readme/db_5.png">
<img src="static/img/readme/db_6.png">
<img src="static/img/readme/db_7.png">
<img src="static/img/readme/db_8.png">
<img src="static/img/readme/db_9.png">

## HOW TO DEPLOY
If you wish to deploy this project of your own take the following steps.

<strong>Clone this project to your own working directory:</strong>

1. In this repository (as you’re reading this readme in it :-) on the top right click the green “Code” button
2. Copy the given url by clicking on the copy icon (or open it up with GitHub Desktop if you have it installed)
3. In your local IDE open Git Bash (or whatever terminal you use to work with Git)
4. Change the current working directory to the location where you want the clone to be created
5. In the terminal type “git clone” and the paste the url you just copied
6. Press Enter. Your local clone will be created in the working directory you’re currently in

Find more details about this procedure <a href="https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository">here</a>

<strong>Set up your local IDE</strong>

You need the latest version of Python 3 installed and you also need to install and import:

- flask
- flask_wtf
- flask_uploads
- flask_pymongo
- bcrypt

I recommend you install these using pip typing "pip3 install packageName" in the terminal

<strong>Set up a MongoDB cloud service</strong>

You need to set up your own MongoDB somewhere. I used Atlas that you find <a href="https://docs.atlas.mongodb.com/getting-started/">here</a> 

If you don’t already have one set up a new account, create a new cluster and within there a new database.

You can name it something different than the name I used, but it is important that the the names of all collections (and key values within) exactly follow the structure described in the "Database structure" section above in this document (Some of theese collections are hard coded while other collections just need to be created empty but with the same name).

In Atlas you also need to whitelist your local machine's ip-address in order for Atlas to grant you access. You can use 0.0.0.0 for limitless access in a development phase, but in a real live deployment it should be set to the ip-adress of server running the app.

Then in the current cluster in the Atlas daschboard, click “Connect” and then “Connect your application”. Select Driver for Python and the latest version in the list. Copy the URI.

In the app.py file you just cloned to your local repository, you need to replace the 
app.config["MONGO_URI"] = os.environ["MONGO_URI"] with the URI you just copied, and app.config["MONGO_DBNAME"] = os.environ["MONGO_DBNAME"] with the name for the database you just set up.
 
I recommend you set it all up in a separate env.py file like this:
os.environ["SECRET_KEY"] = "yourSecretKey" (Any value you wish)
os.environ["MONGO_DBNAME"] = "nameOfTheDataBase" (That you just created)
os.environ["MONGO_URI"] = “Mongo URI” (That you just copied)
Don’t forget to add the env.py to .gitignore. Otherwise it will be pushed onto GitHub where your passwords will be exposed.

You are now ready to work with this project on your local machine. 

<strong>Deploy on Heroku</strong>

1. First you need to create an account on Heroku 
2. Create a new app (Chose region depending on where you live)
3. You can either deploy the project by connecting Heroku to your GitHub repository (follow the instructions on Heroku site)
4. Or use the Heroku CLI (Install the Heroku CLI <a href="https://devcenter.heroku.com/articles/heroku-cli">from here</a>)
5. Once Heroku CLI is installed, login to Heroku by typing “heroku login” in the CLI and you will be redirected to a web browser window where you log in. 
6. Then use Git to clone (app name) source code to your local machine (even if it is already cloned this must be done again). Type: “$ heroku git:clone -a (name of repository you are using)” in the CLI
7. Make this new dir (name of repository) your working directory with command "cd (name of repository)"
8. Make some small change to the code you just cloned in order to be able to push it to Git
9. Stage all files for commit to Git with the command “git add .” + enter
10. Commit to Git with “commit -m (Some commit message)“ + enter
11. Finally in the CLI type "git push heroku master"
12. In a while after a lot of stuff flying past you on the screen has stopped flying past you, the project should be deployed

## TESTING
The test is done manualy in the following browsers:
- Google Chrome 84.0.4147.89 (on PC Windows 10)
- Microsoft Edge Chromium 84.0.522.44 (on PC Windows 10)
- Firefox 78.0.2 (on PC Windows 10)
- Safari (on iPad pro 10.5 iOS 13.6.1)

The testing is done from the perspective of each user story (presented above) in regards of functionality and responsivity.

<img src="static/img/readme/test.png">

## UX

### STRATEGY - PROJECT GOAL
Today most boat owners bring a touchscreen device or a laptop with them on their travels. The goal with this project is to make an app making it easy and fun for recreational boat owners to store ship log entries for Journeys undertaken with their boat using modern technology. See it as a collection of memories in form of notes, images, weather and navigational data.

### SCOPE
The scope for this first MVP version focuses around the users basic abilities to create, view, update and delete log entries (CRUD operations). As a first conceptual product proving the usability of an app like this, the most important aspect is to get the user experience as smooth, intuitive and easy to use as possible. 
 
In a product like this the sheer amount of entries of different types can get immense. Therefore aspects like how the data is presented (structure) is possibly of more importance at this stage, than cool design (even if they are closely related of course)

As the user stories presented above tells focus in this version will be in:
- Authentication (Sign up, sign in, log out)
- Personal space page where the user can view and work with their journeys and logs in an efficient, easy to use and intuitive way.
- Get a basic Google maps up and running marking logs
- This first MVP version is very focused on one single users needs to create and store logs for personal use.

#### Future updates
Features that were thought of but did not make this version includes:
- Present the log info on the map in a info window on each marker
- Ability to filter journeys and log entries for various needs
- Search the database for entries in journeys and logs
- Pagination for journeys and log entries 
- Add ability to add independent log entries not sorted under a specific journey, i.e when the user is in the home port
- Add ability to add issues, service and repair notes
- Add a calendar for events
- Add ability to add to do lists (possibly connected to the above point)
- Add ability to store important information and documents concerning the boat and everything around (i.e manuals, how to guides, important contacts, phone numbers etc.)
- Save favorite locations on the map with some information

The long term ambition with this product is to create a sort of community for recreational boat owners where they also can share information and experiences with each other in discussions and some sort of commenting system.

### STRUCTURE
Most of the main content for the user, that is Journeys and log entries and the map, are rendered on the index template. 
 
Except for that there are just a few supporting templates for adding new entries, updating existing entries, delete entries and for user authentication purposes.

### SKELETON
This is the original wireframe made for this project

<img src="static/img/readme/main_personal_page_WireFrame.png">

I guess the current outcome is not too far from these wireframes with the exception that the map now is hidden on screens with less width than 768px.

### SURFACE
Since this project is more about working with Python and MongoDB than design, I have kept it simple using mostly standard Bootstrap elements extended with some libraries, like "Material Design for Bootstrap".
 
For the very same reason I am just using the Roboto font imported from Google fonts.
 
Future updates could certainly benefit from some refactoring of the design.
 
Other than that, since this is about boats and the ocean, I have chosen to keep the base colors in different variations of blue. Exceptions for user feedback information and warnings where I use some red and orange.
 
Text is in most parts simply either white (or light grey) on dark backgrounds, and dark grey on lighter backgrounds.

## CREDITS

### MEDIA
- LOGOTYPE - pngguru @ https://www.pngguru.com/free-transparent-background-png-clipart-bbegd

- BACKGROUND IMAGE - Wallpaperplay @ https://wallpaperplay.com/walls/full/d/0/5/213076.jpg

- FAVICON IMAGE - 123RF @ https://es.123rf.com/photo_138670176_stock-vector-ship-steering-wheel-logo-design-template-vector-icon.html

### CODE

- LOGIN AUTHENTICATION - 
Pretty Printed @ https://www.youtube.com/watch?v=vVx1737auSE

- IMAGE UPLOADS - 
Pretty Printed @ https://www.youtube.com/watch?v=HNw6shJv9Ck

- GOOGLE MAPS SETUP - 
Traversy Media @ https://www.youtube.com/watch?v=Zxf1mnP5zcw

### AKNOWLEDGEMENTS
Special thank you to my course tutor at Code Institute Cormac Lawlor and my dedicated mentor for this course Aaron Sinnott for all good advice and help along the way!













