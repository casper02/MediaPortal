from imports import *

def fourtubeGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

def fourtubePornstarsListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 

def fourtubeFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
		
class fourtubeGenreScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/fourtubeGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/fourtubeGenreScreen.xml"
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

		self['title'] = Label("4Tube.com")
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
		self.genreliste.append(("--- Search ---", "callSuchen"))
		self.genreliste.append(("Lastest", "http://www.4tube.com/videos?page="))
		self.genreliste.append(("Featured", "http://www.4tube.com/featured?sort=ctr&page="))
		self.genreliste.append(("Full", "http://www.4tube.com/videos/full-length?sort=ctr&page="))
		self.genreliste.append(("Pornstars", "http://www.4tube.com/pornstars?page="	))
		self.genreliste.append(("Anal", "http://www.4tube.com/find/tags/anal?sort=ctr&page="))
		self.genreliste.append(("Asian", "http://www.4tube.com/find/tags/asian?sort=ctr&page="))
		self.genreliste.append(("Babe", "http://www.4tube.com/find/tags/babe?sort=ctr&page="))
		self.genreliste.append(("Big Dick", "http://www.4tube.com/find/tags/big-dick?sort=ctr&page="))
		self.genreliste.append(("Big Tits", "http://www.4tube.com/find/tags/big-tits?sort=ctr&page="))
		self.genreliste.append(("Blowjobs", "http://www.4tube.com/find/tags/blowjobs?sort=ctr&page="))
		self.genreliste.append(("Creampie", "http://www.4tube.com/find/tags/creampie?sort=ctr&page="))
		self.genreliste.append(("Cumshots", "http://www.4tube.com/find/tags/cumshots?sort=ctr&page="))
		self.genreliste.append(("Deepthroat", "http://www.4tube.com/find/tags/deep-throat?sort=ctr&page="))
		self.genreliste.append(("Double Penetration", "http://www.4tube.com/find/tags/double-penetration?sort=ctr&page="))
		self.genreliste.append(("Ebony", "http://www.4tube.com/find/tags/ebony?sort=ctr&page="))
		self.genreliste.append(("Fisting", "http://www.4tube.com/find/tags/fisting?sort=ctr&page="))
		self.genreliste.append(("Handjob", "http://www.4tube.com/find/tags/handjob?sort=ctr&page="))
		self.genreliste.append(("Hardcore", "http://www.4tube.com/find/tags/hardcore?sort=ctr&page="))
		self.genreliste.append(("Interracial", "http://www.4tube.com/find/tags/interracial?sort=ctr&page="))
		self.genreliste.append(("Latinas", "http://www.4tube.com/find/tags/latinas?sort=ctr&page="))
		self.genreliste.append(("Lesbians", "http://www.4tube.com/find/tags/lesbians?sort=ctr&page="))
		self.genreliste.append(("Masturbation", "http://www.4tube.com/find/tags/masturbation?sort=ctr&page="))
		self.genreliste.append(("MILF", "http://www.4tube.com/find/tags/milf?sort=ctr&page="))
		self.genreliste.append(("Solo", "http://www.4tube.com/find/tags/solo?sort=ctr&page="))
		self.genreliste.append(("Squirting", "http://www.4tube.com/find/tags/squirting?sort=ctr&page="))
		self.genreliste.append(("Teens", "http://www.4tube.com/find/tags/teens?sort=ctr&page="))
		self.genreliste.append(("Toys", "http://www.4tube.com/find/tags/toys?sort=ctr&page="))		
		self.chooseMenuList.setList(map(fourtubeGenreListEntry, self.genreliste))

	def keyOK(self):
		streamGenreName = self['genreList'].getCurrent()[0][0]
		if streamGenreName == "--- Search ---":
			self.suchen()
			
		elif streamGenreName == "Pornstars":
			streamGenreLink = self['genreList'].getCurrent()[0][1]
			self.session.open(fourtubePornstarsScreen, streamGenreLink)
			
		else:
			streamGenreLink = self['genreList'].getCurrent()[0][1]
			self.session.open(fourtubeFilmScreen, streamGenreLink)

	def suchen(self):
		self.session.openWithCallback(self.SuchenCallback, VirtualKeyBoard, title = (_("Suchkriterium eingeben")), text = self.suchString)

	def SuchenCallback(self, callback = None, entry = None):
		if callback is not None and len(callback):
			self.suchString = callback.replace(' ', '-')
			streamGenreLink = 'http://www.4tube.com/find/videos/%s?page=' % (self.suchString)
			self.session.open(fourtubeFilmScreen, streamGenreLink)

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

