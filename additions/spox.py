from Plugins.Extensions.mediaportal.resources.imports import *
from Plugins.Extensions.mediaportal.resources.decrypt import *

def spoboxGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 
class spoboxGenreScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/spoboxGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/spoboxGenreScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['title'] = Label("Spobox.tv")
		self['name'] = Label("Genre Auswahl")
		self['coverArt'] = Pixmap()
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.genreliste.append(("Tischtennis", "http://www.spobox.tv/tischtennis"))
		self.genreliste.append(("Volleyball", "http://www.spobox.tv/volleyball"))
		self.genreliste.append(("Sport-Mix", "http://www.spobox.tv/sport-mix"))
		self.genreliste.append(("Tennis", "http://www.spobox.tv/tennis"))
		self.genreliste.append(("Judo", "http://www.spobox.tv/judo"))
		self.genreliste.append(("Beachvolleyball", "http://www.spobox.tv/beachvolleyball"))
		self.genreliste.append(("Hockey", "http://www.spobox.tv/hockey"))
		self.genreliste.append(("Motocross", "http://www.spobox.tv/motocross"))
		self.chooseMenuList.setList(map(spoboxGenreListEntry, self.genreliste))

	def keyOK(self):
		streamGenreName = self['genreList'].getCurrent()[0][0]
		streamGenreLink = self['genreList'].getCurrent()[0][1]
		print streamGenreLink
		self.session.open(spoboxSubGenreScreen, streamGenreName, streamGenreLink)

	def keyCancel(self):
		self.close()

class spoboxSubGenreScreen(Screen):
	
	def __init__(self, session, streamGenreName, streamGenreLink):
		self.session = session
		self.streamGenreName = streamGenreName
		self.streamGenreLink = streamGenreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/spoboxSubGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/spoboxSubGenreScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['title'] = Label("Spobox.tv")
		self['name'] = Label("Genre Auswahl")
		self['coverArt'] = Pixmap()
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		getPage(self.streamGenreLink, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print error

	def loadPageData(self, data):
		genre = re.findall('<li><a href="(/'+self.streamGenreName+'.*?/.*?)">(.*?)</a></li>', data, re.I)
		if genre:
			for (url,name) in genre:
				url = "http://www.spobox.tv%s" % url
				self.genreliste.append((name, url))
		self.chooseMenuList.setList(map(spoboxGenreListEntry, self.genreliste))

	def keyOK(self):
		streamGenreLink = self['genreList'].getCurrent()[0][1]
		print streamGenreLink
		self.session.open(spoboxFilmListeScreen, streamGenreLink)

	def keyCancel(self):
		self.close()
		
def spoboxFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
class spoboxFilmListeScreen(Screen):
	
	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/spoboxFilmListeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/spoboxFilmListeScreen.xml"
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

		self['title'] = Label("Spobox.tv")
		self['name'] = Label("Spot Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.filmliste = []
		self.keckse = {}
		self.page = 1
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		getPage(self.streamGenreLink, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		print "daten bekommen"
		videos = re.findall('<a href="(.*?)" title="(.*?)"><span class="thumb mini">.*?src="(.*?)"', data)
		if videos:
			self.filmliste = []
			for (url,name,image) in videos:
				url = "http://www.spobox.tv%s" % url
				self.filmliste.append((decodeHtml(name), url, image))
			self.chooseMenuList.setList(map(spoboxFilmListEntry, self.filmliste))
			self.keyLocked = False
			self.loadPic()

	def loadPic(self):
		streamName = self['filmList'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamPic = self['filmList'].getCurrent()[0][2]
		downloadPage(streamPic, "/tmp/spoIcon.jpg").addCallback(self.ShowCover)
	
	def ShowCover(self, picData):
		if fileExists("/tmp/spoIcon.jpg"):
			self['coverArt'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/spoIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr.__deref__())
					self['coverArt'].show()
					del self.picload

	def keyOK(self):
		if self.keyLocked:
			return
		streamLink = self['filmList'].getCurrent()[0][1]
		getPage(streamLink, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.findStream).addErrback(self.dataError)

	def findStream(self, data):
		stream = re.findall('<a data-.*?href="(.*?)"', data, re.S)
		if stream:
			streamname = self['filmList'].getCurrent()[0][0]
			sref = eServiceReference(0x1001, 0, stream[0])
			sref.setName(streamname)
			self.session.open(MoviePlayer, sref)			

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
			
	def keyCancel(self):
		self.close()