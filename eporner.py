from imports import *

def epornerGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

def epornerFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
		
class epornerGenreScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/epornerGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/epornerGenreScreen.xml"
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

		self['title'] = Label("Eporner.com")
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
		self.genreliste.append(("--- Search ---", "callSuchen"))
		self.genreliste.append(("New", "http://www.eporner.com//"))
		self.genreliste.append(("On Air", "http://www.eporner.com/currently//"))
		self.genreliste.append(("Popular", "http://www.eporner.com/weekly_top//"))
		self.genreliste.append(("Top Rated", "http://www.eporner.com/top_rated//"))
		self.genreliste.append(("HD", "http://www.eporner.com/hd//"))
		self.genreliste.append(("Amateurs", "http://www.eporner.com/keywords/amateur+amateurs/"))
		self.genreliste.append(("Anal", "http://www.eporner.com/keywords/anal/"))
		self.genreliste.append(("Asian", "http://www.eporner.com/keywords/asian/"))
		self.genreliste.append(("BDSM", "http://www.eporner.com/keywords/bdsm/"))
		self.genreliste.append(("Big Dick", "http://www.eporner.com/keywords/%22Big+dick%22/"))
		self.genreliste.append(("Big Tits", "http://www.eporner.com/keywords/%22big+tits%22/"))
		self.genreliste.append(("Blowjob", "http://www.eporner.com/keywords/Blowjob+Blow+Job/"))
		self.genreliste.append(("Cumshot", "http://www.eporner.com/keywords/cum+cumshot/"))
		self.genreliste.append(("Double Penetration", "http://www.eporner.com/keywords/dp+dual/"))
		self.genreliste.append(("Ebony", "http://www.eporner.com/keywords/ebony/"))
		self.genreliste.append(("Fat", "http://www.eporner.com/keywords/fat/"))
		self.genreliste.append(("Gay", "http://www.eporner.com/keywords/gay/"))
		self.genreliste.append(("Group", "http://www.eporner.com/keywords/group/"))
		self.genreliste.append(("Handjob", "http://www.eporner.com/keywords/handjob/"))
		self.genreliste.append(("Hardcore", "http://www.eporner.com/keywords/hardcore/"))
		self.genreliste.append(("Lesbian", "http://www.eporner.com/keywords/lesbian+lesbians/"))
		self.genreliste.append(("Masturbation", "http://www.eporner.com/keywords/masturbation+masturbate/"))
		self.genreliste.append(("Mature", "http://www.eporner.com/keywords/mature/"))
		self.genreliste.append(("Office", "http://www.eporner.com/keywords/office/"))
		self.genreliste.append(("Old Man", "http://www.eporner.com/keywords/%22old+man%22/"))
		self.genreliste.append(("Outdoor", "http://www.eporner.com/keywords/outdoor/"))
		self.genreliste.append(("Public", "http://www.eporner.com/keywords/public/"))
		self.genreliste.append(("Shemale", "http://www.eporner.com/keywords/shemale/"))
		self.genreliste.append(("Sleep", "http://www.eporner.com/keywords/sleep/"))
		self.genreliste.append(("Solo Girls", "http://www.eporner.com/solo//"))
		self.genreliste.append(("Spy", "http://www.eporner.com/keywords/spy/"))
		self.genreliste.append(("Students", "http://www.eporner.com/keywords/student+students/"))
		self.genreliste.append(("Swingers", "http://www.eporner.com/keywords/swinger+swingers/"))
		self.genreliste.append(("Teens", "http://www.eporner.com/keywords/teen+teens+young/"))
		self.genreliste.append(("Threesome", "http://www.eporner.com/keywords/threesome/"))
		self.genreliste.append(("Toys", "http://www.eporner.com/keywords/toy+toys/"))
		self.genreliste.append(("Uniform", "http://www.eporner.com/keywords/uniform/"))
		self.chooseMenuList.setList(map(epornerGenreListEntry, self.genreliste))

	def keyOK(self):
		streamGenreName = self['genreList'].getCurrent()[0][0]
		if streamGenreName == "--- Search ---":
			self.suchen()

		else:
			streamGenreLink = self['genreList'].getCurrent()[0][1]
			self.session.open(epornerFilmScreen, streamGenreLink)

	def suchen(self):
		self.session.openWithCallback(self.SuchenCallback, VirtualKeyBoard, title = (_("Suchkriterium eingeben")), text = self.suchString)

	def SuchenCallback(self, callback = None, entry = None):
		if callback is not None and len(callback):
			self.suchString = callback.replace(' ', '%20')
			streamGenreLink = 'http://www.eporner.com/keywords/%s/' % (self.suchString)
			self.session.open(epornerFilmScreen, streamGenreLink)

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

