#	-*-	coding:	utf-8	-*-

import Queue
import threading
from Plugins.Extensions.MediaPortal.resources.imports import *

CF_Version = "Clipfish.de v0.91 (experimental)"

CF_siteEncoding = 'utf-8'

"""
Sondertastenbelegung:

Genre Auswahl:
	KeyCancel	: Menu Up / Exit
	KeyOK		: Menu Down / Select
	
Doku Auswahl:
	Bouquet +/-			: Seitenweise blättern in 1er Schritten Up/Down
	'1', '4', '7',
	'3', 6', '9'		: blättern in 2er, 5er, 10er Schritten Down/Up
	Rot/Blau			: Die Beschreibung Seitenweise scrollen

Stream Auswahl:
	Rot/Blau			: Die Beschreibung Seitenweise scrollen
	Gelb				: Videopriorität 'L','M','H'

"""
def CF_menuListentry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 
		
class show_CF_Genre(Screen):

	def __init__(self, session):
		self.session = session
		self.plugin_path = mp_globals.pluginPath
		self.skin_path = mp_globals.pluginPath + "/skins"
		
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
			"cancel": self.keyCancel,
			"up"	: self.keyUp,
			"down"	: self.keyDown,
			"left"	: self.keyLeft,
			"right"	: self.keyRight,
			"red"	: self.keyRed
		}, -1)

		self['title'] = Label(CF_Version)
		self['ContentTitle'] = Label("Genre Auswahl")
		self['name'] = Label("")
		self['F1'] = Label("")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		
		self.menuLevel = 0
		self.menuMaxLevel = 1
		self.menuIdx = [0,0,0]
		self.keyLocked = True
		self.genreSelected = False
		self.menuListe = []
		self.baseUrl = "http://www.clipfish.de"
		self.genreBase = ["/kategorien", "/musikvideos/genre"]
		self.genreName = ["","","",""]
		self.genreUrl = ["","","",""]
		self.genreTitle = ""
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		
		self.genreMenu = [
			[
			("Videos", ""),
			("Musik", "")
			],
			[[
			("Eure Empfehlungen", "/28/%seure-empfehlungen"),
			("Anime & Cartoons", "/2/%sanime-cartoons"),
			("Auto", "/3/%sauto"),
			("Comedy & Humor", "/1/%scomedy-humor"),
			("Freunde & Familie", "/4/%sfreunde-familie"),
			("Games & PC", "/6/%sgames-pc"),
			("Hobbies & Tipps", "/7/%shobbies-tipps"),
			("Kino, TV & Werbung", "/8/%skino-tv-werbung"),
			("Leute & Blogs", "/9/%sleute-blogs"),
			("News & Wissenschaft", "/297/%snews-wissenschaft"),
			("Party & Events", "/13/%sparty-events"),
			("Sexy Videos", "/17/%ssexy-videos"),
			("Sport & Action", "/14/%ssport-action"),
			("Stars & Lifestyle", "/11/%sstars-lifestyle"),
			("Tiere & Natur", "/15/%stiere-natur"),
			("Urlaub & Reisen", "/16/%surlaub-reisen")
			],[
			("Country / Folk", "/207/country-folk"),
			("Dance / Elektro", "/109/dance-electro"),
			("HipHop / Rap", "/211/hip-hop-rap"),
			("Pop", "/4/pop"),
			("Gospel / Christian", "/5911/christian"),
			("World Music", "/163/world-music"),
			("Klassik", "/12/klassik"),
			("R&B / Soul", "/55/r-b-soul"),
			("Blues / Jazz", "/26/blues-jazz"),
			("Latin Music", "/247/latin"),
			("Metal / Hard Rock", "/59/metal-hard-rock"),
			("Rock / Alternative", "/119/rock-alternative"),
			("Schlager", "/38/schlager")
			]
			],
			[
			[None],
			[None]
			]
			]
			
		self.onLayoutFinish.append(self.loadMenu)
		
	def setGenreStrTitle(self):
		genreName = self['genreList'].getCurrent()[0][0]
		genreLink = self['genreList'].getCurrent()[0][1]
		if self.menuLevel in range(self.menuMaxLevel+1):
			if self.menuLevel == 0:
				self.genreName[self.menuLevel] = genreName
			else:
				self.genreName[self.menuLevel] = ':'+genreName
				
			self.genreUrl[self.menuLevel] = genreLink
		self.genreTitle = "%s%s%s" % (self.genreName[0],self.genreName[1],self.genreName[2])
		self['name'].setText("Genre: "+self.genreTitle)

	def loadMenu(self):
		print "Clipfish.de:"
		self.setMenu(0, True)
		self.keyLocked = False

	def keyRed(self):
		pass

	def keyUp(self):
		self['genreList'].up()
		self.menuIdx[self.menuLevel] = self['genreList'].getSelectedIndex()
		self.setGenreStrTitle()
		
	def keyDown(self):
		self['genreList'].down()
		self.menuIdx[self.menuLevel] = self['genreList'].getSelectedIndex()
		self.setGenreStrTitle()
		
	def keyRight(self):
		self['genreList'].pageDown()
		self.menuIdx[self.menuLevel] = self['genreList'].getSelectedIndex()
		self.setGenreStrTitle()
		
	def keyLeft(self):
		self['genreList'].pageUp()
		self.menuIdx[self.menuLevel] = self['genreList'].getSelectedIndex()
		self.setGenreStrTitle()
		
	def keyMenuUp(self):
		print "keyMenuUp:"
		if self.keyLocked:
			return
		self.menuIdx[self.menuLevel] = self['genreList'].getSelectedIndex()
		self.setMenu(-1)

	def keyOK(self):
		print "keyOK:"
		if self.keyLocked:
			return
			
		self.menuIdx[self.menuLevel] = self['genreList'].getSelectedIndex()
		self.setMenu(1)
		
		if self.genreSelected:
			print "Genre selected"
			genreurl = self.baseUrl+self.genreBase[self.menuIdx[0]]+self.genreUrl[0]+self.genreUrl[1]
			print genreurl
			self.session.open(CF_FilmListeScreen, genreurl, self.genreTitle)

	def setMenu(self, levelIncr, menuInit=False):
		print "setMenu: ",levelIncr
		self.genreSelected = False
		if (self.menuLevel+levelIncr) in range(self.menuMaxLevel+1):
			if levelIncr < 0:
				self.genreName[self.menuLevel] = ""
			
			self.menuLevel += levelIncr
			
			if levelIncr > 0 or menuInit:
				self.menuIdx[self.menuLevel] = 0
			
			if self.menuLevel == 0:
				print "level-0"
				if self.genreMenu[0] != None:
					self.menuListe = []
					for (Name,Url) in self.genreMenu[0]:
						self.menuListe.append((Name,Url))
					self.chooseMenuList.setList(map(CF_menuListentry, self.menuListe))
					self['genreList'].moveToIndex(self.menuIdx[0])
				else:
					self.genreName[self.menuLevel] = ""
					self.genreUrl[self.menuLevel] = ""
					print "No menu entrys!"
			elif self.menuLevel == 1:
				print "level-1"
				if self.genreMenu[1][self.menuIdx[0]] != None:
					self.menuListe = []
					for (Name,Url) in self.genreMenu[1][self.menuIdx[0]]:
						self.menuListe.append((Name,Url))
					self.chooseMenuList.setList(map(CF_menuListentry, self.menuListe))
					self['genreList'].moveToIndex(self.menuIdx[1])
				else:
					self.genreName[self.menuLevel] = ""
					self.genreUrl[self.menuLevel] = ""
					self.menuLevel -= levelIncr
					self.genreSelected = True
					print "No menu entrys!"
			elif self.menuLevel == 2:
				print "level-2"
				if self.genreMenu[2][self.menuIdx[0]][self.menuIdx[1]] != None:
					self.menuListe = []
					for (Name,Url) in self.genreMenu[2][self.menuIdx[0]][self.menuIdx[1]]:
						self.menuListe.append((Name,Url))
					self.chooseMenuList.setList(map(CF_menuListentry, self.menuListe))
					self['genreList'].moveToIndex(self.menuIdx[2])
				else:
					self.genreName[self.menuLevel] = ""
					self.genreUrl[self.menuLevel] = ""
					self.menuLevel -= levelIncr
					self.genreSelected = True
					print "No menu entrys!"
		else:
			print "Entry selected"
			self.genreSelected = True
				
		print "menuLevel: ",self.menuLevel
		print "mainIdx: ",self.menuIdx[0]
		print "subIdx_1: ",self.menuIdx[1]
		print "subIdx_2: ",self.menuIdx[2]
		print "genreSelected: ",self.genreSelected
		print "menuListe: ",self.menuListe
		print "genreUrl: ",self.genreUrl
		
		self.setGenreStrTitle()		
		
	def keyCancel(self):
		if self.menuLevel == 0:
			self.close()
		else:
			self.keyMenuUp()
	

