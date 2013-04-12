from Plugins.Extensions.mediaportal.resources.imports import *

def moovizonGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 0, 0, 600, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		]
		
def moovizonListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 600, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]

class moovizonGenreScreen(Screen):
	
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
		self.language = "de"
		self['title'] = Label("moovizon.com")
		self['ContentTitle'] = Label("Genre:")
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
		url = "http://moovizon.com"
		print url, self.language
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def loadPageData(self, data):
		genre_raw = re.findall('>Categories(.*?)>Languages', data, re.S)
		if genre_raw:
			genre = re.findall('<li><a href="/.*?/(.*?)/all">(.*?).:.*?</a></li>', genre_raw[0], re.S)
		if genre:
			self.genreliste = []
			for cat_id,genreName in genre:
				url = "http://moovizon.com/%s/%s/all" % (self.language,cat_id)
				self.genreliste.append((genreName,url))
			self.chooseMenuList.setList(map(moovizonGenreListEntry, self.genreliste))
			self.keyLocked = False

	def dataError(self, error):
		print error

	def keyOK(self):
		if self.keyLocked:
			return
		moovizonGenre = self['genreList'].getCurrent()[0][0]
		moovizonUrl = self['genreList'].getCurrent()[0][1]
		print moovizonGenre, moovizonUrl
		self.session.open(moovizonFilmListeScreen, moovizonGenre, moovizonUrl)

	def keyCancel(self):
		self.close()
		
class moovizonFilmListeScreen(Screen):
	
	def __init__(self, session, genreName, genreLink):
		self.session = session
		self.genreLink = genreLink
		self.genreName = genreName
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"
		
		path = "%s/%s/defaultListScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/defaultListScreen.xml"

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
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown
		}, -1)
		
		self.keyLocked = True
		self.page = 0
		self['title'] = Label("moovizon.com")
		self['ContentTitle'] = Label("%s:" % self.genreName)
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
		self['Page'] = Label("1")
		self['page'] = Label("")
		self['handlung'] = Label("")
		
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['liste'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.keyLocked = True
		url = "%s?page=%s" % (self.genreLink,str(self.page))
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def loadPageData(self, data):
		countp = re.findall('totalPages: (.*?),', data, re.S)
		if countp:
			self['page'].setText(countp[0])

		movies = re.findall('<li><a href="(/movie/.*?)"><img src="(.*?)" alt=".*?" class="cover"></a><h2>(.*?)</h2><img src="http://static.moovizon.com/img/flag/(.*?).png"',data, re.S)
		if movies:
			self.filmliste = []
			for (url,image,title,lang) in movies:
				url = "http://moovizon.com%s" % url.replace('&amp;','&')
				self.filmliste.append((title,url,image))
			self.chooseMenuList.setList(map(moovizonListEntry, self.filmliste))
			self.loadPic()
			self['Page'].setText(str(self.page+1))
			self.keyLocked = False

	def dataError(self, error):
		print error

	def loadPic(self):
		streamPic = self['liste'].getCurrent()[0][2]
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
		self.moovizonName = self['liste'].getCurrent()[0][0]
		moovizonurl = self['liste'].getCurrent()[0][1]
		print self.moovizonName, moovizonurl
		#getPage(moovizonurl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getStream).addErrback(self.dataError)
		
	def getStream(self, data):
		stream = re.findall('so.addVariable\("fullscreenPfad", "(rtmp://.*?)"', data, re.S)
		if stream:
			print stream
			sref = eServiceReference(0x1001, 0, stream[0])
			sref.setName(self.streamName)
			self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()