# This file is based on the Pytohn quickstart in:
#   https://developers.google.com/google-apps/calendar/quickstart/python
#
#

""" Imports
"""
# First, general imports
from __future__ import print_function
import httplib2
import os
import sys
# Then the Google API related ones
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
# Finally, the other py files in this directory
import event_funcs as events
import calendar_funcs as cals


""" Definition of some constants that Google needs
"""
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


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


def preview(service):
    pass


def showhelp(exitcode):
    print(sys.argv[0] + ' <inputfile> -o <outputfile>')
    sys.exit(exitcode)


def main(argv):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object
      and proceeds according to parameters
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    try:
        if sys.argv[1] == "readcsv":
            events.listCsv()
        elif sys.argv[1] == "newcal":
            try:
                cals.create_if_notexisting(service, sys.argv[2])
            except IndexError:
                showhelp(2)
        elif sys.argv[1] == "newevent":
            events.add(service)
        elif sys.argv[1] == "listcal":
            print(cals.list(service))
        elif sys.argv[1] == "getID":
            try:
                search_word = sys.argv[2]
            except IndexError:
                search_word = ""
            events.getIDEvent(service, search_word)
        else:
            preview(service)
    except IndexError:
        events.listEvents(service)


if __name__ == '__main__':
    main(sys.argv[1:])
