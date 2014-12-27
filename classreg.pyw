import wx
import urllib, urllib2, cookielib
import time
import winsound
import smtplib

class ExamplePanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		
		#Timer to repeat execution
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.update, self.timer)
     
		#Log
		self.logger = wx.TextCtrl(self, pos=(20,185), size=(270,60), style=wx.TE_READONLY | wx.TE_MULTILINE )
		
		#Login button
		self.button =wx.Button(self, label="Login", pos=(225, 43))
		self.Bind(wx.EVT_BUTTON, self.OnClick,self.button)
		
		#Start timer
		self.toggleBtn = wx.Button(self, wx.ID_ANY, "Start", pos=(225,148))
		self.toggleBtn.Bind(wx.EVT_BUTTON, self.onToggle)
		
		#EID input
		self.lblname = wx.StaticText(self, label="Your UT EID : ", pos=(20,35))
		self.eid = wx.TextCtrl(self, value="", pos=(100, 30))#, size=(140,-1))
		
		#Password input
		self.lblpw = wx.StaticText(self, label="Password : ", pos=(20, 65))
		self.pw = wx.TextCtrl(self, pos=(100, 60), style=wx.TE_PASSWORD)#, size=(95, -1), choices=self.sampleList, style=wx.CB_DROPDOWN)
		
		#Phone number input (optional)
		self.lblpn = wx.StaticText(self, label="Phone # : ", pos=(20, 125))
		self.pn = wx.TextCtrl(self, pos=(100, 120))#, size=(95, -1), choices=self.sampleList, style=wx.CB_DROPDOWN)
		
		#Course Unique number input
		self.lblcn = wx.StaticText(self, label="Course # : ", pos=(20, 155))
		self.cn = wx.TextCtrl(self, pos=(100, 150))#, size=(95, -1), choices=self.sampleList, style=wx.CB_DROPDOWN)
		
		#shameless plug
		self.plug = wx.StaticText(self, label="by Nikhil Joglekar", pos=(20, 250))
		self.plug2 = wx.StaticText(self, label="nikhiljoglekar@utexas.edu", pos=(165, 250))

	#login handler
	def OnClick(self,event):
		#logs in, creates login cookie
		username = self.eid.GetValue()
		password = self.pw.GetValue()
		loginurl = 'https://utdirect.utexas.edu/security-443/logon_check.logonform'

		login_data = urllib.urlencode({'LOGON' : username, 'PASSWORDS' : password})
		opener.open(loginurl, login_data)

		check = opener.open('https://utdirect.utexas.edu/registrar/nrclav/index.WBX?s_ccyys=20129')
		checkdata = check.read()
		
		#initial check if login is successful
		if 'limit this search by starting time' in checkdata :
			box=wx.MessageDialog(None, 'Login Successful', 'login', wx.OK)
			answer=box.ShowModal()
			box.Destroy()
		else :
			boxf=wx.MessageDialog(None, 'Login Failed', 'fail', wx.OK)
			answer=boxf.ShowModal()
			boxf.Destroy()
	
	#execution start / stop handler
	def onToggle(self, event):
		btnLabel = self.toggleBtn.GetLabel()
		if btnLabel == "Start":
			self.logger.AppendText("Running...\n")
			self.timer.Start(1000)
			self.toggleBtn.SetLabel("Stop")
		else:
			self.logger.AppendText("\nStopped!\n")
			self.timer.Stop()
			self.toggleBtn.SetLabel("Start")
	
	#execution handler	
	def update(self, event):
		append = self.cn.GetValue()
		searchurl = dataurl + append

		resp = opener.open(searchurl)
		html = resp.read()

		reg = False

		if 'Spring 2015 class detail' in html :
			if not 'closed' in html :
				reg = True
			#else : 
			#	self.logger.AppendText('\nRefreshing ')
		else :
			self.timer.Stop()
			self.toggleBtn.SetLabel("Start")
			self.logger.AppendText("\nError\n")
			
		if reg :
			self.logger.AppendText("\nGO REGISTER NOW IT'S OPEN\n")
			now = time.localtime(time.time())
			self.logger.AppendText(time.strftime("%c", now))
			winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
			self.timer.Stop()
			self.toggleBtn.SetLabel("Start")
			
			# sends text message to your phone####################
			#fromaddr = 'Class Sniper'  
			#toaddrs  = "2814329666@txt.att.net"
			#msg = 'Class is open! Go register!'  
			  		  
			# Credentials (if needed)  
			#email = ''  
			#emailpw = ''  
			#server = smtplib.SMTP('smtp.gmail.com:587')  
			#server.starttls()  
			#server.login(email,emailpw)  
			#server.sendmail(fromaddr, toaddrs, msg)  
			#server.quit() 
						
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
dataurl = 'https://utdirect.utexas.edu/registrar/nrclav/details.WBX?s_ccyys=20152&s_unique='
searchurl = ''
app = wx.App(False)
frame = wx.Frame(None, -1, title='Open Class Sniper', pos=(50,50),size=(323,300), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER )
panel = ExamplePanel(frame)
frame.Show()
app.MainLoop()