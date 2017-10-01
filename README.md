Application to control the amount of pills to be taken from Google Calendar

Based on:
https://developers.google.com/google-apps/calendar/quickstart/python


# Pre-requisites:

(ubuntu)
sudo apt-get install python-pip python-dev build-essential
<br>
sudo pip install httplib2
<br>
sudo pip install --upgrade google-api-python-client
<br><br>
# Credentials
You'll need to get your creds under ~/.credentials/pill_cal.json

## How to get your own credentials?
This needs to be updated, still the original method was:
<br><br>
Get your Google API credentials and store them under client_secret.json
<br>
The first time you run it, it will open a webbrowser to authenticate through your user and store the credentials on .credentials/calendar-python-quickstart.json (Yeah I copied the doc's example)
<br>

# Data
Create a csv file on the installation directory, named Calendar.csv, with the following fields as first line:<br>
"event_id","summary","description","start_datetime","end_datetime"<br>
, then add your own entries with the event_id column empty.


# Usage
python pill_cal.py update
... to read entries from your CSV, upload to Google Calendar, and then download the whole list back (including the assigned event ids)

# Known issues


