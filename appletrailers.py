from imports import *

def appletrailersGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

def appletrailersFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
		
class appletrailersGenreScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/appletrailersGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/appletrailersGenreScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok" : self.keyOK,
			"cancel" : self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)

		self['title'] = Label("Apple Movie Trailers")
		self['name'] = Label("Genre Auswahl")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.suchString = ''
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.genreliste.append(("Newest (HD-1080p)", "http://trailers.apple.com/trailers/home/xml/newest_720p.xml", "1080p"))
		self.genreliste.append(("Current (HD-1080p)", "http://trailers.apple.com/trailers/home/xml/current_720p.xml", "1080p"))
		self.genreliste.append(("Newest (HD-720p)", "http://trailers.apple.com/trailers/home/xml/newest_720p.xml", "720p"))
		self.genreliste.append(("Current (HD-720p)", "http://trailers.apple.com/trailers/home/xml/current_720p.xml", "720p"))
		self.genreliste.append(("Newest (HD-480p)", "http://trailers.apple.com/trailers/home/xml/newest_480p.xml", "480p"))
		self.genreliste.append(("Current (HD-480p)", "http://trailers.apple.com/trailers/home/xml/current_480p.xml", "480p"))
		self.genreliste.append(("Newest (SD)", "http://trailers.apple.com/trailers/home/xml/newest.xml", "SD"))
		self.genreliste.append(("Current (SD)", "http://trailers.apple.com/trailers/home/xml/current.xml", "SD"))
		self.chooseMenuList.setList(map(appletrailersGenreListEntry, self.genreliste))

	def keyOK(self):
		streamGenreLink = self['genreList'].getCurrent()[0][1]
		streamHD = self['genreList'].getCurrent()[0][2]
		self.session.open(appletrailersFilmScreen, streamGenreLink, streamHD)
		
	def keyLeft(self):
		self['genreList'].pageUp()
		
	def keyRight(self):
		self['genreList'].pageDown()
		
	def keyUp(self):
		self['genreList'].up()
		
	def keyDown(self):
		self['genreList'].down()

	def keyCancel(self):
		self.close()

class appletrailersFilmScreen(Screen):
	
	def __init__(self, session, phCatLink, phHD):
		self.session = session
		self.phCatLink = phCatLink
		self.phHD = phHD
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/appletrailersFilmScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/appletrailersFilmScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)

		self.useragent = "QuickTime/7.6.2 (qtver=7.6.2;os=Windows NT 5.1Service Pack 3)"

		try:
			config.mediaplayer.useAlternateUserAgent.value = True
			config.mediaplayer.alternateUserAgent.value = self.useragent
			config.mediaplayer.useAlternateUserAgent.save()
			config.mediaplayer.alternateUserAgent.save()
			config.mediaplayer.save()
		except Exception, errormsg:
			config.mediaplayer = ConfigSubsection()
			config.mediaplayer.useAlternateUserAgent = ConfigYesNo(default=True)
			config.mediaplayer.alternateUserAgent = ConfigText(default=self.useragent)		

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok" : self.keyOK,
			"cancel" : self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft,
			"green" : self.keyPageNumber
		}, -1)

		self['title'] = Label("Apple Movie Trailers")
		self['name'] = Label("Film Auswahl")
		self['views'] = Label("")
		self['runtime'] = Label("")
		self['page'] = Label("1")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.page = 1
		
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadpage)
		
	def loadpage(self):
		self.keyLocked = True
		self.filmliste = []
		self['page'].setText(str(self.page))
		url = self.phCatLink
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadData).addErrback(self.dataError)
	
	def loadData(self, data):
		phMovies = re.findall('<movieinfo.*?<title>(.*?)</title>.*?<runtime>(.*?)</runtime>.*?<location>(.*?)</location>.*?<large filesize=".*?">(.*?)</large>', data, re.S)
		if phMovies:
			for (phTitle, phRuntime, phImage, phUrl) in phMovies:
				self.filmliste.append((decodeHtml(phTitle), phUrl, phImage, phRuntime))
			self.chooseMenuList.setList(map(appletrailersFilmListEntry, self.filmliste))
			self.showInfos()
		self.keyLocked = False

	def dataError(self, error):
		print error

	def showInfos(self):
		phTitle = self['genreList'].getCurrent()[0][0]
		phImage = self['genreList'].getCurrent()[0][2]
		phRuntime = self['genreList'].getCurrent()[0][3]
		self['name'].setText(phTitle)
		self['runtime'].setText(phRuntime)
		downloadPage(phImage, "/tmp/Icon.jpg").addCallback(self.ShowCover)
		
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

	def keyPageNumber(self):
		self.session.openWithCallback(self.callbackkeyPageNumber, VirtualKeyBoard, title = (_("Seitennummer eingeben")), text = str(self.page))

	def callbackkeyPageNumber(self, answer):
		if answer is not None:
			self.page = int(answer)
			self.loadpage()
		
	def keyLeft(self):
		if self.keyLocked:
			return
		self['genreList'].pageUp()
		self.showInfos()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['genreList'].pageDown()
		self.showInfos()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['genreList'].up()
		self.showInfos()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['genreList'].down()
		self.showInfos()
		
	def keyOK(self):
		if self.keyLocked:
			return
		phTitle = self['genreList'].getCurrent()[0][0]
		phLink = self['genreList'].getCurrent()[0][1]
		phHD = self.phHD 
		if phHD == "720p":
			phLink = phLink.replace('a720p.m4v','h720p.mov')
		if phHD == "1080p":
			phLink = phLink.replace('a720p.m4v','h1080p.mov')
			phLink = phLink.replace('h720p.mov','h1080p.mov')
		self.keyLocked = False
		self.play(phLink)
		
	def play(self,file):
		xxxtitle = self['genreList'].getCurrent()[0][0]
		sref = eServiceReference(0x1001, 0, file)
		sref.setName(xxxtitle)
		self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		try:
			config.mediaplayer.useAlternateUserAgent.value = False
			config.mediaplayer.alternateUserAgent.value = ""
			config.mediaplayer.useAlternateUserAgent.save()
			config.mediaplayer.alternateUserAgent.save()
			config.mediaplayer.save()
		except Exception, errormsg:
			config.mediaplayer = ConfigSubsection()
			config.mediaplayer.useAlternateUserAgent = ConfigYesNo(default=False)
			config.mediaplayer.alternateUserAgent = ConfigText(default="")
		self.close()
