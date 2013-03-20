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
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/laolaScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/laolaScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
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
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
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
			id = re.findall('streamid=(.*?)&', data, re.S)
			xml = 'http://streamaccess.unas.tv/hdflash/1/hdlaola1_%s.xml?t=.smil&partnerid=1&streamid=%s' % (id[0], id[0])
			if xml:
				getPage(xml, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseXML).addErrback(self.dataError)
			
	def parseXML(self, data):
		laTitle = self['roflList'].getCurrent()[0][0]
		main_url = re.findall('<meta name="httpBase" content="(.*?)"', data)
		url_string = re.findall('<video src="(.*?)" system-bitrate="(.*?)"', data, re.S)
		if main_url and url_string:
			x = len(url_string)-1
			stream_url = "%s%s%s" % (main_url[0], url_string[x][0], url_string[x][1])
			print stream_url
			sref = eServiceReference(0x1001, 0, stream_url)
			sref.setName(laTitle)
			self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()