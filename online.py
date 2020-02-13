import httplib2
import json
import os
import time
from googleapiclient import discovery
from oauth2client.file import Storage
import pill_calendar as pc


''' CONNECTION FUNCTIONS '''


def getCredentials():
    '''Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    '''
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'pill_cal.json')

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


def getConnection():
    ''' Gets a Connection/Service
          from the credentials installed
    '''
    credentials = getCredentials()
    http_handler = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http_handler)
    return service


def getIDCal(service, cal_name):
    ''' Gets the ID for a given Calendar Name
    '''
    resultList = []
    page_token = None
    while True:
        cal_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in cal_list['items']:
            if calendar_list_entry['summary'] == cal_name:
                resultList.append(calendar_list_entry['id'])
        page_token = cal_list.get('nextPageToken')
        if not page_token:
            break
    return resultList[0]


''' HELPER FUNCTIONS '''


def getCSVStructEntry(online_entry):
    ''' Given an entry from Google Calendar
          it builds the entry with only the fields
          that our local CSV needs
    '''
    entry = {}
    entry['event_id'] = online_entry['id']
    entry['summary'] = online_entry['summary']
    entry['description'] = online_entry['description']
    entry['start_datetime'] = online_entry['start']['dateTime']
    entry['end_datetime'] = online_entry['end']['dateTime']
    
    return entry


''' I/O FUNCTIONS '''


def loadCalendar(service, calID, firstyear, lastyear):
    ''' Load online Calendar into memory
    '''
    pc.verbose("Downloading current entries at Google Calendar...", 1)
    calendar_data = []
    for numyear in range(firstyear, lastyear):
        year = str(numyear)
        for month in ('01', '02', '03', '04', '05', '06', '07', '08', '09',
                      '10', '11', '12'):
            thisMin = year+'-'+month+'-01T00:00:00Z'
            if month == '12':
                nextyear = str(int(year)+1)
                thisMax = nextyear+'-01-01T00:00:00Z'
            else:
                nextmonth = str(int(month)+1).zfill(2)
                thisMax = year+'-'+nextmonth+'-01T00:00:00Z'
            eventsResult = service.events().list(
                calendarId=calID, timeMin=thisMin, timeMax=thisMax,
                singleEvents=True, orderBy='startTime').execute()
            events = eventsResult.get('items', [])
            if not events:
                pass
            else:
                for event in events:
                    entry = getCSVStructEntry(event)
                    calendar_data.append(entry)
    return calendar_data


def createCalendar(service, cal_name):
    ''' Create a google calendar with the given name
    '''
    calendar = {'summary': cal_name}
    created_calendar = service.calendars().insert(body=calendar).execute()


def deleteCalendar(service, cal_name):
    ''' Delete a google calendar given its name
    '''
    calID = getIDCal(service, cal_name)
    service.calendars().delete(calendarId=calID).execute()
            

def addEvent(service, event, cal_id):
    ''' Add a new Event to the Google Calendar
          defined by the Calendar ID
    '''
    new_event = service.events().insert(calendarId=cal_id, body=event).execute()
    print ('Event created: ' + str(new_event))


def updateEvent(service, cal_id, event, event_id ):
    ''' Modify an Event, given the event's ID,
          on the Google Calendar defined by the Calendar ID
    '''
    updated_event = service.events().update(calendarId=cal_id, eventId=event_id, body=event).execute()
    print ('Event updated: ' + str(updated_event))


''' TO BE DELETED/CORRECTED '''


def conflict(event_offline, event_online):
  errors = []
  tests = ['event_id','start_datetime','end_datetime','description','summary']
  for test in tests:
    if (event_offline[test] != event_online[test]):
      errors.append(test)
  print("Attention! change on entry " + event_online['event_id'])
  for error in errors:
    print('- ' + error + ' old: ' + event_online[error] + ', new: ' + event_offline[error])
  print('Do you want to overwrite? ') 
  answer = 'wrong'
  while (answer != 'n' and answer != 'no' and
         answer != '' and answer != 'y' and answer != 'yes'):
    answer = raw_input("(y/n, default y) > ").lower()
  if (answer == 'y' or answer == 'yes' or answer == ''):
    return event_offline
  else:
    return event_online
    

def updateOnline(file_in):
  csv_events = pc.CSV2DictArray(file_in)
 #TODO: the following can be substituted for the online service list
  #online_events = csvs.readintoArray('online.csv')
  online_events = pc.loadCalendarFile('online.csv')
