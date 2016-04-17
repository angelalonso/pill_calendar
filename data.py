#
#
#

from datetime import datetime
import csv

def CSVdatetime2gcal(date, time, zone):
  datetime_in = datetime.strptime(date + '-' + time,"%m/%y/%d-%I:%M:%S %p")
  datetime_out = datetime_in.strftime('%Y-%m-%dT%H:%M:%S' + zone)
  return datetime_out

def CSV2DictArray(file_in):
  resultArray = []
  csv_file = open(file_in)
  resultDict = csv.DictReader(csv_file)
  for row in resultDict:
    resultArray.append(row)
  return resultArray

def DictArray2CSV(eventsDictarray):
  print("event_id,summary,description,start_datetime,end_datetime")
  for row in eventsDictarray:
    print(row['event_id'] + "," + row['summary'] + "," + row['description'] + "," + row['start_datetime'] + "," + row['end_datetime'])

def DictArray2CSVFile(eventsDictarray, csv_file):
  f = open(csv_file,"w") 
  f.write("event_id,summary,description,start_datetime,end_datetime\n")
  for row in eventsDictarray:
    f.write(row['event_id'] + "," + row['summary'] + "," + row['description'] + "," + row['start_datetime'] + "," + row['end_datetime'] + "\n")
  f.close()

def DictEntry2Gcal(event):
    # TODO: summary? subject?
  jsonevent = {
    'summary': event['summary'],
    'description': event['description'],
    'start': {
       'dateTime': event['start_datetime'],
    },
    'end': {
       'dateTime': event['end_datetime'],
     },
    'reminders': {
      'useDefault': False,
      'overrides': [
        {'method': 'popup', 'minutes': 10},
      ],
    },
  }

  return jsonevent

if __name__ == '__main__':
    print(csvdatetime2gcal('01/16/18', '09:00:00 PM', '+01:00'))

