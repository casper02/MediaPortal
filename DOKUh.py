#	-*-	coding:	utf-8	-*-

from imports import *
from decrypt import *
import Queue
import threading

DOKUH_Version = "DOKUh.de v0.91"

DOKUH_siteEncoding = 'utf-8'

"""
Sondertastenbelegung:

Genre Auswahl:
	Rot: 	Menu Up
	Blue:	Menu Down / Select
	
Doku Auswahl:
	Bouquet +/-, Rot/Blau	: Seitenweise blättern in 1 Schritten Up/Down
	'1', '4', '7',
	'3', 6', '9'			: blättern in 2er, 5er, 10er Schritten Down/Up

"""
def DOKUHmenuListentry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 
		
#class showDOKUHGenre(Screen):
class showDOKUHGenre(Screen):

	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/showDOKUHGenre.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/showDOKUHGenre.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"] = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up": self.keyUp,
			"down": self.keyDown,
			"blue"	: self.keyOK,
			"red"	: self.keyMenuUp
		}, -1)

		self['title'] = Label(DOKUH_Version)
		self['ContentTitle'] = Label("Genre Auswahl")
		self['name'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.menuLevel = 0
		self.menuMaxLevel = 2
		self.mainIdx = 0
		self.subIdx_1 = 0
		self.subIdx_2 = 0
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
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		#("BELIEBTESTE DOKUS", "/"),
		#("MEISTGESEHENE DOKUS", "/"),
		mainGenre = [
			("NEUESTE DOKUS", ""),
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
			[
			None,subGenre_0,subGenre_1,subGenre_2,subGenre_3,subGenre_4,subGenre_5,subGenre_6,subGenre_7,subGenre_8,subGenre_9
			],
			[
			[
			None
			],
			[
			subGenre_0_0,None,None,None,None,None,None
			],
			[
			subGenre_1_0,subGenre_1_1,subGenre_1_2,subGenre_1_3,None
			],
			[
			subGenre_2_0,subGenre_2_1,None,None,None,None,None,None,None,subGenre_2_9,subGenre_2_10,subGenre_2_11
			],
			[
			None,subGenre_3_1,subGenre_3_2,None,None,subGenre_3_5,None,subGenre_3_7
			],
			[
			subGenre_4_0,None,None,None,None
			],
			[
			None,None,None,subGenre_5_3,None,None,None,None,None
			],
			[
			None,None,None
			],
			[
			None,None,None
			],
			[
			None,None,None
			],
			[
			None,None
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
		self.setMenu(0, 0)
		self.keyLocked = False

	def keyUp(self):
		self['genreList'].up()
		self.setGenreStrTitle()
		
	def keyDown(self):
		self['genreList'].down()
		self.setGenreStrTitle()
		
	def keyMenuUp(self):
		print "keyMenuUp:"
		if self.keyLocked:
			return
		menuIdx = self['genreList'].getSelectedIndex()
		self.setMenu(-1, menuIdx)

	def keyOK(self):
		print "keyOK:"
		if self.keyLocked:
			return
			
		menuIdx = self['genreList'].getSelectedIndex()
		self.setMenu(+1, menuIdx)
		
		if self.genreSelected:
			print "Genre selected"
			genreurl = self.baseUrl+self.genreBase+self.genreUrl[0]+self.genreUrl[1]+self.genreUrl[2]
			print genreurl
			self.session.open(DOKUHFilmListeScreen, genreurl, self.genreTitle)

	def setMenu(self, levelIncr, menuIdx):
		print "setMenu: ",levelIncr,menuIdx
		self.genreSelected = False
		if (self.menuLevel+levelIncr) in range(self.menuMaxLevel+1):
			if levelIncr < 0:
				self.genreName[self.menuLevel] = ""
			self.menuLevel += levelIncr
			self.menuListe = []
			if self.menuLevel == 0:
				if self.genreMenu[0] != None:
					for (Name,Url) in self.genreMenu[0]:
						self.menuListe.append((Name,Url))
					self.chooseMenuList.setList(map(DOKUHmenuListentry, self.menuListe))
					self['genreList'].moveToIndex(self.mainIdx)
				else:
					self.genreName[self.menuLevel] = ""
					self.genreUrl[self.menuLevel] = ""
					self.menuLevel = 0
					print "No menu entrys!"
			elif self.menuLevel == 1:
				if self.genreMenu[1][menuIdx] != None:
					if levelIncr > 0:
						self.mainIdx = menuIdx
						self.subIdx_1 = 0
					for (Name,Url) in self.genreMenu[1][self.mainIdx]:
						self.menuListe.append((Name,Url))
					self.chooseMenuList.setList(map(DOKUHmenuListentry, self.menuListe))
					self['genreList'].moveToIndex(self.subIdx_1)
				else:
					self.genreName[self.menuLevel] = ""
					self.genreUrl[self.menuLevel] = ""
					self.menuLevel -= 1
					self.genreSelected = True
					print "No menu entrys!"
			elif self.menuLevel == 2:
				if self.genreMenu[2][self.mainIdx][menuIdx] != None:
					if levelIncr > 0:
						self.subIdx_1 = menuIdx
						self.subIdx_2 = 0
					for (Name,Url) in self.genreMenu[2][self.mainIdx][self.subIdx_1]:
						self.menuListe.append((Name,Url))
					self.chooseMenuList.setList(map(DOKUHmenuListentry, self.menuListe))
					self['genreList'].moveToIndex(self.subIdx_2)
				else:
					self.genreName[self.menuLevel] = ""
					self.genreUrl[self.menuLevel] = ""
					self.menuLevel -= 1
					self.genreSelected = True
					print "No menu entrys!"
		else:
			self.subIdx_2 = menuIdx
			self.genreSelected = True
				
		print "menuLevel: ",self.menuLevel
		print "mainIdx: ",self.mainIdx
		print "subIdx_1: ",self.subIdx_1
		print "subIdx_2: ",self.subIdx_2
		print "genreSelected: ",self.genreSelected
		print "menuListe: ",self.menuListe
		print "genreUrl: ",self.genreUrl
		
		self.setGenreStrTitle()		
		
	def keyCancel(self):
		self.close()
	

def DOKUHFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
class DOKUHFilmListeScreen(Screen):
	
	def __init__(self, session, genreLink, genreName):
		self.session = session
		self.genreLink = genreLink
		self.genreName = genreName
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/DOKUHFilmListeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/DOKUHFilmListeScreen.xml"
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
		self.baseUrl = "http://dokuh.de"
		self.genreTitle = "Dokus in Genre "
		self.sortParIMDB = ""
		self.sortParAZ = ""
		self.sortOrderStrAZ = ""
		self.sortOrderStrIMDB = ""
		self.sortOrderStrGenre = ""
		self['title'] = Label(DOKUH_Version)
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
		self.dokusListe = []
		self.keckse = {}
		self.page = 0
		self.pages = 0;
		self.genreNEUESTE = re.match(".*?NEUESTE DOKUS",self.genreName)
		#self.genreBELIEBTESTE = re.match(".*?BELIEBTESTE DOKUS",self.genreName)
		#self.genreMEISTGESEHEN = re.match(".*?MEISTGESEHENE DOKUS",self.genreName)
		self.genreBELIEBTESTE = False
		self.genreMEISTGESEHEN = False
		self.genreSpecial = self.genreNEUESTE or self.genreBELIEBTESTE or self.genreMEISTGESEHEN

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
		if not self.genreSpecial:
			url = "%s/page/%d/" % (self.genreLink, self.page)
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
		self.dokusListe.append(("No dokus found !","","",""))
		self.chooseMenuList.setList(map(DOKUHFilmListEntry, self.dokusListe))
		
	def loadPageData(self, data):
		print "loadPageData:"
		
		if self.genreNEUESTE:
			print "Neueste Dokus suche..."
			m=re.search('class="name">neueste Dokus<(.*?)<!-- end .section-box -->',data,re.S)
		elif self.genreBELIEBTESTE:
			print "Beliebteste Dokus suche..."
			m=re.search('class="name">beliebteste Dokus<(.*?)',data,re.S)
		elif self.genreMEISTGESEHEN:
			print "Meistgesehene Dokus suche..."
			m=re.search('class="name">meistgesehene Dokus<(.*?)',data,re.S)
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
		
		streamName = self['filmList'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamPic = self['filmList'].getCurrent()[0][2]
		#streamUrl = self.baseUrl+re.sub('amp;','',self['filmList'].getCurrent()[0][1])
		desc = self['filmList'].getCurrent()[0][3]
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
		print "Open DOKUHStreams:"
		print "Name: ",streamName
		print "Link: ",streamLink
		self.session.open(DOKUHStreams, streamLink, streamName)
	
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

def DOKUHStreamListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0]+entry[3])
		] 
class DOKUHStreams(Screen, ConfigListScreen):
	
	def __init__(self, session, dokuUrl, dokuName):
		self.session = session
		self.dokuUrl = dokuUrl
		self.dokuName = dokuName
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/DOKUHStreams.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/DOKUHStreams.xml"
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
		
		self['title'] = Label(DOKUH_Version)
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
		streamName = self['streamList'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamPic = self['streamList'].getCurrent()[0][2]
		desc = self['streamList'].getCurrent()[0][4]
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
			
	def got_link(self, stream_url):
		print "got_link:"
		if stream_url == None:
			message = self.session.open(MessageBox, _("Stream not found, try another Stream Hoster."), MessageBox.TYPE_INFO, timeout=3)
		else:
			sref = eServiceReference(0x1001, 0, stream_url)
			sref.setName("%s%s" % (self.dokuName,self['streamList'].getCurrent()[0][2]))
			self.session.open(MoviePlayer, sref)

	# code von doku.me geliehen
	def getVideoUrl(self, url):
		# this part is from mtube plugin
		print "got url:", url
		VIDEO_FMT_PRIORITY_MAP = {
			'38' : 1, #MP4 Original (HD)
			'37' : 2, #MP4 1080p (HD)
			'22' : 3, #MP4 720p (HD)
			'18' : 4, #MP4 360p
			'35' : 5, #FLV 480p
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
		