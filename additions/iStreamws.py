#	-*-	coding:	utf-8	-*-

from Plugins.Extensions.mediaportal.resources.imports import *
from Plugins.Extensions.mediaportal.resources.decrypt import *
import Queue
import threading
from Components.ScrollLabel import ScrollLabel

# teilweise von movie2k geliehen
if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/TMDb/plugin.pyo'):
	from Plugins.Extensions.TMDb.plugin import *
	TMDbPresent = True
elif fileExists('/usr/lib/enigma2/python/Plugins/Extensions/IMDb/plugin.pyo'):
	TMDbPresent = False
	IMDbPresent = True
	from Plugins.Extensions.IMDb.plugin import *
else:
	IMDbPresent = False
	TMDbPresent = False

IS_Version = "iStream.ws v1.08"

IS_siteEncoding = 'utf-8'

"""
	Tastenfunktionen in der Filmliste:
		Bouquet +/-				: Seitenweise blättern in 1 Schritten Up/Down
		'1', '4', '7',
		'3', 6', '9'			: blättern in 2er, 5er, 10er Schritten Down/Up
		Grün/Gelb				: Sortierung [A-Z] bzw. [IMDB]
		INFO					: anzeige der IMDB-Bewertung

	Stream Auswahl:
		Rot/Blau				: Die Beschreibung Seitenweise scrollen

"""

def IStreamGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 
class showIStreamGenre(Screen):
	
	def __init__(self, session, mode):
		self.session = session
		self.mode = mode
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"

		path = "%s/%s/defaultGenreScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/defaultGenreScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"] = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label(IS_Version)
		self['ContentTitle'] = Label("M e n ü")
		self['name'] = Label("Genre Auswahl")
		self['F1'] = Label("")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		
		self.keyLocked = True
		self.genreListe = []
		self.keckse = {}
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		print "ISteam.ws:"
		genreListe = []
		if self.mode == "porn":
			Genre = [("Porn", "http://istream.ws/c/porn/page/")]
		else:
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
	
	def __init__(self, session, genreLink, genreName):
		self.session = session
		self.genreLink = genreLink
		self.genreName = genreName
		
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"
		
		path = "%s/%s/defaultListScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/defaultListScreen.xml"

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
			"red" :  self.keyTxtPageUp,
			"blue" :  self.keyTxtPageDown,
			"info" :  self.keyTMDbInfo
		}, -1)

		self.sortOrder = 0;
		self.sortParIMDB = "?imdb_rating=desc"
		self.sortParAZ = "?orderby=title&order=ASC"
		self.genreTitle = "Filme in Genre "
		self.sortOrderStrAZ = " - Sortierung A-Z"
		self.sortOrderStrIMDB = " - Sortierung IMDb"
		self.sortOrderStrGenre = ""
		self['title'] = Label(IS_Version)
		self['ContentTitle'] = Label("")
		self['name'] = Label("")
		self['handlung'] = ScrollLabel("")
		self['coverArt'] = Pixmap()
		self['Page'] = Label("Page")
		self['page'] = Label("")
		self['F1'] = Label("Text-")
		self['F2'] = Label("SortA-Z")
		self['F3'] = Label("SortIMDb")
		self['F4'] = Label("Text+")
		
		self.timerStart = False
		self.seekTimerRun = False
		self.eventL = threading.Event()
		self.eventH = threading.Event()
		self.eventP = threading.Event()
		self.filmQ = Queue.Queue(0)
		self.hanQ = Queue.Queue(0)
		self.picQ = Queue.Queue(0)
		self.updateP = 0
		self.keyLocked = True
		self.filmListe = []
		self.keckse = {}
		self.page = 0
		self.pages = 0;
		self.neueFilme = re.match('.*?Neue Filme',self.genreName)
		self.setGenreStrTitle()
		
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['liste'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)

	def setGenreStrTitle(self):
		if not self.neueFilme:
			if not self.sortOrder:
				self.sortOrderStrGenre = self.sortOrderStrAZ
			else:
				self.sortOrderStrGenre = self.sortOrderStrIMDB
		else:
			self.sortOrderStrGenre = ""
		self['ContentTitle'].setText("%s%s%s" % (self.genreTitle,self.genreName,self.sortOrderStrGenre))

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
		print "eventL ",self.eventL.is_set()
		if not self.eventL.is_set():
			self.eventL.set()
			self.loadPageQueued()
		print "eventL ",self.eventL.is_set()
		
	def loadPageQueued(self):
		print "loadPageQueued:"
		self['name'].setText('Bitte warten...')
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
		self.chooseMenuList.setList(map(IStreamFilmListEntry,	self.filmListe))
		
	def loadPageData(self, data):
		print "loadPageData:"
			
		if not self.neueFilme:
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
			self.loadPicQueued()
		else:
			print "No movies found !"
			self.filmListe.append(("No movies found !",""))
			self.chooseMenuList.setList(map(IStreamFilmListEntry,	self.filmListe))
			if self.filmQ.empty():
				self.eventL.clear()
			else:
				self.loadPageQueued()

	def loadPicQueued(self):
		print "loadPicQueued:"
		self.picQ.put(None)
		if not self.eventP.is_set():
			self.eventP.set()
			self.loadPic()
		print "eventP: ",self.eventP.is_set()
		
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
		
		streamName = self['liste'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamPic = self['liste'].getCurrent()[0][2]
		
		streamUrl = self['liste'].getCurrent()[0][1]
		self.getHandlung(streamUrl)
		self.updateP = 1
		if streamPic == None:
			print "ImageUrl is None !"
			self.ShowCoverNone()
		else:
			print "Download pict."
			downloadPage(streamPic, "/tmp/Icon.jpg").addCallback(self.ShowCover).addErrback(self.dataErrorP)
	
	def dataErrorP(self, error):
		print "dataError:"
		print error
		self.ShowCoverNone()
		
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
			
		m = re.findall('meta property="og:description".*?=\'(.*?)\' />', data)
		if m:
			self['handlung'].setText(decodeHtml(re.sub(r"\s+", " ", m[0])))
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
				
		self.updateP = 0;
		self.keyLocked	= False
		if not self.filmQ.empty():
			self.loadPageQueued()
		else:
			self.eventL.clear()
			self.loadPic()
	
	def keyOK(self):
		if (self.keyLocked|self.eventL.is_set()|self.eventH.is_set()):
			return

		streamLink = self['liste'].getCurrent()[0][1]
		streamName = self['liste'].getCurrent()[0][0]
		imageLink = self['liste'].getCurrent()[0][2]
		self.session.open(IStreamStreams, streamLink, streamName, imageLink)
	
	def keyUp(self):
		if self.keyLocked:
			return
		self['liste'].up()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['liste'].down()
		
	def keyUpRepeated(self):
		#print "keyUpRepeated"
		if self.keyLocked:
			return
		self['liste'].up()
		
	def keyDownRepeated(self):
		#print "keyDownRepeated"
		if self.keyLocked:
			return
		self['liste'].down()
		
	def key_repeatedUp(self):
		#print "key_repeatedUp"
		if self.keyLocked:
			return
		self.loadPicQueued()
		
	def keyLeft(self):
		if self.keyLocked:
			return
		self['liste'].pageUp()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['liste'].pageDown()
			
	def keyLeftRepeated(self):
		if self.keyLocked:
			return
		self['liste'].pageUp()
		
	def keyRightRepeated(self):
		if self.keyLocked:
			return
		self['liste'].pageDown()
			
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
		if (self.keyLocked):
			return
		if self.sortOrder and not self.neueFilme:
			self.sortOrder = 0
			self.setGenreStrTitle()
			self.loadPage()
	
	def keySortIMDB(self):
		if (self.keyLocked):
			return
		if not (self.sortOrder or self.neueFilme):
			self.sortOrder = 1
			self.setGenreStrTitle()
			self.loadPage()
	
	# teilweise von movie2k geliehen
	def keyTMDbInfo(self):
		if not self.keyLocked and TMDbPresent:
			title = self['liste'].getCurrent()[0][0]
			self.session.open(TMDbMain, title)
		elif not self.keyLocked and IMDbPresent:
			title = self['liste'].getCurrent()[0][0]
			self.session.open(IMDB, title)

	def keyTxtPageUp(self):
		self['handlung'].pageUp()
			
	def keyTxtPageDown(self):
		self['handlung'].pageDown()
			
	def keyCancel(self):
		self.close()

def IStreamStreamListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0]+entry[2])
		] 
