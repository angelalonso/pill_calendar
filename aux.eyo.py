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
		calendarbutton = wx.Button(self, -1, "Calendar")
		self.Bind(wx.EVT_BUTTON, self.OnExit, closebutton)
		self.Bind(wx.EVT_BUTTON, self.CalendarScreen, calendarbutton)
        	self.lowerbuttonssizer.Add(closebutton, 1, wx.EXPAND)
        	self.lowerbuttonssizer.Add(calendarbutton, 1, wx.EXPAND)

        	# Use some sizers to see layout options
        	self.sizer.Add(self.maininfosz,1,flag=wx.ALIGN_CENTER)
        	self.sizer.Add(self.lowerbuttonssizer, 0, flag=wx.EXPAND|wx.ALIGN_CENTER)

        	#Layout sizers
        	self.SetSizer(self.sizer)
			
		self.Layout()
	

	def CalendarTableScreen(self, e):
		# Cleanup
		self.DestroyChildren()
                self.tablesizer = wx.BoxSizer(wx.VERTICAL)
		
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
                edittablebutton = wx.Button(self, -1, "Edit")
                orderbydatebutton = wx.Button(self, -1, "Order Table per date")
		closebutton = wx.Button(self, -1, "Close")

                self.Bind(wx.EVT_BUTTON, self.MainScreen, mainscreenbutton)
                self.Bind(wx.EVT_BUTTON, self.SaveNewDoc, savenewdocbutton)
                self.Bind(wx.EVT_BUTTON, self.CalendarEditScreen, edittablebutton)
                self.Bind(wx.EVT_BUTTON, self.OrderByDate, orderbydatebutton)
		self.Bind(wx.EVT_BUTTON, self.OnExit, closebutton)

        	self.calbuttonssz = wx.BoxSizer(wx.HORIZONTAL)
		self.calbuttonssz.Add(closebutton, 1, wx.EXPAND)
		self.calbuttonssz.Add(savenewdocbutton, 1, wx.EXPAND)
		self.calbuttonssz.Add(edittablebutton, 1, wx.EXPAND)
		self.calbuttonssz.Add(orderbydatebutton, 1, wx.EXPAND)
		self.calbuttonssz.Add(mainscreenbutton, 1, wx.EXPAND)
		
		self.tablesizer.Add(panel, 1, flag=wx.EXPAND)
		self.tablesizer.Add(self.calbuttonssz, 0, flag=wx.EXPAND|wx.ALIGN_CENTER)
	
		self.SetSizer(self.tablesizer)

		self.Layout()

	def CalendarUpdate(self):
		self.cal_list.DeleteAllItems()
		for i in cal_entries:
                        index = self.cal_list.InsertStringItem(sys.maxint, i.startdate)
                        self.cal_list.SetStringItem(index, 1, i.subject)
                        self.cal_list.SetStringItem(index, 2, i.description)

	def CalendarScreen(self, e):
		# Cleanup
		self.DestroyChildren()
                self.calsizer = wx.BoxSizer(wx.VERTICAL)

		mainscreenbutton = wx.Button(self, -1, "Back to Main")
		caltablebutton = wx.Button(self, -1, "See Calendar Table")
                closebutton = wx.Button(self, -1, "Close")

                self.Bind(wx.EVT_BUTTON, self.MainScreen, mainscreenbutton)
                self.Bind(wx.EVT_BUTTON, self.CalendarTableScreen, caltablebutton)
                self.Bind(wx.EVT_BUTTON, self.OnExit, closebutton)

                self.caleditbuttonssz = wx.BoxSizer(wx.HORIZONTAL)
                
		self.caleditbuttonssz.Add(closebutton, 1, wx.EXPAND)
		self.caleditbuttonssz.Add(caltablebutton, 1, wx.EXPAND)
                self.caleditbuttonssz.Add(mainscreenbutton, 1, wx.EXPAND)

                self.calsizer.Add(self.caleditbuttonssz, 0, flag=wx.EXPAND|wx.ALIGN_CENTER)

                self.SetSizer(self.calsizer)

                self.Layout()


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
