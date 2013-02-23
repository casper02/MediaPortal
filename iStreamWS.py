#	-*-	coding:	utf-8	-*-

from imports import *
from decrypt import *

def IStreamGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 
class showIStreamGenre(Screen):
	skin = 	"""
		<screen name="IStream" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
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

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		
		self["actions"] = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("IStream.ws")
		self['name'] = Label("Genre Auswahl")
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
		print "ISteam.ws:"
		filmliste = []
		Genre = [("Kino", "http://istream.ws/c/filme/kino/page/"),
			("Neue Filme", "http://istream.ws/page/"),
			("Abenteuer", "http://istream.ws/c/filme/abenteuer/page/"),
			("Action", "http://istream.ws/c/filme/action/page/"),
			("Adventure", "http://istream.ws/c/filme/adventure/page/"),
			("Animation", "http://istream.ws/c/filme/animation/page/"),
			("Anime", "http://istream.ws/c/filme/anime/page/"),
			("Bollywood", "http://istream.ws/c/filme/bollywood/page/"),
			("Comedy", "http://istream.ws/c/filme/comedy/page/"),
			("Crime", "http://istream.ws/c/filme/crime/page/"),
			("Dokumentation", "http://istream.ws/c/filme/dokumentation/page/"),
			("Drama", "http://istream.ws/c/filme/drama/page/"),
			("Family", "http://istream.ws/c/filme/family/page/"),
			("Fantasy", "http://istream.ws/c/filme/fantasy/page/"),
			("Historienfilm", "http://istream.ws/c/filme/historienfilm/page/"),
			("History", "http://istream.ws/c/filme/history/page/"),
			("Horror", "http://istream.ws/c/filme/horror/page/"),
			("Kinderfilm", "http://istream.ws/c/filme/kinderfilm/page/"),
			("Komödie", "http://istream.ws/c/filme/komodie/page/"),
			("Kriegsfilm", "http://istream.ws/c/filme/kriegsfilm/page/"),
			("Kurzfilm", "http://istream.ws/c/filme/kurzfilm/page/"),
			("Martial Arts", "http://istream.ws/c/filme/martial-arts/page/"),
			("Mystery", "http://istream.ws/c/filme/mystery/page/"),
			("Romance", "http://istream.ws/c/filme/romance/page/"),
			("Satire", "http://istream.ws/c/filme/satire/page/"),
			("SciFi", "http://istream.ws/c/filme/science-ficton/page/"),
			("Sitcom", "http://istream.ws/c/filme/sitcom/page/"),
			("Sport", "http://istream.ws/c/filme/sport/page/"),
			("Thriller", "http://istream.ws/c/filme/thriller/page/"),
			("Trickfilm", "http://istream.ws/c/filme/trickfilm/page/"),
			("War", "http://istream.ws/c/filme/war/page/"),
			("Western", "http://istream.ws/c/filme/western/page/")]
					
		for (Name,Url) in Genre:
			self.filmliste.append((Name,Url))
			self.chooseMenuList.setList(map(IStreamGenreListEntry, self.filmliste))
		self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return
		genreName = self['filmList'].getCurrent()[0][0]
		genreLink = self['filmList'].getCurrent()[0][1]
		print genreLink
		self.session.open(IStreamFilmListeScreen, genreLink, genreName)
		
	def keyCancel(self):
		self.close()
		
def IStreamFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
class IStreamFilmListeScreen(Screen):
	skin = 	"""
		<screen name="IStream" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
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
			<widget name="page" position="810,420" size="85,25" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />	
		</screen>"""

	def __init__(self, session, genreLink, genreName):
		self.session = session
		self.genreLink = genreLink
		self.genreName = genreName
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

		self['title'] = Label("IStream.ws")
		self['name'] = Label(self.genreName)
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		self['page'] = Label("")
		
		self.keyLocked = True
		self.filmliste = []
		self.keckse = {}
		self.page = 0
		self.pages = 0;
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		url = "%s%s" % (self.genreLink, str(self.page))
		print url
		getPage(url, cookies=self.keckse, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print "dataError:"
		print error
		self.filmliste.append(("No movies found!",""))
		self.chooseMenuList.setList(map(IStreamFilmListEntry,	self.filmliste))
		
	def loadPageData(self, data):
		print "loadPageData:"
		if not re.match('http://istream.ws/page/',self.genreLink):
			filme = re.findall('<div class="cover">.*?<a href="(.*?)" rel=.*?title="(.*?)"><img class=.*?\?src=(.*?)&h=', data, re.S)
		else:
			filme = re.findall('<div class="voting".*?<a href="(.*?)".*?title="(.*?)">.*?data-original="(.*?)" alt', data)

		if filme:
			print "Movies found!"
			if not self.pages:
				pages = re.findall('<span class=\'pages\'>Seite 1 von (.*?)</', data)
				if pages:
					self.pages = int(pages[0])
				else:
					self.pages = 1
				self.page = 1
				print "Page: %d / %d" % (self.page,self.pages)
				
			self.filmliste = []
			for	(url,name,imageurl) in filme:
				#print	"Url: ", url, "Name: ", name, "ImgUrl: ", imageurl
				self.filmliste.append((decodeHtml(name), url, imageurl))
			self.chooseMenuList.setList(map(IStreamFilmListEntry,	self.filmliste))
			self.keyLocked	= False
			self.loadPic()
		else:
			print "No movies found!"
			self.filmliste.append(("No movies found!",""))
			self.chooseMenuList.setList(map(IStreamFilmListEntry,	self.filmliste))

	def loadPic(self):
		print "loadPic:"
		self['page'].setText("%d / %d" % (self.page,self.pages))
		streamName = self['filmList'].getCurrent()[0][0]
		streamUrl = self['filmList'].getCurrent()[0][1]
		self.getHandlung(streamUrl)
		self['name'].setText(streamName)
		streamPic = self['filmList'].getCurrent()[0][2]
		downloadPage(streamPic, "/tmp/Icon.jpg").addCallback(self.ShowCover)
	
	def getHandlung(self, url):
		getPage(url, cookies=self.keckse, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.setHandlung).addErrback(self.dataErrorH)
	
	def dataErrorH(self, error):
		print "dataErrorH:"
		print error
		self['handlung'].setText("Keine infos gefunden.")

	def setHandlung(self, data):
		print "setHandlung:"
		handlung = re.findall('meta property="og:description".*?=\'(.*?)\' />', data, re.S)
		if handlung:
			#print handlung
			handlung = re.sub(r"\s+", " ", handlung[0])
			self['handlung'].setText(decodeHtml(handlung))
		else:
			print "No Infos found!"
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
		streamName = self['filmList'].getCurrent()[0][0]
		self.session.open(IStreamStreams, streamLink, streamName)
	
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
		print "keyPageDown:"
		if self.keyLocked:
			return
		if not self.page < 2:
			self.page -= 1
			self.loadPage()
			
	def keyPageUp(self):
		print "keyPageUp:"
		if self.keyLocked:
			return
		if self.page < self.pages:
			self.page += 1 
			self.loadPage()
		
	def keyCancel(self):
		self.close()

def IStreamStreamListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0]+entry[2])
		] 
class IStreamStreams(Screen, ConfigListScreen):
	skin = 	"""
		<screen name="iStream" position="center,center" size="900,580" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,80" backgroundColor="#00242424"/>
			<widget name="title" position="25,15" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;26" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="730,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;26" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="580,20" size="300,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;18" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="leftContentTitle" position="0,80" size="900,26" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center"/>
			<widget name="streamlist" position="0,106" size="900,300" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<widget name="stationIcon" position="10,415" size="107,150" transparent="1" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png"/>
			<widget name="handlung" position="140,415" size="740,160" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
	        </screen>
		"""
		
	def __init__(self, session, filmUrl, filmName):
		self.session = session
		self.filmUrl = filmUrl
		self.filmName = filmName
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['title'] = Label("IStream.ws")
		self['leftContentTitle'] = Label("Stream Auswahl")
		self['stationIcon'] = Pixmap()
		self['handlung'] = Label("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		print "FilmUrl: %s" % self.filmUrl
		print "FilmName: %s" % self.filmName
		getPage(self.filmUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		print "parseData:"
		details = re.findall('og:image".*?"(.*?)"', data)
		streams = re.findall('a href="(.*?)".*?title=.*?\[(.*)\](.*)">', data)
		if streams:
			print "Streams found"
			for (isUrl,isStream,streamPart) in streams:
				if re.match('.*?(putlocker|sockshare|streamclou|xvidstage|filenuke|movreel|nowvideo|xvidstream|uploadc|vreer|MonsterUploads|Novamov|Videoweed|Divxstage|Ginbig|Flashstrea|Movshare|yesload|faststream|Vidstream|PrimeShare|flashx|Divxmov|Putme|Zooupload|Click.*?Play)', isStream, re.S|re.I):
					#print isUrl
					#print isStream,streamPart
					self.streamList.append((isStream,isUrl,streamPart))
			self.keyLocked = False			
		else:
			print "No Streams found"
			self.streamList.append(("No streams found!",""))			
		self.streamMenuList.setList(map(IStreamStreamListEntry, self.streamList))
			
		if details:
			#print "Details found"
			coverUrl = details[0]
			downloadPage(coverUrl, "/tmp/Icon.jpg").addCallback(self.ShowCover)			
	
	def ShowCover(self, picData):
		print "ShowCover:"
		if fileExists("/tmp/Icon.jpg"):
			self['stationIcon'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['stationIcon'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/Icon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['stationIcon'].instance.setPixmap(ptr.__deref__())
					self['stationIcon'].show()
					del self.picload

	def dataError(self, error):
		print "dataError:"
		print error
		self.streamList.append(("No streams found!",""))			
		self.streamMenuList.setList(map(IStreamStreamListEntry, self.streamList))
			
	def keyOK(self):
		if self.keyLocked:
			return
		streamLink = self['streamlist'].getCurrent()[0][1]
		streamPart = self['streamlist'].getCurrent()[0][2]
		self.filmName = "%s%s" % (self.filmName,streamPart)
		fp = urllib.urlopen(streamLink.replace('http://video.istream.ws/embed.php?m=','http://istream.ws/mirror.php?m='))
		streamLink = fp.geturl()
		fp.close()
		print "get_streamLink: %s" % streamLink
		get_stream_link(self.session).check_link(streamLink, self.got_link)
			
	def got_link(self, stream_url):
		#print "got_link:"
		if stream_url == None:
			message = self.session.open(MessageBox, _("Stream not found, try another Stream Hoster."), MessageBox.TYPE_INFO, timeout=3)
		else:
			sref = eServiceReference(0x1001, 0, stream_url)
			sref.setName(self.filmName)
			self.session.open(MoviePlayer, sref)
	
	def keyCancel(self):
		self.close()