class IStreamStreams(Screen, ConfigListScreen):
	
	def __init__(self, session, filmUrl, filmName, imageLink):
		self.session = session
		self.filmUrl = filmUrl
		self.filmName = filmName
		self.imageUrl = imageLink
		
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"
		
		path = "%s/%s/defaultListScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/defaultListScreen.xml"

		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"red" 		: self.keyTxtPageUp,
			"blue" 		: self.keyTxtPageDown,
			"ok"    	: self.keyOK,
			"cancel"	: self.keyCancel
		}, -1)
		
		self['title'] = Label(IS_Version)
		self['ContentTitle'] = Label("Stream Auswahl")
		self['coverArt'] = Pixmap()
		self['handlung'] = ScrollLabel("")
		self['name'] = Label(filmName)
		self['Page'] = Label("")
		self['page'] = Label("")
		self['F1'] = Label("Text-")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("Text+")
		
		self.streamListe = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('mediaportal', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['liste'] = self.streamMenuList
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		print "loadPage:"
		streamUrl = self.filmUrl
		#print "FilmUrl: %s" % self.filmUrl
		#print "FilmName: %s" % self.filmName
		getPage(streamUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		print "parseData:"
		streams = re.findall('a href="(.*?)".*?title=.*?\[(.*)\](.*)">', data)
		mdesc = re.search('="og:description" content=\'(.*?)\'',data)
		if mdesc:
			print "Descr. found"
			desc = mdesc.group(1)
		else:
			desc = "Keine weiteren Info's !"
				
		self.streamListe = []
		if streams:
			print "Streams found"
			for (isUrl,isStream,streamPart) in streams:
				if re.match('.*?(putlocker|sockshare|flash strea|streamclou|xvidstage|filenuke|movreel|nowvideo|xvidstream|uploadc|vreer|MonsterUploads|Novamov|Videoweed|Divxstage|Ginbig|Flashstrea|Movshare|yesload|faststream|Vidstream|PrimeShare|flashx|Divxmov|Putme|Zooupload|Click.*?Play|BitShare)', isStream, re.S|re.I):
					#print isUrl
					#print isStream,streamPart
					self.streamListe.append((isStream,isUrl,streamPart))
				else:
					print "No supported hoster:"
					print isStream
					print isUrl
		else:
			print "No Streams found"
			self.streamListe.append(("No streams found !","",""))
			
		self.streamMenuList.setList(map(IStreamStreamListEntry, self.streamListe))
		self['handlung'].setText(decodeHtml(desc))
		self.keyLocked = False			
		print "imageUrl: ",self.imageUrl
		if self.imageUrl:
			downloadPage(self.imageUrl, "/tmp/Icon.jpg").addCallback(self.ShowCover)			
	
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
		self.streamListe.append(("Read error !",""))			
		self.streamMenuList.setList(map(IStreamStreamListEntry, self.streamListe))
			
	def got_link(self, stream_url):
		print "got_link:"
		if stream_url == None:
			message = self.session.open(MessageBox, _("Stream not found, try another Stream Hoster."), MessageBox.TYPE_INFO, timeout=3)
		else:
			sref = eServiceReference(0x1001, 0, stream_url)
			sref.setName("%s%s" % (self.filmName,self['liste'].getCurrent()[0][2]))
			self.session.open(MoviePlayer, sref)
	
	def keyOK(self):
		if self.keyLocked:
			return
		streamLink = self['liste'].getCurrent()[0][1]
		fp = urllib.urlopen(streamLink.replace('http://video.istream.ws/embed.php?m=','http://istream.ws/mirror.php?m='))
		streamLink = fp.geturl()
		fp.close()
		print "get_streamLink:"
		get_stream_link(self.session).check_link(streamLink, self.got_link)
			
	def keyTxtPageUp(self):
		self['handlung'].pageUp()
			
	def keyTxtPageDown(self):
		self['handlung'].pageDown()
			
	def keyCancel(self):
		self.close()