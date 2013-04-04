#	-*-	coding:	utf-8	-*-

from Plugins.Extensions.mediaportal.resources.imports import *
from Plugins.Extensions.mediaportal.resources.decrypt import *
from Plugins.Extensions.mediaportal.resources.yt_url import *
import Queue
import threading
from Components.ScrollLabel import ScrollLabel

DOKUH_Version = "DOKUh.de v0.96"

DOKUH_siteEncoding = 'utf-8'

"""
Sondertastenbelegung:

Genre Auswahl:
	KeyCancel	: Menu Up / Exit
	KeyOK		: Menu Down / Select
	
Doku Auswahl:
	Bouquet +/-,		: Seitenweise blättern in 1er Schritten Up/Down
	Rot/Blau			: Die Beschreibung Seitenweise scrollen
	'1', '4', '7',
	'3', 6', '9'		: blättern in 2er, 5er, 10er Schritten Down/Up

Stream Auswahl:
	Rot/Blau			: Die Beschreibung Seitenweise scrollen
	Gelb				: Videopriorität 'L','M','H'

"""
def DOKUHmenuListentry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 
		
class showDOKUHGenre(Screen):

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
			"right"	: self.keyRight,
			"left"	: self.keyLeft,
			"red"	: self.keyRed
		}, -1)

		self['title'] = Label(DOKUH_Version)
		self['ContentTitle'] = Label("Genre Auswahl")
		self['name'] = Label("")
		self['F1'] = Label("")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		
		self.menuLevel = 0
		self.menuMaxLevel = 2
		self.menuIdx = [0,0,0]
		self.keyLocked = True
		self.genreSelected = False
		self.menuListe = []
		self.baseUrl = "http://dokuh.de"
		self.genreBase = "/doku-online-stream/kategorien"
		self.genreName = ["","","",""]
		self.genreUrl = ["","","",""]
		self.genreTitle = ""
		#self.subMenu = []
		#self.keckse = {}
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		mainGenre = [
			("NEUESTE DOKUS", ""),
			("BELIEBTESTE DOKUS", "/"),
			("MEISTGESEHENE DOKUS", "/"),
			("Geschichte", "/geschichte"),
			("Länder", "/lander"),
			("Menschen", "/menschen"),
			("Gesellschaft", "/gesellschaft"),
			("Umwelt", "/umwelt"),
			("Technologie", "/technologie"),
			("Wissenschaft", "/wissenschaft"),
			("Wirtschaft", "/wirtschaft"),
			("Kurioses", "/kurioses"),
			("Staffeln & HD", "/staffeln-und-hd")
			]
			
			
		subGenre_0 = [
			("Antike", "/antike"),
			("Archäologie", "/archaologie"),
			("Erster Weltkrieg", "/erster-weltkrieg"),
			("Mittelalter", "/mittelalter"),
			("Moderne", "/moderne"),
			("Neuzeit", "/neuzeit"),
			("Zweiter Weltkrieg", "/zweiter-weltkrieg")
			]
		subGenre_0_0 = [
			("Ägyptologie", "/agyptologie"),
			("Römisches Reich", "/romisches-reich")
			]
		subGenre_1 = [
			("Afrika", "/afrika"),
			("Amerika", "/amerika"),
			("Asien", "/asien"),
			("Europa", "/europa"),
			("Urlaub & Reisen", "/urlaub-reisen")
			]
		subGenre_1_0 = [
			("Ägypten", "/agypten")
			]
		subGenre_1_1 = [
			("Nordamerika", "/nordamerika"),
			("Südamerika", "/sudamerika")
			]
		subGenre_1_2 = [
			("China", "/china"),
			("Japan", "/japan"),
			("Norkorea", "/nordkorea")
			]
		subGenre_1_3 = [
			("Deutschland", "/deutschland"),
			("Österreich", "/osterreich"),
			("Russland", "/russland")
			]
		subGenre_2 = [
			("Berufe", "/berufe"),
			("Drogen & Sucht", "/drogen-sucht"),
			("Erotik & Sex", "/erotik-sex"),
			("Gesundheit & Medizin", "/gesundheit-medizin"),
			("Hobby & Freizeit", "/hobby-freizeit"),
			("Körper", "/korper"),
			("Krankheiten", "/krankheiten"),
			("Millionäre", "/millionare"),
			("Musiker", "/musiker"),
			("Nahrungsmittel", "/nahrungsmittel"),
			("Persönlichkeiten", "/personlichkeiten"),
			("Sport", "/sport")
			]
		subGenre_2_0 = [
			("Arzt", "/arzt"),
			("Feuerwehr & Rettungsdienst", "/feuerwehr-rettungsdienst"),
			("Pilot", "/pilot"),
			("Polizei", "/polizei"),
			("Soldat", "/soldat"),
			("sonstige Berufe", "/sonstige-berufe")
			]
		subGenre_2_1 = [
			("Alkohol", "/alkohol"),
			("Cannabis", "/cannabis"),
			("Crystal Meth", "/crystal-meth"),
			("Ecstasy", "/ectasy"),
			("Kokain", "/kokain"),
			("LSD", "/lsd")
			]
		subGenre_2_9 = [
			("Essen", "/essen"),
			("Getränke", "/getraenke")
			]
		subGenre_2_10 = [
			("Autoren", "/autoren"),
			("Diktatoren", "/diktatoren"),
			("Politiker", "/politiker"),
			("Schauspieler", "/schauspieler"),
			("Sportler", "/sportler"),
			("Unternehmer", "/unternehmer")
			]
		subGenre_2_11 = [
			("Fußball", "/fussball"),
			("Kampfsport", "/kampfsport"),
			("Motorsport", "/motorsport"),
			("Extremsport", "/extremsport")
			]
		subGenre_3 = [
			("Fernsehen", "/fernsehen"),
			("Gruppierungen", "/gruppierungen"),
			("Krieg", "/krieg"),
			("Kriminalität", "/kriminalitat"),
			("Kunst", "/kunst"),
			("Medien", "/medien"),
			("Politik", "/politik"),
			("Religion", "/religion")
			]
		subGenre_3_1 = [
			("Gangs", "/gangs"),
			("Hooligans", "/hooligans"),
			("Mafia", "/mafia"),
			("Nazis", "/nazis"),
			("Rassismus", "/rassismus"),
			("Sekten", "/sekten"),
			("Terrorismus", "/terrorismus"),
			("Ultras", "/ultras")
			]
		subGenre_3_2 = [
			("Bundeswehr", "/bundeswehr"),
			("Militär", "/militar"),
			("Waffen", "/waffen")
			]
		subGenre_3_5 = [
			("Musik", "/musik"),
			("Zeitungen & Zeitschriften", "/zeitungen-zeitschriften")
			]
		subGenre_3_7 = [
			("Christentum", "/christentum"),
			("Islam", "/islam"),
			("Judentum", "/judentum")
			]
		subGenre_4 = [
			("Katastrophen", "/katastrophen"),
			("Klima", "/klima"),
			("Natur", "/natur"),
			("Pflanzen", "/pflanzen"),
			("Tiere", "/tiere")
			]
		subGenre_4_0 = [
			("Atomkatastrophen", "/"),
			("Erdbeben", "/"),
			("Ölkatastrophen", "/"),
			("Tsunami", "/"),
			("Wirbelstürme", "/")
			]
		subGenre_5 = [
			("Auto", "/auto"),
			("Bauwerke", "/bauwerke"),
			("Computer", "/computer"),
			("Energie", "/energie"),
			("Handy", "/handy"),
			("Internet", "/internet"),
			("Luft & Raumfahrt", "/luft-raumfahrt"),
			("Schifffahrt", "/schifffahrt"),
			("Technik", "/technik")
			]
		subGenre_5_3 = [
			("Atomkraft", "/atomkraft")
			]
		subGenre_6 = [
			("Astronomie & Weltall", "/astronomie-weltall"),
			("Naturwissenschaft", "/naturwissenschaft"),
			("Tierwissenschaft", "/tierwissenschaft")
			]
		subGenre_7 = [
			("Finanzkrise", "/finanzkrise"),
			("Geld", "/geld"),
			("Unternehmen", "/unternehmen")
			]
		subGenre_8 = [
			("Astrologie", "/astrologie"),
			("Mystery & Mythen", "/mystery-mythen"),
			("Unerklärliches", "/unerklarliches")
			]
		subGenre_9 = [
			("HD", "/hd-extra"),
			("Staffeln", "/staffeln")
			]
			
		self.genreMenu = [mainGenre,
			[None,None,None,subGenre_0,subGenre_1,subGenre_2,subGenre_3,subGenre_4,subGenre_5,subGenre_6,subGenre_7,subGenre_8,subGenre_9
			],
			[
			[None],
			[None],
			[None],
			[subGenre_0_0,None,None,None,None,None,None
			],
			[subGenre_1_0,subGenre_1_1,subGenre_1_2,subGenre_1_3,None
			],
			[subGenre_2_0,subGenre_2_1,None,None,None,None,None,None,None,subGenre_2_9,subGenre_2_10,subGenre_2_11
			],
			[None,subGenre_3_1,subGenre_3_2,None,None,subGenre_3_5,None,subGenre_3_7
			],
			[subGenre_4_0,None,None,None,None
			],
			[None,None,None,subGenre_5_3,None,None,None,None,None
			],
			[None,None,None
			],
			[None,None,None
			],
			[None,None,None
			],
			[None,None
			]
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
		print "DOKUh.de:"
		self.setMenu(0, True)
		self.keyLocked = False

	def keyRight(self):
		self['genreList'].pageDown()
		self.menuIdx[self.menuLevel] = self['genreList'].getSelectedIndex()
		self.setGenreStrTitle()
		
	def keyLeft(self):
		self['genreList'].pageUp()
		self.menuIdx[self.menuLevel] = self['genreList'].getSelectedIndex()
		self.setGenreStrTitle()
		
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
			genreurl = self.baseUrl+self.genreBase+self.genreUrl[0]+self.genreUrl[1]+self.genreUrl[2]
			print genreurl
			self.session.open(DOKUHFilmListeScreen, genreurl, self.genreTitle)

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
					self.chooseMenuList.setList(map(DOKUHmenuListentry, self.menuListe))
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
					self.chooseMenuList.setList(map(DOKUHmenuListentry, self.menuListe))
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
					self.chooseMenuList.setList(map(DOKUHmenuListentry, self.menuListe))
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

def DOKUHFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
class DOKUHFilmListeScreen(Screen):
	
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
		}, -1)

		self.sortOrder = 0
		self.baseUrl = "http://dokuh.de"
		self.genreTitle = "Dokukanäle in Genre "
		self.sortParIMDB = ""
		self.sortParAZ = "?orderby=title"
		self.sortOrderStrAZ = ""
		self.sortOrderStrIMDB = ""
		self.sortOrderStrGenre = ""
		self['title'] = Label(DOKUH_Version)
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
		self.genreNEUESTE = re.match(".*?NEUESTE DOKUS",self.genreName)
		self.genreBELIEBTESTE = re.match(".*?BELIEBTESTE DOKUS",self.genreName)
		self.genreMEISTGESEHEN = re.match(".*?MEISTGESEHENE DOKUS",self.genreName)
		#self.genreBELIEBTESTE = False
		#self.genreMEISTGESEHEN = False
		self.genreSpecial = self.genreNEUESTE or self.genreBELIEBTESTE or self.genreMEISTGESEHEN

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
		if not self.genreSpecial:
			url = "%s/page/%d/%s" % (self.genreLink, self.page, self.sortParAZ)
		else:
			url = self.baseUrl
			
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
		self.chooseMenuList.setList(map(DOKUHFilmListEntry, self.dokusListe))
		
	def loadPageData(self, data):
		print "loadPageData:"
		
		if self.genreNEUESTE:
			print "Neueste Dokus suche..."
			m=re.search('class="name">neueste Dokus<(.*?)<!-- end .section-box -->',data,re.S)
		elif self.genreBELIEBTESTE:
			print "Beliebteste Dokus suche..."
			m=re.search('class="name">beliebteste Dokus<(.*?)<!-- end .section-box -->',data,re.S)
		elif self.genreMEISTGESEHEN:
			print "Meistgesehene Dokus suche..."
			m=re.search('class="name">meistgesehene Dokus<(.*?)<!-- end .section-box -->',data,re.S)
		else:
			print "Normal search.."
			m=re.search('<div class="loop-content.*?class="thumb">(.*)<!-- end .loop-content -->',data,re.S)
			
		if m:
			dokus = re.findall('class="clip-link".*?title="(.*?)" href="(.*?)".*?<img src="(.*?)".*?class="desc">(.*?)</p>', m.group(1), re.S)
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
			for	(name,url,img,desc) in dokus:
				#print	"Url: ", url, "Name: ", name
				self.dokusListe.append((decodeHtml(name), url, img, desc))
			self.chooseMenuList.setList(map(DOKUHFilmListEntry, self.dokusListe))
			
			self.loadPicQueued()
		else:
			print "No dokus found !"
			self.dokusListe.append(("No dokus found !","","",""))
			self.chooseMenuList.setList(map(DOKUHFilmListEntry, self.dokusListe))
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
		
	def keyTxtPageUp(self):
		self['handlung'].pageUp()
			
	def keyTxtPageDown(self):
		self['handlung'].pageDown()
			
	def keyOK(self):
		if (self.keyLocked|self.eventL.is_set()):
			return

		streamLink = self['liste'].getCurrent()[0][1]
		streamName = self['liste'].getCurrent()[0][0]
		print "Open DOKUHStreams:"
		print "Name: ",streamName
		print "Link: ",streamLink
		self.session.open(DOKUHStreams, streamLink, streamName)
	
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

	def keyCancel(self):
		self.close()

def DOKUHStreamListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0]+entry[3])
		] 
class DOKUHStreams(Screen, ConfigListScreen):
	
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
			"ok"    	: self.keyOK,
			"cancel"	: self.keyCancel,
			"up" 		: self.keyUp,
			"down" 		: self.keyDown,
			"right" 	: self.keyPageDown,
			"left" 		: self.keyPageUp,
			"yellow"	: self.keyYellow,
			"red" 		: self.keyTxtPageUp,
			"blue" 		: self.keyTxtPageDown
		}, -1)
		
		self['title'] = Label(DOKUH_Version)
		self['ContentTitle'] = Label("Streams für "+dokuName)
		self['coverArt'] = Pixmap()
		self['handlung'] = ScrollLabel("")
		self['name'] = Label(dokuName)
		self['F1'] = Label("Text-")
		self['F2'] = Label("")
		self['F3'] = Label("VidPrio")
		self['F4'] = Label("Text+")
		self['vPrio'] = Label("")
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
		streams = re.findall('class="related-item".*?loadVideo\(\'(.*?)\'\).*?<img src="(.*?)".*?"duration">'\
					'(.*?)<.*?"title">\s*?(.*?)\s*?</span>.*?<p>(.*?)</p>', data, re.S)
		self.streamListe = []
		if streams:
			print "Streams found"
			for (videoTag,imgUrl,duration,title,desc) in streams:
				self.streamListe.append((title.lstrip().rstrip(),videoTag,imgUrl," ["+duration+"]",desc))
		else:
			print "No dokus found !"
			self.streamListe.append(("No streams found !","","","",""))
			
		self.streamMenuList.setList(map(DOKUHStreamListEntry, self.streamListe))
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
		streamName = self['liste'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamPic = self['liste'].getCurrent()[0][2]
		desc = self['liste'].getCurrent()[0][4]
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
		self.streamListe.append(("Read error !","","","",""))			
		self.streamMenuList.setList(map(DOKUHStreamListEntry, self.streamListe))
			
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
		
	def keyPageUp(self):
		if self.keyLocked:
			return
		self['liste'].pageUp()
		self.loadPic()
		
	def keyPageDown(self):
		if self.keyLocked:
			return
		self['liste'].pageDown()
		self.loadPic()
	
	def keyTxtPageUp(self):
		self['handlung'].pageUp()
			
	def keyTxtPageDown(self):
		self['handlung'].pageDown()
			
	def keyYellow(self):
		self.setVideoPrio()
		
	def keyCancel(self):
		self.close()
		