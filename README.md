# YOUR DIGITAL LOG BOOK
<img src="static/img/logo.png">

## AN INTERACTIVE LOG BOOK FOR YOUR BOAT
### A Code Institute Student Project

## SUMMARY
This project aims to create a digital interactive log book for recreational boats and ships. As tradition on the seas offer, for recreational sailors often these logs are done in a physical logbook by pen and paper. In such a logbook normally the ship's captain enters a log daily, reporting navigational information such as heading, speed. Weather information such as wind direction, wind speed, weather conditions etc. Also there are usually  some notes about important events happening onboard the ship, like accidents, if something needs to be repaired, if the ship got new provisions, entered dock for unload, load etc. In the professional merchant fleet such log entries are mandatory and part of the international regulations. But for recreational ships and boats it is not. While many boat owners keep such a logbook in their ship/boat, often they mostly stay in a drawer collecting dust.

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

### User authentication
As a user i wish to...
- create a new account
- Login to my personal account
- Logout from my account
- Recieve information if I do something not authorized
- Be sure the data I submit is correct (defensive design)

### Usability
As a user I wish to...
- Create one or many new journeys
  (Title, description, from where, to where, expected distance)
- Within each journey create log entries
  (Title, note, image, weather data, trip data)
- See my log entries on a map
- See my home port in the map
- Be able to edit, or delete journeys and log entries as I see fit
- Store my data persistently so that they are accessible when I get back to the site next time

### INFORMATION
As a visitor I wish to…
- Get information on how to use the features
- Get general information about what the app is about




