from imports import *

def beegGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

def beegFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
		
class beegGenreScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/beegGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/beegGenreScreen.xml"
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

		self['title'] = Label("beeg.com")
		self['name'] = Label("Genre Auswahl")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.suchString = ''
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.keyLocked = True
		url = "http://beeg.com/"
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.genreData).addErrback(self.dataError)

	def genreData(self, data):
		phCats = re.findall('href="/tag(.*?)".*?>(.*?)</a>', data, re.S)
		if phCats:
			for (phUrl, phTitle) in phCats:
				self.genreliste.append((phTitle, phUrl))
			self.genreliste.sort()
			self.genreliste.insert(0, ("Longest", "/section/long-videos/"))
			self.genreliste.insert(0, ("Newest", "/section/home/"))
			self.genreliste.insert(0, ("--- Search ---", "callSuchen"))
			self.chooseMenuList.setList(map(beegGenreListEntry, self.genreliste))
			self.keyLocked = False

	def dataError(self, error):
		print error

	def keyOK(self):
		streamGenreName = self['genreList'].getCurrent()[0][0]
		if streamGenreName == "--- Search ---":
			self.suchen()

		else:
			streamGenreLink = self['genreList'].getCurrent()[0][1]
			self.session.open(beegFilmScreen, streamGenreLink, streamGenreName)
		
	def suchen(self):
		self.session.openWithCallback(self.SuchenCallback, VirtualKeyBoard, title = (_("Suchkriterium eingeben")), text = self.suchString)

	def SuchenCallback(self, callback = None, entry = None):
		if callback is not None and len(callback):
			self.suchString = callback.replace(' ', '+')
			streamGenreLink = 'http://beeg.com/search?q=%s' % (self.suchString)
			streamGenreName = "--- Search ---"
			self.session.open(beegFilmScreen, streamGenreLink, streamGenreName)

	def keyLeft(self):
		if self.keyLocked:
			return
		self['genreList'].pageUp()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['genreList'].pageDown()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['genreList'].up()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['genreList'].down()

	def keyCancel(self):
		self.close()

class beegFilmScreen(Screen):
	
	def __init__(self, session, phCatLink, phCatName):
		self.session = session
		self.phCatLink = phCatLink
		self.phCatName = phCatName
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/beegFilmScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/beegFilmScreen.xml"
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

		self['title'] = Label("beeg.com")
		self['name'] = Label("Film Auswahl")
		self['views'] = Label("")
		self['runtime'] = Label("")
		self['page'] = Label("1")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.page = 1
		self.lastpage = 1
		
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadpage)
		
	def loadpage(self):
		self.keyLocked = True
		self['name'].setText('Bitte warten...')
		self.filmliste = []
		self['page'].setText(str(self.page))
		if self.phCatName == "--- Search ---":
			url = "%s&page=%s" % (self.phCatLink, str(self.page))
		elif self.phCatName == "Newest":
			url = "http://beeg.com%s%s/" % (self.phCatLink, str(self.page))
		elif self.phCatName == "Longest":
			url = "http://beeg.com%s%s/" % (self.phCatLink, str(self.page))
		else:
			url = "http://beeg.com/tag%s/%s/" % (self.phCatLink, str(self.page))		
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadData).addErrback(self.dataError)
	
	def loadData(self, data):
		pagerbox = re.search('<div class="pager-box">(.*?)</div>', data, re.S)
		if pagerbox:
			lastp = re.findall('<a href=".*?" target="_self">(.*?)</a>', pagerbox.group(1), re.S)
			if lastp:
				last = lastp[len(lastp)-1]
				self.lastpage = int(last)
		else:
			self.lastpage = 1
		m = re.search('tumbid  =\[(.*)\].*?var tumbalt',data,re.S)
		n = re.search('tumbalt =\[(.*)\].*?var writestr',data,re.S)
		mx = m.group(1) + ","
		nx = n.group(1) + ","
		phId = re.findall('(.*?),', mx, re.S)
		phThumb = re.findall('\'(.*?)\',', nx, re.S)
		x = 0
		if phId:
			for phVideoId in phId:
				phUrl = 'http://beeg.com/%s' % phVideoId
				phImage = 'http://cdn.anythumb.com/236x177/%s.jpg' % phVideoId
				phTitle = phThumb[x]
				phTitle = phTitle.replace("\\'","'")
				self.filmliste.append((phTitle, phUrl, phImage))
				x = x + 1
			self.chooseMenuList.setList(map(beegFilmListEntry, self.filmliste))
			self.showInfos()
		self.keyLocked = False

	def dataError(self, error):
		print error

	def showInfos(self):
		phTitle = self['genreList'].getCurrent()[0][0]
		phImage = self['genreList'].getCurrent()[0][2]
		self['name'].setText(phTitle)
		if not phImage == None:
			downloadPage(phImage, "/tmp/Icon.jpg").addCallback(self.ShowCover)
		else:
			self.ShowCoverNone()
		
	def ShowCover(self, picData):
		picPath = "/tmp/Icon.jpg"
		self.ShowCoverFile(picPath)
		
	def ShowCoverNone(self):
		picPath = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/images/no_coverArt.png" % config.mediaportal.skin.value
		self.ShowCoverFile(picPath)

	def ShowCoverFile(self, picPath):
		if fileExists(picPath):
			self['coverArt'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode(picPath, 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr.__deref__())
					self['coverArt'].show()
					del self.picload

	def keyPageNumber(self):
		self.session.openWithCallback(self.callbackkeyPageNumber, VirtualKeyBoard, title = (_("Seitennummer eingeben")), text = str(self.page))

	def callbackkeyPageNumber(self, answer):
		if answer is not None:
			if int(answer) < self.lastpage + 1:
				self.page = int(answer)
				self.loadpage()
			else:
				self.page = self.lastpage
				self.loadpage()

	def keyPageDown(self):
		print "PageDown"
		if self.keyLocked:
			return
		if not self.page < 2:
			self.page -= 1
			self.loadpage()
		
	def keyPageUp(self):
		print "PageUP"
		if self.keyLocked:
			return
		if self.page < self.lastpage:
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
		phLink = self['genreList'].getCurrent()[0][1]
		if not phLink == None:
			url = '%s' % phLink
			self.keyLocked = True
			getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getVideoPage).addErrback(self.dataError)

	def getVideoPage(self, data):
		videoPage = re.findall('\'file\': \'(.*?)\',', data, re.S)
		if videoPage:
			for phurl in videoPage:
				print phurl
				url = phurl
				self.play(url)
		self.keyLocked = False
		
	def play(self,file):
		xxxtitle = self['genreList'].getCurrent()[0][0]
		sref = eServiceReference(0x1001, 0, file)
		sref.setName(xxxtitle)
		self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()
