Application to control the amount of pills to be taken from Google Calendar

Based on:
https://developers.google.com/google-apps/calendar/quickstart/python


# Installation:

Not much, just make sure you have everything python-ready:
<br>
sudo apt-get install python-pip python-dev build-essential
<br>
sudo pip install httplib2
<br>
sudo pip install --upgrade google-api-python-client
<br><br>
Get your Google API credentials and store them under ~/.credentials/pill-calendar-python.json
<br>
Create a csv file on the installation directory, named Calendar.csv, with the following fields as first line:<br>
"event_id","summary","description","start_datetime","end_datetime"<br>
, then add your own entries with the event_id column empty.


# Usage
python cal_pill.py update
... to read entries from your CSV, upload to Google Calendar, and then download the whole list back (including the assigned event ids)

# Known issues
Error (...) summary field (...) invalid
<br>
This is probably because your CSV file
Then do the regular run with:

