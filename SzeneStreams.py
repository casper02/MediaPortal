from imports import *
from decrypt import *

def SzeneStreamsGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		]

def SzeneStreamsFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 

def SzeneStreamsHosterListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

class SzeneStreamsGenreScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/SzeneStreamsGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/SzeneStreamsGenreScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['title'] = Label("Szene-Streams.com")
		self['name'] = Label("Genre Auswahl")
		self['coverArt'] = Pixmap()
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.genreliste.append(("Kinofilme", "http://szene-streams.com/publ/aktuelle_kinofilme/1-"))
		self.genreliste.append(("Alle Filme", "http://szene-streams.com/publ/0-"))
		self.chooseMenuList.setList(map(SzeneStreamsGenreListEntry, self.genreliste))

	def keyOK(self):
		streamGenreLink = self['genreList'].getCurrent()[0][1]
		self.session.open(SzeneStreamsFilmeListeScreen, streamGenreLink)

	def keyCancel(self):
		self.close()

class SzeneStreamsFilmeListeScreen(Screen):
	
	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/SzeneStreamsFilmeListeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/SzeneStreamsFilmeListeScreen.xml"
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
			"left" : self.keyLeft,
			"red" : self.keyTMDbInfo,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown
		}, -1)

		self['title'] = Label("Szene-Streams.com")
		self['name'] = Label("Filme Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		self['page'] = Label("1")
		
		self.keyLocked = True
		self.page = 1
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		url = "%s%s" % (self.streamGenreLink, str(self.page))
		print url
		getPage(url, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		print "daten bekommen"
		movies = re.findall('<div class="ImgWrapNews"><a href="(.*?.[jpg|png])".*?<a class="newstitl entryLink" href="(.*?)"><h2><b>(.*?)</b></h2></a>.*?<div class="MessWrapsNews2" style="height:110px;">(.*?)<', data, re.S)
		if movies:
			self.filmliste = []
			for (image,url,title,h) in movies:
				print title
				self.filmliste.append((decodeHtml(title), url, image, h))
			self.chooseMenuList.setList(map(SzeneStreamsFilmListEntry, self.filmliste))
			self.keyLocked = False
			self.loadPic()

	def loadPic(self):
		self['page'].setText(str(self.page))
		streamName = self['filmList'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamHandlung = self['filmList'].getCurrent()[0][3]
		self['handlung'].setText(decodeHtml(streamHandlung.replace('\n','')))
		streamPic = self['filmList'].getCurrent()[0][2]
		downloadPage(streamPic, "/tmp/Icon.jpg").addCallback(self.ShowCover)
			
	def ShowCover(self, picData):
		if fileExists("/tmp/Icon.jpg"):
			self['coverArt'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/Icon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr.__deref__())
					self['coverArt'].show()
					del self.picload

	def keyOK(self):
		if self.keyLocked:
			return
		streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]
		self.session.open(SzeneStreamsStreamListeScreen, streamLink, streamName)

	def keyTMDbInfo(self):
		if TMDbPresent:
			title = self['filmList'].getCurrent()[0][0]
			self.session.open(TMDbMain, title)

	def keyLeft(self):
		if self.keyLocked:
			return
		self['filmList'].pageUp()
		self.loadPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['filmList'].pageDown()
		self.loadPic()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['filmList'].up()
		self.loadPic()

	def keyDown(self):
		if self.keyLocked:
			return
		self['filmList'].down()
		self.loadPic()
		
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
		self.page += 1
		self.loadPage()
			
	def keyCancel(self):
		self.close()

class SzeneStreamsStreamListeScreen(Screen):
	
	def __init__(self, session, streamFilmLink, streamName):
		self.session = session
		self.streamFilmLink = streamFilmLink
		self.streamName = streamName

		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/SzeneStreamsStreamListeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/SzeneStreamsStreamListeScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("Szene-Streams.com")
		self['name'] = Label(self.streamName)
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		getPage(self.streamFilmLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		print "daten bekommen"
		raw = re.findall('(<legend><b><font color="#ff0000">.*?</fieldset></div>)', data, re.S)
		if raw:
			streams = []
			for each in raw:
				if re.match('.*?iframe src', each, re.S|re.I):
					streams += re.findall('<font color="#ff0000">(.*?)</font>.*?<iframe src="(.*?)"', each, re.S|re.I)
				else:
					streams += re.findall('<font color="#ff0000">(.*?)</font>.*?target="_blank" href="(.*?)"', each, re.S|re.I)

		if streams:
			for (hostername,stream) in streams:
				if re.match('.*?(putlocker|sockshare|streamclou|xvidstage|filenuke|movreel|nowvideo|xvidstream|uploadc|vreer|MonsterUploads|Novamov|Videoweed|Divxstage|Ginbig|Flashstrea|Movshare|yesload|faststream|Vidstream|PrimeShare|flashx|Divxmov|Putme|Zooupload|Wupfile)', hostername.strip(' '), re.S|re.I):
					print hostername.strip(' '), stream.strip('\n')
					self.filmliste.append((hostername.strip(' '), stream.strip('\n')))
			self.chooseMenuList.setList(map(SzeneStreamsHosterListEntry, self.filmliste))
			self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return
		streamLink = self['filmList'].getCurrent()[0][1]
		print self.streamName, streamLink
		get_stream_link(self.session).check_link(streamLink, self.got_link)

	def got_link(self, stream_url):
		if stream_url == None:
			message = self.session.open(MessageBox, _("Stream not found, try another Stream Hoster."), MessageBox.TYPE_INFO, timeout=3)
		else:
			sref = eServiceReference(0x1001, 0, stream_url)
			sref.setName(self.streamName)
			self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()
