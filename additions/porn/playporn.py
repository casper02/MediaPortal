from Plugins.Extensions.mediaportal.resources.imports import *

def playpornGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

def playpornFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
		
def playpornHosterListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 
		
sitechrx = ''

special_headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31',
	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4',
	'Referer': 'http://playporn.to/'
}

class playpornGenreScreen(Screen):
	
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

		self['title'] = Label("PlayPorn.to")
		self['name'] = Label("Genre Auswahl")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.suchString = ''
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.get_site_cookie1)
		
	def get_site_cookie1(self):
		self.keyLocked = True
		url = "http://playporn.to"
		getPage(url, headers=special_headers).addCallback(self.get_site_cookie2).addErrback(self.dataError)
		
	def get_site_cookie2(self, data):
		self.keyLocked = True
		raw = re.findall('javascript"\ssrc="(.*?)">.*?scf\(\'(.*?)\'\+\'(.*?)\'.*?', data, re.S)
		url = "http://playporn.to" + str(raw[0][0])
		getPage(url, headers=special_headers).addCallback(self.get_site_cookie3, raw[0][1], raw[0][2]).addErrback(self.dataError)
		
	def get_site_cookie3(self, data, cookie1, cookie2):
		raw = re.findall('escape\(hsh.*?"(.*?)"\)', data, re.S)
		global sitechrx
		sitechrx = str(cookie1) + str(cookie2) + str(raw[0])
		print 'sitechrx='+sitechrx
		self.layoutFinished()

	def layoutFinished(self):
		self.genreliste.append(("--- Search ---", "callSuchen"))
		self.genreliste.append(("Newest", "http://playporn.to/category/xxx-movie-stream/page/"))
		self.genreliste.append(("Amateur", "http://playporn.to/category/xxx-movie-stream/amateure/page/"))
		self.genreliste.append(("Anal", "http://playporn.to/category/xxx-movie-stream/anal/page/"))
		self.genreliste.append(("Asian", "http://playporn.to/category/xxx-movie-stream/asia/page/"))
		self.genreliste.append(("Big Tits", "http://playporn.to/category/xxx-movie-stream/grose-bruste/page/"))
		self.genreliste.append(("Black", "http://playporn.to/category/xxx-movie-stream/black/page/"))
		self.genreliste.append(("Blowjob", "http://playporn.to/category/xxx-movie-stream/blowjob/page/"))
		self.genreliste.append(("Fetish", "http://playporn.to/category/xxx-movie-stream/fetish/page/"))
		self.genreliste.append(("German", "http://playporn.to/category/xxx-movie-stream/deutsch/page/"))
		self.genreliste.append(("Group Sex", "http://playporn.to/category/xxx-movie-stream/gangbang-gruppensex/page/"))
		self.genreliste.append(("Hardcore", "http://playporn.to/category/xxx-movie-stream/harcore/page/"))
		self.genreliste.append(("Lesbian", "http://playporn.to/category/xxx-movie-stream/lesben/page/"))
		self.genreliste.append(("Masturbation", "http://playporn.to/category/xxx-movie-stream/masturbation/page/"))
		self.genreliste.append(("Pornstars", "http://playporn.to/category/xxx-movie-stream/pornstars/page/"))
		self.genreliste.append(("Teens", "http://playporn.to/category/xxx-movie-stream/teens-xxx-movie-stream/page/"))
		self.chooseMenuList.setList(map(playpornGenreListEntry, self.genreliste))
		self.keyLocked = False

	def dataError(self, error):
		print error

	def keyOK(self):
		streamGenreName = self['genreList'].getCurrent()[0][0]
		if streamGenreName == "--- Search ---":
			self.suchen()

		else:
			streamGenreLink = self['genreList'].getCurrent()[0][1]
			self.session.open(playpornFilmScreen, streamGenreLink, streamGenreName)
		
	def suchen(self):
		self.session.openWithCallback(self.SuchenCallback, VirtualKeyBoard, title = (_("Suchkriterium eingeben")), text = self.suchString)

	def SuchenCallback(self, callback = None, entry = None):
		if callback is not None and len(callback):
			self.suchString = callback.replace(' ', '+')
			streamGenreLink = '%s' % (self.suchString)
			streamGenreName = "--- Search ---"
			self.session.open(playpornFilmScreen, streamGenreLink, streamGenreName)

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

