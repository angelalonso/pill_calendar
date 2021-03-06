import data as dat
import events
import cals

def newCal(service, cal_name):
  calendar = {'summary': cal_name}
  created_calendar = service.calendars().insert(body=calendar).execute()

def delCal(service, cal_name):
  calID = getIDCal(service, cal_name)
  service.calendars().delete(calendarId=calID).execute()
            

def getIDCal(service, cal_name):
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
  csv_events = dat.CSV2DictArray(file_in)
 #TODO: the following can be substituted for the online service list
  online_events = csvs.readintoArray('online.csv')
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
  cal_id = cals.getIDCal(service, cal_name)
  # lists
  csv_events = dat.CSV2DictArray(csv_file)
  online_events = events.online2DictArray(service, getIDCal(service, cal_name), firstyear, lastyear)
  for csv_event in csv_events:
    if (csv_event['event_id'] == ""):
      print("##new one: " + str(csv_event))
      events.addEvent(service, dat.DictEntry2Gcal(csv_event), cal_id)
    else:
      for onl_event in online_events:
      # Changed something on an existing ID?
        if (csv_event['event_id'] == onl_event['event_id']):
          if (csv_event['start_datetime'] != onl_event['start_datetime']
           or csv_event['end_datetime'] != onl_event['end_datetime']  
           or csv_event['description'] != onl_event['description']
           or csv_event['summary'] != onl_event['summary']):
            chosen_event = conflict(csv_event,onl_event)
            events.updateEvent(service, cal_id, dat.DictEntry2Gcal(chosen_event), chosen_event['event_id'] )
      
