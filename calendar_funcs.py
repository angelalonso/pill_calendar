import datetime

""" Info functions
"""


def listCal(service):
    resultList = []
    page_token = None
    while True:
        cal_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in cal_list['items']:
            resultList.append(calendar_list_entry['summary'])
        page_token = cal_list.get('nextPageToken')
        if not page_token:
            break
    return resultList


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
    return resultList


""" Creation functions
"""


def newCal(service, cal_name):
    calendar = {
        'summary': cal_name
    }

    created_calendar = service.calendars().insert(body=calendar).execute()
    print created_calendar['id']


def create_if_notexisting(service, cal_name):
    if cal_name in list(service):
        print(cal_name + ' exists')
    else:
        print(cal_name + ' does not exist, creating...')
        newCal(service, cal_name)


""" Destruction functions
"""


def clearCal(service, cal_name):
    calID = getIDCal(service, cal_name)
    service.calendars().clear(
      calendarId=calID
      ).execute()


def delCal(service, cal_name):
    calID = getIDCal(service, cal_name)
    service.calendars().delete(
      calendarId=calID
      ).execute()


def listEntries(service):
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='alonsofonseca.angel@gmail.com', timeMin=now,
        maxResults=10, singleEvents=True, orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


def getIDEntry(service, search_word):
    print('Getting event: ' + search_word)
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' UTC time
    print(now)
    eventsResult = service.events().list(
        calendarId='alonsofonseca.angel@gmail.com', q=search_word,
        maxResults=250, singleEvents=True, orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

""" Main control
"""
if __name__ == '__main__':
    listEntries()
