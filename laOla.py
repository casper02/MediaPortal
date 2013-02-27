from imports import *
from decrypt import *

def laola2ListEntry(entry):
	date_time = re.findall('(.*?,.*?),(.*?)$', entry[3], re.S)
	info = re.findall('(.*?,.*?),(.*?)$', entry[0], re.S)
	(time, date) = date_time[0]
	print time, date
	(sport, teams) = info[0]
	print sport, teams
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 150, 25, 0, RT_HALIGN_RIGHT | RT_VALIGN_CENTER, time),
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 25, 150, 25, 0, RT_HALIGN_RIGHT | RT_VALIGN_CENTER, date),
		(eListboxPythonMultiContent.TYPE_TEXT, 200, 0, 560, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, sport),
		(eListboxPythonMultiContent.TYPE_TEXT, 200, 25, 560, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, teams)
		]
		
class laolaScreen(Screen):
	skin = 	"""
		<screen name="Laola1.tv" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="roflList" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="roflPic" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
		</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up"    : self.keyUp,
			"down"  : self.keyDown,
			"left"  : self.keyLeft,
			"right" : self.keyRight,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown
		}, -1)
		
		self.keyLocked = True
		self.page = 1
		self['title'] = Label("Laola1.tv")
		self['roflPic'] = Pixmap()
		self['name'] = Label("")
		self.laListe = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(50)
		self['roflList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.keyLocked = True
		url = "http://www.laola1.tv/de/de/upcoming-livestreams/video/0-1369-.html"
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def loadPageData(self, data):
		laStreams = re.findall('<div class="teaser_bild_live" title="LIVE:.(.*?)"><a href="(http://www.laola1.tv/.*?)"><img src="(.*?.jpg)" border="0" />.*?<div class="teaser_head_live".*?>(.*?)<', data, re.S)
		if laStreams:
			self.laListe = []
			for (laTitle,laUrl,laImage,laTime) in laStreams:
				self.laListe.append((laTitle,laUrl,laImage,laTime))
			self.chooseMenuList.setList(map(laola2ListEntry, self.laListe))
			self.keyLocked = False
			self.showPic()

	def dataError(self, error):
		print error
		
	def showPic(self):
		laTitle = self['roflList'].getCurrent()[0][0]
		laPicLink = self['roflList'].getCurrent()[0][2]
		self['name'].setText(laTitle)
		downloadPage(laPicLink, "/tmp/laPic.jpg").addCallback(self.roflCoverShow)
		
	def roflCoverShow(self, data):
		if fileExists("/tmp/laPic.jpg"):
			self['roflPic'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['roflPic'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/laPic.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['roflPic'].instance.setPixmap(ptr.__deref__())
					self['roflPic'].show()
					del self.picload

	def keyPageDown(self):
		print "PageDown"
		if self.keyLocked:
			return
		if not self.page < 2:
			self.page -= 1
			self.loadPage()
		
	def keyPageUp(self):
		print "PageUP"
		if self.keyLocked:
			return
		if not self.page > 2:
			self.page += 1
			self.loadPage()
		
	def keyLeft(self):
		if self.keyLocked:
			return
		self['roflList'].pageUp()
		self.showPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['roflList'].pageDown()
		self.showPic()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['roflList'].up()
		self.showPic()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['roflList'].down()
		self.showPic()
		
	def keyOK(self):
		if self.keyLocked:
			return
		laUrl = self['roflList'].getCurrent()[0][1]
		print laUrl
		getPage(laUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)

	def parseData(self, data):
		if re.match('.*?Dieser Stream ist bereits beendet', data, re.S):
			print "Dieser Stream ist bereits beendet."
			message = self.session.open(MessageBox, _("Dieser Stream ist bereits beendet."), MessageBox.TYPE_INFO, timeout=3)
		elif re.match('.*?(Dieser Stream beginnt am|This stream starts at)', data, re.S):
			print "Dieser Stream wurde noch nicht gestartet."
			message = self.session.open(MessageBox, _("Dieser Stream wurde noch nicht gestartet."), MessageBox.TYPE_INFO, timeout=3)
		else:
			xml = re.findall('"flashvars".*?videopfad=(.*?.xml)', data)
			if xml:
				getPage(xml[0], headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseXML).addErrback(self.dataError)
			
	def parseXML(self, data):
		laTitle = self['roflList'].getCurrent()[0][0]
		main_url = re.findall('<meta name="httpBase" content="(.*?)"', data)
		url_string = re.findall('<video src="(.*?)" system-bitrate="(.*?)"', data, re.S)
		if main_url and url_string:
			(hash, bitrate) =  url_string[-1]
			stream_url = "%s%s%s" % (main_url[0], hash, bitrate)
			print stream_url
			sref = eServiceReference(0x1001, 0, stream_url)
			sref.setName(laTitle)
			self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()