class playpornFilmScreen(Screen):
	
	def __init__(self, session, phCatLink, phCatName):
		self.session = session
		self.phCatLink = phCatLink
		self.phCatName = phCatName
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

		self['title'] = Label("PlayPorn.to")
		self['name'] = Label("Film Auswahl")
		self['views'] = Label("")
		self['runtime'] = Label("")
		self['page'] = Label("")
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
		if self.phCatName == "--- Search ---":
			url = "http://playporn.to/page/%s/?s=%s&submit=Search" % (str(self.page), self.phCatLink)
		else:
			url = "%s%s" % (self.phCatLink, str(self.page))
		print url
		getPage(url, agent=special_headers, headers={'Cookie': 'sitechrx='+sitechrx}).addCallback(self.loadData).addErrback(self.dataError)
	
	def loadData(self, data):
		lastp = re.findall('class=\'pages\'>.*?of (.*?)</span>', data, re.S)
		if lastp:
			lastp = lastp[0]
			print lastp
			self.lastpage = int(lastp)
		else:
			self.lastpage = 1
		self['page'].setText(str(self.page) + ' / ' + str(self.lastpage))	
		phMovies = re.findall('class="photo-thumb">.*?<a\shref="(.*?)"\stitle="(.*?)".*?thumbindex"\ssrc="(.*?)"', data, re.S)
		if phMovies:
			for (phUrl, phTitle, phImage) in phMovies:
				if re.search('images-box.com|rapidimg.org', str(phImage), re.S):
					phImage = None
				self.filmliste.append((decodeHtml(phTitle), phUrl, phImage))
			self.chooseMenuList.setList(map(playpornFilmListEntry, self.filmliste))
			self.chooseMenuList.moveToIndex(0)
			self.keyLocked = False
			self.showInfos()

	def dataError(self, error):
		print error

	def showInfos(self):
		phTitle = self['genreList'].getCurrent()[0][0]
		phImage = self['genreList'].getCurrent()[0][2]
		self['name'].setText(phTitle)
		print phImage
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
			answer = re.findall('\d+', answer)
		else:
			return
		if answer:
			if int(answer[0]) < self.lastpage + 1:
				self.page = int(answer[0])
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
		phTitle = self['genreList'].getCurrent()[0][0]
		phLink = self['genreList'].getCurrent()[0][1]
		self.session.open(playpornStreamListeScreen, phLink, phTitle)

	def keyCancel(self):
		self.close()

class playpornStreamListeScreen(Screen):
	
	def __init__(self, session, streamFilmLink, streamName):
		self.session = session
		self.streamFilmLink = streamFilmLink
		self.streamName = streamName

		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/XXXGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/XXXGenreScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("PlayPorn.to")
		self['name'] = Label(self.streamName)
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		getPage(self.streamFilmLink, agent=special_headers, headers={'Cookie': 'sitechrx='+sitechrx}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		print "daten bekommen"
		streams = re.findall('<a\s{0,3}id="(.*?)".*?href="(.*?)".*?</a>', data, re.S)
		if streams:
			for (hostername, stream) in streams:
				if re.match('.*?(putlocker|sockshare|streamclou|xvidstage|filenuke|movreel|nowvideo|xvidstream|uploadc|vreer|MonsterUploads|Novamov|Videoweed|Divxstage|Ginbig|Flashstrea|Movshare|yesload|faststream|Vidstream|PrimeShare|flashx|Divxmov|Putme|Zooupload|Wupfile)', hostername.strip(' '), re.S|re.I):
					print hostername, stream
					hostername = hostername.replace('streamcloud1','Streamcloud (Teil 1)').replace('streamcloud2','Streamcloud (Teil 2)')
					self.filmliste.append((hostername, stream))
		else:
			self.filmliste.append(('Keine Streams gefunden.', None))
		self.chooseMenuList.setList(map(playpornHosterListEntry, self.filmliste))
		self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return
		streamLink = self['genreList'].getCurrent()[0][1]
		if streamLink == None:
			return
		getPage(streamLink, agent=special_headers, headers={'Cookie': 'sitechrx='+sitechrx}).addCallback(self.getVideoPage).addErrback(self.dataError)

	def getVideoPage(self, data):
		videoPage = re.findall('iframe\ssrc="(.*?)"', data, re.S)
		if not videoPage:
			videoPage = re.findall('iframe.*?src="http://playporn.to/stream/all/\?file=(.*?)"', data, re.S)
		if videoPage:
			for phurl in videoPage:
				url = phurl
				url = url.replace('&amp;','&')
				self.get_stream(url)
		
	def get_stream(self,url):
		get_stream_link(self.session).check_link(url, self.got_link)
		
	def got_link(self, stream_url):
		if stream_url == None:
			message = self.session.open(MessageBox, _("Stream not found, try another Stream Hoster."), MessageBox.TYPE_INFO, timeout=3)
		else:
			sref = eServiceReference(0x1001, 0, stream_url)
			sref.setName(self.streamName)
			self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()
