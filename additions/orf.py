from Plugins.Extensions.mediaportal.resources.imports import *
from Components.config import config
from Plugins.Extensions.mediaportal.resources.playrtmpmovie import PlayRtmpMovie

def ORFGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]

def ORFFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 

class ORFGenreScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/RTLnowGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/RTLnowGenreScreen.xml"
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
		
		self['title'] = Label("ORF.de")
		self['name'] = Label("Auswahl der Sendungen.")
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
		url = "http://tvthek.orf.at/"
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def loadPageData(self, data):
		sendungen = re.findall('<a href="(/programs/.*?)" title="(.*?)">.*?<img src="(http://tvthek.orf.at/assets.*?)"', data, re.S)
		if sendungen:
			self.genreliste = []
			for (url,title,image) in sendungen:
				url = "http://tvthek.orf.at%s" % url
				self.genreliste.append((title,url,image))
			self.chooseMenuList.setList(map(ORFGenreListEntry, self.genreliste))
			self.loadPic()
			self.keyLocked = False

	def dataError(self, error):
		print error

	def loadPic(self):
		streamName = self['List'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamPic = self['List'].getCurrent()[0][2]
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
		self.streamGenreLink = self['List'].getCurrent()[0][1]
		getPage(self.streamGenreLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.check_xml).addErrback(self.dataError)

	def dataError(self, error):
		print error
		
	def check_xml(self,data):
		if re.match('.*?<span>Weitere Folgen</span>', data, re.S):
			print "mehr folgen.."
			self.session.open(ORFFilmeListeScreen, self.streamGenreLink)
		else:
			print "eine fole."
			xml = re.findall("ORF.flashXML = '(.*?)'", data, re.S)
			if xml:
				data = urllib.unquote(xml[0])
				self.session.open(ORFStreamListeScreen, data)
		
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

class ORFFilmeListeScreen(Screen):
	
	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/RTLnowFilmeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/RTLnowFilmeScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("ORF.de")
		self['name'] = Label("Folgen Auswahl")
		
		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['List'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		getPage(self.streamGenreLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		self.filmliste = []
		folgen = re.findall('<li.*?><a href="#" class="nolink">(.*?)</a>.*?<li><a href="(.*?)">(.*?)</a></li>', data, re.S)
		if folgen:
			for (datum,url,title) in folgen:
				url = "http://tvthek.orf.at%s" % url
				title = "%s - %s" % (datum, title)
				self.filmliste.append((title,url))
			self.chooseMenuList.setList(map(ORFFilmListEntry, self.filmliste))
			self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return
		streamName = self['List'].getCurrent()[0][0]
		url = self['List'].getCurrent()[0][1]
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.get_xml).addErrback(self.dataError)

	def get_xml(self, data):
			xml = re.findall("ORF.flashXML = '(.*?)'", data, re.S)
			if xml:
				data = urllib.unquote(xml[0])
				self.session.open(ORFStreamListeScreen, data)

	def keyCancel(self):
		self.close()
		
class ORFStreamListeScreen(Screen):
	
	def __init__(self, session, data_raw):
		self.session = session
		self.data_raw = data_raw
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/RTLnowFilmeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/RTLnowFilmeScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("ORF.de")
		self['name'] = Label("Folgen Auswahl")
		
		self.keyLocked = True
		self.streamliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['List'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		print "hole daten"
		folgen = re.findall('<Title><!\[CDATA\[(.*?)\]\]></Title>.*?<VideoUrl><!\[CDATA\[(.*?mp4)\]\]></VideoUrl>', self.data_raw, re.S)
		if folgen:
			self.streamliste = []
			for (title,rtmp_link) in folgen:
					print title
					self.streamliste.append((title,rtmp_link))
			self.chooseMenuList.setList(map(ORFFilmListEntry, self.streamliste))
			self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return
		title = self['List'].getCurrent()[0][0]
		url = self['List'].getCurrent()[0][1]
		
		# wird das hier benoetigt?
		#if config.mediaportal.useRtmpDump.value:
		#	movieinfo = [url,title+".mp4"]
		#	self.session.open(PlayRtmpMovie, movieinfo, title)
		#else:
			final = "%s" % url
			print final
			sref = eServiceReference(0x1001, 0, final)
			sref.setName(title)
			self.session.open(MoviePlayer, sref)
		
	def keyCancel(self):
		self.close()
