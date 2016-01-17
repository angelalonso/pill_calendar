import datetime

def add(service):
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    event = {
      'summary': 'Google I/O 2015',
      'location': '800 Howard St., San Francisco, CA 94103',
      'description': 'A chance to hear more about Google\'s developer products.',
      'start': {
        'dateTime': '2015-05-28T09:00:00-07:00',
      },
      'end': {
        'dateTime': '2015-05-28T17:00:00-07:00',
      },
      'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=2'
      ],
      'attendees': [
        {'email': 'lpage@example.com'},
        {'email': 'sbrin@example.com'},
      ],
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }

    event = service.events().insert(calendarId='Pills', body=event).execute()
    print 'Event created: %s' % (event.get('htmlLink'))

def listEvents(service):
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='alonsofonseca.angel@gmail.com', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def getIDEvent(service,search_word):
    print('Getting event: ' + search_word)
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(now)
    time_min ='2016-01-01T14:11:59.408061Z'
    eventsResult = service.events().list(
        calendarId='alonsofonseca.angel@gmail.com', q=search_word, maxResults=250, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

if __name__ == '__main__':
    listEntries()

