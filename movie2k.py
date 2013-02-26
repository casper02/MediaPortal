from imports import *
from decrypt import *

def m2kGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 
class m2kGenreScreen(Screen):
	skin = 	"""
		<screen name="movie2k.to" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="genreList" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,440" size="160,120" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
		</screen>"""

	def __init__(self, session, showM2kPorn):
		self.session = session
		self.showM2kPorn = showM2kPorn
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['title'] = Label("movie2k.to")
		self['name'] = Label("Genre Auswahl")
		self['coverArt'] = Pixmap()
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.genreliste.append(("Kinofilme", "http://www.movie2k.to/index.php?lang=de"))
		self.genreliste.append(("Videofilme", "http://www.movie2k.to/index.php?lang=de"))
		self.genreliste.append(("Neue Updates (Filme)", "http://www.movie2k.to/movies-updates-"))
		self.genreliste.append(("Empfohlene Serien", "http://www.movie2k.to/tvshows_featured.php"))
		self.genreliste.append(("Letzte Updates (Serien)", "http://www.movie2k.to/tvshows_featured.php"))
		if self.showM2kPorn == True:
			self.genreliste.append(("Letzte Updates (XXX)", "http://www.movie2k.to/xxx-updates.html"))
		self.genreliste.append(("Abenteuer", "http://movie2k.to/movies-genre-4-"))
		self.genreliste.append(("Action", "http://movie2k.to/movies-genre-1-"))
		self.genreliste.append(('Biografie', 'http://movie2k.to/movies-genre-6-'))
		self.genreliste.append(('Bollywood', 'http://movie2k.to/movies-genre-27-'))
		self.genreliste.append(('Dokumentation', 'http://movie2k.to/movies-genre-8-'))
		self.genreliste.append(('Drama', 'http://movie2k.to/movies-genre-2-'))
		self.genreliste.append(('Erwachsene', 'http://movie2k.to/movies-genre-58-'))
		self.genreliste.append(('Familie', 'http://movie2k.to/movies-genre-9-'))
		self.genreliste.append(('Fantasy', 'http://movie2k.to/movies-genre-10-'))
		self.genreliste.append(('Film Noir', 'http://movie2k.to/movies-genre-60-'))
		self.genreliste.append(('Game Show', 'http://movie2k.to/movies-genre-61-'))
		self.genreliste.append(('History', 'http://movie2k.to/movies-genre-13-'))
		self.genreliste.append(('Horror', 'http://movie2k.to/movies-genre-14-'))
		self.genreliste.append(('Comedy', 'http://movie2k.to/movies-genre-3-'))
		self.genreliste.append(('Kriegsfilme', 'http://movie2k.to/movies-genre-24-'))
		self.genreliste.append(('Krimi', 'http://movie2k.to/movies-genre-7-'))
		self.genreliste.append(('Kurzfilme', 'http://movie2k.to/movies-genre-55-'))
		self.genreliste.append(('Musicals', 'http://movie2k.to/movies-genre-56-'))
		self.genreliste.append(('Musik', 'http://movie2k.to/movies-genre-15-'))
		self.genreliste.append(('Mystery', 'http://movie2k.to/movies-genre-17-'))
		self.genreliste.append(('News', 'http://movie2k.to/movies-genre-62-'))
		self.genreliste.append(('Reality TV', 'http://movie2k.to/movies-genre-59-'))
		if self.showM2kPorn == True:
			self.genreliste.append(('Pornos', 'http://www.movie2k.to/genres-xxx.html'))
		self.genreliste.append(('Romanzen', 'http://movie2k.to/movies-genre-20-'))
		self.genreliste.append(('Sci-Fy', 'http://movie2k.to/movies-genre-21-'))
		self.genreliste.append(('Andere', 'http://movie2k.to/movies-'))
		self.genreliste.append(('Sport', 'http://movie2k.to/movies-'))
		self.genreliste.append(('Talk Shows', 'http://movie2k.to/movies-genre-63-'))
		self.genreliste.append(('Thriller', 'http://movie2k.to/movies-genre-23-'))
		self.genreliste.append(('Animation', 'http://movie2k.to/movies-genre-5-'))
		self.genreliste.append(('Western', 'http://movie2k.to/movies-genre-25-'))
		self.chooseMenuList.setList(map(m2kGenreListEntry, self.genreliste))

	def keyOK(self):
		streamGenreName = self['genreList'].getCurrent()[0][0]
		streamGenreLink = self['genreList'].getCurrent()[0][1]
		if streamGenreName == "Kinofilme":
			self.session.open(m2kKinoFilmeListeScreen, streamGenreLink)
		elif streamGenreName == "Videofilme":
			self.session.open(m2kVideoFilmeListeScreen, streamGenreLink)
		elif streamGenreName == "Letzte Updates (Filme)":
			self.session.open(m2kupdateFilmeListeScreen, streamGenreLink)
		elif streamGenreName == "Empfohlene Serien":
			self.session.open(m2kTopSerienFilmeListeScreen, streamGenreLink)
		elif streamGenreName == "Letzte Updates (Serien)":
			self.session.open(m2kSerienUpdateFilmeListeScreen, streamGenreLink)
		elif streamGenreName == "Letzte Updates (XXX)":
			self.session.open(m2kXXXUpdateFilmeListeScreen, streamGenreLink, '')
		else:
			self.session.open(m2kKinoAlleFilmeListeScreen, streamGenreLink)

	def keyCancel(self):
		self.close()

