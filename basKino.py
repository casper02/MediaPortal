from imports import *
from decrypt import *

def baskinoMainListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT, entry[0])
		]
		
class baskino(Screen):
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/baskino.xml" % config.mediaportal.skin.value
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
		
		self['title'] = Label("Baskino.com")
		self['leftContentTitle'] = Label("Movies")
		self['stationIcon'] = Pixmap()
		self['page'] = Label("1")
		self['name'] = Label("Choose a Movie")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = False
		self.page = 1
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.keyLocked = True
		url = "http://baskino.com/new/page/%s/" % str(self.page)
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		movies = re.findall('<div class="postcover">.*?<a href="(.*?)">.*?<img title="(.*?)" src="(.*?)"', data, re.S)
		if movies:
			self.streamList = []
			for (url,title,image) in movies:
				self.streamList.append((decodeHtml(title), url, image))
			self.streamMenuList.setList(map(baskinoMainListEntry, self.streamList))
		self.keyLocked = False
		self.showInfos()
			
	def dataError(self, error):
		print error

	def showInfos(self):
		self['page'].setText("%s" % str(self.page))
		coverUrl = self['streamlist'].getCurrent()[0][2]
		self.filmName = self['streamlist'].getCurrent()[0][0]
		self['name'].setText(self.filmName)
		if coverUrl:
			downloadPage(coverUrl, "/tmp/baIcon.jpg").addCallback(self.showCover)
		
	def showCover(self, picData):
		if fileExists("/tmp/baIcon.jpg"):
			self['stationIcon'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['stationIcon'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/baIcon.jpg", 0, 0, False) == 0:
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
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseVideo).addErrback(self.dataError)
		
	def parseVideo(self, data):
		video = re.findall('file:"(.*?)"', data, re.S)
		if video:
			print video
			sref = eServiceReference(0x1001, 0, video[0])
			sref.setName(self.filmName)
			self.session.open(MoviePlayer, sref)
		else:
			message = self.session.open(MessageBox, _("No Stream Found."), MessageBox.TYPE_INFO, timeout=3)

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
