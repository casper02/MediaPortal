from Plugins.Extensions.mediaportal.resources.imports import *
#from Plugins.Extensions.mediaportal.resources.playrtmpmovie import PlayRtmpMovie

def kikaListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 600, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0]),
		(eListboxPythonMultiContent.TYPE_TEXT, 620, 0, 300, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[1])
		]

class kikaGenreScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"
		
		path = "%s/%s/defaultGenreScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/defaultGenreScreen.xml"

		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self.keyLocked = True
		self['title'] = Label("KIKA+")
		self['ContentTitle'] = Label("Sendungen von A-Z")
		self['name'] = Label("")
		self['F1'] = Label("Exit")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		self['F1'].hide()
		self['F2'].hide()
		self['F3'].hide()
		self['F4'].hide()

		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.keyLocked = True
		url = "http://www.kikaplus.net/clients/kika/kikaplus"
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def loadPageData(self, data):
		kiVideos = re.findall('<a href="(\?programm=.*?)" title="(.*?)" class="overlay_link" >(.*?)</a><br />', data, re.S)
		if kiVideos:
			self.genreliste = []
			for (url,count_videos,title) in kiVideos:
				url = "http://kikaplus.net/clients/kika/kikaplus/index.php%s" % url.replace('&amp;','&')
				self.genreliste.append((title,count_videos,url))
			self.chooseMenuList.setList(map(kikaListEntry, self.genreliste))
			self.keyLocked = False

	def dataError(self, error):
		print error

	def keyOK(self):
		if self.keyLocked:
			return
		kikaurl = self['genreList'].getCurrent()[0][2]
		print kikaurl
		self.session.open(kikaFilmListeScreen, kikaurl)

	def keyCancel(self):
		self.close()
		
class kikaFilmListeScreen(Screen):
	
	def __init__(self, session, genreLink):
		self.session = session
		self.genreLink = genreLink
		
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/defaultListScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/defaultListScreen.xml"
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
		
		self.keyLocked = True
		self['title'] = Label("KIKA+")
		self['ContentTitle'] = Label("Folgen:")
		self['name'] = Label("")
		self['F1'] = Label("Exit")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		self['F1'].hide()
		self['F2'].hide()
		self['F3'].hide()
		self['F4'].hide()
		self['coverArt'] = Pixmap()
		self['page'] = Label("")
		self['Page'] = Label("")
		self['handlung'] = Label("")
		
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['liste'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.keyLocked = True
		getPage(self.genreLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def loadPageData(self, data):
		kiVideos = re.findall('href="(\?id=.*?programm=.*?)".*?<img alt="" src="..(.*?)".*?</label><br />(.*?)<br /><br />Sendedatum:.(.*?)<br />', data, re.S)
		if kiVideos:
			print "ja"
			self.filmliste = []
			for (url,image,title,datum) in kiVideos:
				url = "http://kikaplus.net/clients/kika/kikaplus/index.php%s" % url.replace('&amp;','&')
				image = "http://kikaplus.net/clients/kika%s" % image
				self.filmliste.append((title,datum,url,image))
			self.chooseMenuList.setList(map(kikaListEntry, self.filmliste))
			self.keyLocked = False

	def dataError(self, error):
		print error

	def loadPic(self):
		streamPic = self['liste'].getCurrent()[0][3]
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

	def keyLeft(self):
		if self.keyLocked:
			return
		self['liste'].pageUp()
		self.loadPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['liste'].pageDown()
		self.loadPic()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['liste'].up()
		self.loadPic()

	def keyDown(self):
		if self.keyLocked:
			return
		self['liste'].down()
		self.loadPic()
		
	def keyOK(self):
		if self.keyLocked:
			return
		self.streamName = self['liste'].getCurrent()[0][0]
		kikaurl = self['liste'].getCurrent()[0][2]
		print kikaurl
		getPage(kikaurl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getStream).addErrback(self.dataError)
		
	def getStream(self, data):
		stream = re.findall('so.addVariable\("fullscreenPfad", "(rtmp://.*?)"', data, re.S)
		if stream:
			print stream
			sref = eServiceReference(0x1001, 0, stream[0])
			sref.setName(self.streamName)
			self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()