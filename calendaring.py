import csv
import shutil
import datetime
from datetime import timedelta

class Cal_entry(object):
	def __init__(self, pos=None, subject=None, startdate=None, starttime=None, enddate=None, endtime=None, allday=None, description=None, location=None, private=None):
		self.pos = pos
		self.subject = subject
		self.startdate = startdate
		self.starttime = starttime
		self.enddate = enddate
		self.endtime = endtime
		self.allday = allday
		self.description = description
		self.location = location
		self.private = private
	


def ReadFile(file_in,entries):
	with file_in as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
	# Maybe using this: http://www.coderholic.com/parsing-csv-data-in-python/ in the future...
	# But for now I just strip the first line
		title = True
		pos_counter = 0
		for row in spamreader:
			if title == False:
				entries.append(Cal_entry(str(pos_counter),row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))
				pos_counter += 1
			title = False	

def Save2NewFileSintrom(entries,filename):
	today = datetime.datetime.now().strftime("%Y%m%d_%H%M")
	file_out = filename + "." + today
	shutil.copy2(filename, file_out)
	resultFile = open(filename,'wb')
	wr = csv.writer(resultFile, dialect='excel')
	# Print titles, I'm still too lazy to automate this
        Title2Write = ['Subject','Start Date','Start Time','End Date','End Time','All Day Event','Description','Location','Private']
	wr.writerow(Title2Write)
	for i in entries:
		Line2Write=[]
		Line2Write.append(i.subject)
		Line2Write.append(i.startdate)
		Line2Write.append(i.starttime)
                Line2Write.append(i.enddate)
                Line2Write.append(i.endtime)
                Line2Write.append(i.allday)
                Line2Write.append(i.description)
                Line2Write.append(i.location)
                Line2Write.append(i.private)
		
		wr.writerow(Line2Write)

def OrderByField(entries,field1,field2,reverse_order):
	ordered = sorted(entries, key=lambda x: datetime.datetime.strptime(x.startdate+" "+x.starttime,"%m/%y/%d %I:%M:%S %p"), reverse=reverse_order)
	pos_counter = 0
	for i in ordered:
		i.pos = pos_counter
		pos_counter += 1
	return ordered

def SearchByDate(entries,date):
	for value in entries:
		if value.startdate == date:
			return value

def SearchByField(entries,field2search,data2search):
	Results = []
	for value in entries:
		if getattr(value, field2search) == data2search:
			Results.append(value)
	return Results

def SearchByDateAndField(entries,field2search,data2search,date):
	Results = []
	for value in entries:
		if value.startdate == date:
			if getattr(value, field2search) == data2search:
				Results.append(value)
	return Results

def AddEntry(entries,entrylist):
	for row in entrylist:
		entries.append(Cal_entry('999',row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))
	auxentries = OrderByField(entries,'startdate','starttime',True)	
	return auxentries

def DeleteEntry(entries,position):
	auxentries = []
	print "deleting..."
	print position
	for entry in entries:
		if entry.pos != position:
			auxentries.append(entry)
	return auxentries

def TranslateDateTime(to_translate,source_type):
	if source_type == 'date':
		try:
			result = datetime.datetime.strptime(to_translate,"%m/%y/%d").strftime('%d.%m.%Y')
		except ValueError:
			result = to_translate	
	elif source_type == 'time':
		try:
			result = datetime.datetime.strptime(to_translate,"%I:%M:%S %p").strftime('%H:%M:%S')
		except IOError:
			result = to_translate	
	# Future: datetime type?
	# else
	return result

###########################
# SINTROM RELATED FUNCTIONS

def sintrom_overview(entries,daysshown):
	backdays = daysshown / 2
	result_list = []
	for i in range(daysshown):
		date_i = datetime.datetime.now() - timedelta(days=(daysshown-(backdays+i)))
		result_list.append(date_i.strftime("%d-%m-%Y") + ":" + SearchByDate(entries,date_i.strftime("%m/%y/%d")).description + "\n")
	return ''.join(result_list) 

def sintrom_next_test(entries):
	nexttest = getattr(SearchByField(entries,'description','Test Blood')[0],'startdate')
	return nexttest

def sintrom_update_test(entries,newday,newamount,futuretestday):
	entrylist = []

	lasttestday = str(datetime.datetime.strptime(str(newday),"%a %d %b %Y %H:%M:%S %p %Z").strftime("%m/%y/%d"))
	futuretestday = str(datetime.datetime.strptime(str(futuretestday),"%a %d %b %Y %H:%M:%S %p %Z").strftime("%m/%y/%d"))

	expectedtest = SearchByField(entries,'description','Test Blood')[0]
	entries = DeleteEntry(entries,expectedtest.pos)
	
	entrylist.append(('Sintrom Test Done',lasttestday,'11:15:00 AM',lasttestday,'12:00:00 AM','False','Blood Level: ' + str(newamount),'','False'))
	entrylist.append(('Sintrom Test',futuretestday,'11:15:00 AM',futuretestday,'12:00:00 AM','False','Test Blood','','False'))

	entries = AddEntry(entries,entrylist)
	return entries

def sintrom_conflict(entries,newentry_date):

	conflicts = SearchByDateAndField(entries,"description","Sintrom",newentry_date)	
	return conflicts

def main():
	filename = '/home/aaf/Documentos/Calendar.csv'
	now_raw = datetime.datetime.now()
	now = now_raw.strftime("%m/%y/%d")
	file_in = open(filename)
	entries = []
	read_file(file_in, entries)
	print ("SINTROM AMOUNT FOR TODAY, " + now_raw.strftime("%d-%m-%Y") + ":")
	print SearchByDate(entries,now).description
	#print search_bydateandfield(entries,"description","Sintrom",now)
	print sintrom_overview(entries,7)

if __name__ == '__main__':
	    main()
