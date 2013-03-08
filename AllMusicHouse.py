#	-*-	coding:	utf-8	-*-

from imports import *
from decrypt import *
import Queue
import threading

AMH_Version = "AllMusicHouse.de v0.92"

AMH_siteEncoding = 'utf-8'

"""
Sondertastenbelegung:

Genre Auswahl:
	KeyLeft: 			Menu Up
	KeyOK,KeyRight:		Menu Down / Select
	
Doku Auswahl:
	Bouquet +/-, Rot/Blau	: Seitenweise blättern in 1er Schritten Up/Down
	'1', '4', '7',
	'3', 6', '9'			: blättern in 2er, 5er, 10er Schritten Down/Up

"""
def AMH_menuListentry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 
		
#class show_AMH_Genre(Screen):
class show_AMH_Genre(Screen):

	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/show_AMH_Genre.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/show_AMH_Genre.xml"
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
			"left"	: self.keyMenuUp,
			"right"	: self.keyOK,
			"red"	: self.keyRed
		}, -1)

		self['title'] = Label(AMH_Version)
		self['ContentTitle'] = Label("Musik Auswahl")
		self['name'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.menuLevel = 0
		self.menuMaxLevel = 0
		self.menuIdx = [0,0,0]
		self.keyLocked = True
		self.genreSelected = False
		self.menuListe = []
		self.baseUrl = "http://www.allmusichouse.de"
		self.genreBase = "/category"
		self.genreName = ["","","",""]
		self.genreUrl = ["","","",""]
		self.genreTitle = ""
		#self.subMenu = []
		#self.keckse = {}
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		mainGenre = [
			("0-9", "/0-9"),
			("A-B", "/a-c"),
			("C-D", "/d-f"),
			("E-F", "/g-i"),
			("G-H", "/j-l"),
			("I-J", "/m-o"),
			("K-L", "/p-r"),
			("M-N", "/s-u"),
			("O-P-Q", "/v-z"),
			("R-S", "/r-s"),
			("T-U", "/t-u"),
			("V-W", "/v-w"),
			("X-Y-Z", "/x-y-z"),
			]
			
		self.genreMenu = [mainGenre,
			[None],
			[
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
		self['name'].setText("Auswahl: "+self.genreTitle)

	def loadMenu(self):
		print "AllMusicHouse.de:"
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
			genreurl = self.baseUrl+self.genreBase+self.genreUrl[0]+self.genreUrl[1]
			print genreurl
			self.session.open(AMH_FilmListeScreen, genreurl, self.genreTitle)

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
					self.chooseMenuList.setList(map(AMH_menuListentry, self.menuListe))
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
					self.chooseMenuList.setList(map(AMH_menuListentry, self.menuListe))
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
					self.chooseMenuList.setList(map(AMH_menuListentry, self.menuListe))
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
		self.close()
	

def AMH_FilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
class AMH_FilmListeScreen(Screen):
	
	def __init__(self, session, genreLink, genreName):
		self.session = session
		self.genreLink = genreLink
		self.genreName = genreName
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/AMH_FilmListeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/AMH_FilmListeScreen.xml"
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
			"blue" :  self.keyPageUp,
			"red" :  self.keyPageDown
			#"seekBackManual" :  self.keyPageDownMan,
			#"seekFwdManual" :  self.keyPageUpMan,
			#"seekFwd" :  self.keyPageUp,
			#"seekBack" :  self.keyPageDown
		}, -1)

		self.sortOrder = 0
		self.baseUrl = "http://www.allmusichouse.de"
		self.genreTitle = "Musik in Auswahl "
		self.sortParIMDB = ""
		self.sortParAZ = ""
		self.sortOrderStrAZ = ""
		self.sortOrderStrIMDB = ""
		self.sortOrderStrGenre = ""
		self['title'] = Label(AMH_Version)
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
		self.eventP = threading.Event()
		self.keyLocked = True
		self.musicListe = []
		self.keckse = {}
		self.page = 0
		self.pages = 0;
		self.genreSpecials = False

		self.setGenreStrTitle()
		
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)

	def setGenreStrTitle(self):
		genreName = "%s%s" % (self.genreTitle,self.genreName)
		#print genreName
		self['leftContentTitle'].setText(genreName)

	def loadPage(self):
		print "loadPage:"
		#if not self.genreSpecials:
		url = "%s/page/%d/" % (self.genreLink, self.page)
		#else:
		#	url = 
			
		if self.page:
			self['page'].setText("%d / %d" % (self.page,self.pages))
			
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
		self.musicListe.append(("No music found !","","",""))
		self.chooseMenuList.setList(map(AMH_FilmListEntry, self.musicListe))
		
	def loadPageData(self, data):
		print "loadPageData:"
		
		if self.genreSpecials:
			print "Specials Dokus suche..."
			m=re.search('<div id="content">(.*?)<!-- #content -->',data,re.S)
		else:
			print "Normal search.."
			m=re.search('<div id="content">(.*?)<!-- #content -->',data,re.S)
			
		if m:
			music = re.findall('<h2 class="title"><a href="(.*?)".*?rel="bookmark">(.*?)</a>.*?class="entry clearfix">'\
								'.*?<p>(.*?)</p>', m.group(1), re.S)
		else:
			music = None
		
		if music:
			print "Music found !"
			if not self.pages:
				m = re.findall('class=\'pages\'>Seite.*?von (.*?)</', data)
				if m:
					self.pages = int(m[0])
				else:
					self.pages = 1
				self.page = 1
				print "Page: %d / %d" % (self.page,self.pages)
				self['page'].setText("%d / %d" % (self.page,self.pages))
			
			self.musicListe = []
			for	(url,name,desc) in music:
				#print	"Url: ", url, "Name: ", name
				self.musicListe.append((decodeHtml(name), url, desc.lstrip().rstrip()))
			self.chooseMenuList.setList(map(AMH_FilmListEntry, self.musicListe))
			
			self.loadPicQueued()
		else:
			print "No music found !"
			self.musicListe.append(("No music found !","",""))
			self.chooseMenuList.setList(map(AMH_FilmListEntry, self.musicListe))
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
		
		if self.updateP:
			print "Pict. or descr. update in progress"
			print "eventP: ",self.eventP.is_set()
			print "updateP: ",self.updateP
			return
			
		while not self.picQ.empty():
			self.picQ.get_nowait()
		
		streamName = self['filmList'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamPic = None
		#streamUrl = self.baseUrl+re.sub('amp;','',self['filmList'].getCurrent()[0][1])
		desc = self['filmList'].getCurrent()[0][2]
		#print "streamName: ",streamName
		#print "streamPic: ",streamPic
		#print "streamUrl: ",streamUrl
		self.getHandlung(desc)
		self.updateP = 1
		if streamPic == None:
			print "ImageUrl is None !"
			self.ShowCoverNone()
		else:
			print "Download pict."
			#print "Url: ",streamPic
			downloadPage(streamPic, "/tmp/Icon.jpg").addCallback(self.ShowCover).addErrback(self.dataErrorP)
		
	def dataErrorP(self, error):
		print "dataError:"
		print error
		self.ShowCoverNone()
		
	def getHandlung(self, desc):
		print "getHandlung:"
		if desc == None:
			print "No Infos found !"
			self['handlung'].setText("Keine infos gefunden.")
			return
		self.setHandlung(desc)
		
	def setHandlung(self, data):
		print "setHandlung:"
		self['handlung'].setText(decodeHtml(data))
		
	def ShowCover(self, picData):
		print "ShowCover:"
		picPath = "/tmp/Icon.jpg"
		self.ShowCoverFile(picPath)
		
	def ShowCoverNone(self):
		print "ShowCoverNone:"
		picPath = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png"
		self.ShowCoverFile(picPath)
	
	def ShowCoverFile(self, picPath):
		print "showCoverFile:"
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
		if (self.keyLocked|self.eventL.is_set()):
			return

		streamLink = self['filmList'].getCurrent()[0][1]
		streamName = self['filmList'].getCurrent()[0][0]
		print "Open AMH_Streams:"
		print "Name: ",streamName
		print "Link: ",streamLink
		self.session.open(AMH_Streams, streamLink, streamName)
	
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

	def keyCancel(self):
		self.close()

def AMH_StreamListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
class AMH_Streams(Screen, ConfigListScreen):
	
	def __init__(self, session, dokuUrl, dokuName):
		self.session = session
		self.dokuUrl = dokuUrl
		self.dokuName = dokuName
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/AMH_Streams.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/AMH_Streams.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)
		
		self['title'] = Label(AMH_Version)
		self['ContentTitle'] = Label("Streams für "+dokuName)
		self['coverArt'] = Pixmap()
		self['handlung'] = Label("")
		self['name'] = Label(dokuName)
		
		self.streamListe = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamList'] = self.streamMenuList
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		print "loadPage:"
		streamUrl = self.dokuUrl
		#print "FilmUrl: %s" % self.dokuUrl
		#print "FilmName: %s" % self.dokuName
		getPage(streamUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		print "parseData:"
		#http://www.youtube.com/(embed|v)/3NDBxP2MEHw?
		m = re.search('"http://www.youtube.com/(embed|v)/(.*?)("|\?).*?data-text="(.*?)"', data, re.S)
		parts = re.search('<p>Part 1 von (.*?)<br', data)
		self.streamListe = []
		#if streams:
		if m:
			print "Streams found"
			desc = ""
			#for (videoTag,title) in streams:
			if parts:
				self.nParts = int(parts.group(1))
				pstr = " [1/%d]" % self.nParts
			else:
				self.nParts = 0
				pstr = ""
				
			self.streamListe.append((decodeHtml(m.group(4))+pstr,m.group(2),desc))
		else:
			print "No music found !"
			self.streamListe.append(("No streams found !","",""))
		self.streamMenuList.setList(map(AMH_StreamListEntry, self.streamListe))
		self.loadPic()
		
	def getHandlung(self, desc):
		print "getHandlung:"
		if desc == None:
			print "No Infos found !"
			self['handlung'].setText("Keine infos gefunden.")
			return
		self.setHandlung(desc)
		
	def setHandlung(self, data):
		print "setHandlung:"
		self['handlung'].setText(decodeHtml(data))
		
	def loadPic(self):
		print "loadPic:"
		streamName = self['streamList'].getCurrent()[0][0]
		self['name'].setText(streamName)
		#streamPic = self['streamList'].getCurrent()[0][2]
		streamPic = None
		desc = self['streamList'].getCurrent()[0][2]
		print "streamName: ",streamName
		print "streamPic: ",streamPic
		self.getHandlung(desc)
		if streamPic == None:
			print "ImageUrl is None !"
			self.ShowCoverNone()
		else:
			print "Download pict."
			print "Url: ",streamPic
			downloadPage(streamPic, "/tmp/Icon.jpg").addCallback(self.ShowCover).addErrback(self.dataErrorP)
		
	def dataErrorP(self, error):
		print "dataErrorP:"
		print error
		self.ShowCoverNone()
	
	def ShowCover(self, picData):
		print "ShowCover:"
		picPath = "/tmp/Icon.jpg"
		self.ShowCoverFile(picPath)
		
	def ShowCoverNone(self):
		print "ShowCoverNone:"
		picPath = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png"
		self.ShowCoverFile(picPath)
	
	def ShowCoverFile(self, picPath):
		print "showCoverFile:"
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
		self.keyLocked	= False
			
	def dataError(self, error):
		print "dataError:"
		print error
		self.streamListe.append(("Read error !","",""))			
		self.streamMenuList.setList(map(AMH_StreamListEntry, self.streamListe))
			
	# code von doku.me geliehen
	def getVideoUrl(self, url):
		# this part is from mtube plugin
		print "got url:", url
		"""
		VIDEO_FMT_PRIORITY_MAP = {
			'38' : 1, #MP4 Original (HD)
			'37' : 2, #MP4 1080p (HD)
			'22' : 3, #MP4 720p (HD)
			'18' : 4, #MP4 360p
			'35' : 5, #FLV 480p
			'34' : 6, #FLV 360p
		}
		"""
		VIDEO_FMT_PRIORITY_MAP = {
			'38' : 3, #MP4 Original (HD)
			'37' : 4, #MP4 1080p (HD)
			'22' : 2, #MP4 720p (HD)
			'18' : 5, #MP4 360p
			'35' : 1, #FLV 480p
			'34' : 6, #FLV 360p
		}
		video_url = None
		video_id = url

		# Getting video webpage
		#URLs for YouTube video pages will change from the format http://www.youtube.com/watch?v=ylLzyHk54Z0 to http://www.youtube.com/watch#!v=ylLzyHk54Z0.
		watch_url = 'http://www.youtube.com/watch?v=%s&gl=US&hl=en' % video_id
		watchrequest = Request(watch_url, None, std_headers)
		try:
			print "[MyTube] trying to find out if a HD Stream is available",watch_url
			watchvideopage = urlopen2(watchrequest).read()
		except (URLError, HTTPException, socket.error), err:
			print "[MyTube] Error: Unable to retrieve watchpage - Error code: ", str(err)
			print "test", video_url

		# Get video info
		for el in ['&el=embedded', '&el=detailpage', '&el=vevo', '']:
			info_url = ('http://www.youtube.com/get_video_info?&video_id=%s%s&ps=default&eurl=&gl=US&hl=en' % (video_id, el))
			request = Request(info_url, None, std_headers)
			try:
				infopage = urlopen2(request).read()
				videoinfo = parse_qs(infopage)
				if ('url_encoded_fmt_stream_map' or 'fmt_url_map') in videoinfo:
					break
			except (URLError, HTTPException, socket.error), err:
				print "[MyTube] Error: unable to download video infopage",str(err)
				return video_url

		if ('url_encoded_fmt_stream_map' or 'fmt_url_map') not in videoinfo:
			# Attempt to see if YouTube has issued an error message
			if 'reason' not in videoinfo:
				print '[MyTube] Error: unable to extract "fmt_url_map" or "url_encoded_fmt_stream_map" parameter for unknown reason'
			else:
				reason = unquote_plus(videoinfo['reason'][0])
				print '[MyTube] Error: YouTube said: %s' % reason.decode('utf-8')
			print video_url

		video_fmt_map = {}
		fmt_infomap = {}
		if videoinfo.has_key('url_encoded_fmt_stream_map'):
			tmp_fmtUrlDATA = videoinfo['url_encoded_fmt_stream_map'][0].split(',')
		else:
			tmp_fmtUrlDATA = videoinfo['fmt_url_map'][0].split(',')
		for fmtstring in tmp_fmtUrlDATA:
			fmturl = fmtid = fmtsig = ""
			if videoinfo.has_key('url_encoded_fmt_stream_map'):
				try:
					for arg in fmtstring.split('&'):
						if arg.find('=') >= 0:
							print arg.split('=')
							key, value = arg.split('=')
							if key == 'itag':
								if len(value) > 3:
									value = value[:2]
								fmtid = value
							elif key == 'url':
								fmturl = value
							elif key == 'sig':
								fmtsig = value
								
					if fmtid != "" and fmturl != "" and fmtsig != ""  and VIDEO_FMT_PRIORITY_MAP.has_key(fmtid):
						video_fmt_map[VIDEO_FMT_PRIORITY_MAP[fmtid]] = { 'fmtid': fmtid, 'fmturl': unquote_plus(fmturl), 'fmtsig': fmtsig }
						fmt_infomap[int(fmtid)] = "%s&signature=%s" %(unquote_plus(fmturl), fmtsig)
					fmturl = fmtid = fmtsig = ""

				except:
					print "error parsing fmtstring:",fmtstring
					
			else:
				(fmtid,fmturl) = fmtstring.split('|')
			if VIDEO_FMT_PRIORITY_MAP.has_key(fmtid) and fmtid != "":
				video_fmt_map[VIDEO_FMT_PRIORITY_MAP[fmtid]] = { 'fmtid': fmtid, 'fmturl': unquote_plus(fmturl) }
				fmt_infomap[int(fmtid)] = unquote_plus(fmturl)
		print "[MyTube] got",sorted(fmt_infomap.iterkeys())
		if video_fmt_map and len(video_fmt_map):
			print "[MyTube] found best available video format:",video_fmt_map[sorted(video_fmt_map.iterkeys())[0]]['fmtid']
			best_video = video_fmt_map[sorted(video_fmt_map.iterkeys())[0]]
			video_url = "%s&signature=%s" %(best_video['fmturl'].split(';')[0], best_video['fmtsig'])
			print "[MyTube] found best available video url:",video_url

		return video_url
		
	def keyOK(self):
		print "keyOK:"
		if self.keyLocked:
			return
		dhTitle = self['streamList'].getCurrent()[0][0]
		dhVideoId = self['streamList'].getCurrent()[0][1]
		print "Title: ",dhTitle
		print "VideoId: ",dhVideoId
		dhLink = self.getVideoUrl(dhVideoId)
		if dhLink:
			print dhLink
			sref = eServiceReference(0x1001, 0, dhLink)
			sref.setName(dhTitle)
			self.session.open(MoviePlayer, sref)
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['streamList'].up()
		self.loadPic()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['streamList'].down()
		self.loadPic()
		
	def keyLeft(self):
		if self.keyLocked:
			return
		self['streamList'].pageUp()
		self.loadPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['streamList'].pageDown()
		self.loadPic()
	
	def keyCancel(self):
		self.close()
		