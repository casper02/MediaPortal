from imports import *
from decrypt import *

def autoBildGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 
class autoBildGenreScreen(Screen):

	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/autoBildGenreScreen.xml" % config.mediaportal.skin.value
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['title'] = Label("Autobild.de")
		self['name'] = Label("Genre Auswahl")
		self['coverArt'] = Pixmap()
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.genreliste.append(("Alle Videos", "http://www.autobild.de/videos/?page="))
		self.genreliste.append(("Erlkoenige", "http://www.autobild.de/videos/erlkoenige/?page="))
		self.genreliste.append(("Tests", "http://www.autobild.de/videos/tests/?page="))
		self.genreliste.append(("Crashtests", "http://www.autobild.de/videos/crashtests/?page="))
		self.genreliste.append(("Heft-Dvd", "http://www.autobild.de/videos/heft-dvd/?page="))
		self.genreliste.append(("Klassik", "http://www.autobild.de/videos/klassik/?page="))
		self.genreliste.append(("Messen", "http://www.autobild.de/videos/messen/?page="))
		self.genreliste.append(("Ratgeber", "http://www.autobild.de/videos/ratgeber/?page="))
		self.genreliste.append(("MotorSport", "http://www.autobild.de/index_3398533.html?page="))
		self.chooseMenuList.setList(map(autoBildGenreListEntry, self.genreliste))

	def keyOK(self):
		streamGenreLink = self['genreList'].getCurrent()[0][1]
		print streamGenreLink
		self.session.open(autoBildFilmListeScreen, streamGenreLink)

	def keyCancel(self):
		self.close()
		
def autoBildFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
class autoBildFilmListeScreen(Screen):
	def __init__(self, session, streamGenreLink):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/autoBildFilmListeScreen.xml" % config.mediaportal.skin.value
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		self.streamGenreLink = streamGenreLink
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown
		}, -1)

		self['title'] = Label("Autobild.de")
		self['name'] = Label("Spot Auswahl")
		self['handlung'] = Label("")
		self['page'] = Label("0")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.filmliste = []
		self.keckse = {}
		self.page = 1
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
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
		videos = re.findall('<div class="horizontal teaser clearfix">.*?<div class="pictureblock"><img src="(.*?)".*?<h2 class="kicker"><a href="(.*?)">(.*?)</a>.*?<p class="text">(.*?)</p>', data, re.S)
		if videos:
			self.filmliste = []
			for (image,url,title,handlung) in videos:
				self.filmliste.append((decodeHtml(title), url, image, handlung))
			self.chooseMenuList.setList(map(autoBildFilmListEntry, self.filmliste))
			self.keyLocked = False
			self.loadPic()

	def loadPic(self):
		streamName = self['filmList'].getCurrent()[0][0]
		self['name'].setText(streamName)
		handlung = self['filmList'].getCurrent()[0][3]
		self['handlung'].setText(decodeHtml(handlung))
		self['page'].setText(str(self.page))
		streamPic = self['filmList'].getCurrent()[0][2]
		downloadPage(streamPic, "/tmp/abIcon.jpg").addCallback(self.ShowCover)
	
	def ShowCover(self, picData):
		if fileExists("/tmp/abIcon.jpg"):
			self['coverArt'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/abIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr.__deref__())
					self['coverArt'].show()
					del self.picload

	def keyOK(self):
		if self.keyLocked:
			return
		streamLink = self['filmList'].getCurrent()[0][1]
		self.keyLocked = True
		url = "%s%s" % (streamLink ,"?getxml=1")
		print url
		getPage(url, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.findStream).addErrback(self.dataError)

	def findStream(self, data):
		self.keyLocked = False
		streamname = self['filmList'].getCurrent()[0][0]
		stream_url = re.findall('src="(.*?)"', data, re.S)
		if stream_url:
			sref = eServiceReference(0x1001, 0, stream_url[0])
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
		
	def keyPageDown(self):
		print "PageDown"
		if self.keyLocked:
			return
		if not self.page < 1:
			self.page -= 1
			self.loadPage()
			
	def keyPageUp(self):
		print "PageUp"
		if self.keyLocked:
			return
		self.page += 1 
		self.loadPage()
			
	def keyCancel(self):
		self.close()
