import wx
import wx.lib.mixins.listctrl as listmix
import wx.html as html
import os
import datetime
from datetime import timedelta
import sys
import calendaring

# Until I find a better way: this is the PATH:

path='/home/aaf/scripts/e-yo/eyo_python/'

#class EditableListCtrl(wx.ListCtrl, listmix.TextEditMixin):
class EditableListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.TextEditMixin):
	# As seen on http://www.blog.pythonlibrary.org/2011/01/04/wxpython-wx-listctrl-tips-and-tricks/
	# TextEditMixin allows any column to be edited.
 
	# Constructor
	def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition,size=wx.DefaultSize, style=0):
		wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
		listmix.TextEditMixin.__init__(self)
		listmix.ListCtrlAutoWidthMixin.__init__(self)
		self.setResizeColumn(5)
 
class Frame(wx.Frame):

	bmpset = dict()
    	
	def __init__(self, *args, **kwargs):
		super(Frame, self).__init__(*args, **kwargs)		
		
		global calfile 
		calfile = '/home/aaf/Documentos/Calendar.csv'
		
		self.MainScreen(kwargs['title'])

	def MainScreen(self, *args, **kwargs):
	
		# Cleanup
		self.DestroyChildren()
		
		# Sizers
		self.fullsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sidemenusz = wx.BoxSizer(wx.VERTICAL)
		self.mainboxsz = wx.BoxSizer(wx.VERTICAL)
		self.titleedgebox = wx.BoxSizer(wx.VERTICAL)
		self.uppermenusz = wx.BoxSizer(wx.HORIZONTAL)

		# Side Menu
			## Side Title
		titleedge = wx.StaticText(self, 1, 'Main')
		font = wx.Font(20, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
		titleedge.SetFont(font)
		self.titleedgebox.Add(titleedge, 1, wx.EXPAND)
		self.titleedgebox.SetMinSize((100,100))

		self.sidemenusz.Add(self.titleedgebox, 1, wx.EXPAND)

		caltablebutton = wx.Button(self, -1, 'Calendar')
		caleditbutton = wx.Button(self, -1, 'Calendar Edit')
		addresultbutton = wx.Button(self, -1, 'Add Results after a new Test')

		self.Bind(wx.EVT_BUTTON, self.CalendarControlScreen, caltablebutton)
		self.Bind(wx.EVT_BUTTON, self.CalEditScreen, caleditbutton)
		self.Bind(wx.EVT_BUTTON, self.SintromAddResults, addresultbutton)

		self.sidemenusz.Add(caltablebutton, 0, wx.EXPAND)
		self.sidemenusz.Add(caleditbutton, 0, wx.EXPAND)
		self.sidemenusz.Add(addresultbutton, 0, wx.EXPAND)

		# Upper Buttons
		## New images
		closebmp = wx.Bitmap("/home/aaf/scripts/e-yo/eyo_python/deco/close.png", wx.BITMAP_TYPE_ANY)
		self.bmpset['close'] = closebmp
		orderbmp = wx.Bitmap("/home/aaf/scripts/e-yo/eyo_python/deco/order.png", wx.BITMAP_TYPE_ANY)
		self.bmpset['order'] = orderbmp
		savebmp = wx.Bitmap("/home/aaf/scripts/e-yo/eyo_python/deco/save.png", wx.BITMAP_TYPE_ANY)
		self.bmpset['save'] = savebmp
		
		## Buttons
		exitbutton = wx.BitmapButton(self, -1, bitmap=closebmp, size=(closebmp.GetWidth()+10, closebmp.GetHeight()+10))
		self.Bind(wx.EVT_BUTTON, self.OnExit, exitbutton)

		self.uppermenusz.Add(exitbutton, 0, flag=wx.ALIGN_RIGHT)

		self.mainboxsz.Add(self.uppermenusz, 0, flag=wx.ALIGN_RIGHT)

		# Central Info
		read_only_upper_txtCtrl = wx.StaticText(self,-1,"\nSINTROM AMOUNT FOR TODAY, " + now_raw.strftime("%d-%m-%Y") + ": \n\n" 
			+ calendaring.SearchByDate(cal_entries,now).description + "\n\n" 
			+ str(calendaring.sintrom_overview(cal_entries,7))
			,style=wx.TE_CENTRE)	

		self.mainboxsz.Add(read_only_upper_txtCtrl,1, wx.EXPAND)

		# Adding everything	
		self.fullsizer.Add(self.sidemenusz, 0)
		self.fullsizer.Add(self.mainboxsz, 1, flag=wx.EXPAND)
	
		self.SetSizer(self.fullsizer)

		self.Layout()


	def CalendarControlScreen(self, *args, **kwargs):

		# Cleanup
		self.DestroyChildren()

		# Sizers		
		self.fullsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sidemenusz = wx.BoxSizer(wx.VERTICAL)
		self.mainboxsz = wx.BoxSizer(wx.VERTICAL)
		self.titleedgebox = wx.BoxSizer(wx.VERTICAL)
		self.uppermenusz = wx.BoxSizer(wx.HORIZONTAL)
		
		# Side Menu
		
		## Side Title
		titleedge = wx.StaticText(self, 1, 'Calendar')
		font = wx.Font(20, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
		titleedge.SetFont(font)
		self.titleedgebox.Add(titleedge, 1, wx.EXPAND)
		self.titleedgebox.SetMinSize((100,100))

		self.sidemenusz.Add(self.titleedgebox, 1, wx.EXPAND)

		mainscreenbutton = wx.Button(self, -1, "Back to Main")
		orderbydatebutton = wx.Button(self, -1, "Order Table per date")
		caleditbutton = wx.Button(self, -1, "Edit Calendar")

		self.Bind(wx.EVT_BUTTON, self.MainScreen, mainscreenbutton)
		self.Bind(wx.EVT_BUTTON, self.OrderByDate, orderbydatebutton)
		self.Bind(wx.EVT_BUTTON, self.CalEditScreen, caleditbutton)

		self.sidemenusz.Add(orderbydatebutton, 0, wx.EXPAND)
		self.sidemenusz.Add(caleditbutton, 0, wx.EXPAND)
		self.sidemenusz.Add(mainscreenbutton, 0, wx.EXPAND)
		
		# Upper Buttons
		
		## Images
		closebmp = self.bmpset['close']
		orderbmp = self.bmpset['order']
		savebmp = self.bmpset['save']
		
		## Buttons
		orderbutton = wx.BitmapButton(self, -1, bitmap=orderbmp, size=(orderbmp.GetWidth()+10, orderbmp.GetHeight()+10))
		self.Bind(wx.EVT_BUTTON, self.OrderByDate, orderbutton)
		savebutton = wx.BitmapButton(self, -1, bitmap=savebmp, size=(savebmp.GetWidth()+10, savebmp.GetHeight()+10))
		self.Bind(wx.EVT_BUTTON, self.SaveNewDoc, savebutton)
		exitbutton = wx.BitmapButton(self, -1, bitmap=closebmp, size=(closebmp.GetWidth()+10, closebmp.GetHeight()+10))
		self.Bind(wx.EVT_BUTTON, self.OnExit, exitbutton)

		self.uppermenusz.Add(orderbutton, 0, flag=wx.ALIGN_RIGHT)
		self.uppermenusz.Add(savebutton, 0, flag=wx.ALIGN_RIGHT)
		self.uppermenusz.Add(exitbutton, 0, flag=wx.ALIGN_RIGHT)

		self.mainboxsz.Add(self.uppermenusz, 0, flag=wx.ALIGN_RIGHT)

		# Central Info
# http://www.blog.pythonlibrary.org/2011/01/04/wxpython-wx-listctrl-tips-and-tricks/		
		#self.cal_list =  wx.ListCtrl(self, -1, style=wx.LC_REPORT)
		self.cal_list =  EditableListCtrl(self, -1, style=wx.LC_REPORT|wx.TR_HAS_VARIABLE_ROW_HEIGHT)
		#self.cal_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onTableItemSelected)
		self.cal_list.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.onTableItemChanged)
		self.cal_list.InsertColumn(0, 'pos')
		self.cal_list.InsertColumn(1, 'startdate')
		self.cal_list.InsertColumn(2, 'starttime')
        	self.cal_list.InsertColumn(3, 'subject')
        	self.cal_list.InsertColumn(4, 'description')


		# Spacing the columns manually
    		self.cal_list.SetColumnWidth(0, 50)
    		self.cal_list.SetColumnWidth(1, 100)
    		self.cal_list.SetColumnWidth(2, 150)
    		self.cal_list.SetColumnWidth(3, 350)
    		#self.cal_list.SetColumnWidth(4, col_width)

		self.CalendarUpdate()

		self.mainboxsz.Add(self.cal_list, 1, flag=wx.EXPAND)

		# Adding everything 	
		self.fullsizer.Add(self.sidemenusz, 0)
		self.fullsizer.Add(self.mainboxsz, 1, flag=wx.EXPAND)
	
		self.SetSizer(self.fullsizer)

		self.Layout()
	
    	def onTableItemChanged(self, event):
		global cal_entries
        	#currentItem = event.m_itemIndex
		new_value = event.m_item.GetText()
		new_column = event.m_item.GetColumn()
		new_col_label = self.cal_list.GetColumn(new_column).GetText()

		old_pos = event.GetIndex()
        	saved_entry = cal_entries[old_pos]
		setattr(saved_entry,new_col_label,new_value)

		entrylist = []
		entrylist.append((saved_entry.subject, saved_entry.startdate, saved_entry.starttime, saved_entry.enddate, saved_entry.endtime, saved_entry.allday, saved_entry.description, saved_entry.location, saved_entry.private))
		
		cal_entries = calendaring.DeleteEntry(cal_entries,saved_entry.pos)
		calendaring.AddEntry(cal_entries,entrylist)
		#variables = [i for i in dir(saved_entry) if not callable(i)]	
		#for x in variables:
		#	 print getattr(saved_entry,x)
	
	
	def CalEditScreen(self, e):
		# Cleanup
                self.DestroyChildren()
                self.sizer = wx.BoxSizer(wx.VERTICAL)

		self.caleditsz = wx.BoxSizer(wx.VERTICAL)
		
		editpanel = wx.Panel(self, -1)

		# Edit Panel Layout: Though unneeded, I'll try to keep order here
                self.LastEntriesTxtCtrl = wx.StaticText(editpanel,-1,"\nSINTROM AMOUNT FOR TODAY, " + now_raw.strftime("%d-%m-%Y") + ": \n\n"
                        + calendaring.SearchByDate(cal_entries,now).description + "\n\n"
                        + str(calendaring.sintrom_overview(cal_entries,7))
                        ,style=wx.TE_CENTRE)

		self.AddEntryBox = wx.StaticBox(editpanel, -1, 'Add an Entry', (5, 350), size=(400, 175 ))

		self.DatePickerTitle = wx.StaticText(editpanel, -1, 'Date', (15, 400))
		self.DatePicker = wx.DatePickerCtrl( editpanel, wx.ID_ANY,
        		wx.DefaultDateTime, (15,425), wx.Size( 140,-1 ),
        		wx.DP_DEFAULT|wx.DP_SHOWCENTURY | wx.DP_SPIN ) 
	
		self.AddEntrySintromAmountTitle = wx.StaticText(editpanel, -1, 'How Much Sintrom (mg)?', (175, 400))
		self.AddEntrySintromAmount = wx.SpinCtrl(editpanel, -1, '1', (175, 425), (150, -1), min=0, max=2)
		AddEntrybutton = wx.Button(editpanel, -1, 'Insert this entry', (5, 495), size=(400, -1 ))	

                self.caleditsz.Add(self.LastEntriesTxtCtrl,0,  flag=wx.ALIGN_CENTER)

		self.Bind(wx.EVT_BUTTON, self.CalMessage, AddEntrybutton)		

		# Buttons Layout
		mainscreenbutton = wx.Button(self, -1, "Back to Main")
                caltablebutton = wx.Button(self, -1, "Show Calendar Table")
                closebutton = wx.Button(self, -1, "Close")

                self.Bind(wx.EVT_BUTTON, self.MainScreen, mainscreenbutton)
                self.Bind(wx.EVT_BUTTON, self.CalendarControlScreen, caltablebutton)
                self.Bind(wx.EVT_BUTTON, self.OnExit, closebutton)

                self.caleditbuttonssz = wx.BoxSizer(wx.HORIZONTAL)

                self.caleditbuttonssz.Add(closebutton, 1, wx.EXPAND)
                self.caleditbuttonssz.Add(caltablebutton, 1, wx.EXPAND)
                self.caleditbuttonssz.Add(mainscreenbutton, 1, wx.EXPAND)

		# All mixed here and properly shown
		editpanel.SetSizer(self.caleditsz)

		self.sizer.Add(editpanel, 1, flag=wx.EXPAND)
                self.sizer.Add(self.caleditbuttonssz, 0, flag=wx.EXPAND|wx.ALIGN_CENTER)

                self.SetSizer(self.sizer)

                self.Layout()


	def SintromAddResults(self, e):
		# Some useful variables
		nexttest = datetime.datetime.strptime(calendaring.sintrom_next_test(cal_entries),"%m/%y/%d").strftime("%d%m%Y")

                # Cleanup
                self.DestroyChildren()
		
		self.addresultsz = wx.BoxSizer(wx.VERTICAL)		
		self.addresultmainsz = wx.GridBagSizer(10, 10)		

		self.AddResultTitle = wx.StaticText(self, 1, 'Add the Date and Result of latest Test')
		self.AddResultTitleLine = wx.StaticLine(self)

		self.AddResultDatePickerTitle = wx.StaticText(self, 1, 'When did this test happen?')
		self.AddResultDatePicker = wx.DatePickerCtrl(self, 1,
        		wx.DefaultDateTime, (1,1), wx.Size( 140,-1 ),
        		wx.DP_DEFAULT|wx.DP_SHOWCENTURY | wx.DP_SPIN ) 
		self.AddResultDatePicker.SetValue(wx.DateTimeFromDMY(int(nexttest[0:2]), int(nexttest[2:4]), int(nexttest[4:8])))

		self.AddResultAmountPickerTitle = wx.StaticText(self, 1, 'Result of the Test')
		self.AddResultAmountPicker = wx.TextCtrl(self, 1, "3.0", size=(175, -1))

		nextdate_guess = self.AddResultDatePicker.GetValue()
		self.NextDatePickerTitle = wx.StaticText(self, 1, 'When should next Test take place?')
		self.NextDatePicker = wx.DatePickerCtrl(self, 1,
        		wx.DefaultDateTime, (1,1), wx.Size( 140,-1 ),
        		wx.DP_DEFAULT|wx.DP_SHOWCENTURY | wx.DP_SPIN ) 
		nextguessmonth = (int(nexttest[2:4]) + 1) % 13
		# Building this up from last test (+ 1 month)
		if nextguessmonth == 0: 
			nextguessyear = int(nexttest[4:8]) + 1
		else:
			nextguessyear = int(nexttest[4:8])
		self.NextDatePicker.SetValue(wx.DateTimeFromDMY(int(nexttest[0:2]), nextguessmonth, nextguessyear))

		sendtestbutton = wx.Button(self, -1, "Update the DB")
		self.Bind(wx.EVT_BUTTON, self.TestAddMessage, sendtestbutton)

		self.addresultmainsz.Add(self.AddResultTitle, pos=(1,1), span=(1,2))
		self.addresultmainsz.Add(self.AddResultTitleLine, pos=(1,4), span=(1,2), flag=wx.EXPAND|wx.BOTTOM)
		self.addresultmainsz.Add(self.AddResultDatePickerTitle, pos=(3,1))
		self.addresultmainsz.Add(self.AddResultDatePicker, pos=(3,2))
		self.addresultmainsz.Add(self.NextDatePickerTitle, pos=(5,1))
		self.addresultmainsz.Add(self.NextDatePicker, pos=(5,2))
		self.addresultmainsz.Add(self.AddResultAmountPickerTitle, pos=(3,4))
		self.addresultmainsz.Add(self.AddResultAmountPicker, pos=(3,5))
		self.addresultmainsz.Add(sendtestbutton, pos=(5,5))

		# Button sizer
                self.lowerbuttonssz = wx.BoxSizer(wx.HORIZONTAL)
                closebutton = wx.Button(self, -1, "Close")
                caleditbutton = wx.Button(self, -1, "Calendar Table")
                self.Bind(wx.EVT_BUTTON, self.OnExit, closebutton)
                self.Bind(wx.EVT_BUTTON, self.CalendarControlScreen, caleditbutton)
                self.lowerbuttonssz.Add(closebutton, 1, wx.EXPAND)
                self.lowerbuttonssz.Add(caleditbutton, 1, wx.EXPAND)

                # Layout sizers
		self.addresultsz.Add(self.addresultmainsz, 1, flag=wx.EXPAND)
		self.addresultsz.Add(self.lowerbuttonssz, 0, flag=wx.EXPAND|wx.ALIGN_CENTER)
                self.SetSizer(self.addresultsz)

                self.Layout()



	def TestAddMessage(self,e):
		global cal_entries
		testdate = self.AddResultDatePicker.GetValue()
		testresult = self.AddResultAmountPicker.GetValue()
		nexttestdate = self.NextDatePicker.GetValue()

		ConfirmationMessage = wx.MessageDialog(self, "\n Do you want to add the following result?: \n\n"
                        + str(testresult) + " on " + str(testdate) + "\n\n Additionally next test will be scheduled for \n\n" + 
			str(nexttestdate), 'Please confirm', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

        	try:
            		if ConfirmationMessage.ShowModal() == wx.ID_YES:
				cal_entries = calendaring.sintrom_update_test(cal_entries,testdate,testresult,nexttestdate)
				#No error handling thus far
				e = 'No error'
				self.SaveNewDoc(e)
        	finally:
            		ConfirmationMessage.Destroy()

 
	def CalMessage(self,e):
		Date = datetime.datetime.strptime(str(self.DatePicker.GetValue()),"%a %d %b %Y %H:%M:%S %p %Z").strftime("%m/%y/%d")	
		SintromAmount = self.AddEntrySintromAmount.GetValue()
		
		ErrorMessage = ""
		Conflicts = calendaring.sintrom_conflict(cal_entries,Date)
		for i in range(len(Conflicts)):
			ErrorMessage += Conflicts[i] 
			ErrorMessage += "\n"

		print ErrorMessage
		ConfirmationMessage = wx.MessageDialog(self, "\n You have seleted to add an entry for: \n\n"
                        + str(Date) + ",\n\nto have " + str(SintromAmount) + " mg. of Sintrom\n\n\n" + str(len(Conflicts))
			+ " Entries exist already for that day: \n\n"
			+ ErrorMessage + "\n\nAre you sure?"
			, 'Please confirm', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

        	try:
            		if ConfirmationMessage.ShowModal() == wx.ID_YES:
                		print ('YES')
        	finally:
            		ConfirmationMessage.Destroy()

	def CalAddEntryPopup(self, e):
		Date = self.DatePicker.GetValue()	
		SintromAmount = self.AddEntrySintromAmount.GetValue()

		Popup = wx.Frame(self, 1)
		PopupSizer = wx.BoxSizer(wx.VERTICAL)
		MessageSizer = wx.BoxSizer(wx.HORIZONTAL)
		ButtonSizer = wx.BoxSizer(wx.HORIZONTAL)

                Message = wx.StaticText(Popup,-1,"\n You have seleted to add an entry for: \n\n" 
			+ str(Date) + "\n\n, to have \n\n" + str(SintromAmount) + " mg. of Sintrom"
                        ,style=wx.TE_RIGHT)

		MessageSizer.Add(Message,1, flag=wx.EXPAND)


		okbutton = wx.Button(Popup, -1, "OK")
		cancelbutton = wx.Button(Popup, -1, "Cancel")

		self.Bind(wx.EVT_BUTTON, self.OnExitCalAddEntryPopup(Popup), okbutton)
		self.Bind(wx.EVT_BUTTON, self.OnExitCalAddEntryPopup(Popup), cancelbutton)

		ButtonSizer.Add(okbutton, 1)
		ButtonSizer.Add(cancelbutton, 1)

		
		PopupSizer.Add(MessageSizer,1)
		PopupSizer.Add(ButtonSizer,0, flag=wx.EXPAND)
		Popup.SetSizer(PopupSizer)
		Popup.Show()
		#Popup.Raise()
	
	def OnExitCalAddEntryPopup(self, Frame2Close):
		Frame2Close.Close(True)

	def CalendarUpdate(self):
		self.cal_list.DeleteAllItems()
		for i in cal_entries:
                        index = self.cal_list.InsertStringItem(sys.maxint, str(i.pos))
                        self.cal_list.SetStringItem(index, 1, calendaring.TranslateDateTime(i.startdate,'date'))
                        self.cal_list.SetStringItem(index, 2, calendaring.TranslateDateTime(i.starttime,'time'))
                        self.cal_list.SetStringItem(index, 3, i.subject)
                        self.cal_list.SetStringItem(index, 4, i.description)
			if i.subject == 'Sintrom Test Done':
                		self.cal_list.SetItemBackgroundColour(index, "yellow")
			elif i.subject == 'Sintrom Test':
				self.cal_list.SetItemBackgroundColour(index, "orange")
			elif i.subject == 'Sintrom Amount':
				date =  datetime.datetime.strptime(i.startdate,"%m/%y/%d").strftime('%Y%m%d')
				today = datetime.datetime.now().strftime('%Y%m%d')
				if date <= today:
					if date < today:
						self.cal_list.SetItemBackgroundColour(index, "lightgrey")
					else:
						mainfont = wx.Font(14, family=wx.FONTFAMILY_DEFAULT, style=wx.NORMAL, weight=wx.FONTWEIGHT_BOLD)
						self.cal_list.SetItemFont(index, mainfont)
					if i.description == 'Sintrom Amount: 1':
						self.cal_list.SetItemTextColour(index, "darkcyan")
					elif i.description == 'Sintrom Amount: 2':
						self.cal_list.SetItemTextColour(index, "darkred")
				elif date > today:
					self.cal_list.SetItemTextColour(index, "white")
					if i.description == 'Sintrom Amount: 1':
						self.cal_list.SetItemBackgroundColour(index, "darkcyan")
					elif i.description == 'Sintrom Amount: 2':
						self.cal_list.SetItemBackgroundColour(index, "darkred")

	def SaveNewDoc(self, e):
		calendaring.Save2NewFileSintrom(cal_entries,filename)

	def OrderByDate(self, e):
		global cal_entries
		cal_entries = calendaring.OrderByField(cal_entries,'startdate','starttime',True)
		self.CalendarUpdate()

    	def OnExit(self,e):
        	self.Close(True)  # Close the frame.

	

# Start it all up

filename = '/home/aaf/Documentos/Calendar.csv'
now_raw = datetime.datetime.now()
now = now_raw.strftime("%m/%y/%d")
file_in = open(filename)
cal_entries = []
calendaring.ReadFile(file_in, cal_entries)

app = wx.App()
fullscreensize = wx.GetDisplaySize() 
frame = Frame(None, title='E-Yo',size=fullscreensize )
frame.Show()

app.MainLoop()
