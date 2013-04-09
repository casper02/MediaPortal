from Plugins.Extensions.mediaportal.resources.imports import *

def pornostreamsGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

def pornostreamsFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
		
def pornostreamsHosterListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 
		
class pornostreamsGenreScreen(Screen):
	
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

		self['title'] = Label("Porno-Streams.com")
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
		url = "http://www.porno-streams.com"
		getPage(url, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.genreData).addErrback(self.dataError)

	def genreData(self, data):
		parse = re.search('Kategorien</h2>(.*)class="main-cat-bottom', data, re.S)
		print "Parse OK"
		phCat = re.findall('<a\shref="(.*?)".*?main-cat-name">(.*?)</div>', parse.group(1), re.S)
		if phCat:
			for (phUrl, phTitle) in phCat:
				phUrl = phUrl + "page/"
				self.genreliste.append((phTitle, phUrl))
			self.genreliste.sort()
			self.genreliste.insert(0, ("Newest", "http://www.porno-streams.com/page/"))
			self.genreliste.insert(0, ("--- Search ---", "callSuchen", None))
			self.chooseMenuList.setList(map(pornostreamsGenreListEntry, self.genreliste))
			self.keyLocked = False

	def dataError(self, error):
		print error

	def keyOK(self):
		streamGenreName = self['genreList'].getCurrent()[0][0]
		if streamGenreName == "--- Search ---":
			self.suchen()

		else:
			streamGenreLink = self['genreList'].getCurrent()[0][1]
			self.session.open(pornostreamsFilmScreen, streamGenreLink, streamGenreName)
		
	def suchen(self):
		self.session.openWithCallback(self.SuchenCallback, VirtualKeyBoard, title = (_("Suchkriterium eingeben")), text = self.suchString)

	def SuchenCallback(self, callback = None, entry = None):
		if callback is not None and len(callback):
			self.suchString = callback.replace(' ', '+')
			streamGenreLink = '%s' % (self.suchString)
			streamGenreName = "--- Search ---"
			self.session.open(pornostreamsFilmScreen, streamGenreLink, streamGenreName)

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

class pornostreamsFilmScreen(Screen):
	
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

		self['title'] = Label("Porno-Streams.com")
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
			url = "http://www.porno-streams.com/page/%s/?s=%s&submit=+" % (str(self.page), self.phCatLink)
		else:
			url = "%s%s" % (self.phCatLink, str(self.page))
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadData).addErrback(self.dataError)
	
	def loadData(self, data):
		lastp = re.findall('class=\'pages\'>.*?von (.*?)</span>', data, re.S)
		if lastp:
			lastp = lastp[0]
			print lastp
			self.lastpage = int(lastp)
		else:
			self.lastpage = 1
		self['page'].setText(str(self.page) + ' / ' + str(self.lastpage))	
		phMovies = re.findall('class="main-stream".*?class="cover-image">.*?<a\shref="(.*?)"\stitle="(.*?)".*?<img\ssrc="(.*?)"', data, re.S)
		if phMovies:
			for (phUrl, phTitle, phImage) in phMovies:
				if re.search('images-box.com|rapidimg.org', str(phImage), re.S):
					phImage = None
				self.filmliste.append((decodeHtml(phTitle), phUrl, phImage))
			self.chooseMenuList.setList(map(pornostreamsFilmListEntry, self.filmliste))
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
		self.session.open(pornostreamsStreamListeScreen, phLink, phTitle)

	def keyCancel(self):
		self.close()

class pornostreamsStreamListeScreen(Screen):
	
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

		self['title'] = Label("Porno-Streams.com")
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
		getPage(self.streamFilmLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		print "daten bekommen"
		parse = re.search('role="main">(.*)id="comments', data, re.S)
		streams = re.findall('.*?"(http://.*?(streamcloud.eu|flashx|userporn|jpg).*?)".*?', parse.group(1), re.S)
		if streams:
			for (stream, hostername) in streams:
				if re.match('.*?(streamcloud.eu|flashx|userporn)', hostername, re.S|re.I):
					print hostername, stream
					hostername = hostername.replace('.eu','')
					hostername = hostername.title()
					disc = re.search('.*?(CD-1|CD1|CD-2|CD2|_a.avi|_b.avi|-a.avi|-b.avi|DISC1|DISC2).*?', stream, re.S|re.I)
					if disc:
						discno = disc.group(1)
						discno = discno.replace('CD1','Teil 1').replace('CD2','Teil 2').replace('CD-1','Teil 1').replace('CD-2','Teil 2').replace('_a.avi','Teil 1').replace('_b.avi','Teil 2')
						discno = discno.replace('-a.avi','Teil 1').replace('-b.avi','Teil 2').replace('DISC1','Teil 1').replace('DISC2','Teil 2').replace('Disc1','Teil 1').replace('Disc2','Teil 2')
						hostername = hostername + ' (' + discno + ')'
					self.filmliste.append((hostername, stream))
		else:
			self.filmliste.append(('Keine Streams gefunden.', None))
		self.filmliste = list(set(self.filmliste))
		self.filmliste.sort()
		self.chooseMenuList.setList(map(pornostreamsHosterListEntry, self.filmliste))
		self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return
		streamLink = self['genreList'].getCurrent()[0][1]
		if streamLink == None:
			return
		url = streamLink
		url = url.replace('&amp;','&')
		url = url.replace('&#038;','&')
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
