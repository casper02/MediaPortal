from Plugins.Extensions.MediaPortal.resources.imports import *

def ZDFGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]

def ZDFFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 

class ZDFGenreScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/RTLnowGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/RTLnowGenreScreen.xml"
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)
		
		self['title'] = Label("ZDF Mediathek")
		self['name'] = Label("Auswahl der Sendung")
		self['handlung'] = Label("")
		self['Pic'] = Pixmap()
		
		self.genreliste = []
		self.keyLocked = True
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['List'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.genreliste = []
		for c in xrange(26):
			self.genreliste.append((chr(ord('A') + c), None))
		self.genreliste.insert(0, ('0-9', None))
		self.chooseMenuList.setList(map(ZDFGenreListEntry, self.genreliste))
		self.keyLocked = False

	def dataError(self, error):
		print error

	def keyOK(self):
		if self.keyLocked:
			return
		streamGenreLink = self['List'].getCurrent()[0][0]
		self.session.open(ZDFSubGenreScreen, streamGenreLink)
		
	def keyLeft(self):
		self['List'].pageUp()
		
	def keyRight(self):
		self['List'].pageDown()
		
	def keyUp(self):
		self['List'].up()

	def keyDown(self):
		self['List'].down()

	def keyCancel(self):
		self.close()
		
class ZDFSubGenreScreen(Screen):
	
	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/RTLnowGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/RTLnowGenreScreen.xml"
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)
		
		self['title'] = Label("ZDF Mediathek")
		self['name'] = Label("Auswahl der Sendung")
		self['handlung'] = Label("")
		self['Pic'] = Pixmap()
		
		self.genreliste = []
		self.keyLocked = True
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['List'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.keyLocked = True
		url = "http://www.zdf.de/ZDFmediathek/xmlservice/web/sendungenAbisZ?detailLevel=2&characterRangeStart=%s&characterRangeEnd=%s" % (self.streamGenreLink, self.streamGenreLink)
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def loadPageData(self, data):
		sendungen = re.findall('<teaserimage alt=".*?" key="298x168">(.*?)</teaserimage>.*?<title>(.*?)</title>.*?<detail>(.*?)</detail>.*?<assetId>(.*?)</assetId>', data, re.S)
		if sendungen:
			for (image,title,handlung,id) in sendungen:
				self.genreliste.append((decodeHtml(title),id,image,handlung))
		else:
			self.genreliste.append(('Keine Sendungen mit diesem Buchstaben vorhanden.', None, None, None))
		self.chooseMenuList.setList(map(ZDFGenreListEntry, self.genreliste))
		self.keyLocked = False
		self.loadPic()

	def dataError(self, error):
		print error

	def loadPic(self):
		streamPic = self['List'].getCurrent()[0][2]
		if streamPic == None:
			return
		streamName = self['List'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamHandlung = self['List'].getCurrent()[0][3]
		self['handlung'].setText(decodeHtml(streamHandlung))
		downloadPage(streamPic, "/tmp/Icon.jpg").addCallback(self.ShowCover)
			
	def ShowCover(self, picData):
		if fileExists("/tmp/Icon.jpg"):
			self['Pic'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['Pic'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/Icon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['Pic'].instance.setPixmap(ptr.__deref__())
					self['Pic'].show()
					del self.picload

	def keyOK(self):
		if self.keyLocked:
			return
		streamGenreLink = self['List'].getCurrent()[0][1]
		if streamGenreLink == None:
			return
		self.session.open(ZDFFilmeListeScreen, streamGenreLink)
		
	def keyLeft(self):
		if self.keyLocked:
			return
		self['List'].pageUp()
		self.loadPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['List'].pageDown()
		self.loadPic()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['List'].up()
		self.loadPic()

	def keyDown(self):
		if self.keyLocked:
			return
		self['List'].down()
		self.loadPic()

	def keyCancel(self):
		self.close()

class ZDFFilmeListeScreen(Screen):
	
	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/RTLnowGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/RTLnowGenreScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)

		self['title'] = Label("ZDF Mediathek")
		self['name'] = Label("Folgen Auswahl")
		self['handlung'] = Label("")
		self['Pic'] = Pixmap()
		
		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['List'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		url = "http://www.zdf.de/ZDFmediathek/xmlservice/web/aktuellste?maxLength=50&id="+self.streamGenreLink+"&ak=web&ganzeSendungen=false&offset=0"
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		self.filmliste = []
		folgen = re.findall('<type>video</type>.*?<teaserimage alt=".*?" key="298x168">(.*?)</teaserimage>.*?<title>(.*?)</title>.*?<detail>(.*?)</detail>.*?<assetId>(.*?)</assetId>', data, re.S)
		if folgen:
			for (image,title,handlung,id) in folgen:
				self.filmliste.append((decodeHtml(title),id,image,handlung))
		else:
			self.filmliste.append(('Keine Folgen gefunden.', None, None, None))
		self.chooseMenuList.setList(map(ZDFFilmListEntry, self.filmliste))
		self.keyLocked = False
		self.loadPic()

	def loadPic(self):
		streamPic = self['List'].getCurrent()[0][2]
		if streamPic == None:
			return
		streamName = self['List'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamHandlung = self['List'].getCurrent()[0][3]
		self['handlung'].setText(decodeHtml(streamHandlung))
		downloadPage(streamPic, "/tmp/Icon.jpg").addCallback(self.ShowCover)
			
	def ShowCover(self, picData):
		if fileExists("/tmp/Icon.jpg"):
			self['Pic'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['Pic'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/Icon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['Pic'].instance.setPixmap(ptr.__deref__())
					self['Pic'].show()
					del self.picload

	def keyOK(self):
		if self.keyLocked:
			return
		self.streamName = self['List'].getCurrent()[0][0]
		id = self['List'].getCurrent()[0][1]
		if id == None:
			return
		url = "http://www.zdf.de/ZDFmediathek/xmlservice/web/beitragsDetails?ak=web&id="+id
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.get_xml).addErrback(self.dataError)

	def get_xml(self, data):
		print "xml data"
		stream = re.findall('basetype="h264_aac_mp4_http_na_na".*?<quality>veryhigh</quality>.*?<url>(http://rodl.zdf.de.*?mp4)</url>', data, re.S)
		if stream:
			sref = eServiceReference(0x1001, 0, stream[0])
			sref.setName(self.streamName)
			self.session.open(MoviePlayer, sref)
			
	def keyLeft(self):
		if self.keyLocked:
			return
		self['List'].pageUp()
		self.loadPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['List'].pageDown()
		self.loadPic()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['List'].up()
		self.loadPic()

	def keyDown(self):
		if self.keyLocked:
			return
		self['List'].down()
		self.loadPic()

	def keyCancel(self):
		self.close()
