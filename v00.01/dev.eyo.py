import wx
import wx.html as html
import os
import datetime
from datetime import timedelta
import sys
import calendaring
 
class Frame(wx.Frame):
    	def __init__(self, *args, **kwargs):
        	super(Frame, self).__init__(*args, **kwargs)		
		
		global calfile 
		calfile = '/home/aaf/Documentos/Calendar.csv'
		
		self.MainScreen(kwargs['title'])

	def MainScreen(self, *args, **kwargs):
		self.DestroyChildren()
		self.sizer = wx.BoxSizer(wx.VERTICAL)

		# Upper Info
        	self.maininfosz = wx.BoxSizer(wx.HORIZONTAL)
		read_only_upper_txtCtrl = wx.StaticText(self,-1,"\nSINTROM AMOUNT FOR TODAY, " + now_raw.strftime("%d-%m-%Y") + ": \n\n" 
			+ calendaring.SearchByDate(cal_entries,now).description + "\n\n" 
			+ str(calendaring.sintrom_overview(cal_entries,7))
			,style=wx.TE_CENTRE)	
		self.maininfosz.Add(read_only_upper_txtCtrl,1, wx.EXPAND)

		# Lower buttons
        	self.lowerbuttonssizer = wx.BoxSizer(wx.HORIZONTAL)

		closebutton = wx.Button(self, -1, "Close")
		caleditbutton = wx.Button(self, -1, "Calendar")
		addresultbutton = wx.Button(self, -1, "Add Results after a new Test")
		self.Bind(wx.EVT_BUTTON, self.OnExit, closebutton)
		self.Bind(wx.EVT_BUTTON, self.CalEditScreen, caleditbutton)
		self.Bind(wx.EVT_BUTTON, self.SintromAddResults, addresultbutton)
        	self.lowerbuttonssizer.Add(closebutton, 1, wx.EXPAND)
        	self.lowerbuttonssizer.Add(caleditbutton, 1, wx.EXPAND)
        	self.lowerbuttonssizer.Add(addresultbutton, 1, wx.EXPAND)

        	# Use some sizers to see layout options	
        	self.sizer.Add(self.maininfosz,1,flag=wx.ALIGN_CENTER)
        	self.sizer.Add(self.lowerbuttonssizer, 0, flag=wx.EXPAND|wx.ALIGN_CENTER)

        	#Layout sizers
        	self.SetSizer(self.sizer)
			
		self.Layout()

	def SintromAddResults(self, e):
                # Cleanup
                self.DestroyChildren()
		
		self.addresultsz = wx.BoxSizer(wx.VERTICAL)		

		self.addresultmainsz = wx.GridBagSizer(10, 10)		
	

		self.AddResultTitle = wx.StaticText(self, 1, 'Add the Date and Result of latest Test')
		self.AddResultTitleLine = wx.StaticLine(self)

		self.AddResultDatePickerTitle = wx.StaticText(self, 1, 'Date of the Test')
		self.AddResultDatePicker = wx.DatePickerCtrl(self, 1,
        		wx.DefaultDateTime, (1,1), wx.Size( 140,-1 ),
        		wx.DP_DEFAULT|wx.DP_SHOWCENTURY | wx.DP_SPIN ) 

		self.AddResultAmountPickerTitle = wx.StaticText(self, 1, 'Result of the Test')
		self.AddResultAmountPicker = wx.TextCtrl(self, 1, "0.0", size=(175, -1))

		self.addresultmainsz.Add(self.AddResultTitle, pos=(1,1), span=(1,2))
		self.addresultmainsz.Add(self.AddResultTitleLine, pos=(1,4), span=(1,2), flag=wx.EXPAND|wx.BOTTOM)
		self.addresultmainsz.Add(self.AddResultDatePickerTitle, pos=(3,1))
		self.addresultmainsz.Add(self.AddResultDatePicker, pos=(3,2))
		self.addresultmainsz.Add(self.AddResultAmountPickerTitle, pos=(3,4))
		self.addresultmainsz.Add(self.AddResultAmountPicker, pos=(3,5))



		# Button sizer
                self.lowerbuttonssz = wx.BoxSizer(wx.HORIZONTAL)
                closebutton = wx.Button(self, -1, "Close")
                caleditbutton = wx.Button(self, -1, "Calendar")
                self.Bind(wx.EVT_BUTTON, self.OnExit, closebutton)
                self.Bind(wx.EVT_BUTTON, self.CalEditScreen, caleditbutton)
                self.lowerbuttonssz.Add(closebutton, 1, wx.EXPAND)
                self.lowerbuttonssz.Add(caleditbutton, 1, wx.EXPAND)

                # Layout sizers