#TODO: add id-les, compare, update clear ones, show conflicts, ask for decision, automate decision
# same id, different calendar, different content -> default choose offline but show and  offer to revert
# different id, different calendar, same content <- update, choose offline, show message
  for csv_event in csv_events:
    if (csv_event['event_id'] == ""):
      print("##new one: " + str(csv_event))
    else:
      for onl_event in online_events:
      # Changed something on an existing ID?
        if (csv_event['event_id'] == onl_event['event_id']):
          if (csv_event['start_datetime'] != onl_event['start_datetime']
           or csv_event['end_datetime'] != onl_event['end_datetime']  
           or csv_event['description'] != onl_event['description']
           or csv_event['summary'] != onl_event['summary']):
            print('##conflict, chose: ' + str(conflict(csv_event,onl_event)))
# same id, same calendar different content
# different id, same calendar, same content -< clean up automatically(choose one), show message
# cleanup_cal(csv_event)
# cleanup_cal(onl_event)
  return ""

def updatefromCSV(service, csv_file, cal_name, zone, firstyear, lastyear):
  cal_id = getIDCal(service, cal_name)
  # lists
  csv_events = pc.CSV2DictArray(csv_file)
  online_events = online2DictArray(service, getIDCal(service, cal_name), firstyear, lastyear)
  for csv_event in csv_events:
    if (csv_event['event_id'] == ""):
      print("##new one: " + str(csv_event))
      addEvent(service, pc.DictEntry2Gcal(csv_event), cal_id)
    else:
      for onl_event in online_events:
      # Changed something on an existing ID?
        if (csv_event['event_id'] == onl_event['event_id']):
          if (csv_event['start_datetime'] != onl_event['start_datetime']
           or csv_event['end_datetime'] != onl_event['end_datetime']  
           or csv_event['description'] != onl_event['description']
           or csv_event['summary'] != onl_event['summary']):
            chosen_event = conflict(csv_event,onl_event)
            updateEvent(service, cal_id, pc.DictEntry2Gcal(chosen_event), chosen_event['event_id'] )
     
''' OLD EVENTS '''


## TODO: to be deleted
def listonline(service, calID, firstyear, lastyear):
    eventsList = []
    for numyear in range(firstyear, lastyear):
        year = str(numyear)
        for month in ('01', '02', '03', '04', '05', '06', '07', '08', '09',
                      '10', '11', '12'):
            thisMin = year+'-'+month+'-01T00:00:00Z'
            if month == '12':
                nextyear = str(int(year)+1)
                thisMax = nextyear+'-01-01T00:00:00Z'
            else:
                nextmonth = str(int(month)+1).zfill(2)
                thisMax = year+'-'+nextmonth+'-01T00:00:00Z'
            eventsResult = service.events().list(
                calendarId=calID, timeMin=thisMin, timeMax=thisMax,
                singleEvents=True, orderBy='startTime').execute()
            events = eventsResult.get('items', [])

            if not events:
                pass
            else:
                for event in events:
                    eventsList.append(event)
    return eventsList

def online2DictArray(service,calID,firstyear,lastyear):
  resultArray = []
  eventslist = listonline(service,calID,firstyear,lastyear)
# TODO: for each one, transform to JSON, read from there, show only needed fields
# http://stackoverflow.com/questions/13940272/python-json-loads-returns-items-prefixing-with-u
# eventslist[0] is a dict
  for event in eventslist:
    row = {}
    j_event = json.loads(json.dumps(event, ensure_ascii=False))
    #Good test for "description key error"
    #print(j_event)
    event_id = j_event["id"]
    summary = j_event["summary"]
    description = j_event["description"]
    start_datetime = j_event["start"]["dateTime"]
    end_datetime = j_event["end"]["dateTime"]
    row['event_id'] = event_id
    row['start_datetime'] = start_datetime
    row['end_datetime'] = end_datetime
    row['description'] = description
    row['summary'] = summary
    resultArray.append(row)

  return resultArray
## TODO: deprecate the old format, use the new one

def uploadCSV(service, csv_file, cal_name, zone, firstyear, lastyear):
  cal_id = online.getIDCal(service, cal_name)
  entryDictArray = pc.CSV2DictArray(csv_file)
  for year in range(firstyear, lastyear):
    time.sleep(5)
    for entry in entryDictArray:
      if (str(year) == pc.CSVdatetime2gcal(entry['Start Date'], entry['Start Time'], zone).split('-')[0]):
        event = {
              'summary': entry['Subject'],
              'description': entry['Description'],
              'start': {
                       'dateTime': pc.CSVdatetime2gcal(entry['Start Date'], entry['Start Time'], zone),
                       },
              'end': {
                     'dateTime': pc.CSVdatetime2gcal(entry['End Date'], entry['End Time'], zone),
                     },
              'reminders': {
                           'useDefault': False,
                           'overrides': [
                                        {'method': 'popup', 'minutes': 10},
                                        ],
                           },
              }
        addEvent(service, pc.DictEntry2Gcal(event), cal_id)


def deleteEvent(service, event, cal_id, event_id):
  service.events().delete(calendarId=cal_id, eventId=event_id).execute()
