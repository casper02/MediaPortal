#	-*-	coding:	utf-8	-*-

from Plugins.Extensions.mediaportal.resources.imports import *
from Plugins.Extensions.mediaportal.resources.decrypt import *
from Plugins.Extensions.mediaportal.resources.yt_url import *
import Queue
import threading
from Components.ScrollLabel import ScrollLabel

DH_Version = "DokuHouse.de v0.94"

DH_siteEncoding = 'utf-8'

"""
Sondertastenbelegung:

Genre Auswahl:
	KeyCancel	: Menu Up / Exit
	KeyOK		: Menu Down / Select
	
Doku Auswahl:
	Bouquet +/-				: Seitenweise blättern in 1er Schritten Up/Down
	'1', '4', '7',
	'3', 6', '9'			: blättern in 2er, 5er, 10er Schritten Down/Up
	Rot/Blau				: Die Beschreibung Seitenweise scrollen

Stream Auswahl:
	Rot/Blau				: Die Beschreibung Seitenweise scrollen
	Gelb					: Videopriorität 'L','M','H'
"""
def DH_menuListentry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 
		
#class show_DH_Genre(Screen):
class show_DH_Genre(Screen):

	def __init__(self, session):
		self.session = session
		
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
			"cancel": self.keyCancel,
			"up"	: self.keyUp,
			"down"	: self.keyDown,
			"left"	: self.keyLeft,
			"right"	: self.keyRight,
			"red"	: self.keyRed
		}, -1)

		self['title'] = Label(DH_Version)
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
		self.baseUrl = "http://www.dokuhouse.de"
		self.genreBase = "/category"
		self.genreName = ["","","",""]
		self.genreUrl = ["","","",""]
		self.genreTitle = ""
		#self.subMenu = []
		#self.keckse = {}
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.genreMenu = [
			[
			("*Specials", "/language"),
			("Geschichte", "/geschichte"),
			("Gesellschaft", "/gesellschaft"),
			("Kriminalität", "/kriminalitat"),
			("Medien", "/medien"),
			("Politik", "/politik"),
			("Technologie", "/technologie"),
			("Umwelt", "/umwelt"),
			("Wissenschaft", "/wissenschaft")
			],
			[
			#subGenre_0 = 
			[
			("Aktenzeichen XY", "/aktenzeichen-xy-spezial"),
			("Ancient Aliens", "/ancient-aliens-spezial"),
			("Da wird mir übel", "/da-wird-mir-ubel-spezial"),
			("Die Deutschen", "/die-deutschen-spezial"),
			("Die großen Kriminalfälle", "/die-grosen-kriminalfalle-spezial"),
			("Die Stone-Skala", "/die-stone-skala-spezial"),
			("Drogen im Visier", "/drogen-im-visier-special"),
			("Hotdokus", "/hotdokus"),
			("Junior Docs", "/junior-docs-special"),
			("Medical Detectives", "/medical-detectives"),
			("Mysteriöse Todesfälle", "/mysteriose-todesfalle-spezial"),
			("Nicht nachmachen!", "/nicht-nachmachen-spezial"),
			("Österreich II", "/osterreich-ii"),
			("UFO Jäger", "/ufo-jager"),
			("Unser Universum", "/unser-universum-spezial"),
			("Wunder des Weltalls", "/wunder-des-weltalls-spezial"),
			("Zukunft ohne Menschen", "/zukunft-ohne-menschen")
			],
			#subGenre_1 = 
			[
			("Antike", "/antike"),
			("DDR", "/ddr"),
			("International", "/international"),
			("Irakkrieg", "/irakkrieg"),
			("Kriege", "/kriege"),
			("Mittelalter", "/mittelalter"),
			("National", "/national"),
			("Tschernobyl", "/tschernobyl"),
			("Vietnamkrieg", "/vietnamkrieg"),
			("Weltkrieg I", "/weltkrieg-i"),
			("Weltkrieg II", "/weltkrieg-ii")
			],
			#subGenre_2 = 
			[
			("Drogen", "/drogen"),
			("Ernährung", "/ernahrung"),
			("Gesundheit", "/gesundheit"),
			("Konsum", "/konsum"),
			("Lebensretter", "/lebensretter"),
			("Menschen", "/menschen-gesellschaft"),
			("Militär", "/militar"),
			("Religion", "/religion"),
			("Sexualität", "/sexualitat"),
			("Sport", "/sport")
			],
			#subGenre_3 = 
			[
			("Banden", "/banden"),
			("Gesetzeshüter", "/gesetzeshuter"),
			("Kriminalfälle", "/kriminalfalle-allgemein"),
			("Serienmörder", "/serienmorder"),
			("Strafanstalten", "/strafanstalten")
			],
			#subGenre_4 = 
			[
			("Games", "/games"),
			("Internet", "/internet"),
			("Kunst", "/kunst"),
			("Musik", "/musik"),
			("Television", "/television")
			],
			#subGenre_5 = 
			[
			("9/11", "/911"),
			("Linksextremismus", "/linksextremismus"),
			("Rechtsextremismus", "/rechtsextremismus"),
			("Revolution", "/revolution"),
			("Verschwörungen", "/verschworungen"),
			("Wirtschaft", "/wirtschaft")
			],
			#subGenre_6 = 
			[
			("Technik", "/technik"),
			("Verkehrsmittel", "/verkehrsmittel"),
			("Waffen", "/waffen-technologie")
			],
			#subGenre_7 = 
			[
			("Architektur", "/architektur"),
			("Erdkunde", "/erdkunde"),
			("Mystery", "/mystery"),
			("Natur", "/natur"),
			("Tiere", "/tiere")
			],
			#subGenre_8 = 
			[
			("Ägyptologie", "/agyptologie"),
			("Archäologie", "/archaologie"),
			("Astronomie", "/astronomie"),
			("Evolution", "/evolution"),
			("Hochkulturen", "/hochkulturen"),
			("Medizin", "/medizin-wissenschaft"),
			("Physik", "/physik"),
			("Ufologie", "/ufologie")
			]
			],
			[
			#subGenre_0_0
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
		print "DOKUHOUSE.de:"
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

	def keyRight(self):
		self['genreList'].pageDown()
		self.menuIdx[self.menuLevel] = self['genreList'].getSelectedIndex()
		self.setGenreStrTitle()
		
	def keyLeft(self):
		self['genreList'].pageUp()
		self.menuIdx[self.menuLevel] = self['genreList'].getSelectedIndex()
		self.setGenreStrTitle()
		
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
			self.session.open(DH_FilmListeScreen, genreurl, self.genreTitle)

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
					self.chooseMenuList.setList(map(DH_menuListentry, self.menuListe))
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
					self.chooseMenuList.setList(map(DH_menuListentry, self.menuListe))
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
					self.chooseMenuList.setList(map(DH_menuListentry, self.menuListe))
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
	

def DH_FilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
class DH_FilmListeScreen(Screen):
	
	def __init__(self, session, genreLink, genreName):
		self.session = session
		self.genreLink = genreLink
		self.genreName = genreName
		
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"
		
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
			#"seekBackManual" :  self.keyPageDownMan,
			#"seekFwdManual" :  self.keyPageUpMan,
			#"seekFwd" :  self.keyPageUp,
			#"seekBack" :  self.keyPageDown
		}, -1)

		self.sortOrder = 0
		self.baseUrl = "http://www.dokuhouse.de"
		self.genreTitle = "Dokus in Genre "
		self.sortParIMDB = ""
		self.sortParAZ = ""
		self.sortOrderStrAZ = ""
		self.sortOrderStrIMDB = ""
		self.sortOrderStrGenre = ""
		self['title'] = Label(DH_Version)
		self['ContentTitle'] = Label("")
		self['name'] = Label("")
		self['handlung'] = ScrollLabel("")
		self['coverArt'] = Pixmap()
		self['page'] = Label("")
		self['F1'] = Label("Text-")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("Text+")
		self['Page'] = Label("Page")
		self['VideoPrio'] = Label("")
		self['vPrio'] = Label("")
		
		self.timerStart = False
		self.seekTimerRun = False
		self.filmQ = Queue.Queue(0)
		self.hanQ = Queue.Queue(0)
		self.picQ = Queue.Queue(0)
		self.updateP = 0
		self.eventL = threading.Event()
		self.eventP = threading.Event()
		self.keyLocked = True
		self.dokusListe = []
		self.keckse = {}
		self.page = 0
		self.pages = 0;
		self.genreSpecials = re.match('.*?\*SPECIALS',self.genreName)

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
		self.dokusListe.append(("No dokus found !","","",""))
		self.chooseMenuList.setList(map(DH_FilmListEntry, self.dokusListe))
		
	def loadPageData(self, data):
		print "loadPageData:"
		
		if self.genreSpecials:
			print "Specials Dokus suche..."
			m=re.search('<div id="content">(.*?)<!-- #content -->',data,re.S)
		else:
			print "Normal search.."
			m=re.search('<div id="content">(.*?)<!-- #content -->',data,re.S)
			
		if m:
			dokus = re.findall('<div class="featured-.*?<a href="(.*?)"><img.*?src="(.*?)".*?title='\
								'"(.*?)" />.*?<p>(.*?)</p>', m.group(1), re.S)
		else:
			dokus = None
		
		if dokus:
			print "Dokus found !"
			if not self.pages:
				m = re.findall('class=\'pages\'>Seite.*?von (.*?)</', data)
				if m:
					self.pages = int(m[0])
				else:
					self.pages = 1
				self.page = 1
				print "Page: %d / %d" % (self.page,self.pages)
				self['page'].setText("%d / %d" % (self.page,self.pages))
			
			self.dokusListe = []
			for	(url,img,name,desc) in dokus:
				#print	"Url: ", url, "Name: ", name
				self.dokusListe.append((decodeHtml(name), url, img, desc.lstrip().rstrip()))
			self.chooseMenuList.setList(map(DH_FilmListEntry, self.dokusListe))
			
			self.loadPicQueued()
		else:
			print "No dokus found !"
			self.dokusListe.append(("No dokus found !","","",""))
			self.chooseMenuList.setList(map(DH_FilmListEntry, self.dokusListe))
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
		
		streamName = self['liste'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamPic = self['liste'].getCurrent()[0][2]
		#streamUrl = self.baseUrl+re.sub('amp;','',self['liste'].getCurrent()[0][1])
		desc = self['liste'].getCurrent()[0][3]
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

		streamLink = self['liste'].getCurrent()[0][1]
		streamName = self['liste'].getCurrent()[0][0]
		print "Open DH_Streams:"
		print "Name: ",streamName
		print "Link: ",streamLink
		self.session.open(DH_Streams, streamLink, streamName)
	
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

def DH_StreamListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
class DH_Streams(Screen, ConfigListScreen):
	
	def __init__(self, session, dokuUrl, dokuName):
		self.session = session
		self.dokuUrl = dokuUrl
		self.dokuName = dokuName
		
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"
		
		path = "%s/%s/dokuListScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/dokuListScreen.xml"

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
			"left" : self.keyLeft,
			"yellow"	: self.keyYellow,
			"red" : self.keyPageUp,
			"blue" : self.keyPageDown,
		}, -1)
		
		self['title'] = Label(DH_Version)
		self['ContentTitle'] = Label("Streams für "+dokuName)
		self['handlung'] = ScrollLabel("")
		self['name'] = Label(self.dokuName)
		self['vPrio'] = Label("")
		self['F1'] = Label("Text-")
		self['F2'] = Label("")
		self['F3'] = Label("VidPrio")
		self['F4'] = Label("Text+")
		self['coverArt'] = Pixmap()
		self['VideoPrio'] = Label("VideoPrio")
		self['Page'] = Label("")
		self['page'] = Label("")
		
		self.videoPrio = 1
		self.videoPrioS = ['L','M','H']
		self.setVideoPrio()
		self.streamListe = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('mediaportal', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['liste'] = self.streamMenuList
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
		m = re.search('<!-- aeBeginAds -->(.*?)<!-- aeEndAds -->', data, re.S)
		if m:
			ldesc = re.findall('<p>(.*?</p>)',m.group(1),re.S)
			if ldesc:
				desc = ""
				i = 0
				for txt in ldesc:
					txt = re.sub('<span.*?</span>','',txt)
					txt = re.sub('\n','',txt)
					if i > 0:
						txt = re.sub('</p>','\n',txt)
					txt = re.sub('&nbsp;',' ',txt)
					desc = "%s%s" % (desc,re.sub('<.*?>','',txt))
					i += 1
		
		self.streamListe = []
		m2 = re.search('"http://www.youtube.com/(embed|v)/(.*?)("|\?).*?data-text="(.*?)"', m.group(1), re.S)
		parts = re.search('<p>Part 1 von (.*?)<br', m.group(1))
		img = re.search('<img class=.*?src="(.*?)"', m.group(1))
		if img:
			imgurl = img.group(1)
			print "Image: ",imgurl
		else:
			imgurl = None
			
		if m2:
			print "Streams found"
			if parts:
				self.nParts = int(parts.group(1))
				pstr = " [1/%d]" % self.nParts
			else:
				self.nParts = 0
				pstr = ""
				
			self.streamListe.append((decodeHtml(m2.group(4))+pstr,m2.group(2),desc,imgurl))
		else:
			print "No dokus found !"
			desc = None
			self.streamListe.append(("No streams found !","","",""))
			
		self.streamMenuList.setList(map(DH_StreamListEntry, self.streamListe))
		self.loadPic()
		
	def getHandlung(self, desc):
		print "getHandlung:"
		if desc == None:
			print "No Infos found !"
			self['handlung'].setText("Keine weiteren Info's vorhanden !")
		else:
			self.setHandlung(desc)
		
	def setHandlung(self, data):
		print "setHandlung:"
		self['handlung'].setText(decodeHtml(data))
		
	def loadPic(self):
		print "loadPic:"
		streamName = self['liste'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamPic = self['liste'].getCurrent()[0][3]
		desc = self['liste'].getCurrent()[0][2]
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
		self.streamListe.append(("Read error !","","",""))			
		self.streamMenuList.setList(map(DH_StreamListEntry, self.streamListe))
			
	def setVideoPrio(self):
		if self.videoPrio+1 > 2:
			self.videoPrio = 0
		else:
			self.videoPrio += 1
			
		self['vPrio'].setText(self.videoPrioS[self.videoPrio])
		
	def keyOK(self):
		print "keyOK:"
		if self.keyLocked:
			return
		dhTitle = self['liste'].getCurrent()[0][0]
		dhVideoId = self['liste'].getCurrent()[0][1]
		#print "Title: ",dhTitle
		#print "VideoId: ",dhVideoId
		dhLink = youtubeUrl(self.session).getVideoUrl(dhVideoId, self.videoPrio)
		if dhLink:
			#print dhLink
			sref = eServiceReference(0x1001, 0, dhLink)
			sref.setName(dhTitle)
			self.session.open(MoviePlayer, sref)

	def keyPageUp(self):
		self['handlung'].pageUp()
			
	def keyPageDown(self):
		self['handlung'].pageDown()
			
	def keyYellow(self):
		self.setVideoPrio()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['liste'].up()
		self.loadPic()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['liste'].down()
		self.loadPic()
		
	def keyLeft(self):
		if self.keyLocked:
			return
		self['liste'].pageUp()
		self.loadPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['liste'].pageDown()
		self.loadPic()
	
	def keyCancel(self):
		self.close()
		