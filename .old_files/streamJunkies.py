from imports import *
from decrypt import *

def streamGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		]
class streamGenreScreen(Screen):
	skin = 	"""
		<screen name="Streamjunkies.org" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="mediaportal;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="mediaportal;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="mediaportal;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="genreList" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,440" size="160,120" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="mediaportal;26" valign="top" />
		</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("Streamjunkies.org")
		self['name'] = Label("Genre Auswahl")
		self['coverArt'] = Pixmap()
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.genreliste.append(("Neusten", "http://streamjunkies.org"))
		self.genreliste.append(("Kino", "http://streamjunkies.org/wp-content/themes/Streamjunkies/neu.php"))
		self.genreliste.append(("Abenteuer", "http://streamjunkies.org/thema/abenteuer/"))
		self.genreliste.append(("Action", "http://streamjunkies.org/thema/action/"))
		self.genreliste.append(("Anime", "http://streamjunkies.org/thema/anime/"))
		self.genreliste.append(("Biografie", "http://streamjunkies.org/thema/Biografie/"))
		self.genreliste.append(("Dokus", "http://streamjunkies.org/thema/dokus/"))
		self.genreliste.append(("Drama", "http://streamjunkies.org/thema/drama/"))
		self.genreliste.append(("Familie", "http://streamjunkies.org/thema/familie/"))
		self.genreliste.append(("Fantasy", "http://streamjunkies.org/thema/fantasy/"))
		self.genreliste.append(("Historie", "http://streamjunkies.org/thema/historie/"))
		self.genreliste.append(("Horror", "http://streamjunkies.org/thema/horror/"))
		self.genreliste.append(("Komodie", "http://streamjunkies.org/thema/komodie/"))
		self.genreliste.append(("Kriegsfilme", "http://streamjunkies.org/thema/Kriegsfilme/"))
		self.genreliste.append(("Krimi", "http://streamjunkies.org/thema/krimi/"))
		self.genreliste.append(("Martial-arts", "http://streamjunkies.org/thema/martial-arts/"))
		self.genreliste.append(("Musik", "http://streamjunkies.org/thema/musik/"))
		self.genreliste.append(("Romantik", "http://streamjunkies.org/thema/romantik/"))
		self.genreliste.append(("Scifi", "http://streamjunkies.org/thema/scifi/"))
		self.genreliste.append(("Thriller", "http://streamjunkies.org/thema/thriller/"))
		self.genreliste.append(("Western", "http://streamjunkies.org/thema/western/"))
		self.genreliste.append(("Zeichentrick", "http://streamjunkies.org/thema/zeichentrick/"))
		self.chooseMenuList.setList(map(streamGenreListEntry, self.genreliste))

	def keyOK(self):
		streamGenreLink = self['genreList'].getCurrent()[0][1]
		print streamGenreLink
		self.session.open(streamFilmListeScreen, streamGenreLink)

	def keyCancel(self):
		self.close()

def streamFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
		
class streamFilmListeScreen(Screen):
	skin = 	"""
		<screen name="Streamjunkies.org" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="mediaportal;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="mediaportal;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="mediaportal;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="filmList" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="mediaportal;26" valign="top" />
			<widget name="handlung" position="185,473" size="700,140" backgroundColor="#00101214" transparent="1" font="mediaportal;20" valign="top" />
		</screen>"""

	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft,
		}, -1)

		self['title'] = Label("Streamjunkies.org")
		self['name'] = Label("Film Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.filmliste = []
		self.keckse = {}
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		print "check", self.streamGenreLink, "ok"
		getPage(self.streamGenreLink, agent=std_headers).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		print "daten bekommen"
		if self.streamGenreLink == "http://streamjunkies.org":
			print "last update"
			search = re.findall('<h2>Last Update</h2>(.*?)<div class="sidebar_right">', data, re.S)
			if search:
				streamFilme = re.findall('<a href="(http://streamjunkies.org.*?)" title="(.*?)"><img src="(.*?)"', search[0])
				for streamLink,streamName,streamPic in streamFilme:
					if not streamName == "Streamjunkies":
						#print streamLink,streamName,streamPic
						self.filmliste.append((decodeHtml(streamName), streamLink, streamPic))
				self.chooseMenuList.setList(map(streamFilmListEntry, self.filmliste))
				self.keyLocked = False
				self.loadPic()
				
		elif self.streamGenreLink == "http://streamjunkies.org/wp-content/themes/Streamjunkies/neu.php":
			print "kino"
			streamFilme = re.findall('<a href="(http://streamjunkies.org.*?)".*?img src="(.*?)".*?title="(.*?)"', data, re.S)
			if streamFilme:
				for streamLink,streamPic,streamName in streamFilme:
					if not streamName == "Streamjunkies":
						#print streamLink,streamName,streamPic
						self.filmliste.append((decodeHtml(streamName), streamLink, streamPic))
				self.chooseMenuList.setList(map(streamFilmListEntry, self.filmliste))
				self.keyLocked = False
				self.loadPic()
		else:
			print "normal"
			streamFilme = re.findall('<a href="(http://streamjunkies.org.*?)" title="(.*?)"><img src="(.*?)"', data)
			if streamFilme:
				for streamLink,streamName,streamPic in streamFilme:
					if not streamName == "Streamjunkies":
						self.filmliste.append((decodeHtml(streamName), streamLink, streamPic))
				self.chooseMenuList.setList(map(streamFilmListEntry, self.filmliste))
				self.keyLocked = False
				self.loadPic()

	def loadPic(self):
		streamName = self['filmList'].getCurrent()[0][0]
		streamFilmLink = self['filmList'].getCurrent()[0][1]
		self['name'].setText(streamName)
		streamPic = self['filmList'].getCurrent()[0][2]
		downloadPage(streamPic, "/tmp/spIcon.jpg").addCallback(self.ShowCover)
		#print streamPic
		#print streamFilmLink
		getPage(streamFilmLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageInfos).addErrback(self.dataError)
		
	def loadPageInfos(self, data):
		if re.match('.*?Genre :', data, re.S):
			handlung = re.findall('<div class="embed">.*?Genre :.*?<p>(.*?)</p>', data, re.S)
			if handlung:
				print handlung
				self['handlung'].setText(decodeHtml(handlung[0]))
			else:
				self['handlung'].setText("keine infos")
		else:
			handlung = re.findall('<div class="embed">.*?</div>.*?<p>.*?</b><br />\n<br />\n(.*?)</p>', data, re.S)
			if handlung:
			#	print handlung
				self['handlung'].setText(decodeHtml(handlung[0]))
			else:
				self['handlung'].setText("keine infos")
	
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
					
	def keyOK(self):
		if self.keyLocked:
			return
		streamLink = self['filmList'].getCurrent()[0][1]
		print streamLink
		getPage(streamLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.findStreamcloud).addErrback(self.dataError)

	def findStreamcloud(self, data):
		streamName = self['filmList'].getCurrent()[0][0]
		#self.streamParts = re.findall('<a title="Streamcloud" href="(http://streamcloud.eu/.*?)"', data)
		self.streamParts = re.findall('<div class="spoiler-body"><a title="(.*?)" href="(.*?)"', data)
		if self.streamParts:
			self.session.open(streamCDListeScreen, self.streamParts, streamName)
		else:
			message = self.session.open(MessageBox, _("Kein Streamcloud Stream verfuegbar."), MessageBox.TYPE_INFO, timeout=5)

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

def streamCDListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 
		
class streamCDListeScreen(Screen):
	skin = 	"""
		<screen name="Streamjunkies.org" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="mediaportal;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="mediaportal;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="mediaportal;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="filmList" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,440" size="160,120" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="mediaportal;26" valign="top" />
		</screen>"""

	def __init__(self, session, parts, streamfilmname):
		self.session = session
		self.streamParts = parts
		self.streamfilmname = streamfilmname
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("Streamjunkies.org")
		self['name'] = Label("Part Auswahl")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = False
		self.keckse = {}
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		for (name,link) in self.streamParts:
			if re.match('.*?(STREAMCLOUD|XVIDSTAGE|ZOOUPLOUD)', name, re.S|re.I):
				self.filmliste.append((name,link))
		self.chooseMenuList.setList(map(streamCDListEntry, self.filmliste))		
		
	def keyOK(self):
		if self.keyLocked:
			return

		self.streamLink = self['filmList'].getCurrent()[0][1]
		self.keyLocked = True
		get_stream_link(self.session).check_link(self.streamLink, self.got_link)
			
	def got_link(self, stream_url):
		print "callback"
		self.keyLocked = False
		if stream_url == None:
			message = self.session.open(MessageBox, _("Stream not found, try another Stream Hoster."), MessageBox.TYPE_INFO, timeout=3)
		else:
			sref = eServiceReference(0x1001, 0, stream_url)
			sref.setName(self.streamfilmname)
			self.session.open(MoviePlayer, sref)

	def dataError(self, error):
		self.keyLocked = False
		print error
		
	def keyCancel(self):
		self.close()