#		self.addresultsz.Add(self.lowerbuttonssz, pos=(5, 0), span=(1, 5), flag=wx.LEFT, border=10)
		self.addresultsz.Add(self.addresultmainsz, 1, flag=wx.EXPAND)
		self.addresultsz.Add(self.lowerbuttonssz, 0, flag=wx.EXPAND|wx.ALIGN_CENTER)
#		self.addresultmainsz.AddGrowableCol(2)
                self.SetSizer(self.addresultsz)

                self.Layout()


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

		self.DatePickerTitle = wx.StaticText(editpanel, -1, 'When?', (15, 400))
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
                self.Bind(wx.EVT_BUTTON, self.CalendarTableScreen, caltablebutton)
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


	def CalendarTableScreen(self, e):
		# Cleanup
		self.DestroyChildren()
                self.sizer = wx.BoxSizer(wx.VERTICAL)
		
		listbox = wx.BoxSizer(wx.HORIZONTAL)	
		panel = wx.Panel(self, -1)

		self.cal_list =  wx.ListCtrl(panel, -1, style=wx.LC_REPORT)
		self.cal_list.InsertColumn(0, 'startdate')
        	self.cal_list.InsertColumn(1, 'subject')
        	self.cal_list.InsertColumn(2, 'description')
		
		# Little trick to space the columns equally
		table_width = fullscreensize[0] #GetSize returns (width, height) tuple
		num_col = self.cal_list.GetColumnCount()
		col_width = table_width/num_col
		for i in range(0, num_col):
    			self.cal_list.SetColumnWidth(i, col_width)

		self.CalendarUpdate()

		listbox.Add(self.cal_list, 1, wx.EXPAND)
		panel.SetSizer(listbox)	

                mainscreenbutton = wx.Button(self, -1, "Back to Main")
                savenewdocbutton = wx.Button(self, -1, "Save to New doc")
                orderbydatebutton = wx.Button(self, -1, "Order Table per date")
                caleditbutton = wx.Button(self, -1, "Edit Calendar")
		closebutton = wx.Button(self, -1, "Close")

                self.Bind(wx.EVT_BUTTON, self.MainScreen, mainscreenbutton)
                self.Bind(wx.EVT_BUTTON, self.SaveNewDoc, savenewdocbutton)
                self.Bind(wx.EVT_BUTTON, self.OrderByDate, orderbydatebutton)
		self.Bind(wx.EVT_BUTTON, self.CalEditScreen, caleditbutton)
		self.Bind(wx.EVT_BUTTON, self.OnExit, closebutton)

        	self.calbuttonssz = wx.BoxSizer(wx.HORIZONTAL)
		self.calbuttonssz.Add(closebutton, 1, wx.EXPAND)
		self.calbuttonssz.Add(savenewdocbutton, 1, wx.EXPAND)
		self.calbuttonssz.Add(orderbydatebutton, 1, wx.EXPAND)
		self.calbuttonssz.Add(caleditbutton, 1, wx.EXPAND)
		self.calbuttonssz.Add(mainscreenbutton, 1, wx.EXPAND)
		
		self.sizer.Add(panel, 1, flag=wx.EXPAND)
		self.sizer.Add(self.calbuttonssz, 0, flag=wx.EXPAND|wx.ALIGN_CENTER)
	
		self.SetSizer(self.sizer)

		self.Layout()
	
 
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
                        index = self.cal_list.InsertStringItem(sys.maxint, i.startdate)
                        self.cal_list.SetStringItem(index, 1, i.subject)
                        self.cal_list.SetStringItem(index, 2, i.description)

	def SaveNewDoc(self, e):
		calendaring.Save2NewFileSintrom(cal_entries,filename)

	def OrderByDate(self, e):
		global cal_entries
		cal_entries = calendaring.OrderByField(cal_entries,'startdate','starttime')
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
