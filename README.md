Application to control the amount of pills to be taken from Google Calendar

Based on:
https://developers.google.com/google-apps/calendar/quickstart/python

Installation:

Not much, just make sure you have everything python-ready:
sudo apt-get install python-pip python-dev build-essential
sudo pip install httplib2

get the client_secret.json too, as well as the .credentials files.
Also remember to first run the following to get the credentials right(*): 

python RUNME.py

(*) if anything goes wrong or you want to get rid of these credentials:
rm ~/.credentials/*

python pill_calendar.py delcal
python pill_calendar.py newcal
python pill_calendar.py loadcsv
