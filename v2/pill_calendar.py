from __future__ import print_function
import httplib2
from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
''' END - obsolete imports? '''
'''
  We assume there is only one entry for a given start_datetime
  TODO: - Check and alert when it's not the case
'''
import csv
import datetime
import itertools
import os
import sys
import yaml
import online

CSV_FILE = 'test_files/Calendar.csv'

class bcolors:
    # stole this from stackoverflow
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'


''' HELPER FUNCTIONS '''


def getEnvVar(env_var):
    ''' Helper function to Error properly if a required environment variable is not set
    '''
    if env_var in os.environ:
        return os.environ[env_var], 0
    else:
        return 'Environment Variable ' + env_var + ' not defined', 2


def verbose(message, level):
    ''' Helper function to show different visuals on messages
    '''
    if level == 0:
        print(bcolors.BOLD + str(message) + bcolors.ENDC)
    elif level == 1:
        print("-> " + str(message))
    elif level == 2:
        print(" --> " + str(message))
    elif level == 3:
        print("  ---> " + str(message))
    elif level == 'debug':
        print(bcolors.BLUE + "DEBUG: " + bcolors.ENDC + bcolors.BOLD
              + str(message) + bcolors.ENDC)  # noqa W503
    elif level == 'warn':
        print(bcolors.YELLOW + "WARN: " + bcolors.ENDC + bcolors.BOLD
              + str(message) + bcolors.ENDC)  # noqa W503
    elif level == 'error':
        print(bcolors.RED + "ERROR: " + bcolors.ENDC)
        print("         " + str(message))
        sys.exit(1)
    else:
        print("         " + str(message))


''' I/O FUNCTIONS '''


def loadCalendarFile(csv_file):
    ''' Load CSV file into memory
    '''
    calendar_data = []
    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for dct in map(dict, reader):
            calendar_data.append(dct)
    return calendar_data


def saveCalendarFile(entries, cal_file):
    ''' Save entries in CSV format
    '''
    f = open(cal_file,"w") 
    f.write("event_id,summary,description,start_datetime,end_datetime\n")
    for row in entries:
      f.write(row['event_id'] + "," + row['summary'] + "," + row['description'] + "," + row['start_datetime'] + "," + row['end_datetime'] + "\n")
    f.close()


''' MAIN FUNCTIONS '''


def createEntries(start, day_count, pattern):
    result = []
    start_date = datetime.date(int(start.split('/')[2]), int(start.split('/')[1]), int(start.split('/')[0]))
    pattern_ix = 0
    for date in (start_date + datetime.timedelta(n) for n in range(day_count)):
        entry = {}
        formatted_date = date.strftime('%Y-%m-%d')
        entry['start_datetime'] = formatted_date + 'T18:45:00Z'
        entry['end_datetime'] = formatted_date + 'T20:15:00Z'
        entry['event_id'] = ''
        ix = pattern_ix % len(pattern)
        entry['summary'] = entry['description'] = 'Sintrom Amount: ' + str(pattern[ix])
        result.append(entry)
        pattern_ix += 1
    return result


def addEntries(data_set, new_entries):
    result = getCommonEntries(data_set, new_entries)
    return result


def addEntry(data_set, start_datetime, end_datetime, description):
    entry = {}
    entry['event_id'] = ''
    entry['start_datetime'] = start_datetime
    entry['end_datetime'] = end_datetime
    entry['description'] = description
    entry['summary'] = description
    data_set.append(entry)
    return data_set


def getEntries(data_set, entry_type):
    ''' From a data set, get only entries
          that belong in a predefined category
    '''
    result = []
    if entry_type == 'Blood Level':
        result = []
        for item in data_set:
            if 'Blood' in item['summary']:
                result.append(item)
        return result
    elif entry_type == 'Pills':
        for item in data_set:
            if 'Amount' in item['summary']:
                result.append(item)
        return result


def getNewTestDate(previous_test_entry):
    ''' From the previous date, get the next 6 Saturdays
          Make the user choose, default is in 4 weeks
    '''
    prev_date = datetime.datetime.strptime(previous_test_entry['start_datetime'], '%Y-%m-%dT%H:%M:%SZ')
    date = prev_date
    found_dates = []
    while len(found_dates) < 6:
        date += datetime.timedelta(1)
        if date.strftime('%A') == 'Saturday':
            found_dates.append(date)

    print('Choose the date for your next test:')
    for ix in range(len(found_dates)):
        print('[' + str(ix + 1) + '] - ' + found_dates[ix].strftime('%d/%m/%Y'))
    while True:
        try:
            response = int(input("Choose one (1-" + str(len(found_dates)) + ") ")) - 1
        except ValueError:
            print("Please enter a number between 1 and " + str(len(found_dates)))
        if response < len(found_dates):
            return found_dates[response]
        else:
            print("Please enter a number between 1 and " + str(len(found_dates)))


