import wx
import wx.html as html
import os
import datetime
from datetime import timedelta
import calendaring
 
class MainWindow(wx.Frame):
	def __init__(self, parent, title):
		
		global calfile 
		calfile = '/home/aaf/Documentos/Calendar.csv'

		# Initializing in Fullscreen mode while getting the parameters right	
		fullscreensize = wx.GetDisplaySize() 
        	wx.Frame.__init__(self, parent, title=title, size=fullscreensize)
		
		self.MainScreen(parent,title)

		self.Show()


	def MainScreen(self, parent, title):
		# Temporarily building our data here
	
		now_raw = datetime.datetime.now()
        	now = now_raw.strftime("%m/%y/%d")
        	file_in = open('/home/aaf/Documentos/Calendar.csv')
        	entries = []
        	calendaring.read_file(file_in, entries)

		# Upper Info
        	self.upperinfosizer = wx.BoxSizer(wx.HORIZONTAL)
		read_only_upper_txtCtrl = wx.StaticText(self,-1,"\nSINTROM AMOUNT FOR TODAY, " + now_raw.strftime("%d-%m-%Y") + ": \n\n" 
			+ calendaring.search_bydate(entries,now).description + "\n\n" 
			+ str(calendaring.sintrom_overview(entries,7))
			,style=wx.TE_CENTRE)	
		self.upperinfosizer.Add(read_only_upper_txtCtrl,1, wx.EXPAND)


		# Lower buttons
        	self.lowerbuttonssizer = wx.BoxSizer(wx.HORIZONTAL)

		closebutton = wx.Button(self, -1, "Close")
		calendarbutton = wx.Button(self, -1, "Calendar")
		self.Bind(wx.EVT_BUTTON, self.OnExit, closebutton)
		self.Bind(wx.EVT_BUTTON, self.CalendarScreen(parent,title), calendarbutton)
        	self.lowerbuttonssizer.Add(closebutton, 1, wx.EXPAND)
        	self.lowerbuttonssizer.Add(calendarbutton, 1, wx.EXPAND)



        	# Use some sizers to see layout options
        	self.sizer = wx.BoxSizer(wx.VERTICAL)
        	self.sizer.Add(self.upperinfosizer,1,flag=wx.ALIGN_CENTER)
        	self.sizer.Add(self.lowerbuttonssizer, 0, flag=wx.EXPAND|wx.ALIGN_CENTER)

        	#Layout sizers
        	self.SetSizer(self.sizer)
		
        	self.Layout()
	
	def CalendarScreen(self, parent, title):
		# Upper Info
        	self.UnsetSizer(self.sizer)

    	def OnExit(self,e):
        	self.Close(True)  # Close the frame.

app = wx.App()
frame = MainWindow(None, "E-Yo")
app.MainLoop()
