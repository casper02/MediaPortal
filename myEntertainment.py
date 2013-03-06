from imports import *
from decrypt import *
kekse = {}
def MEHDGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 
class showMEHDGenre(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/showMEHDGenre.xml" % config.mediaportal.skin.value
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"] = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("My-Entertainment.biz")
		self['name'] = Label("Genre Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		filmliste = []
		Genre = [("Neueinsteiger", "http://my-entertainment.biz/forum/content.php?r=1969-Aktuelle-HD-Filme&page="),
			("Cineline", "http://my-entertainment.biz/forum/list.php?r=category/169-Cineline&page="),
			("Collection", "http://my-entertainment.biz/forum/content.php?r=3501-hd-collection&page="),
			("Abenteuer", "http://my-entertainment.biz/forum/list.php?r=category/65-HD-Abenteuer&page="),
			("Action", "http://my-entertainment.biz/forum/list.php?r=category/35-HD-Action&page="),
			("Biografie", "http://my-entertainment.biz/forum/list.php?r=category/70-HD-Biografie&page="),
			("Doku", "http://my-entertainment.biz/forum/list.php?r=category/64-HD-Doku&page="),
			("Drama", "http://my-entertainment.biz/forum/list.php?r=category/36-HD-Drama&page="),
			("Fantasy", "http://my-entertainment.biz/forum/list.php?r=category/37-HD-Fantasy&page="),
			("Horror", "http://my-entertainment.biz/forum/list.php?r=category/38-HD-Horror&page="),
			("Komoedie", "http://my-entertainment.biz/forum/list.php?r=category/39-HD-Kom%F6die&page="),
			("Kriegsfilm", "http://my-entertainment.biz/forum/list.php?r=category/66-HD-Kriegsfilm&page="),
			("Krimi", "http://my-entertainment.biz/forum/list.php?r=category/56-HD-Krimi&page="),
			("Musik", "http://my-entertainment.biz/forum/list.php?r=category/63-HD-Musik&page="),
			("Mystery", "http://my-entertainment.biz/forum/list.php?r=category/62-HD-Mystery&page="),
			("Romanze", "http://my-entertainment.biz/forum/list.php?r=category/40-HD-Romanze&page="),
			("SciFi", "http://my-entertainment.biz/forum/list.php?r=category/41-HD-SciFi&page="),
			("Thriller", "http://my-entertainment.biz/forum/list.php?r=category/42-HD-Thriller&page="),
			("Zeichentrick", "http://my-entertainment.biz/forum/list.php?r=category/43-HD-Zeichentrick&page=")]
					
		for (Name,Url) in Genre:
			self.filmliste.append((Name,Url))
			self.chooseMenuList.setList(map(MEHDGenreListEntry, self.filmliste))
		self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return
		genreName = self['filmList'].getCurrent()[0][0]
		genreLink = self['filmList'].getCurrent()[0][1]
		print genreLink
		self.session.open(MEHDFilmListeScreen, genreLink, genreName)
		
	def keyCancel(self):
		self.close()
		
def MEHDFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
class MEHDFilmListeScreen(Screen):
	
	def __init__(self, session, genreLink, genreName):
		self.session = session
		self.genreLink = genreLink
		self.genreName = genreName
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/MEHDFilmListeScreen.xml" % config.mediaportal.skin.value
		print path
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

		self['title'] = Label("My-Entertainment.biz")
		self['name'] = Label(self.genreName)
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		self['page'] = Label("1")
		
		self.keyLocked = True
		self.filmliste = []
		self.page = 1
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		url = "%s%s" % (self.genreLink, str(self.page))
		print url
		getPage(url, cookies=kekse, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		print "daten bekommen"
		filme = re.findall('<div class="article_preview">.*?<a href="(.*?)"><span>(.*?)</span>.*?<img.*?src="(.*?)"', data, re.S)
		if filme:
			self.filmliste = []
			for (url,name,image) in filme:
				name = name.replace("HD: ","")
				self.filmliste.append((decodeHtml(name), url, image))
			self.chooseMenuList.setList(map(MEHDFilmListEntry, self.filmliste))
			self.keyLocked = False
			self.loadPic()

	def loadPic(self):
		self['page'].setText(str(self.page))
		streamName = self['filmList'].getCurrent()[0][0]
		streamUrl = self['filmList'].getCurrent()[0][1]
		self.getHandlung(streamUrl)
		self['name'].setText(streamName)
		streamPic = self['filmList'].getCurrent()[0][2]
		downloadPage(streamPic, "/tmp/Icon.jpg").addCallback(self.ShowCover)
	
	def getHandlung(self, url):
		getPage(url, cookies=kekse, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.setHandlung).addErrback(self.dataError)
	
	def setHandlung(self, data):
		handlung = re.findall('<div class="bbcode_quote_container"></div>(.*?)<', data, re.S)
		if handlung:
			#print handlung
			handlung = re.sub(r"\s+", " ", handlung[0])
			self['handlung'].setText(decodeHtml(handlung))
		else:
			self['handlung'].setText("Keine infos gefunden.")

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

	def keyOK(self):
		if self.keyLocked:
			return
		streamLink = self['filmList'].getCurrent()[0][1]
		getPage(streamLink, cookies=kekse, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getStream).addErrback(self.dataError)
		
	def getStream(self, data):
		stream = re.findall('href="(http://my-entertainment.biz/.*?/Free-Membe.*?.php\?mov=.*?)"', data)
		# Wenn nur ein Link, dann stream starten, ansonsten handelt es sich wohl um eine Collection
		if len(stream) == 1:
			print 'Ein Free Stream....',stream
			getPage(stream[0], cookies=kekse, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getStreamLink).addErrback(self.dataError)
		else:
			searchTitle = re.findall('<title>(.*?)</title>', data, re.S)
			searchCol = re.findall('<img src="(http://my-entertainment.biz.*?)".*?href="(http://my-entertainment.biz/server/Free-Member.php\\?mov=.*?)"', data, re.S)
			print 'Mehrere Free-Streams...',searchCol
			# Jetzt muessen wir eine neue Screen oeffnen um die Filme der Collection anzuzeigen
			self.session.open(enterColListScreen, searchCol, searchTitle)

	def getStreamLink(self, data):
			#print data
			streamName = self['filmList'].getCurrent()[0][0]
			stream_url = re.findall('src="(http://.*?my-entertainment.biz.*?)"', data, re.S)
			if stream_url:
				streamName = self['filmList'].getCurrent()[0][0]
				sref = eServiceReference(0x1001, 0, stream_url[0])
				sref.setName(streamName)
				self.session.open(MoviePlayer, sref)			
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['filmList'].up()
		self.loadPic()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['filmList'].down()
		self.loadPic()
		
	def keyLeft(self):
		if self.keyLocked:
			return
		self['filmList'].pageUp()
		self.loadPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['filmList'].pageDown()
		self.loadPic()
			
	def keyPageDown(self):
		print "PageDown"
		if self.keyLocked:
			return
		if not self.page < 1:
			self.page -= 1
			self.loadPage()
			
	def keyPageUp(self):
		print "PageUp"
		if self.keyLocked:
			return
		self.page += 1 
		self.loadPage()
		
	def keyCancel(self):
		self.close()
		
def enterColListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 
		
class enterColListScreen(Screen):
	
	def __init__(self, session, pageCol, pageTitle,):
		self.session = session
		self.pageCol = pageCol
		self.pageTitle = pageTitle
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/enterColListScreen.xml" % config.mediaportal.skin.value
		print path
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
			"left" : self.keyLeft,
		}, -1)

		self['title'] = Label("My-Entertainment.biz")
		self['name'] = Label("Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.auswahlColListe = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['auswahlColList'] = self.chooseMenuList
		self.onLayoutFinish.append(self.showColData)
		
		
	def showColData(self):
		i=1
		if self.pageCol:
			for enterPic,enterUrl in self.pageCol:
				self.auswahlColListe.append((self.pageTitle[0]+' '+str(i), enterUrl, enterPic))
				i=i+1
			self.chooseMenuList.setList(map(enterColListEntry, self.auswahlColListe))
			self.keyLocked = False
			self.loadPic()
			
	def loadPic(self):
		streamName = self['auswahlColList'].getCurrent()[0][0]
		streamFilmLink = self['auswahlColList'].getCurrent()[0][1]
		self['name'].setText(streamName)
		streamPic = self['auswahlColList'].getCurrent()[0][2]
		downloadPage(streamPic, "/tmp/spIcon.jpg").addCallback(self.ShowCover)

		
	def ShowCover(self, picData):
		if fileExists("/tmp/spIcon.jpg"):
			self['coverArt'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/spIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr.__deref__())
					self['coverArt'].show()
					del self.picload
					
					
	def getRealLink(self, data):
		print 'getRealLink'
		stream_url = re.findall('src="(http://.*?my-entertainment.biz.*?)"', data, re.S)
		print stream_url
		if stream_url:
			print stream_url
			self.startMovie(stream_url[0])

	def startMovie(self, link):
		sref = eServiceReference(4097, 0, link)
		sref.setName(self.streamName)
		self.session.open(MoviePlayer, sref)
			
					
	def keyOK(self):
		if self.keyLocked:
			return
		streamLink = self['auswahlColList'].getCurrent()[0][1]
		self.streamName = self['auswahlColList'].getCurrent()[0][0]
		print 'RealStreamLink...', streamLink
		getPage(streamLink, cookies=kekse, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getRealLink).addErrback(self.dataError)
	
	def dataError(self, error):
		print error
		
	def keyLeft(self):
		if self.keyLocked:
			return
		self['auswahlColList'].pageUp()
		self.loadPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['auswahlColList'].pageDown()
		self.loadPic()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['auswahlColList'].up()
		self.loadPic()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['auswahlColList'].down()
		self.loadPic()
		
	def keyCancel(self):
		self.close()