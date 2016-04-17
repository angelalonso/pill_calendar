from datetime import datetime
import json
import time
import data as dat
import cals

def listonline(service,calID,firstyear,lastyear):
    
    eventsList = []
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' for UTC time
    for numyear in range(firstyear, lastyear):
        year=str(numyear)
        for month in ('01','02','03','04','05','06','07','08','09','10','11','12'): 
            thisMin=year+'-'+month+'-01T00:00:00Z'
            if month == '12':
                nextyear=str(int(year)+1)
                thisMax=nextyear+'-01-01T00:00:00Z'
            else:
                nextmonth=str(int(month)+1).zfill(2)
                thisMax=year+'-'+nextmonth+'-01T00:00:00Z'
            eventsResult = service.events().list(
                calendarId=calID, timeMin=thisMin, timeMax=year+'-'+nextmonth+'-01T00:00:00Z',
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
  #print("event_id,subject,description,start_datetime,end_datetime,")
  for event in eventslist:
    j_event = json.loads(json.dumps(event, ensure_ascii=False))
    event_id = j_event["id"]
    subject = j_event["summary"]
    description = j_event["description"]
    start_datetime = j_event["start"]["dateTime"]
    end_datetime = j_event["end"]["dateTime"]
    #print(event_id + "," + subject + "," + description + "," + start_datetime + "," + end_datetime + ",")
    row = (event_id + "," + subject + "," + description + "," + start_datetime + "," + end_datetime + ",")
    row = "{'event_id': '" + event_id + "', 'start_datetime': '" + start_datetime + "', 'end_datetime': '" + end_datetime + "', 'description': '" + description + "', 'subject': '" + subject + "'}"
    resultArray.append(row)

  return resultArray
## TODO: deprecate the old format, use the new one

def uploadCSV(service, csv_file, cal_name, zone, firstyear, lastyear):
  cal_id = cals.getIDCal(service, cal_name)
  entryDictArray = dat.CSV2DictArray(csv_file)
  for year in range(firstyear, lastyear):
    time.sleep(5)
    for entry in entryDictArray:
      if (str(year) == dat.CSVdatetime2gcal(entry['Start Date'], entry['Start Time'], zone).split('-')[0]):
        event = {
              'summary': entry['Subject'],
              'description': entry['Description'],
              'start': {
                       'dateTime': dat.CSVdatetime2gcal(entry['Start Date'], entry['Start Time'], zone),
                       },
              'end': {
                     'dateTime': dat.CSVdatetime2gcal(entry['End Date'], entry['End Time'], zone),
                     },
              'reminders': {
                           'useDefault': False,
                           'overrides': [
                                        {'method': 'popup', 'minutes': 10},
                                        ],
                           },
              }
        addEvent(service, event, cal_id)

def addEvent(service, event, cal_id):
  event = service.events().insert(calendarId=cal_id, body=event).execute()
  print ('Event created: ' + str(event))