class fourtubePornstarsScreen(Screen):
	
	def __init__(self, session, phCatLink):
		self.session = session
		self.phCatLink = phCatLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/fourtubePornstarsScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/fourtubePornstarsScreen.xml"
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

		self['title'] = Label("4Tube.com")
		self['name'] = Label("Pornstars Auswahl")
		self['views'] = Label("")
		self['runtime'] = Label("")
		self['page'] = Label("1")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.page = 1
		
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadpage)
		
	def loadpage(self):
		self.keyLocked = True
		self.filmliste = []
		self['page'].setText(str(self.page))
		url = "%s%s" % (self.phCatLink, str(self.page))
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadData).addErrback(self.dataError)
	
	def loadData(self, data):
		Movies = re.findall('pornstarInfoLarge_pornstar"><a title=.*?href="(.*?)".*?class="thumb" src="(.*?)" title="(.*?)"',data,re.S) 
		if Movies:
			for (Url, Image, Title) in Movies:
				self.filmliste.append((Title,Url,Image))
			self.chooseMenuList.setList(map(fourtubePornstarsListEntry, self.filmliste))
			self.showInfos()
		self.keyLocked = False

	def dataError(self, error):
		print error

	def showInfos(self):
		phTitle = self['genreList'].getCurrent()[0][0]
		phImage = self['genreList'].getCurrent()[0][2]
		self['name'].setText(phTitle)
		downloadPage(phImage, "/tmp/phIcon.jpg").addCallback(self.ShowCover)
		
	def ShowCover(self, picData):
		if fileExists("/tmp/phIcon.jpg"):
			self['coverArt'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/phIcon.jpg", 0, 0, False) == 0:
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
		
	def keyCancel(self):
		self.close()

	def keyOK(self):
		if self.keyLocked:
			return
		streamGenreLink = self['genreList'].getCurrent()[0][1] + '?page='
		self.session.open(fourtubeFilmScreen, streamGenreLink)

class fourtubeFilmScreen(Screen):
	
	def __init__(self, session, phCatLink):
		self.session = session
		self.phCatLink = phCatLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/fourtubeFilmScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/fourtubeFilmScreen.xml"
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

		self['title'] = Label("4Tube.com")
		self['name'] = Label("Film Auswahl")
		self['views'] = Label("")
		self['runtime'] = Label("")
		self['page'] = Label("1")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.page = 1
		
		self.filmliste = []
		self.filmQualitaet = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadpage)
		
	def loadpage(self):
		self.keyLocked = True
		self.filmliste = []
		self['page'].setText(str(self.page))
		url = "%s%s" % (self.phCatLink, str(self.page))
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadData).addErrback(self.dataError)
	
	def loadData(self, data):
		phMovies = re.findall('videoInfoPornstar.*?item" href="(.*?)">.*?src="(.*?.jpeg)" title="(.*?)".*?length">(.*?)<', data, re.S)
		if phMovies:
			for (phUrl, phImage, phTitle, phRuntime) in phMovies:
				self.filmliste.append((phTitle,phUrl,phImage,phRuntime))
			self.chooseMenuList.setList(map(fourtubeFilmListEntry, self.filmliste))
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
		phLink = self['genreList'].getCurrent()[0][1]
		self.filmQualitaet = []
		self.keyLocked = True
		getPage(phLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getVideoPage).addErrback(self.dataError)

	def getVideoPage(self, data):
		videoPage = re.findall("videoUrl = '(.*?)'.*?flashvars','config=(.*?)'", data, re.S)
		if videoPage:
			for (phFile, phTeilurl) in videoPage:
				url = 'http://www.4tube.com%s%s' % (phTeilurl, phFile)
				videos = urllib.unquote(url)
				getPage(videos, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getVideoStreams).addErrback(self.dataError)

	def getVideoStreams(self, data):
		videoQualiLink = re.findall('<stream label="(.*?)".*?<file>(.*?)<', data, re.S)
		if videoQualiLink:
			for (quali, videoPlay) in videoQualiLink:
				temp2 = videoPlay.replace('amp;', '')
				videoPlay = temp2 + '&start=0'
				self.filmQualitaet.append((quali, videoPlay))
				self.keyLocked = False
			 
			print self.filmQualitaet[0][0], self.filmQualitaet[0][1]
			file = self.filmQualitaet[0][1]
			self.play(file)
		
	def play(self,file):
		xxxtitle = self['genreList'].getCurrent()[0][0]
		sref = eServiceReference(0x1001, 0, file)
		sref.setName(xxxtitle)
		self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()
