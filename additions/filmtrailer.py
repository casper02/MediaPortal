from Plugins.Extensions.mediaportal.resources.imports import *
from Plugins.Extensions.mediaportal.resources.decrypt import *

def trailerMainListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT, entry[0])
		]
		
class trailer(Screen, ConfigListScreen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/trailer.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/trailer.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown
		}, -1)
		
		self['title'] = Label("Filmtrailer.net")
		self['leftContentTitle'] = Label("Trailer")
		self['stationIcon'] = Pixmap()
		self['page'] = Label("1")
		self['name'] = Label("Trailer Auswahl")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('mediaportal', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = False
		self.page = 1
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.keyLocked = True
		url = "http://www.filmtrailer.net/page/%s" % str(self.page)
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		trailer = re.findall('<div class="entry-content">.*?<a href="(http://www.filmtrailer.net/trailer/.*?)".*?<span class="slide-title">(.*?)</span>.*?<img class="attachment-thumbnail" src="(http://www.filmtrailer.net/filmposter/.*?)"', data, re.S)
		if trailer:
			self.streamList = []
			for (url,title,image) in trailer:
				self.streamList.append((decodeHtml(title), url, image))
			self.streamMenuList.setList(map(trailerMainListEntry, self.streamList))
		self.keyLocked = False
		self.showInfos()
			
	def dataError(self, error):
		print error

	def showInfos(self):
		self['page'].setText("%s" % str(self.page))
		coverUrl = self['streamlist'].getCurrent()[0][2]
		self.filmtrailer = self['streamlist'].getCurrent()[0][0]
		self['name'].setText(self.filmtrailer)
		if coverUrl:
			downloadPage(coverUrl, "/tmp/trIcon.jpg").addCallback(self.showCover)
		
	def showCover(self, picData):
		if fileExists("/tmp/trIcon.jpg"):
			self['stationIcon'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['stationIcon'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/trIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['stationIcon'].instance.setPixmap(ptr.__deref__())
					self['stationIcon'].show()
					del self.picload
					
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		url = self['streamlist'].getCurrent()[0][1]
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseID).addErrback(self.dataError)

	def parseID(self, data):
		channelID = re.findall('http://de.player-feed.filmtrailer.com/v2.0/cinema/(.*?)/', data, re.S)
		if channelID:
			print channelID
			url = "http://de.player-feed.filmtrailer.com/v2.0/cinema/" + channelID[0]
			getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseVideo).addErrback(self.dataError)
		
	def parseVideo(self, data):
		video = re.findall('<url>(.*?)<', data, re.S)
		if video:
			print video
			sref = eServiceReference(0x1001, 0, video[-1])
			sref.setName(self.filmtrailer)
			self.session.open(MoviePlayer, sref)

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