def mergeEntries(group_a, group_b):
    ''' Find common entries,
          ask for confirmation on which version to use,
          and put them on a third group.
          Finally, append all three groups
    '''
    # List of entries that exist on both groups
    common_entries = []
    # List of entries that only exist on group a
    clean_group_a = []
    # List of entries that only exist on group b
    clean_group_b = []
    # Amount of entries that our merge will change
    changed = 0
    for a_entry in group_a:
        new_a_entry = True
        for b_entry in group_b:
            if a_entry['start_datetime'] == b_entry['start_datetime']:
                new_a_entry = False
                overwrite, changes_nr = overwriteAfterConfirm(a_entry, b_entry)
                if overwrite == True:
                    replace_entry = {'start_datetime': b_entry['start_datetime'],
                        'end_datetime': b_entry['end_datetime'],
                        'summary': b_entry['summary'],
                        'description': b_entry['description'],
                        'event_id': a_entry['event_id']}
                    common_entries.append(replace_entry)
                    changed += 1
                else:
                    common_entries.append(a_entry)
        if new_a_entry:
            clean_group_a.append(a_entry)
    for b_entry in group_b:
        new_b_entry = True
        for common_entry in common_entries:
            if b_entry['start_datetime'] == common_entry['start_datetime']:
                new_b_entry = False
        if new_b_entry:
            clean_group_b.append(b_entry)
    result = clean_group_a + common_entries + clean_group_b
    print("\n" + bcolors.YELLOW + str(changed) + " CHANGED, " + bcolors.BLUE + str(len(clean_group_b)) + " NEW" + bcolors.ENDC)
    return result


def overwriteAfterConfirm(entry_a, entry_b):
    '''
    Shows changes to be done, and returns
      if the change has to take place
      e.g.: no change needed or user said no, both mean False
    '''
    changes = []
    for parameter in ['start_datetime', 'end_datetime', 'summary', 'description']:
        if entry_a[parameter] != entry_b[parameter]:
            changes.append(parameter)
    if len(changes) > 0:
        print("\nChanging entry for " + entry_a['start_datetime'])
        for parameter in changes:
            print(parameter + ':\t' + entry_a[parameter] + ' -> ' + bcolors.YELLOW + entry_b[parameter] + bcolors.ENDC)
        if not input("Do you want to overwrite? (y/n): ").lower().strip()[:1] == "y":
            return False, len(changes)
        else:
            return True, len(changes)
    return False, len(changes)


def overwriteWithoutConfirm(search_entries, search_parameter, search_string, new_entry):
    overwritten_entries = []
    previous_entry = {}
    for entry in search_entries:
        if search_string in entry[search_parameter]:
            previous_entry = entry
            full_new_entry = {}
            for param in ['event_id', 'start_datetime', 'end_datetime', 'summary', 'description']:
                try:
                    if new_entry[param] == '':
                        full_new_entry[param] = entry[param]
                    else:
                        full_new_entry[param] = new_entry[param]
                except KeyError:
                    full_new_entry[param] = entry[param]
            overwritten_entries.append(full_new_entry)
        else:
            overwritten_entries.append(entry)
    return overwritten_entries, previous_entry


''' DEBUG FUNCTIONS '''


def showCompare(entry_a, entry_b):
    verbose("comparing:", 0)
    verbose(entry_a['event_id'] + " <-> " + entry_b['event_id'], 1)
    verbose(entry_a['start_datetime'] + " <-> " + entry_b['start_datetime'], 1)
    verbose(entry_a['end_datetime'] + " <-> " + entry_b['end_datetime'], 1)
    verbose(entry_a['summary'] + " <-> " + entry_b['summary'], 1)
    verbose(entry_a['description'] + " <-> " + entry_b['description'], 1)


def showYAML(yaml_data):
    print(yaml.dump(yaml_data, default_flow_style=False, default_style=''))


def showEntries(data_set):
    for entry in data_set:
        print(entry['start_datetime'] + " - " + entry['summary'])


def showHelp():
    print("SYNTAX:")
    print(" add_pattern '15/04/2020' 35 '[1, 2, 2, 1, 2, 2, 2]'")
    print(" add_test")


''' START - OLD DATA FUNCTIONS '''

def CSVdatetime2gcal(date, time, zone):
  datetime_in = datetime.datetime.strptime(date + '-' + time,"%m/%y/%d-%I:%M:%S %p")
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


''' END - OLD DATA FUNCTIONS '''

