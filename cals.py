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