class epornerFilmScreen(Screen):
	
	def __init__(self, session, phCatLink):
		self.session = session
		self.phCatLink = phCatLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/epornerFilmScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/epornerFilmScreen.xml"
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
			"left" : self.keyLeft,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown,
			"green" : self.keyPageNumber
		}, -1)

		self['title'] = Label("Eporner.com")
		self['name'] = Label("Film Auswahl")
		self['views'] = Label("")
		self['runtime'] = Label("")
		self['page'] = Label("1")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.page = 0
		
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadpage)
		
	def loadpage(self):
		self.keyLocked = True
		self.filmliste = []
		self['page'].setText(str(self.page+1))
		url = "%s%s//" % (self.phCatLink, str(self.page))
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadData).addErrback(self.dataError)
	
	def loadData(self, data):
		if self.phCatLink == "http://www.eporner.com/top_rated//":
			phMovies = re.findall('<div class="mbtit"><a href="(.*?)" title="(.*?)".*?src="(.*?)".*?<span>TIME:</span> (.*?)</div>', data, re.S)
			if phMovies:
				Views = []
				for (phUrl, phTitle, phImage, phRuntime) in phMovies:
					self.filmliste.append((decodeHtml(phTitle), phUrl, phImage, phRuntime, Views))
				self.chooseMenuList.setList(map(epornerFilmListEntry, self.filmliste))
				self.showInfos()
		else:
			phMovies = re.findall('<div class="mbtit"><a href="(.*?)" title="(.*?)".*?src="(.*?)".*?<span>TIME:</span> (.*?)</div>.*?<span>VIEWS:</span> (.*?)</div>', data, re.S)
			if phMovies:
				for (phUrl, phTitle, phImage, phRuntime, phViews) in phMovies:
					self.filmliste.append((decodeHtml(phTitle), phUrl, phImage, phRuntime, phViews))
				self.chooseMenuList.setList(map(epornerFilmListEntry, self.filmliste))
				self.showInfos()
		self.keyLocked = False

	def dataError(self, error):
		print error

	def showInfos(self):
		phTitle = self['genreList'].getCurrent()[0][0]
		phImage = self['genreList'].getCurrent()[0][2]
		phRuntime = self['genreList'].getCurrent()[0][3]
		phViews = self['genreList'].getCurrent()[0][4]
		self['name'].setText(phTitle)
		self['runtime'].setText(phRuntime)
		self['views'].setText(phViews)
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
		self.session.openWithCallback(self.callbackkeyPageNumber, VirtualKeyBoard, title = (_("Seitennummer eingeben")), text = str(self.page+1))

	def callbackkeyPageNumber(self, answer):
		if answer is not None:
			self.page = int(answer)-1
			self.loadpage()

	def keyPageDown(self):
		print "PageDown"
		if self.keyLocked:
			return
		if not self.page < 1:
			self.page -= 1
			self.loadpage()
		
	def keyPageUp(self):
		print "PageUP"
		if self.keyLocked:
			return
		self.page += 1
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
		url = 'http://www.eporner.com%s' % (self['genreList'].getCurrent()[0][1])
		self.keyLocked = True
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getXMLPage).addErrback(self.dataError)

	def getXMLPage(self, data):
		videoPage = re.findall(r"player4\\([^\\]*)\\", data, re.S)
		if videoPage:
			for phurl in videoPage:
				xml = 'http://www.eporner.com/config5%s' % (phurl)
		getPage(xml, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getVideoPage).addErrback(self.dataError)

	def getVideoPage(self, data):
		videoPage = re.findall('<hd.file>(.*?)</hd.file>', data, re.S)
		if videoPage:
			for phurl in videoPage:
				self.keyLocked = False
				self.play(phurl)
		else:
			videoPage = re.findall('<file>(.*?)</file>', data, re.S)
			if videoPage:
				for phurl in videoPage:
					self.keyLocked = False
					self.play(phurl)
		
	def play(self,file):
		xxxtitle = self['genreList'].getCurrent()[0][0]
		sref = eServiceReference(0x1001, 0, file)
		sref.setName(xxxtitle)
		self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()
