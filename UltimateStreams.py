#	-*-	coding:	utf-8	-*-

from imports import *
from decrypt import *
import Queue
import threading

US_Version = "Ultimate-Streams.Com v1.01"

US_siteEncoding = 'iso-8859-1'

def USGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 
class showUSGenre(Screen):

	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/showUSGenre.xml" % config.mediaportal.skin.value
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"] = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label(US_Version)
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
		print "UltimateStreams:"
		genreListe = []
		Genre = [("Kino", "http://ultimate-streams.com/index.php?area=kinofilme&type=&pageno="),
			("Letzte Einträge", "http://ultimate-streams.com/index.php?area=&type=&pageno="),
			("LAST 100", "http://ultimate-streams.com/index.php?area=last100&type=&pageno="),
			("Top Streams", "http://ultimate-streams.com/index.php?area=&type=&pageno="),
			("Abenteuer", "http://ultimate-streams.com/index.php?area=abenteuer&type=&pageno="),
			("Action", "http://ultimate-streams.com/index.php?area=action&type=&pageno="),
			("Anime", "http://ultimate-streams.com/index.php?area=anime&type=&pageno="),
			("Biografie", "http://ultimate-streams.com/index.php?area=biografie&type=&pageno="),
			("Bollywood", "http://ultimate-streams.com/index.php?area=bollywood&type=&pageno="),
			("Dokumentation", "http://ultimate-streams.com/index.php?area=doku&type=&pageno="),
			("Drama", "http://ultimate-streams.com/index.php?area=drama&type=&pageno="),
			("Familie", "http://ultimate-streams.com/index.php?area=familie&type=&pageno="),
			("Fantasy", "http://ultimate-streams.com/index.php?area=fantasy&type=&pageno="),
			("Historienfilm", "http://ultimate-streams.com/index.php?area=historie&type=&pageno="),
			("Horror", "http://ultimate-streams.com/index.php?area=horror&type=&pageno="),
			("Komödie", "http://ultimate-streams.com/index.php?area=komoedie&type=&pageno="),
			("Kriegsfilm", "http://ultimate-streams.com/index.php?area=kriegsfilm&type=&pageno="),
			("Krimi", "http://ultimate-streams.com/index.php?area=krimi&type=&pageno="),
			("Martial Arts", "http://ultimate-streams.com/index.php?area=eastern&type=&pageno="),
			("Märchen", "http://ultimate-streams.com/index.php?area=maerchen&type=&pageno="),
			("Musikfilm", "http://ultimate-streams.com/index.php?area=musikfilme&type=&pageno="),
			("Mystery", "http://ultimate-streams.com/index.php?area=mystery&type=&pageno="),
			("Romantik", "http://ultimate-streams.com/index.php?area=romanze&type=&pageno="),
			("SciFi", "http://ultimate-streams.com/index.php?area=scifi&type=&pageno="),
			("Sport", "http://ultimate-streams.com/index.php?area=sport&type=&pageno="),
			("Thriller", "http://ultimate-streams.com/index.php?area=thriller&type=&pageno="),
			("Western", "http://ultimate-streams.com/index.php?area=western&type=&pageno="),
			("Zeichentrick", "http://ultimate-streams.com/index.php?area=zeichentrick&type=&pageno=")]
					
		for (Name,Url) in Genre:
			self.genreListe.append((Name,Url))
			self.chooseMenuList.setList(map(USGenreListEntry, self.genreListe))
		self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return
		genreName = self['genreList'].getCurrent()[0][0]
		genreLink = self['genreList'].getCurrent()[0][1]
		print genreLink
		self.session.open(USFilmListeScreen, genreLink, genreName)
		
	def keyCancel(self):
		self.close()
		
def USFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
class USFilmListeScreen(Screen):
	
	def __init__(self, session, genreLink, genreName):
		self.session = session
		self.genreLink = genreLink
		self.genreName = genreName
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/USFilmListeScreen.xml" % config.mediaportal.skin.value
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
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
			"yellow" : self.keySortIMDB,
			"blue" :  self.keyPageUp,
			"red" :  self.keyPageDown
			#"seekBackManual" :  self.keyPageDownMan,
			#"seekFwdManual" :  self.keyPageUpMan,
			#"seekFwd" :  self.keyPageUp,
			#"seekBack" :  self.keyPageDown
		}, -1)

		self.sortOrder = 0;
		"""
		self.sortParIMDB = "?imdb_rating=desc"
		self.sortParAZ = "?orderby=title&order=ASC"
		self.genreTitle = "Filme in Genre "
		self.sortOrderStrAZ = " - Sortierung A-Z"
		self.sortOrderStrIMDB = " - Sortierung IMDB"
		self.sortOrderStrGenre = ""
		self['title'] = Label("UltimateStreams.Com")
		"""
		self.baseUrl = "http://ultimate-streams.com/index.php"
		self.genreTitle = "Filme in Genre "
		self.sortParIMDB = ""
		self.sortParAZ = ""
		self.sortOrderStrAZ = ""
		self.sortOrderStrIMDB = ""
		self.sortOrderStrGenre = ""
		self['title'] = Label(US_Version)
		self['leftContentTitle'] = Label("")
		self['name'] = Label("")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		self['page'] = Label("")
		
		self.timerStart = False
		self.seekTimerRun = False
		self.filmQ = Queue.Queue(0)
		self.hanQ = Queue.Queue(0)
		self.picQ = Queue.Queue(0)
		self.updateP = 0
		self.eventL = threading.Event()
		self.eventH = threading.Event()
		self.eventP = threading.Event()
		self.keyLocked = True
		self.filmListe = []
		self.keckse = {}
		self.page = 0
		self.pages = 0;
		self.neueFilme = re.match('.*?Letzte Einträge',self.genreName)
		self.topStreams = re.match('.*?Top Streams',self.genreName)
		self.Last100 = re.match('.*?LAST 100',self.genreName)
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

		#if self.seekTimerRun:
		#	return
			
		self.filmQ.put(url)
		if not self.eventL.is_set():
			self.eventL.set()
			self.loadPageQueued()
		print "eventL ",self.eventL.is_set()
		
	def loadPageQueued(self):
		print "loadPageQueued:"
		self['name'].setText('Bitte warten..')
		while not self.filmQ.empty():
			url = self.filmQ.get_nowait()
		#self.eventL.clear()
		print url
		getPage(url, cookies=self.keckse, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def dataError(self, error):
		self.eventL.clear()
		print "dataError:"
		print error
		self.filmListe.append(("No movies found !",""))
		self.chooseMenuList.setList(map(USFilmListEntry, self.filmListe))
		
	def loadPageData(self, data):
		print "loadPageData:"
			
		if self.Last100:
			print "Last 100 search.."
			m=re.search('<!-- start content -->(.*)<!-- end content -->',data,re.S)
			if m:
				filme = re.findall('.*?id="title".*?<a href="(.*?)".*?: none;">(.*?)</font>', m.group(1), re.S)
			else:
				filme = None
		elif self.topStreams:
			print "Top Streams search.."
			m=re.search('Top(.*?)Streams(.*?)Views</b><br/></div>\n',data,re.S)
			if m:
				filme = re.findall('.*?<a href="(.*?)" title="(.*?)"><img src="(.*?)"', m.group(2))
			else:
				filme = None
		else:
			print "Normal search.."
			filme = re.findall('id="list" height="205".*?<a href="(.*?)" title="(.*?)"><img src="(.*?)" height=', data, re.S)
		
		if filme:
			print "Movies found !"
			if not self.pages:
				m = re.findall('\( Page 1 of (.*?) \)', data)
				if m:
					self.pages = int(m[0])
				else:
					self.pages = 1
				self.page = 1
				print "Page: %d / %d" % (self.page,self.pages)
				self['page'].setText("%d / %d" % (self.page,self.pages))
			
			self.filmListe = []
			if not self.Last100:
				#self.filmListe = filme
				for	(url,name,img) in filme:
					#print	"Url: ", url, "Name: ", name
					self.filmListe.append((rawDecode(name).lstrip(), url, img))
			else:
				for	(url,name) in filme:
					#print	"Url: ", url, "Name: ", name
					self.filmListe.append((rawDecode(name).lstrip(), url, None))
			self.chooseMenuList.setList(map(USFilmListEntry, self.filmListe))
			
			self.loadPicQueued()
		else:
			print "No movies found !"
			self.filmListe.append(("No movies found !",""))
			self.chooseMenuList.setList(map(USFilmListEntry, self.filmListe))
			if self.filmQ.empty():
				self.eventL.clear()
			else:
				self.loadPageQueued()

	def loadPic(self):
		print "loadPic:"
		
		if self.picQ.empty():
			self.eventP.clear()
			print "picQ is empty"
			return
		
		if self.eventH.is_set() or self.updateP:
			print "Pict. or descr. update in progress"
			print "eventH: ",self.eventH.is_set()
			print "eventP: ",self.eventP.is_set()
			print "updateP: ",self.updateP
			return
			
		while not self.picQ.empty():
			self.picQ.get_nowait()
		
		streamName = self['filmList'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamPic = self['filmList'].getCurrent()[0][2]
		streamUrl = self.baseUrl+re.sub('amp;','',self['filmList'].getCurrent()[0][1])
		#print "streamName: ",streamName
		#print "streamPic: ",streamPic
		#print "streamUrl: ",streamUrl
		self.getHandlung(streamUrl)
		self.updateP = 1
		if streamPic == None:
			print "ImageUrl is None !"
			self.ShowCoverNone()
		else:
			print "Download pict."
			downloadPage(streamPic, "/tmp/Icon.jpg").addCallback(self.ShowCover)
		
	def getHandlung(self, url):
		print "getHandlung:"
		if url == None:
			print "No Infos found !"
			self['handlung'].setText("Keine infos gefunden.")
			return
			
		self.hanQ.put(url)
		if not self.eventH.is_set():
			self.eventH.set()
			self.getHandlungQeued()
		print "eventH: ",self.eventH.is_set()
		
	def getHandlungQeued(self):
		while not self.hanQ.empty():
			url = self.hanQ.get_nowait()
		#print url
		getPage(url, cookies=self.keckse, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.setHandlung).addErrback(self.dataErrorH)
		
	def dataErrorH(self, error):
		self.eventH.clear()
		print "dataErrorH:"
		print error
		self['handlung'].setText("Keine infos gefunden.")

	def setHandlung(self, data):
		print "setHandlung:"
			
		m = re.findall('<tr height="22.*?<td id="views".*?">(.*?)</td>', data, re.S)
		if m:
			self['handlung'].setText(rawDecode(re.sub(r"\s+", " ", m[0])))
		else:
			print "No Infos found !"
			self['handlung'].setText("Keine infos gefunden.")
			
		if not self.hanQ.empty():
			self.getHandlungQeued()
		else:
			self.eventH.clear()
			self.loadPic()
		print "eventH: ",self.eventH.is_set()
		print "eventL: ",self.eventL.is_set()
		
	def ShowCover(self, picData):
		print "ShowCover:"
		picPath = "/tmp/Icon.jpg"
		self.ShowCoverFile(picPath)
		
	def ShowCoverNone(self):
		print "ShowCoverNone:"
		picPath = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png"
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
				
		self.updateP = 0;
		self.keyLocked	= False
		if not self.filmQ.empty():
			self.loadPageQueued()
		else:
			self.eventL.clear()
			self.loadPic()
			
	def loadPicQueued(self):
		print "loadPicQueued:"
		self.picQ.put(None)
		if not self.eventP.is_set():
			self.eventP.set()
			self.loadPic()
		print "eventP: ",self.eventP.is_set()
		
	def keyOK(self):
		if (self.keyLocked|self.eventL.is_set()|self.eventH.is_set()):
			return

		streamLink = self.baseUrl+re.sub('amp;','',self['filmList'].getCurrent()[0][1])
		streamName = self['filmList'].getCurrent()[0][0]
		imageLink = self['filmList'].getCurrent()[0][2]
		self.session.open(USStreams, streamLink, streamName, imageLink)
	
	def keyUp(self):
		if self.keyLocked:
			return
		self['filmList'].up()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['filmList'].down()
		
	def keyUpRepeated(self):
		#print "keyUpRepeated"
		if self.keyLocked:
			return
		self['filmList'].up()
		
	def keyDownRepeated(self):
		#print "keyDownRepeated"
		if self.keyLocked:
			return
		self['filmList'].down()
		
	def key_repeatedUp(self):
		#print "key_repeatedUp"
		if self.keyLocked:
			return
		self.loadPicQueued()
		
	def keyLeft(self):
		if self.keyLocked:
			return
		self['filmList'].pageUp()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['filmList'].pageDown()
			
	def keyLeftRepeated(self):
		if self.keyLocked:
			return
		self['filmList'].pageUp()
		
	def keyRightRepeated(self):
		if self.keyLocked:
			return
		self['filmList'].pageDown()
			
	def keyPageDown(self):
		#print "keyPageDown()"
		if self.seekTimerRun:
			self.seekTimerRun = False
		self.keyPageDownFast(1)
			
	def keyPageUp(self):
		#print "keyPageUp()"
		if self.seekTimerRun:
			self.seekTimerRun = False
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

	#def keyPageDownMan(self):
	#	self.keyPageDownUp = 0;
	#	self.seekTimerRun = True

	#def keyPageUpMan(self):
	#	self.keyPageDownUp = 1;
	#	self.seekTimerRun = True

	#def seekTimer(self):
	#	print "seekTimer:"
	#	if self.seekTimerRun:
	#		if not self.keyPageDownUp:
	#			self.keyPageDown()
	#		else:
	#			self.keyPageUp()
		
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
		#if (self.keyLocked):
		#	return
		#if self.sortOrder and not self.neueFilme:
		#	self.sortOrder = 0
		#	self.setGenreStrTitle()
		#	self.loadPage()
		pass
		
	def keySortIMDB(self):
		#if (self.keyLocked):
		#	return
		#if not (self.sortOrder or self.neueFilme):
		#	self.sortOrder = 1
		#	self.setGenreStrTitle()
		#	self.loadPage()
		pass
		
	def keyCancel(self):
		self.close()

def USStreamListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 
class USStreams(Screen, ConfigListScreen):
	
	def __init__(self, session, filmUrl, filmName, imageLink):
		self.session = session
		self.filmUrl = filmUrl
		self.filmName = filmName
		self.imageUrl = imageLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/USStreams.xml" % config.mediaportal.skin.value
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['title'] = Label(US_Version)
		self['ContentTitle'] = Label("Stream Auswahl")
		self['coverArt'] = Pixmap()
		self['handlung'] = Label("")
		self['name'] = Label(filmName)
		
		self.baseUrl = "http://ultimate-streams.com/index.php"
		self.streamListe = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamList'] = self.streamMenuList
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		print "loadPage:"
		streamUrl = self.filmUrl
		#print "FilmUrl: ", streamUrl
		#print "FilmName: ", self.filmName
		getPage(streamUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		print "parseData:"
		streams = re.findall('<a title=.*?href="(.*?)".*?" alt="(.*?)" width=', data)
		self.streamListe = []
		if streams:
			print "Streams found"
			for (isUrl,isStream) in streams:
				if re.match('.*?(putlocker|sockshare|streamclou|xvidstage|filenuke|movreel|nowvideo|xvidstream|uploadc|vreer|MonsterUploads|Novamov|Videoweed|Divxstage|Ginbig|Flashstrea|Movshare|yesload|faststream|Vidstream|PrimeShare|flashx|Divxmov|Putme|Zooupload|Click.*?Play)', isStream, re.S|re.I):
					#print isUrl
					#print isStream,streamPart
					self.streamListe.append((isStream,isUrl))
				else:
					print "No supported hoster:"
					print isStream
					print isUrl
		else:
			print "No streams found"
			self.streamListe.append(("No streams found !",""))			
		self.streamMenuList.setList(map(USStreamListEntry, self.streamListe))
		self.keyLocked = False			
		print "imageUrl: ",self.imageUrl
		if self.imageUrl:
			downloadPage(self.imageUrl, "/tmp/Icon.jpg").addCallback(self.ShowCover)			
	
	def ShowCover(self, picData):
		print "ShowCover:"
		if fileExists("/tmp/Icon.jpg") or picData == None:
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
		self.streamListe.append(("Read error !",""))			
		self.streamMenuList.setList(map(USStreamListEntry, self.streamListe))
			
	def keyOK(self):
		if self.keyLocked:
			return
		streamLink = self['streamList'].getCurrent()[0][1]
		print "get_streamLink:"
		get_stream_link(self.session).check_link(streamLink, self.got_link)
			
	def got_link(self, stream_url):
		print "got_link:"
		if stream_url == None:
			message = self.session.open(MessageBox, _("Stream not found, try another Stream Hoster."), MessageBox.TYPE_INFO, timeout=3)
		else:
			sref = eServiceReference(0x1001, 0, stream_url)
			sref.setName(self.filmName)
			self.session.open(MoviePlayer, sref)
	
	def keyCancel(self):
		self.close()
		
def rawDecode(txt):
	txt = txt.replace('\xe4','ä').replace('\xf6','ö').replace('\xfc','ü').replace('\xdf','ß')
	txt = txt.replace('\xc4','Ä').replace('\xd6','Ö').replace('\xdc','Ü')
	return decodeHtml(txt)
	