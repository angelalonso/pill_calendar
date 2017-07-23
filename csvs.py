#
#
# Based on
# http://stackoverflow.com/questions/17413261/retrieve-first-row-of-csv-using-dictionary
#

import csv

def readintoArray(file_in):
  resultArray = []
  csv_file = open(file_in)
  resultDict = csv.DictReader(csv_file)
  for row in resultDict:
    resultArray.append(row)
  return resultArray
