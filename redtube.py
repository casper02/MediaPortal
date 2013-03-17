from imports import *

def redtubeGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

def redtubeFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
		
class redtubeGenreScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/XXXGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/XXXGenreScreen.xml"
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

		self['title'] = Label("RedTube.com")
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
		self.genreliste.append(("Newest", "http://www.redtube.com/?page="))
		self.genreliste.append(("Top Rated", "http://www.redtube.com/top?page="))
		self.genreliste.append(("Most Viewed", "http://www.redtube.com/mostviewed?page="))
		self.genreliste.append(("Most Favored", "http://www.redtube.com/mostfavored?page="))
		self.genreliste.append(("Amateur", "http://www.redtube.com/redtube/amateur?page="))
		self.genreliste.append(("Anal", "http://www.redtube.com/redtube/anal?page="))
		self.genreliste.append(("Asian", "http://www.redtube.com/redtube/asian?page="))
		self.genreliste.append(("Big Tits", "http://www.redtube.com/redtube/bigtits?page="))
		self.genreliste.append(("Blonde", "http://www.redtube.com/redtube/blonde?page="))
		self.genreliste.append(("Blowjob", "http://www.redtube.com/redtube/blowjob?page="))
		self.genreliste.append(("Creampie", "http://www.redtube.com/redtube/creampie?page="))
		self.genreliste.append(("Cumshot", "http://www.redtube.com/redtube/cumshot?page="))
		self.genreliste.append(("Double Penetration", "http://www.redtube.com/redtube/doublepenetration?page="))
		self.genreliste.append(("Ebony", "http://www.redtube.com/redtube/ebony?page="))
		self.genreliste.append(("Facials", "http://www.redtube.com/redtube/facials?page="))
		self.genreliste.append(("Fetish", "http://www.redtube.com/redtube/fetish?page="))
		self.genreliste.append(("Gangbang", "http://www.redtube.com/redtube/gangbang?page="))
		self.genreliste.append(("Gay", "http://www.redtube.com/redtube/gay?page="))
		self.genreliste.append(("Group", "http://www.redtube.com/redtube/group?page="))
		self.genreliste.append(("Hentai", "http://www.redtube.com/redtube/hentai?page="))
		self.genreliste.append(("Interracial", "http://www.redtube.com/redtube/interracial?page="))
		self.genreliste.append(("Japanese", "http://www.redtube.com/redtube/japanese?page="))
		self.genreliste.append(("Latina", "http://www.redtube.com/redtube/latina?page="))
		self.genreliste.append(("Lesbian", "http://www.redtube.com/redtube/lesbian?page="))
		self.genreliste.append(("Lingerie", "http://www.redtube.com/redtube/lingerie?page="))
		self.genreliste.append(("Masturbation", "http://www.redtube.com/redtube/masturbation?page="))
		self.genreliste.append(("Mature", "http://www.redtube.com/redtube/mature?page="))
		self.genreliste.append(("MILF", "http://www.redtube.com/redtube/milf?page="))
		self.genreliste.append(("POV", "http://www.redtube.com/redtube/pov?page="))
		self.genreliste.append(("Public", "http://www.redtube.com/redtube/public?page="))
		self.genreliste.append(("Redhead", "http://www.redtube.com/redtube/redhead?page="))
		self.genreliste.append(("Shemale", "http://www.redtube.com/redtube/shemale?page="))
		self.genreliste.append(("Squirting", "http://www.redtube.com/redtube/squirting?page="))
		self.genreliste.append(("Teens", "http://www.redtube.com/redtube/teens?page="))
		self.genreliste.append(("Vintage", "http://www.redtube.com/redtube/vintage?page="))
		self.genreliste.append(("Wild & Crazy", "http://www.redtube.com/redtube/wildcrazy?page="))
		self.chooseMenuList.setList(map(redtubeGenreListEntry, self.genreliste))

	def keyOK(self):
		streamGenreName = self['genreList'].getCurrent()[0][0]
		if streamGenreName == "--- Search ---":
			self.suchen()

		else:
			streamGenreLink = self['genreList'].getCurrent()[0][1]
			self.session.open(redtubeFilmScreen, streamGenreLink)
		
	def suchen(self):
		self.session.openWithCallback(self.SuchenCallback, VirtualKeyBoard, title = (_("Suchkriterium eingeben")), text = self.suchString)

	def SuchenCallback(self, callback = None, entry = None):
		if callback is not None and len(callback):
			self.suchString = callback.replace(' ', '+')
			streamGenreLink = 'http://www.redtube.com/?search=%s&page=' % (self.suchString)
			self.session.open(redtubeFilmScreen, streamGenreLink)

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

class redtubeFilmScreen(Screen):
	
	def __init__(self, session, phCatLink):
		self.session = session
		self.phCatLink = phCatLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/XXXFilmScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/XXXFilmScreen.xml"
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

		self['title'] = Label("RedTube.com")
		self['name'] = Label("Film Auswahl")
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
		self['name'].setText('Bitte warten...')
		self.filmliste = []
		self['page'].setText(str(self.page))
		url = "%s%s" % (self.phCatLink, str(self.page))
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadData).addErrback(self.dataError)
	
	def loadData(self, data):
		phMovies = re.findall('class="video".*?<a href="(.*?)".*?title="(.*?)".*?class="te" src="(.*?)".*?class="time".*?span class="d">(.*?)</span>.*?style="float:left;">(.*?)</div>', data, re.S)
		if phMovies:
			for (phUrl, phTitle, phImage, phRuntime, phViews) in phMovies:
				self.filmliste.append((decodeHtml(phTitle), phUrl, phImage, phRuntime, phViews))
			self.chooseMenuList.setList(map(redtubeFilmListEntry, self.filmliste))
			self.showInfos()
		self.keyLocked = False

	def dataError(self, error):
		print error

	def showInfos(self):
		phTitle = self['genreList'].getCurrent()[0][0]
		phImage = self['genreList'].getCurrent()[0][2]
		phRuntime = self['genreList'].getCurrent()[0][3]
		phViews = self['genreList'].getCurrent()[0][4]
		phViews = phViews.replace('\t','')
		phViews = phViews.replace(' views','')
		phViews = phViews.replace('\r','')
		phViews = phViews.replace('\n','')
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
		phLink = 'http://www.redtube.com' + self['genreList'].getCurrent()[0][1]
		self.keyLocked = True
		getPage(phLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getVideoPage).addErrback(self.dataError)

	def getVideoPage(self, data):
		videoPage = re.findall("source src='(.*?)'", data, re.S)
		if videoPage:
			for (phurl) in videoPage:
				url = '%s' % (phurl)
				videos = urllib.unquote(url)
				self.keyLocked = False
				self.play(videos)
		
	def play(self,file):
		xxxtitle = self['genreList'].getCurrent()[0][0]
		sref = eServiceReference(0x1001, 0, file)
		sref.setName(xxxtitle)
		self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()
