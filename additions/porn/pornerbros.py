from Plugins.Extensions.MediaPortal.resources.imports import *

def pornerbrosGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

def pornerbrosStreamListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 

class pornerbrosGenreScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/XXXGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/XXXGenreScreen.xml"
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

		self['title'] = Label("Pornerbros.com")
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
		url = "http://www.pornerbros.com/categories/"
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.genreData).addErrback(self.dataError)

	def genreData(self, data):
		phCats = re.findall('class="contents_gallery_item">.*?<a href="(.*?)" title="(.*?)">.*?<img alt=.*?data-original="(.*?)" onClick', data, re.S)
		if phCats:
			for (phUrl, phTitle, phImage) in phCats:
				phUrl = "http://www.pornerbros.com" + phUrl + 'page'
				self.genreliste.append((phTitle, phUrl, phImage))
			self.genreliste.sort()
			self.genreliste.insert(0, ("Longest", "http://www.pornerbros.com/longest/page", None))
			self.genreliste.insert(0, ("Most Discussed", "http://www.pornerbros.com/discussed/page", None))
			self.genreliste.insert(0, ("Most Viewed", "http://www.pornerbros.com/popular/page", None))
			self.genreliste.insert(0, ("Top Rated", "http://www.pornerbros.com/best/page", None))
			self.genreliste.insert(0, ("New", "http://www.pornerbros.com/page", None))
			self.genreliste.insert(0, ("--- Search ---", "callSuchen", None))
			self.chooseMenuList.setList(map(pornerbrosGenreListEntry, self.genreliste))
			self.chooseMenuList.moveToIndex(0)
			self.keyLocked = False
			self.showInfos()	

	def dataError(self, error):
		print error

	def showInfos(self):
		phImage = self['genreList'].getCurrent()[0][2]
		print phImage
		if not phImage == None:
			downloadPage(phImage, "/tmp/phIcon.jpg").addCallback(self.ShowCover)
		else:
			self.ShowCoverNone()

	def ShowCover(self, picData):
		picPath = "/tmp/phIcon.jpg"
		self.ShowCoverFile(picPath)
		
	def ShowCoverNone(self):
		picPath = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/images/no_coverArt.png" % config.mediaportal.skin.value
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

	def keyOK(self):
		if self.keyLocked:
			return
		streamGenreName = self['genreList'].getCurrent()[0][0]
		if streamGenreName == "--- Search ---":
			self.suchen()

		else:
			streamGenreLink = self['genreList'].getCurrent()[0][1]
			self.session.open(pornerbrosFilmScreen, streamGenreLink)
		
	def suchen(self):
		self.session.openWithCallback(self.SuchenCallback, VirtualKeyBoard, title = (_("Suchkriterium eingeben")), text = self.suchString)

	def SuchenCallback(self, callback = None, entry = None):
		if callback is not None and len(callback):
			self.suchString = callback.replace(' ', '+')
			streamGenreLink = 'http://www.pornerbros.com/search/?q=%s&page=' % (self.suchString)
			self.session.open(pornerbrosFilmScreen, streamGenreLink)

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
		
class pornerbrosFilmScreen(Screen):
	
	def __init__(self, session, phCatLink):
		self.session = session
		self.phCatLink = phCatLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/XXXFilmScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/XXXFilmScreen.xml"
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
		
		self['title'] = Label("Pornerbros.com")
		self['name'] = Label("Film Auswahl")
		self['views'] = Label("")
		self['runtime'] = Label("")
		self['page'] = Label("")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.page = 1
		self.lastpage = 1

		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.streamMenuList.l.setItemHeight(25)
		self['genreList'] = self.streamMenuList

		self.onLayoutFinish.append(self.loadpage)

	def loadpage(self):
		self.keyLocked = True
		self['name'].setText('Bitte warten...')
		self.streamList = []
		cat = self.phCatLink
		search = re.search('/search/(.*)', cat, re.S)
		if search:
			url = '%s%s' % (self.phCatLink, str(self.page))
		else:
			url = "%s%s/" % (self.phCatLink, str(self.page))
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.pageData).addErrback(self.dataError)

	def pageData(self, data):
		lastp = re.findall('<title>Page.*?of\s(.*?[0-9])\s', data, re.S)
		if lastp:
			lastp = lastp[0]
			print lastp
			self.lastpage = int(lastp)
		else:
			self.lastpage = 1
		self['page'].setText(str(self.page) + ' / ' + str(self.lastpage))
		parse = re.search('<h2>Today(.*)', data, re.S)
		if not parse:
			parse = re.search('<h2>Videos found(.*)', data, re.S)
		xhListe = re.findall('<div class="contents_gallery_item">.*?<a href="(.*?)" title="(.*?)".*?gid="(.*?)".*?data-original="(.*?.jpg)".*?length">(.*?)<.*?views">(.*?)</span>', parse.group(1), re.S)
		if xhListe:
			for (xhLink, xhName, xhIdnr, xhImage, xhRuntime, xhViews) in xhListe:
				self.streamList.append((decodeHtml(xhName), xhLink, xhIdnr, xhImage, xhRuntime, xhViews))
			self.streamMenuList.setList(map(pornerbrosStreamListEntry, self.streamList))
			self.streamMenuList.moveToIndex(0)
			self.keyLocked = False
			self.showInfos()

	def showInfos(self):
		ptTitle = self['genreList'].getCurrent()[0][0]
		ptImage = self['genreList'].getCurrent()[0][3]
		ptRuntime = self['genreList'].getCurrent()[0][4]
		ptViews = self['genreList'].getCurrent()[0][5]
		ptViews = ptViews.replace(' ','')
		ptViews = ptViews.replace('views','')
		ptViews = ptViews.replace('\r','')
		ptViews = ptViews.replace('\n','')
		ptViews = ptViews.replace('\t','')
		self.ptRead(ptImage)
		self['name'].setText(ptTitle)
		self['runtime'].setText(ptRuntime)
		self['views'].setText(ptViews)
		
	def ptRead(self, stationIconLink):
		downloadPage(stationIconLink, "/tmp/xhIcon.jpg").addCallback(self.ptCoverShow)

	def ptCoverShow(self, picData):
		if fileExists("/tmp/xhIcon.jpg"):
			self['coverArt'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/xhIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr.__deref__())
					self['coverArt'].show()
					del self.picload

	def dataError(self, error):
		print error
	
	def keyOK(self):
		if self.keyLocked:
			return
                scriptid = self['genreList'].getCurrent()[0][2]
                xhLink = 'http://www.pornerbros.com/content/%s.js' % scriptid
		xhTitle = self['genreList'].getCurrent()[0][0]
            	data = urllib.urlopen(xhLink).read()
            	xhStream = re.findall("url.*?escape.*?'(.*?)'", data, re.S)
		
		if xhStream:
			sref = eServiceReference(0x1001, 0, xhStream[0])
			sref.setName(xhTitle)
			self.session.open(MoviePlayer, sref)
            	else:
                	print "no video url found."

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
		
	def keyCancel(self):
		self.close()