''' START - OLD PILLCAL FUNCTIONS '''


# TODO: remove this
def main(mode):
  """Shows basic usage of the Google Calendar API.

  Creates a Google Calendar API service object
  and proceeds according to parameters
  """
  # This is already on online.py
  if (ONLINE != 'false'):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
  # TODO: remove the part above
  # TODO: make sure the part below is not in use
  try:
    if mode == "list":
      dat.DictArray2CSV((events.online2DictArray(service, online.getIDCal(service, CAL_NAME), FIRSTYEAR, LASTYEAR)))
      # TODO: Download directly to CSV; ask before
    if mode == "download":
      dat.DictArray2CSVFile((events.online2DictArray(service, online.getIDCal(service, CAL_NAME), FIRSTYEAR, LASTYEAR)), cal_file)
    if mode == "upload":
      events.uploadCSV(service, cal_file, CAL_NAME, ZONE, FIRSTYEAR, LASTYEAR)
    if mode == "update":
      online.updatefromCSV(service, cal_file, CAL_NAME, ZONE, FIRSTYEAR, LASTYEAR)
      dat.DictArray2CSVFile((events.online2DictArray(service, online.getIDCal(service, CAL_NAME), FIRSTYEAR, LASTYEAR)), cal_file)
    if mode == "clearcal":
      #TODO: Ask the user before deleting!!
      online.delCal(service, CAL_NAME)
      online.newCal(service, CAL_NAME)
    elif mode == "test":
      print(online.updateOnline("test.csv"))
  except IndexError:
    showhelp()

def ifMain(): # TODO TO BE DELETED
  try:
    mode = sys.argv[1]
  except IndexError:
    showhelp()
  main(mode)


''' END - OLD PILLCAL FUNCTIONS '''


if __name__ == '__main__':
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
    ZONE = '+02:00'
    FIRSTYEAR = 2012
    LASTYEAR = 2025

    cal_file, err = getEnvVar('CAL_FILE')
    if err == 2:
        cal_file = 'Calendar.csv'
    data_set = loadCalendarFile(cal_file)

    try:
        if sys.argv[1] == 'add_pattern':
            START_DATE = sys.argv[2]
            NR_DAYS = int(sys.argv[3])
            PATTERN = sys.argv[4].split(',')
            new_entries = createEntries(START_DATE, NR_DAYS, PATTERN)
            merged = mergeEntries(data_set, new_entries)
            saveCalendarFile(merged, cal_file)
        elif sys.argv[1] == 'add_test':
            # TODO: ask for new value
            new_test_result = input("Enter test result: ")
            new_entry = {}
            new_entry['summary'] = 'Blood Level: ' + str(new_test_result)
            new_entry['description'] = new_entry['summary']
            data_set, previous_test_entry = overwriteWithoutConfirm(data_set, 'summary', 'Test Blood', new_entry)
            # TODO: propose a new date for Test Blood, add it
            new_date = getNewTestDate(previous_test_entry)
            data_set = addEntry(data_set, new_date.strftime('%Y-%m-%dT09:15:00Z'), new_date.strftime('%Y-%m-%dT10:00:00Z'), 'Test Blood')
            saveCalendarFile(data_set, cal_file)
        # TODO: redo this
        elif sys.argv[1] == "list":
            dat.DictArray2CSV((events.online2DictArray(service, online.getIDCal(service, CAL_NAME), FIRSTYEAR, LASTYEAR)))
            # TODO: Download directly to CSV; ask before
        # TODO: redo this
        if sys.argv[1] == "download":
            dat.DictArray2CSVFile((events.online2DictArray(service, online.getIDCal(service, CAL_NAME), FIRSTYEAR, LASTYEAR)), cal_file)
        # TODO: is this needed?
        if sys.argv[1] == "upload":
            events.uploadCSV(service, cal_file, CAL_NAME, ZONE, FIRSTYEAR, LASTYEAR)
        # TODO: redo this
        if sys.argv[1] == "update":
            online.updatefromCSV(service, cal_file, CAL_NAME, ZONE, FIRSTYEAR, LASTYEAR)
            dat.DictArray2CSVFile((events.online2DictArray(service, online.getIDCal(service, CAL_NAME), FIRSTYEAR, LASTYEAR)), cal_file)
        # TODO: redo this
        if sys.argv[1] == "clearcal":
            #TODO: Ask the user before deleting!!
            online.delCal(service, CAL_NAME)
            online.newCal(service, CAL_NAME)
        # TODO: NEW function to clean up cal (remove duplicates...)
        elif sys.argv[1] == "test":
            print(online.updateOnline("test.csv"))
        else:
            showHelp()
    except IndexError:
        showHelp()
