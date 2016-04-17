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
  for row in eventsDictarray:
    print(str(row))

if __name__ == '__main__':
    print(csvdatetime2gcal('01/16/18', '09:00:00 PM', '+01:00'))

