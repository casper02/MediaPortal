from imports import *
from decrypt import *

def dreamscreencastListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 830, 25, 0, RT_HALIGN_LEFT, entry[0])
		]
class dreamscreencast(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/dreamscreencast.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/dreamscreencast.xml"
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
			"left" : self.keyLeft
		}, -1)
		
		self['title'] = Label("Dreamscreencast.com")
		self['leftContentTitle'] = Label("Videos:")
		self['stationIcon'] = Pixmap()
		self['name'] = Label("")
		self['handlung'] = Label("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.streamList = []
		url = "http://feeds.feedburner.com/dreamscreencast?format=xml"
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		videos = re.findall('<item>.*?<title>(.*?)</title>.*?<link>(.*?)</link>.*?<itunes:summary>(.*?)</itunes:summary>.*?<media:content url="(.*?)"', data, re.S)
		if videos:
			for (title,url,handlung,stream) in videos:
				print title
				if title != "Dreamscreencast - Vision and Sound":
					self.streamList.append((decodeHtml(title),url,handlung,stream))
			self.streamMenuList.setList(map(dreamscreencastListEntry, self.streamList))
			self.keyLocked = False
			self.showInfos()
					
	def dataError(self, error):
		print error
			
	def showInfos(self):
		self.Dscname = self['streamlist'].getCurrent()[0][0]
		handlung = self['streamlist'].getCurrent()[0][2]
		url = self['streamlist'].getCurrent()[0][1]
		self['handlung'].setText(decodeHtml(handlung))
		self['name'].setText(self.Dscname)
		if url:
			print url
			getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getImage).addErrback(self.dataError)
			
	def getImage(self, data):
		image = re.findall('<a rel="gallery" href="(.*?)"', data, re.S)
		if image:
			print image[0]
			downloadPage(image[0], "/tmp/dscIcon.jpg").addCallback(self.showCover)
		
	def showCover(self, picData):
		if fileExists("/tmp/dscIcon.jpg"):
			self['stationIcon'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['stationIcon'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/dscIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['stationIcon'].instance.setPixmap(ptr.__deref__())
					self['stationIcon'].show()
					del self.picload			

	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		stream = self['streamlist'].getCurrent()[0][3]
		if stream:
			print stream
			sref = eServiceReference(0x1001, 0, stream)
			sref.setName(self.Dscname)
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
		
	def keyCancel(self):
		self.close()