def m2kFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 


class m2kKinoAlleFilmeListeScreen(Screen):
	skin = 	"""
		<screen name="movie2k.to" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="filmList" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="185,473" size="700,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
			<eLabel text="Page" position="750,420" size="100,25" backgroundColor="#00101214" transparent="1" foregroundColor="#00555556" font="Regular;20" valign="top" />
			<widget name="page" position="850,420" size="45,25" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />	
		</screen>"""

	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown,
			"green" : self.keyPageNumber
		}, -1)

		self['title'] = Label("movie2k.to")
		self['name'] = Label("Filme Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.filmliste = []
		self.XXX = False
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		self.page = 1
		self['page'] = Label("1")
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		url = ''
		if self.streamGenreLink == 'http://www.movie2k.to/genres-xxx.html':
			url = str(self.streamGenreLink)
			getPage(url, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadXXXPageData).addErrback(self.dataError)
		else:
			url = '%s%s%s' % (self.streamGenreLink, self.page, '.html')
			getPage(url, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print error

	def loadXXXPageData(self, data):
		self.XXX = True
		xxxGenre = re.findall('<TD id="tdmovies" width="155">.*?<a href="(.*?)">(.*?)</a>', data, re.S)
		if xxxGenre:
			self.filmliste = []
			for teil_url, title in xxxGenre:
				url = '%s%s' % ('http://www.movie2k.to/', teil_url)
				title.replace("\t","")
				self.filmliste.append((decodeHtml(title), url))
			self.chooseMenuList.setList(map(m2kFilmListEntry, self.filmliste))
			self.keyLocked = False
			self['page'].setText(str(self.page))

	def loadPageData(self, data):
		print "daten bekommen"
		kino = re.findall('<TR id="coverPreview(.*?)">.*?<a href="(.*?)">(.*?)     ', data, re.S)
		if kino:
			self.filmliste = []
			for image, teil_url, title in kino:
				url = '%s%s' % ('http://www.movie2k.to/', teil_url)
				print title
				self.filmliste.append((decodeHtml(title), url, image))
			self.chooseMenuList.setList(map(m2kFilmListEntry, self.filmliste))
			self.keyLocked = False
			self['page'].setText(str(self.page))

	def loadPic(self):
		url = self['filmList'].getCurrent()[0][1]
		data = urllib.urlopen(url).read()
		filmdaten = re.findall('<div style="float:left">.*?<img src="(.*?)".*?<div class="moviedescription">(.*?)</div>', data, re.S)
		if filmdaten:
			streamPic, handlung = filmdaten[0]
			downloadPage(streamPic, "/tmp/Icon.jpg").addCallback(self.ShowCover)
			self['handlung'].setText(decodeHtml(handlung))
		
	def showHandlung(self, data):
		handlung = re.findall('<div class="moviedescription">(.*?)<', data, re.S)
		if handlung:
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

	def keyPageNumber(self):
		self.session.openWithCallback(self.callbackkeyPageNumber, VirtualKeyBoard, title = (_("Seitennummer eingeben")), text = str(self.page))

	def callbackkeyPageNumber(self, answer):
		if answer is not None:
			self.page = int(answer)
			self.loadPage()

	def keyOK(self):
		if self.keyLocked:
			return
		if self.XXX == False:
			streamName = self['filmList'].getCurrent()[0][0]
			streamLink = self['filmList'].getCurrent()[0][1]
			self.session.open(m2kStreamListeScreen, streamLink, streamName, "movie")
		else:
			xxxGenreName = self['filmList'].getCurrent()[0][0]
			xxxGenreLink = self['filmList'].getCurrent()[0][1]
			self.session.open(m2kXXXUpdateFilmeListeScreen, xxxGenreLink, 'X')

	def keyLeft(self):
		if self.keyLocked:
			return
		self['filmList'].pageUp()
		if self.XXX == False:
			self.loadPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['filmList'].pageDown()
		if self.XXX == False:
			self.loadPic()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['filmList'].up()
		if self.XXX == False:
			self.loadPic()

	def keyDown(self):
		if self.keyLocked:
			return
		self['filmList'].down()
		if self.XXX == False:
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

class m2kKinoFilmeListeScreen(Screen):
	skin = 	"""
		<screen name="movie2k.to" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="filmList" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="185,473" size="700,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
		</screen>"""

	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)

		self['title'] = Label("movie2k.to")
		self['name'] = Label("Filme Auswahl")
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
		getPage(self.streamGenreLink, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		print "daten bekommen"
		kino = re.findall('<div style="float:left"><a href="(.*?)" ><img src="(.*?)" border=0 style="width:105px;max-width:105px;max-height:160px;min-height:140px;" alt=".*?kostenlos" title="(.*?).kostenlos"></a>', data, re.S)
		if kino:
			for url,image,title in kino:
				url = "%s%s" % ("http://www.movie2k.to/", url)
				print title
				self.filmliste.append((decodeHtml(title), url, image))
			self.chooseMenuList.setList(map(m2kFilmListEntry, self.filmliste))
			self.keyLocked = False
			self.loadPic()

	def loadPic(self):
		streamName = self['filmList'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamUrl = self['filmList'].getCurrent()[0][1]
		getPage(streamUrl, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.showHandlung).addErrback(self.dataError)
		streamPic = self['filmList'].getCurrent()[0][2]
		downloadPage(streamPic, "/tmp/Icon.jpg").addCallback(self.ShowCover)
		
	def showHandlung(self, data):
		handlung = re.findall('<div class="moviedescription">(.*?)<', data, re.S)
		if handlung:
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
		streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]
		self.session.open(m2kStreamListeScreen, streamLink, streamName, "movie")

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
			
	def keyCancel(self):
		self.close()

class m2kVideoFilmeListeScreen(Screen):
	skin = 	"""
		<screen name="movie2k.to" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="filmList" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="185,473" size="700,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
		</screen>"""

	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)

		self['title'] = Label("movie2k.to")
		self['name'] = Label("Filme Auswahl")
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
		getPage(self.streamGenreLink, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		print "daten bekommen"
		video = re.findall('<div style="float: left;"><a href="(.*?)" ><img src="(.*?)" alt=".*?" title="(.*?)" border="0" style="width:105px;max-width:105px;max-height:160px;min-height:140px;"></a>', data, re.S)
		if video:
			for url,image,title in video:
				url = "%s%s" % ("http://www.movie2k.to/", url)
				print title
				self.filmliste.append((decodeHtml(title), url, image))
			self.chooseMenuList.setList(map(m2kFilmListEntry, self.filmliste))
			self.keyLocked = False
			self.loadPic()

	def loadPic(self):
		streamName = self['filmList'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamUrl = self['filmList'].getCurrent()[0][1]
		getPage(streamUrl, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.showHandlung).addErrback(self.dataError)
		streamPic = self['filmList'].getCurrent()[0][2]
		downloadPage(streamPic, "/tmp/Icon.jpg").addCallback(self.ShowCover)
		
	def showHandlung(self, data):
		handlung = re.findall('<div class="moviedescription">(.*?)<', data, re.S)
		if handlung:
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
		streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]
		self.session.open(m2kStreamListeScreen, streamLink, streamName, "movie")

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
			
	def keyCancel(self):
		self.close()

class m2kupdateFilmeListeScreen(Screen):
	skin = 	"""
		<screen name="movie2k.to" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="filmList" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="185,473" size="700,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
		</screen>"""

	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)

		self['title'] = Label("movie2k.to")
		self['name'] = Label("Filme Auswahl")
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
		getPage(self.streamGenreLink, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		print "daten bekommen"
		updates = re.findall('<td valign="top" height="100%"><a href="(.*?)" ><font color="#000000" size="-1"><strong>(.*?)</strong></font></a></td>', data, re.S)
		if updates:
			for url,title in updates:
				url = "%s%s" % ("http://www.movie2k.to/", url)
				print title
				self.filmliste.append((decodeHtml(title), url))
			self.chooseMenuList.setList(map(m2kFilmListEntry, self.filmliste))
			self.keyLocked = False
			self.loadPic()

	def loadPic(self):
		streamName = self['filmList'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamUrl = self['filmList'].getCurrent()[0][1]
		getPage(streamUrl, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.showHandlung).addErrback(self.dataError)
		
	def showHandlung(self, data):
		image = re.findall('<meta property="og:image" content="(.*?)"', data, re.S)
		if image:
			downloadPage(image[0], "/tmp/Icon.jpg").addCallback(self.ShowCover)

		handlung = re.findall('<div class="moviedescription">(.*?)<', data, re.S)
		if handlung:
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
		streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]
		self.session.open(m2kStreamListeScreen, streamLink, streamName, "movie")

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
			
	def keyCancel(self):
		self.close()

class m2kTopSerienFilmeListeScreen(Screen):
	skin = 	"""
		<screen name="movie2k.to" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="filmList" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="185,473" size="700,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
		</screen>"""

	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)

		self['title'] = Label("movie2k.to")
		self['name'] = Label("Serien Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.keckse = {}
		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.m2kcookie)

	def m2kcookie(self):
		url = "http://www.movie2k.to/index.php?lang=de"
		getPage(url, agent=std_headers, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getm2kcookie).addErrback(self.dataError)
		
	def getm2kcookie(self, data):
		self.loadPage()

	def loadPage(self):
		getPage(self.streamGenreLink, agent=std_headers, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print error

	def loadPageData(self, data):
		print "daten bekommen"
		serien = re.findall('<div style="float:left"><a href="(.*?)"><img src="(.*?)" border=0 width=105 height=150 alt=".*?" title="(.*?)"></a>', data, re.S)
		if serien:
			for url,image,title in serien:
				url = "%s%s" % ("http://www.movie2k.to/", url)
				print title
				self.filmliste.append((decodeHtml(title), url, image))
			self.chooseMenuList.setList(map(m2kFilmListEntry, self.filmliste))
			self.keyLocked = False
			self.loadPic()

	def loadPic(self):
		streamName = self['filmList'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamUrl = self['filmList'].getCurrent()[0][1]
		getPage(streamUrl, agent=std_headers, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.showHandlung).addErrback(self.dataError)
		streamPic = self['filmList'].getCurrent()[0][2]
		downloadPage(streamPic, "/tmp/Icon.jpg").addCallback(self.ShowCover)
		
	def showHandlung(self, data):
		handlung = re.findall('<div class="moviedescription">(.*?)<', data, re.S)
		if handlung:
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
		streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]
		print streamName, streamLink
		self.session.open(m2kEpisodenListeScreen, streamLink, streamName)

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
			
	def keyCancel(self):
		self.close()

class m2kSerienUpdateFilmeListeScreen(Screen):
	skin = 	"""
		<screen name="movie2k.to" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="filmList" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="185,473" size="700,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
		</screen>"""

	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)

		self['title'] = Label("movie2k.to")
		self['name'] = Label("Serien Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.filmliste = []
		self.keckse = {}
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.m2kcookie)

	def m2kcookie(self):
		url = "http://www.movie2k.to/index.php?lang=de"
		getPage(url, agent=std_headers, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getm2kcookie).addErrback(self.dataError)
		
	def getm2kcookie(self, data):
		self.loadPage()

	def loadPage(self):
		getPage(self.streamGenreLink, agent=std_headers, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		print "daten bekommen"
		serien = re.findall('<td id="tdmovies"> <img style="vertical-align:top;".*?<a href="(.*?)">.*?<font color="#000000">(.*?)</font></a>', data, re.S)
		if serien:
			for url,title in serien:
				url = "%s%s" % ("http://www.movie2k.to/", url)
				print title
				self.filmliste.append((decodeHtml(title), url))
			self.chooseMenuList.setList(map(m2kFilmListEntry, self.filmliste))
			self.keyLocked = False
			self.loadPic()

	def loadPic(self):
		streamName = self['filmList'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamUrl = self['filmList'].getCurrent()[0][1]
		getPage(streamUrl, agent=std_headers, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.showHandlung).addErrback(self.dataError)
		
	def showHandlung(self, data):
		image = re.findall('<meta property="og:image" content="(.*?)"', data, re.S)
		if image:
			downloadPage(image[0], "/tmp/Icon.jpg").addCallback(self.ShowCover)

		handlung = re.findall('<div class="moviedescription">(.*?)<', data, re.S)
		if handlung:
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
		streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]
		print streamName, streamLink
		self.session.open(m2kEpisodenListeScreen, streamLink, streamName)

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
			
	def keyCancel(self):
		self.close()

class m2kStreamListeScreen(Screen):
	skin = 	"""
		<screen name="movie2k.to" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="filmList" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="185,473" size="700,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
		</screen>"""

	def __init__(self, session, streamGenreLink, streamName, which):
		self.session = session
		self.streamGenreLink = streamGenreLink
		self.streamName = streamName
		self.which = which
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("movie2k.to")
		self['name'] = Label("Stream Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.filmliste = []
		self.keckse = {}
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		getPage(self.streamGenreLink, agent=std_headers, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		print "daten bekommen"
		if self.which == "movie":
			hoster = re.findall('<tr id=.*?tablemoviesindex2.*?><td height=.*?20.*?width.*?"150.*?><a href.*?"(.*?.html).*?>(.*?).<.*?src.*?"http://img.movie2k.to/img/.*?\..*?> \&nbsp;(.*?)</a>.*?alt.*?"(Movie quality.*?)" title=', data, re.S)
			if hoster:
				for url,datum,hostername,quali in hoster:
					url = "%s%s" % ("http://www.movie2k.to/", url)
					print hostername, url
					if re.match('.*?(putlocker|sockshare|streamclou|xvidstage|filenuke|movreel|nowvideo|xvidstream|uploadc|vreer|MonsterUploads|Novamov|Videoweed|Divxstage|Ginbig|Flashstrea|Movshare|yesload|faststream|Vidstream|PrimeShare|flashx|Divxmov|Putme|Zooupload|Wupfile)', hostername, re.S|re.I):
						self.filmliste.append((url, datum, hostername, quali.replace('Movie quality ','').replace('\\','')))
				self.chooseMenuList.setList(map(self.m2kStreamListEntry, self.filmliste))
				self.keyLocked = False
				self.loadPic()
		else:
			hoster = re.findall('"tablemoviesindex2.*?<a href.*?"(.*?.html).*?style.*?src.*?"http://img.movie2k.to/img/.*?.[gif|png].*?> \&nbsp;(.*?)</a></td></tr>', data, re.S)
			if hoster:
				for url,hostername in hoster:
					url = "%s%s" % ("http://www.movie2k.to/", url)		
					print hostername, url
					if re.match('.*?(putlocker|sockshare|streamclou|xvidstage|filenuke|movreel|nowvideo|xvidstream|uploadc|vreer|MonsterUploads|Novamov|Videoweed|Divxstage|Ginbig|Flashstrea|Movshare|yesload|faststream|Vidstream|PrimeShare|flashx|Divxmov|Putme|Zooupload|Wupfile)', hostername, re.S|re.I):
						self.filmliste.append((url, hostername))
				self.chooseMenuList.setList(map(self.m2kStream2ListEntry, self.filmliste))
				self.keyLocked = False
				self.loadPic()
		
	def m2kStreamListEntry(self, entry):
		return [entry,
			(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 200, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[1]),
			(eListboxPythonMultiContent.TYPE_TEXT, 250, 0, 200, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[2]),
			(eListboxPythonMultiContent.TYPE_TEXT, 450, 0, 430, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[3])
			]
			
	def m2kStream2ListEntry(self, entry):
		return [entry,
			(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 200, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[1])
			]

	def loadPic(self):
		getPage(self.streamGenreLink, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.showHandlung).addErrback(self.dataError)
		
	def showHandlung(self, data):
		image = re.findall('<meta property="og:image" content="(.*?)"', data, re.S)
		if image:
			downloadPage(image[0], "/tmp/Icon.jpg").addCallback(self.ShowCover)
			
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
		streamLink = self['filmList'].getCurrent()[0][0]
		print self.streamName, streamLink
		getPage(streamLink, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.get_streamlink, streamLink).addErrback(self.dataError)
		
	def get_streamlink(self, data, streamLink):
		if re.match('.*?(http://img.movie2k.to/img/parts/teil1_aktiv.png|http://img.movie2k.to/img/parts/teil1_inaktiv.png)', data, re.S):
			self.session.open(m2kPartListeScreen, streamLink, self.streamName)
		else:
			link = re.findall('<a target="_blank" href="(.*?)"', data, re.S)
			if link:
				print link
				get_stream_link(self.session).check_link(link[0], self.got_link)
			else:
				link = re.findall('<div id="emptydiv"><iframe.*?src=["|\'](.*?)["|\']', data, re.S)
				if link:
					print link[0]
					get_stream_link(self.session).check_link(link[0], self.got_link)

	def got_link(self, stream_url):
		if stream_url == None:
			message = self.session.open(MessageBox, _("Stream not found, try another Stream Hoster."), MessageBox.TYPE_INFO, timeout=3)
		else:
			sref = eServiceReference(0x1001, 0, stream_url)
			sref.setName(self.streamName)
			self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()

class m2kPartListeScreen(Screen):
	skin = 	"""
		<screen name="movie2k.to" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="filmList" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="185,473" size="700,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
		</screen>"""

	def __init__(self, session, streamGenreLink, streamName):
		self.session = session
		self.streamGenreLink = streamGenreLink
		self.streamName = streamName
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("movie2k.to")
		self['name'] = Label("Part Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(41)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		id = re.findall('[film-|movie-](\d+)\.html', self.streamGenreLink, re.S)
		if id:
			print id
			url1 = "%s%s%s" % ("http://www.movie2k.to/movie.php?id=", id[0], "&part=1")
			url2 = "%s%s%s" % ("http://www.movie2k.to/movie.php?id=", id[0], "&part=2")
			self.filmliste.append(("1", url1))
			self.filmliste.append(("2", url2))
			self.chooseMenuList.setList(map(self.m2kPartsListEntry, self.filmliste))
			self.keyLocked = False
		else:
			print "id fehler.."

	def m2kPartsListEntry(self, entry):
		part = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/teil%s.png" % entry[0]
		return [entry,
			(eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST, 396, 3, 108, 35, LoadPixmap(part))
			]

	def keyOK(self):
		if self.keyLocked:
			return
		streamPart = self['filmList'].getCurrent()[0][0]
		streamLinkPart = self['filmList'].getCurrent()[0][1]
		self.sname = "%s - Teil %s" % (self.streamName, streamPart)
		print self.sname, streamLinkPart
		getPage(streamLinkPart, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.get_streamlink).addErrback(self.dataError)

	def get_streamlink(self, data):
		link = re.findall('<a target="_blank" href="(.*?)"', data, re.S)
		if link:
			print link
			get_stream_link(self.session).check_link(link[0], self.got_link)
		else:
			link = re.findall('<div id="emptydiv"><iframe.*?src=["|\'](.*?)["|\']', data, re.S)
			if link:
				print link[0]
				get_stream_link(self.session).check_link(link[0], self.got_link)

	def got_link(self, stream_url):
		if stream_url == None:
			message = self.session.open(MessageBox, _("Stream not found, try another Stream Hoster."), MessageBox.TYPE_INFO, timeout=3)
		else:
			sref = eServiceReference(0x1001, 0, stream_url)
			sref.setName(self.sname)
			self.session.open(MoviePlayer, sref)

	def dataError(self, error):
		print error
		
	def keyCancel(self):
		self.close()

class m2kEpisodenListeScreen(Screen):
	skin = 	"""
		<screen name="movie2k.to" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="filmList" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="185,473" size="700,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
		</screen>"""

	def __init__(self, session, streamGenreLink, streamName):
		self.session = session
		self.streamGenreLink = streamGenreLink
		self.streamName = streamName
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("movie2k.to")
		self['name'] = Label("Episoden Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.filmliste = []
		self.keckse = {}
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		getPage(self.streamGenreLink, agent=std_headers, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		print "daten bekommen"
		folgen = re.findall('<FORM name="episodeform(.*?)">(.*?)</FORM>', data, re.S)
		if folgen:
			for staffel,ep_data in folgen:
				episodes = re.findall('<OPTION value="(.*?)".*?>Episode.(.*?)</OPTION>', ep_data, re.S)
				if episodes:
					for url_to_streams, episode in episodes:
						url_to_streams = "%s%s" % ("http://www.movie2k.to/", url_to_streams)
						if int(staffel) < 10:
							staffel3 = "S0"+str(staffel)
						else:
							staffel3 = "S"+str(staffel)
							
						if int(episode) < 10:
							episode3 = "E0"+str(episode)
						else:
							episode3 = "E"+str(episode)
						staffel_episode = "%s - %s%s" % (self.streamName,staffel3,episode3)
						self.filmliste.append((staffel_episode,url_to_streams))
			self.chooseMenuList.setList(map(self.m2kStreamListEntry, self.filmliste))
			self.keyLocked = False
			self.loadPic()
			
	def m2kStreamListEntry(self, entry):
		return [entry,
			(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0]),
			]

	def loadPic(self):
		getPage(self.streamGenreLink, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.showHandlung).addErrback(self.dataError)
		
	def showHandlung(self, data):
		image = re.findall('<meta property="og:image" content="(.*?)"', data, re.S)
		if image:
			downloadPage(image[0], "/tmp/Icon.jpg").addCallback(self.ShowCover)
			
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
		streamEpisode = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]
		print streamEpisode, streamLink
		self.session.open(m2kStreamListeScreen, streamLink, streamEpisode, "tv")

	def keyCancel(self):
		self.close()

class m2kXXXUpdateFilmeListeScreen(Screen):
	skin = """
		<screen name="movie2k.to" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="filmList" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="185,473" size="700,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
      <eLabel text="Page" position="750,420" size="100,25" backgroundColor="#00101214" transparent="1" foregroundColor="#00555556" font="Regular;20" valign="top" />
      <widget name="page" position="850,420" size="45,25" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
		</screen>"""

	def __init__(self, session, streamXXXLink, genre):
		self.session = session
		self.streamXXXLink = streamXXXLink
		self.genre = False
		if genre == 'X':
			self.genre = True
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft,
			"green" : self.keyPageNumber,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown
		}, -1)

		self['title'] = Label("movie2k.to")
		self['name'] = Label("XXX Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.filmliste = []
		self.keckse = {}
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		self.page = 1
		self['page'] = Label("1")
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		print 'load xxx updates...'
		print 'Link...', self.streamXXXLink
		if self.genre == True:
			shortUrl = re.findall('http://www.movie2k.to/xxx-genre-[0-9]*[0-9]*.*?',self.streamXXXLink)
			shortUrlC = str(shortUrl[0])
			url = shortUrlC + '-' + str(self.page) + '.html'
			print url
		else:
			url = str(self.streamXXXLink)
		opener = urllib2.build_opener()
		opener.addheaders.append(('Cookie', 'xxx2=ok'))
		resp = opener.open(url)
		pageData = resp.read()
		self.loadPageData(pageData)
		#getPage(self.streamGenreLink, agent=std_headers, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		print "daten bekommen"
		self.filmliste = []
		if self.genre == False:
			serien = re.findall('<TD id="tdmovies" width="380">.*?<a href="(.*?)">(.*?)</a>', data, re.S)
		else:
			serien = re.findall('<TD width="550" id="tdmovies">.*?<a href="(.*?)">(.*?)</a>', data, re.S)
		#serien = re.findall('<td id="tdmovies"> <img style="vertical-align:top;".*?<a href="(.*?)">.*?<font color="#000000">(.*?)</font></a>', data, re.S)
		if serien:
			for url,title in serien:
				url = "%s%s" % ("http://www.movie2k.to/", url)
				title.replace("\t","")
				self.filmliste.append((decodeHtml(title), url))
			self.chooseMenuList.setList(map(m2kFilmListEntry, self.filmliste))
			self.keyLocked = False
			self['page'].setText(str(self.page))
			self.loadPic()

	def loadPic(self):
		streamName = self['filmList'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamUrl = self['filmList'].getCurrent()[0][1]
		getPage(streamUrl, agent=std_headers, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.showHandlung).addErrback(self.dataError)
		
	def showHandlung(self, data):
		image = re.findall('<meta property="og:image" content="(.*?)"', data, re.S)
		if image:
			downloadPage(image[0], "/tmp/Icon.jpg").addCallback(self.ShowCover)

		handlung = re.findall('<div class="moviedescription">(.*?)<', data, re.S)
		if handlung:
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

	def keyPageNumber(self):
		self.session.openWithCallback(self.callbackkeyPageNumber, VirtualKeyBoard, title = (_("Seitennummer eingeben")), text = str(self.page))

	def callbackkeyPageNumber(self, answer):
		if answer is not None:
			self.page = int(answer)
			self.loadPage()
				
	def keyOK(self):
		if self.keyLocked:
			return
		streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]
		self.session.open(m2kStreamListeScreen, streamLink, streamName, "movie")
		
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
		self['filmList'].pageUp()
		self.loadPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['filmList'].pageDown()
		self.loadPic()
		
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
			
	def keyCancel(self):
		self.close()
