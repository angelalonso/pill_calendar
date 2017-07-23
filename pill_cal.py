# Google Calendar API, focused on a pill-taking schedule
#
# This file is based on the Pytohn quickstart in:
#   https://developers.google.com/google-apps/calendar/quickstart/python
#
# Created by Angel Alonso Fonseca
#

""" Imports
"""
# First, general imports
from __future__ import print_function
import httplib2
import os
import sys

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None

# Finally, the other py files in this directory
import cals
import events
import data as dat


""" CONSTANTS
"""
## Scopes
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Pill Calendar'
## End of Scopes
# ONLINE = 'false'
ONLINE = 'true'
CAL_NAME = 'Pill_Calendar'
CSV_FILE = 'Calendar.csv'
ZONE = '+02:00'
FIRSTYEAR = 2012
LASTYEAR = 2020


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'pill_cal.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def showhelp(exitcode):
  print(sys.argv[0] + ' [update|list|download|upload|clearcal||delcal|newcal|loadcsv|readcsv*|loadcsv*|getID*|clearcal*|newevent*|listcalendars*|getID*]')
  sys.exit(exitcode)


def main(mode):
  """Shows basic usage of the Google Calendar API.

  Creates a Google Calendar API service object
  and proceeds according to parameters
  """
  if (ONLINE != 'false'):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

  try:
    if mode == "list":
      dat.DictArray2CSV((events.online2DictArray(service, cals.getIDCal(service, CAL_NAME), FIRSTYEAR, LASTYEAR)))
      # TODO: Download directly to CSV; ask before
    if mode == "download":
      dat.DictArray2CSVFile((events.online2DictArray(service, cals.getIDCal(service, CAL_NAME), FIRSTYEAR, LASTYEAR)), CSV_FILE)
    if mode == "upload":
      events.uploadCSV(service, CSV_FILE, CAL_NAME, ZONE, FIRSTYEAR, LASTYEAR)
    if mode == "update":
      cals.updatefromCSV(service, CSV_FILE, CAL_NAME, ZONE, FIRSTYEAR, LASTYEAR)
      dat.DictArray2CSVFile((events.online2DictArray(service, cals.getIDCal(service, CAL_NAME), FIRSTYEAR, LASTYEAR)), CSV_FILE)
    if mode == "clearcal":
      #TODO: Ask the user before deleting!!
      cals.delCal(service, CAL_NAME)
      cals.newCal(service, CAL_NAME)
    elif mode == "test":
      print(cals.updateOnline("test.csv"))
  except IndexError:
    showhelp(2)

if __name__ == '__main__':
  try:
    mode = sys.argv[1]
  except IndexError:
    showhelp(2)
  main(mode)