def CF_FilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
class CF_FilmListeScreen(Screen):
	
	def __init__(self, session, genreLink, genreName):
		self.session = session
		self.genreLink = genreLink
		self.genreName = genreName
		self.plugin_path = mp_globals.pluginPath
		self.skin_path = mp_globals.pluginPath + "/skins"

		path = "%s/%s/dokuListScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/dokuListScreen.xml"
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
			"blue" :  self.keyTxtPageDown,
			"red" :  self.keyTxtPageUp
		}, -1)

		self.sortOrder = 0
		self.baseUrl = "http://www.clipfish.de"
		self.genreTitle = "Titel in Genre "
		self.sortParIMDB = ""
		self.sortParAZ = ""
		self.sortOrderStrAZ = ""
		self.sortOrderStrIMDB = ""
		self.sortOrderStrGenre = ""
		self['title'] = Label(CF_Version)
		self['ContentTitle'] = Label("")
		self['name'] = Label("")
		self['handlung'] = ScrollLabel("")
		self['page'] = Label("")
		self['F1'] = Label("Text-")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("Text+")
		self['VideoPrio'] = Label("")
		self['vPrio'] = Label("")
		self['Page'] = Label("Page")
		self['coverArt'] = Pixmap()
		
		self.timerStart = False
		self.seekTimerRun = False
		self.filmQ = Queue.Queue(0)
		self.eventL = threading.Event()
		self.keyLocked = True
		self.musicListe = []
		self.keckse = {}
		self.page = 0
		self.pages = 0;
		self.genreSpecials = False
		self.genreVideos = re.match('.*?Videos', self.genreName)

		self.setGenreStrTitle()
		
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['liste'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)

	def setGenreStrTitle(self):
		genreName = "%s%s" % (self.genreTitle,self.genreName)
		#print genreName
		self['ContentTitle'].setText(genreName)

	def loadPage(self):
		print "loadPage:"
		if not self.genreVideos:
			url = "%s/beste/%d/#" % (self.genreLink, self.page)
		else:
			link = self.genreLink % 'neu/'
			url = "%s/%d/" % (link, self.page)
			
		if self.page:
			self['page'].setText("%d / %d" % (self.page,self.pages))
			
		self.filmQ.put(url)
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
		getPage(url, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		self.eventL.clear()
		print "dataError:"
		print error
		self['handlung'].setText("Fehler:\n" + str(error))
		
	def loadPageData(self, data):
		print "loadPageData:"
		a = 0
		l = len(data)
		self.musicListe = []
		while a < l:
			mg = re.search('<li id="cf-video-item_(.*?)</li>', data[a:], re.S)
			if mg:
				a += mg.end()
				m1 = re.search('href="(.*?)".*?title="(.*?)">.*?<img.*?src="(.*?)"', mg.group(1), re.S)
				if m1:
					title = decodeHtml(m1.group(2))
					url = m1.group(1)
					img = m1.group(3)
					
					self.musicListe.append((title, "%s%s" % (self.baseUrl, url), img))
			else:
				a = l
				
		if len(self.musicListe) == 0:
			print "No videos found!"
			self.pages = 0
			self.musicListe.append(('Keine Videos gefunden !','',''))
		else:
			menu_len = len(self.musicListe)
			print "Music videos found: ",menu_len
	
			if not self.pages:
				m1 = re.search('class="cf-page-stepper">(.*?)</div>', data, re.S)
				if m1:
					m2 = re.findall('">(\d*?)</a>', m1.group(1))
					
				if m1 and m2:
					pages = 0
					for i in m2:
						x = int(i)
						if x > pages:
							pages = x
					
					if pages > 999:
						self.pages = 999
					else:
						self.pages = pages
				else:
					self.pages = 1
					
				self.page = 1
				print "Page: %d / %d" % (self.page,self.pages)
				self['page'].setText("%d / %d" % (self.page,self.pages))
	
		self.chooseMenuList.setList(map(CF_FilmListEntry, self.musicListe))
		self.loadPic()
	
	def loadPic(self):
		print "loadPic:"
		streamName = self['liste'].getCurrent()[0][0]
		self['name'].setText(streamName)
		desc = None
		print "streamName: ",streamName
		#print "streamUrl: ",streamUrl
		self.getHandlung(desc)
		
		if not self.filmQ.empty():
			self.loadPageQueued()
		else:
			self.eventL.clear()
		self.keyLocked	= False
		
		url = self['liste'].getCurrent()[0][2]
		if url != '':
			downloadPage(url, "/tmp/Icon.jpg").addCallback(self.ShowCover).addErrback(self.dataError)
		else:
			self.ShowCoverNone()
		
	def getHandlung(self, desc):
		print "getHandlung:"
		if desc == None:
			print "No Infos found !"
			self['handlung'].setText("Keine weiteren Info's vorhanden.")
			return
		self.setHandlung(desc)
		
	def setHandlung(self, data):
		print "setHandlung:"
		self['handlung'].setText(decodeHtml(data))

	def getVid(self, data):
		print "getVid: "
		if not self.genreVideos:
			m = re.search('NAME="FlashVars".*?data=(.*?)&amp', data)
		else:
			m = re.search('data: "(.*?)"', data, re.S)
			
		if m:
			url = self.baseUrl + m.group(1)
			getPage(url, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getXml).addErrback(self.dataError)
		else:
			print "No xml data found!"
			self.dataError('No video data found!')
	
	def getXml(self, data):
		print "getXml:"
		url = None
		if not self.genreVideos:
			print "musik url:"
			m = re.search('<filename>.*?ondemand/(.*?):(.*?)\?', data)
			if m:
				url = 'http://video.clipfish.de/' + m.group(2) + '.' + m.group(1)
		else:
			print "film url:"
			#print "data: ",data
			m = re.search('<filename>.*?clipfish.de/(.*?)(flv|f4v|mp4).*?</filename>', data, re.S)
			if m:
				print "m: ",m.group(1)
				url = 'http://video.clipfish.de/' + m.group(1) + m.group(2)
		
		if url != None:
			self.playVid(url)
		else:
			print "No video url found!"
			self.dataError('No video data found!')
	
	def playVid(self, url):
		print "playVid: ",url
		title = self['liste'].getCurrent()[0][0]
		sref = eServiceReference(0x1001, 0, url)
		sref.setName(title)
		self.session.open(MoviePlayer, sref)
		
	def ShowCover(self, picData):
		print "ShowCover:"
		picPath = "/tmp/Icon.jpg"
		self.ShowCoverFile(picPath)
		
	def ShowCoverNone(self):
		print "ShowCoverNone:"
		picPath = self.plugin_path + "/images/no_coverArt.png"
		self.ShowCoverFile(picPath)
	
	def ShowCoverFile(self, picPath):
		print "showCoverFile:"
		if fileExists(picPath):
			print "picpath: ",picPath
			self['coverArt'].instance.setPixmap(None)
			#self['coverArt'].instance.setPixmap(enigma.gPixmapPtr())
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
		if (self.keyLocked|self.eventL.is_set()):
			return
		url = self['liste'].getCurrent()[0][1]
		print "keyOK: ", len(url), ',', url
		getPage(url, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getVid).addErrback(self.dataError)
	
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
		self.loadPic()
		
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
			self.page = 1
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
			self.page = self.pages
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

	def keyTxtPageUp(self):
		self['handlung'].pageUp()
			
	def keyTxtPageDown(self):
		self['handlung'].pageDown()
			
	def keyCancel(self):
		self.close()

