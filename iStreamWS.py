#	-*-	coding:	utf-8	-*-

from imports import *
from decrypt import *
import Queue

def IStreamGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
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
			<widget name="ContentTitle" position="0,60" size="900,25" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center"/>
			<widget name="genreList" position="0,85" size="900,325" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="185,460" size="700,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="185,420" size="700,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
		</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		
		self["actions"] = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("IStream.ws")
		self['ContentTitle'] = Label("M e n ü")
		self['name'] = Label("Genre Auswahl")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.genreListe = []
		self.keckse = {}
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		print "ISteam.ws:"
		genreListe = []
		Genre = [("Kino", "http://istream.ws/c/filme/kino/page/"),
			("Neue Filme", "http://istream.ws/page/"),
			("Alle Filme", "http://istream.ws/c/filme/page/"),
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
			self.genreListe.append((Name,Url))
			self.chooseMenuList.setList(map(IStreamGenreListEntry, self.genreListe))
		self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return
		genreName = self['genreList'].getCurrent()[0][0]
		genreLink = self['genreList'].getCurrent()[0][1]
		print genreLink
		self.session.open(IStreamFilmListeScreen, genreLink, genreName)
		
	def keyCancel(self):
		self.close()
		
def IStreamFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
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
			<widget name="leftContentTitle" position="0,60" size="900,25" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center"/>
			<widget name="filmList" position="0,85" size="900,325" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="185,460" size="700,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="185,420" size="550,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="185,473" size="700,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
			<eLabel text="Page" position="750,420" size="100,25" backgroundColor="#00101214" transparent="1" foregroundColor="#00555556" font="Regular;20" valign="top" />
			<widget name="page" position="810,420" size="100,25" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />	
		</screen>"""

	def __init__(self, session, genreLink, genreName):
		self.session = session
		self.genreLink = genreLink
		self.genreName = genreName
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions","DirectionActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft,
			"upUp" : self.key_repeatedUp,
			"rightUp" : self.key_repeatedUp,
			"leftUp" : self.key_repeatedUp,
			"downUp" : self.key_repeatedUp,
			"upRepeated" : self.keyUpRepeated,
			"downRepeated" : self.keyDownRepeated,
			"rightRepeated" : self.keyRightRepeated,
			"leftRepeated" : self.keyLeftRepeated,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown,
			"1" : self.key_1,
			"3" : self.key_3,
			"4" : self.key_4,
			"6" : self.key_6,
			"7" : self.key_7,
			"9" : self.key_9,
			"green" : self.keySortAZ,
			"yellow" : self.keySortIMDB
		}, -1)

		self.sortOrder = 0;
		self.sortParIMDB = "?imdb_rating=desc"
		self.sortParAZ = "?orderby=title&order=ASC"
		self.genreTitle = "Filme in Genre "
		self.sortOrderStrAZ = " - Sortierung A-Z"
		self.sortOrderStrIMDB = " - Sortierung IMDB"
		self.sortOrderStrGenre = ""
		self['title'] = Label("IStream.ws")
		self['leftContentTitle'] = Label("")
		self['name'] = Label("")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		self['page'] = Label("")
		
		self.filmQ = Queue.Queue(0)
		self.hanQ = Queue.Queue(0)
		self.semaL = 0
		self.semaH = 0
		self.keyLocked = True
		self.filmListe = []
		self.keckse = {}
		self.page = 0
		self.pages = 0;
		self.neueFilme = re.match('Neue Filme',self.genreName)
		self.setGenreStrTitle()
		
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)

	def setGenreStrTitle(self):
		if not self.neueFilme:
			if not self.sortOrder:
				self.sortOrderStrGenre = self.sortOrderStrAZ
			else:
				self.sortOrderStrGenre = self.sortOrderStrIMDB
		else:
			self.sortOrderStrGenre = ""
		self['leftContentTitle'].setText("%s%s%s" % (self.genreTitle,self.genreName,self.sortOrderStrGenre))

	def loadPage(self):
		print "loadPage:"
		if not self.sortOrder:
			url = "%s%s%s" % (self.genreLink, str(self.page), self.sortParAZ)
		else:
			url = "%s%s%s" % (self.genreLink, str(self.page), self.sortParIMDB)
		if self.page:
			self['page'].setText("%d / %d" % (self.page,self.pages))

		self.filmQ.put(url)
		print "semaL ",self.semaL
		if not self.semaL:
			self.semaL = 1
			self.loadPageQueued()
		else:
			return
		
	def loadPageQueued(self):
		while not self.filmQ.empty():
			url = self.filmQ.get_nowait()
		#self.semaL = 0
		print url
		getPage(url, cookies=self.keckse, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def dataError(self, error):
		self.semaL=0
		print "dataError:"
		print error
		self.filmListe.append(("No movies found !",""))
		self.chooseMenuList.setList(map(IStreamFilmListEntry,	self.filmListe))
		
	def loadPageData(self, data):
		print "loadPageData:"
			
		if not re.match('http://istream.ws/page/',self.genreLink):
			filme = re.findall('<div class="cover">.*?<a href="(.*?)" rel=.*?title="(.*?)"><img class=.*?\?src=(.*?)&h=', data, re.S)
		else:
			filme = re.findall('<div class="voting".*?<a href="(.*?)".*?title="(.*?)">.*?data-original="(.*?)" alt', data)

		if filme:
			print "Movies found !"
			if not self.pages:
				m = re.findall('<span class=\'pages\'>Seite 1 von (.*?)</', data)
				if m:
					self.pages = int(m[0])
				else:
					self.pages = 1
				self.page = 1
				print "Page: %d / %d" % (self.page,self.pages)
				self['page'].setText("%d / %d" % (self.page,self.pages))
				
			self.filmListe = []
			for	(url,name,imageurl) in filme:
				#print	"Url: ", url, "Name: ", name, "ImgUrl: ", imageurl
				self.filmListe.append((decodeHtml(name), url, imageurl))
			self.chooseMenuList.setList(map(IStreamFilmListEntry,	self.filmListe))
			
			#if not self.filmQ.empty():
			#	self.loadPageQueued()
			#	return
			self.loadPic()
		else:
			print "No movies found !"
			self.filmListe.append(("No movies found !",""))
			self.chooseMenuList.setList(map(IStreamFilmListEntry,	self.filmListe))
			if self.filmQ.empty():
				self.semaL = 0
			else:
				self.loadPageQueued()

	def loadPic(self):
		print "loadPic:"
		streamName = self['filmList'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamPic = self['filmList'].getCurrent()[0][2]
		
		streamUrl = self['filmList'].getCurrent()[0][1]
		self.getHandlung(streamUrl)
		downloadPage(streamPic, "/tmp/Icon.jpg").addCallback(self.ShowCover)
		
	def getHandlung(self, url):
		print "getHandlung:"
		self.hanQ.put(url)
		if not self.semaH:
			self.semaH = 1
			self.getHandlungQeued()
		else:
			return
		
	def getHandlungQeued(self):
		while not self.hanQ.empty():
			url = self.hanQ.get_nowait()
		#print url
		getPage(url, cookies=self.keckse, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.setHandlung).addErrback(self.dataErrorH)
		
	def dataErrorH(self, error):
		self.semaH = 0
		print "dataErrorH:"
		print error
		self['handlung'].setText("Keine infos gefunden.")

	def setHandlung(self, data):
		print "setHandlung:"
			
		m = re.findall('meta property="og:description".*?=\'(.*?)\' />', data)
		if m:
			self['handlung'].setText(decodeHtml(re.sub(r"\s+", " ", m[0])))
		else:
			print "No Infos found !"
			self['handlung'].setText("Keine infos gefunden.")
			
		if not self.hanQ.empty():
			self.getHandlungQeued()
		else:
			self.semaH = 0;
		#print "semaH: ",self.semaH
		#print "semaL: ",self.semaL
		
	def ShowCover(self, picData):
		print "ShowCover:"
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
					
		if not self.filmQ.empty():
			self.loadPageQueued()
		else:
			self.semaL = 0;
		
		#print "semaH: ",self.semaH
		#print "semaL: ",self.semaL
		self.keyLocked	= False
			
	def keyOK(self):
		if (self.keyLocked|self.semaL|self.semaH):
			return

		streamLink = self['filmList'].getCurrent()[0][1]
		streamName = self['filmList'].getCurrent()[0][0]
		self.session.open(IStreamStreams, streamLink, streamName)
	
	def keyUp(self):
		if (self.keyLocked|self.semaL|self.semaH):
			return
		self['filmList'].up()
		self.loadPic()
		
	def keyDown(self):
		if (self.keyLocked|self.semaL|self.semaH):
			return
		self['filmList'].down()
		self.loadPic()
		
	def keyUpRepeated(self):
		#print "keyUpRepeated"
		if (self.keyLocked|self.semaL|self.semaH):
			return
		self['filmList'].up()
		
	def keyDownRepeated(self):
		#print "keyDownRepeated"
		if (self.keyLocked|self.semaL|self.semaH):
			return
		self['filmList'].down()
		
	def key_repeatedUp(self):
		#print "key_repeatedUp"
		self.loadPic()
		
	def keyLeft(self):
		if (self.keyLocked|self.semaL|self.semaH):
			return
		self['filmList'].pageUp()
		
	def keyRight(self):
		if (self.keyLocked|self.semaL|self.semaH):
			return
		self['filmList'].pageDown()
			
	def keyLeftRepeated(self):
		if (self.keyLocked|self.semaL|self.semaH):
			return
		self['filmList'].pageUp()
		
	def keyRightRepeated(self):
		if (self.keyLocked|self.semaL|self.semaH):
			return
		self['filmList'].pageDown()
			
	def keyPageDown(self):
		#print "keyPageDown()"
		self.keyPageDownFast(1)
			
	def keyPageUp(self):
		#print "keyPageUp()"
		self.keyPageUpFast(1)
			
	def keyPageUpFast(self,step):
		if self.keyLocked:
			return
		#print "keyPageUpFast: ",step
		oldpage = self.page
		if (self.page + step) <= self.pages:
			self.page += step
		else:
			self.page += self.pages - self.page
		#print "Page %d/%d" % (self.page,self.pages)
		if oldpage != self.page:
			self.loadPage()
		
	def keyPageDownFast(self,step):
		if self.keyLocked:
			return
		print "keyPageDownFast: ",step
		oldpage = self.page
		if (self.page - step) >= 1:
			self.page -= step
		else:
			self.page -=  -1 + self.page
		#print "Page %d/%d" % (self.page,self.pages)
		if oldpage != self.page:
			self.loadPage()

	def key_1(self):
		#print "keyPageDownFast(2)"
		self.keyPageDownFast(2)
		
	def key_4(self):
		#print "keyPageDownFast(5)"
		self.keyPageDownFast(5)
		
	def key_7(self):
		#print "keyPageDownFast(10)"
		self.keyPageDownFast(10)
		
	def key_3(self):
		#print "keyPageUpFast(2)"
		self.keyPageUpFast(2)
		
	def key_6(self):
		#print "keyPageUpFast(5)"
		self.keyPageUpFast(5)
		
	def key_9(self):
		#print "keyPageUpFast(10)"
		self.keyPageUpFast(10)

	def keySortAZ(self):
		if (self.keyLocked|self.semaL|self.semaH):
			return
		if self.sortOrder and not self.neueFilme:
			self.sortOrder = 0
			self.setGenreStrTitle()
			self.loadPage()
	
	def keySortIMDB(self):
		if (self.keyLocked|self.semaL|self.semaH):
			return
		if not (self.sortOrder or self.neueFilme):
			self.sortOrder = 1
			self.setGenreStrTitle()
			self.loadPage()
	
	def keyCancel(self):
		self.close()

def IStreamStreamListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0]+entry[2])
		] 
class IStreamStreams(Screen, ConfigListScreen):
	skin = 	"""
		<screen name="iStream" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,80" backgroundColor="#00242424"/>
			<widget name="title" position="25,15" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;26" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="730,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;26" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="580,20" size="300,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;18" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="ContentTitle" position="0,60" size="900,26" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center"/>
			<widget name="streamList" position="0,85" size="900,325" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="185,460" size="700,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="185,420" size="700,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="185,473" size="700,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
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
		self['ContentTitle'] = Label("Stream Auswahl")
		self['coverArt'] = Pixmap()
		self['handlung'] = Label("")
		self['name'] = Label(filmName)
		
		self.streamListe = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamList'] = self.streamMenuList
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		print "FilmUrl: %s" % self.filmUrl
		print "FilmName: %s" % self.filmName
		getPage(self.filmUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		print "parseData:"
		streams = re.findall('a href="(.*?)".*?title=.*?\[(.*)\](.*)">', data)
		if streams:
			print "Streams found"
			for (isUrl,isStream,streamPart) in streams:
				if re.match('.*?(putlocker|sockshare|streamclou|xvidstage|filenuke|movreel|nowvideo|xvidstream|uploadc|vreer|MonsterUploads|Novamov|Videoweed|Divxstage|Ginbig|Flashstrea|Movshare|yesload|faststream|Vidstream|PrimeShare|flashx|Divxmov|Putme|Zooupload|Click.*?Play)', isStream, re.S|re.I):
					#print isUrl
					#print isStream,streamPart
					self.streamListe.append((isStream,isUrl,streamPart))
				else:
					print "No supported hoster:"
					print isStream
					print isUrl
			self.keyLocked = False			
		else:
			print "No Streams found"
			self.streamListe.append(("No streams found !",""))			
		self.streamMenuList.setList(map(IStreamStreamListEntry, self.streamListe))
			
		m = re.findall('og:image".*?"(.*?)"', data)
		if m:
			#print "CoverURL found"
			downloadPage(m[0], "/tmp/Icon.jpg").addCallback(self.ShowCover)			
	
	def ShowCover(self, picData):
		print "ShowCover:"
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

	def dataError(self, error):
		print "dataError:"
		print error
		self.streamListe.append(("No streams found !",""))			
		self.streamMenuList.setList(map(IStreamStreamListEntry, self.streamListe))
			
	def keyOK(self):
		if self.keyLocked:
			return
		streamLink = self['streamList'].getCurrent()[0][1]
		fp = urllib.urlopen(streamLink.replace('http://video.istream.ws/embed.php?m=','http://istream.ws/mirror.php?m='))
		#fp = urllib.urlopen(streamLink)
		streamLink = fp.geturl()
		fp.close()
		print "get_streamLink:"
		get_stream_link(self.session).check_link(streamLink, self.got_link)
			
	def got_link(self, stream_url):
		print "got_link:"
		if stream_url == None:
			message = self.session.open(MessageBox, _("Stream not found, try another Stream Hoster."), MessageBox.TYPE_INFO, timeout=3)
		else:
			sref = eServiceReference(0x1001, 0, stream_url)
			sref.setName("%s%s" % (self.filmName,self['streamList'].getCurrent()[0][2]))
			self.session.open(MoviePlayer, sref)
	
	def keyCancel(self):
		self.close()