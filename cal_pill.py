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
import httplib2
import os
import sys
# Then the Google API related ones
from apiclient import discovery
import oauth2client
# Finally, the other py files in this directory
import cals
import events
import data as dat


""" CONSTANTS
"""
# ONLINE = 'false'
ONLINE = 'true'
CAL_NAME = 'Pill_Calendar'
CSV_FILE = 'Calendar.csv'
ZONE = '+02:00'
FIRSTYEAR = 2012
LASTYEAR = 2020


def showhelp(exitcode):
  print(sys.argv[0] + ' [update|list|download|upload|clearcal||delcal|newcal|loadcsv|readcsv*|loadcsv*|getID*|clearcal*|newevent*|listcalendars*|getID*]')
  sys.exit(exitcode)


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
                                 'pill-calendar-python.json')

  store = oauth2client.file.Storage(credential_path)
  credentials = store.get()
  if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    flow.user_agent = APPLICATION_NAME
    flags = None
    if flags:
      credentials = tools.run_flow(flow, store, flags)
    else:  # Needed only for compatibility with Python 2.6
      credentials = tools.run(flow, store)
    print('Storing credentials to ' + credential_path)
  return credentials


def main(argv):
  """Shows basic usage of the Google Calendar API.

  Creates a Google Calendar API service object
  and proceeds according to parameters
  """
  if (ONLINE != 'false'):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

  try:
    if sys.argv[1] == "list":
      dat.DictArray2CSV((events.online2DictArray(service, cals.getIDCal(service, CAL_NAME), FIRSTYEAR, LASTYEAR)))
      # TODO: Download directly to CSV; ask before
    if sys.argv[1] == "download":
      dat.DictArray2CSVFile((events.online2DictArray(service, cals.getIDCal(service, CAL_NAME), FIRSTYEAR, LASTYEAR)), CSV_FILE)
    if sys.argv[1] == "upload":
      events.uploadCSV(service, CSV_FILE, CAL_NAME, ZONE, FIRSTYEAR, LASTYEAR)
    if sys.argv[1] == "update":
      cals.updatefromCSV(service, CSV_FILE, CAL_NAME, ZONE, FIRSTYEAR, LASTYEAR)
      dat.DictArray2CSVFile((events.online2DictArray(service, cals.getIDCal(service, CAL_NAME), FIRSTYEAR, LASTYEAR)), CSV_FILE)
    if sys.argv[1] == "clearcal":
      #TODO: Ask the user before deleting!!
      cals.delCal(service, CAL_NAME)
      cals.newCal(service, CAL_NAME)
    elif sys.argv[1] == "test":
      print(cals.updateOnline("test.csv"))
  except IndexError:
    showhelp(2)

if __name__ == '__main__':
  main(sys.argv[1:])

