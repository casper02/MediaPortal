from imports import *
from decrypt import *

def xhamsterstreamListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 

class xhamster(Screen):
	skin = 	"""
		<screen name="xhamster.com" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="streamlist" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget source="session.CurrentService" render="Label" position="640,420" size="120,40" font="Regular;26" foregroundColor="#00e5b243" backgroundColor="#00101214" halign="right" transparent="1">
				<convert type="ServicePosition">Length</convert>
			</widget>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,440" size="160,120" transparent="1" alphatest="blend" />
			<eLabel text="Views" position="230,470" size="100,25" backgroundColor="#00101214" transparent="1" foregroundColor="#00555556" font="Regular;20" valign="top" />
			<widget name="views" position="330,470" size="580,25" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
			<eLabel text="Runtime" position="230,500" size="100,25" backgroundColor="#00101214" transparent="1" foregroundColor="#00555556" font="Regular;20" valign="top" />
			<widget name="runtime" position="330,500" size="580,25" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
			<eLabel text="Page" position="230,530" size="100,25" backgroundColor="#00101214" transparent="1" foregroundColor="#00555556" font="Regular;20" valign="top" />
			<widget name="page" position="330,530" size="580,25" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
			<widget source="session.CurrentService" render="Label" position="330,70" size="120,24" zPosition="1" font="Regular;24" halign="left" transparent="1">
					<convert type="ServicePosition">Position,ShowHours</convert>
			</widget>
		</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok" : self.keyOK,
			"cancel" : self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown
		}, -1)
		
		self['title'] = Label("xHamster.com")
		self['coverArt'] = Pixmap()
		self['name'] = Label("")
		self['views'] = Label("")
		self['runtime'] = Label("")
		self['page'] = Label("1")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 23))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList

		self.keyLocked = False
		self.page = 1

		self.onLayoutFinish.append(self.loadpage)
		
	def loadpage(self):
		self.keyLocked = True
		self.streamList = []
		ptUrl = "http://xhamster.com/new/%s.html" % str(self.page)
		print ptUrl
		getPage(ptUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.pageData).addErrback(self.dataError)
		
	def pageData(self, data):
		xhListe = re.findall('<a href="(/movies/.*?)" class=\'hRotator\' >.*?<img src=\'(.*?)\'.*?alt="(.*?)"/>.*?<div class="moduleFeaturedDetails">Runtime: (.*?)<BR>Views: (.*?)</div>', data, re.S)
		if xhListe:
			for (xhLink, xhImage, xhName, xhRuntime, xhxhViews) in xhListe:
				xhLink = "http://xhamster.com"+xhLink
				self.streamList.append((xhName, xhImage, xhLink, xhxhViews, xhRuntime))
			self.streamMenuList.setList(map(xhamsterstreamListEntry, self.streamList))
			self.keyLocked = False
			self.showInfos()

	def showInfos(self):
		if self.keyLocked:
			return
		ptTitle = self['streamlist'].getCurrent()[0][0]
		ptImage = self['streamlist'].getCurrent()[0][1]
		ptViews  = self['streamlist'].getCurrent()[0][3]
		ptRuntime = self['streamlist'].getCurrent()[0][4]
		self.ptRead(ptImage)
		self['name'].setText(ptTitle)
		self['views'].setText(ptViews)
		self['runtime'].setText(ptRuntime)
		self['page'].setText(str(self.page))

	def ptRead(self, stationIconLink):
		downloadPage(stationIconLink, "/tmp/xhIcon.jpg").addCallback(self.ptCoverShow)
		
	def ptCoverShow(self, picData):
		if fileExists("/tmp/xhIcon.jpg"):
			self['coverArt'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/xhIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr.__deref__())
					self['coverArt'].show()
					del self.picload

	def dataError(self, error):
		print error
		
	def keyOK(self):
		if self.keyLocked:
			return
		xhLink = self['streamlist'].getCurrent()[0][2]
		print xhLink
		getPage(xhLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.playData).addErrback(self.dataError)
		
	def playData(self, data):
		xhTitle = self['streamlist'].getCurrent()[0][0]
		xhServer = re.findall("'srv': '(.*?)'", data)
		xhFile = re.findall("'file': '(.*?)'", data)
		if re.match('.*?http%3A', xhFile[0]):
			xhStream = urllib2.unquote(xhFile[0])
			print xhStream
		else:
			xhStream = xhServer[0]+"/key="+xhFile[0]
			print xhStream
		
		if xhStream:
			sref = eServiceReference(0x1001, 0, xhStream)
			sref.setName(xhTitle)
			self.session.open(MoviePlayer, sref)

	def keyPageDown(self):
		print "PageDown"
		if self.keyLocked:
			return
		if not self.page < 2:
			self.page -= 1
			self.loadpage()
		
	def keyPageUp(self):
		print "PageUP"
		if self.keyLocked:
			return
		self.page += 1
		self.loadpage()
		
	def keyLeft(self):
		if self.keyLocked:
			return
		self['streamlist'].pageUp()
		self.showInfos()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['streamlist'].pageDown()
		self.showInfos()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['streamlist'].up()
		self.showInfos()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['streamlist'].down()
		self.showInfos()
		
	def keyCancel(self):
		self.close()