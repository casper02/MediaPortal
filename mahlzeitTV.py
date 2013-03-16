from imports import *
from decrypt import *

def mahlzeitTVGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

class chooseMenuList(MenuList):
	def __init__(self, list):
		MenuList.__init__(self, list, True, eListboxPythonMultiContent)
		self.l.setFont(0, gFont("mediaportal", 20))
		self.l.setItemHeight(25)
		
class mahlzeitMainScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/mahlzeitMainScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/mahlzeitMainScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"up"    : self.keyUp,
			"down"  : self.keyDown,
			"cancel": self.keyCancel,
			"left"  : self.keyLeft,
			"right" : self.keyRight,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown
		}, -1)
		
		self['title'] = Label("mahlzeit.tv")
		self['name'] = Label("Genre Auswahl")
		
		self['Vorspeisen'] = Label("Vorspeisen")
		self['Hauptspeisen'] = Label("Hauptspeisen")
		self['Desserts'] = Label("Desserts")
		self['Kuchen'] = Label("Kuchen & Gebaeck")
		self['Weiteres'] = Label("Weiteres")
		
		self.hauptspeisen = []
		self.desserts = []
		self.vorspeisen = []
		self.kuchen = []
		self.weiteres = []

		self['vorspeisen'] = chooseMenuList([])
		self['hauptspeisen'] = chooseMenuList([])
		self['desserts'] = chooseMenuList([])
		self['kuchen'] = chooseMenuList([])
		self['weiteres'] = chooseMenuList([])
		
		self.currenlist = "desserts"

		self.onLayoutFinish.append(self.layoutFinished)
		
	def hauptListEntry(self, name):
		res = [(name)]
		res.append(MultiContentEntryText(pos=(0, 0), size=(260, 25), font=0, text=name, flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER))
		return res
		
	def layoutFinished(self):
		self.vorspeisen.append(self.hauptListEntry("Salate"))
		self.vorspeisen.append(self.hauptListEntry("Suppen"))	
		self["vorspeisen"].setList(self.vorspeisen)
		
		self.hauptspeisen.append(self.hauptListEntry("Fleischgerichte"))
		self.hauptspeisen.append(self.hauptListEntry("Gefluegelgerichte"))
		self.hauptspeisen.append(self.hauptListEntry("Fischgerichte"))
		self.hauptspeisen.append(self.hauptListEntry("Nudelgerichte"))
		self.hauptspeisen.append(self.hauptListEntry("Meeresfruechte"))
		self.hauptspeisen.append(self.hauptListEntry("Reisgerichte"))
		self.hauptspeisen.append(self.hauptListEntry("Kartoffelgerichte"))
		self.hauptspeisen.append(self.hauptListEntry("Gemuesegerichte"))
		self["hauptspeisen"].setList(self.hauptspeisen)
		
		self.desserts.append(self.hauptListEntry("Suesse Desserts"))
		self.desserts.append(self.hauptListEntry("Kalte Desserts"))	
		self.desserts.append(self.hauptListEntry("Warme Desserts"))	
		self["desserts"].setList(self.desserts)
		
		self.kuchen.append(self.hauptListEntry("Kuchen"))
		self.kuchen.append(self.hauptListEntry("Torten"))	
		self.kuchen.append(self.hauptListEntry("Kekse & Plaetzchen"))	
		self["kuchen"].setList(self.kuchen)
		
		self.weiteres.append(self.hauptListEntry("Tipps & Tricks"))
		self.weiteres.append(self.hauptListEntry("Suchen.."))	
		self["weiteres"].setList(self.weiteres)
		
		self.keyRight()

	def keyUp(self):
		exist = self[self.currenlist].getCurrent()
		if exist == None:
			return
		self[self.currenlist].up()
		auswahl = self[self.currenlist].getCurrent()[0]
		self.title = auswahl
		self['name'].setText(auswahl)
		
	def keyDown(self):
		exist = self[self.currenlist].getCurrent()
		if exist == None:
			return
		self[self.currenlist].down()
		auswahl = self[self.currenlist].getCurrent()[0]
		self.title = auswahl
		self['name'].setText(auswahl)

	def keyRight(self):
		self.cur_idx = self[self.currenlist].getSelectedIndex()
		self["vorspeisen"].selectionEnabled(0)
		self["hauptspeisen"].selectionEnabled(0)
		self["desserts"].selectionEnabled(0)
		self["kuchen"].selectionEnabled(0)
		self["weiteres"].selectionEnabled(0)
		if self.currenlist == "vorspeisen":
			self["hauptspeisen"].selectionEnabled(1)
			self.currenlist = "hauptspeisen"
			cnt_tmp_ls = len(self.hauptspeisen)
		elif self.currenlist == "hauptspeisen":
			self["desserts"].selectionEnabled(1)
			self.currenlist = "desserts"
			cnt_tmp_ls = len(self.desserts)
		elif self.currenlist == "desserts":
			self["vorspeisen"].selectionEnabled(1)
			self.currenlist = "vorspeisen"
			cnt_tmp_ls = len(self.vorspeisen)
		elif self.currenlist == "kuchen":
			self["weiteres"].selectionEnabled(1)
			self.currenlist = "weiteres"
			cnt_tmp_ls = len(self.weiteres)
		elif self.currenlist == "weiteres":
			self["kuchen"].selectionEnabled(1)
			self.currenlist = "kuchen"
			cnt_tmp_ls = len(self.kuchen)
			
		cnt_tmp_ls = int(cnt_tmp_ls)
		if int(self.cur_idx) < int(cnt_tmp_ls):
			self[self.currenlist].moveToIndex(int(self.cur_idx))
		else:
			idx = int(cnt_tmp_ls) -1
			self[self.currenlist].moveToIndex(int(idx))
			
		auswahl = self[self.currenlist].getCurrent()[0]
		self.title = auswahl
		self['name'].setText(auswahl)
		
	def keyLeft(self):
		self.cur_idx = self[self.currenlist].getSelectedIndex()
		self["vorspeisen"].selectionEnabled(0)
		self["hauptspeisen"].selectionEnabled(0)
		self["desserts"].selectionEnabled(0)
		self["kuchen"].selectionEnabled(0)
		self["weiteres"].selectionEnabled(0)
		if self.currenlist == "desserts":
			self["hauptspeisen"].selectionEnabled(1)
			self.currenlist = "hauptspeisen"
			cnt_tmp_ls = len(self.hauptspeisen)
		elif self.currenlist == "hauptspeisen":
			self["vorspeisen"].selectionEnabled(1)
			self.currenlist = "vorspeisen"
			cnt_tmp_ls = len(self.vorspeisen)
		elif self.currenlist == "vorspeisen":
			self["desserts"].selectionEnabled(1)
			self.currenlist = "desserts"
			cnt_tmp_ls = len(self.desserts)
		elif self.currenlist == "kuchen":
			self["weiteres"].selectionEnabled(1)
			self.currenlist = "weiteres"
			cnt_tmp_ls = len(self.weiteres)
		elif self.currenlist == "weiteres":
			self["kuchen"].selectionEnabled(1)
			self.currenlist = "kuchen"
			cnt_tmp_ls = len(self.kuchen)
	
		cnt_tmp_ls = int(cnt_tmp_ls)
		print self.cur_idx, cnt_tmp_ls
		if int(self.cur_idx) < int(cnt_tmp_ls):
			self[self.currenlist].moveToIndex(int(self.cur_idx))
		else:
			idx = int(cnt_tmp_ls) -1
			self[self.currenlist].moveToIndex(int(idx))

		auswahl = self[self.currenlist].getCurrent()[0]
		self.title = auswahl
		self['name'].setText(auswahl)
		
	def keyPageDown(self):
		self.cur_idx = self[self.currenlist].getSelectedIndex()
		self["vorspeisen"].selectionEnabled(0)
		self["hauptspeisen"].selectionEnabled(0)
		self["desserts"].selectionEnabled(0)
		self["kuchen"].selectionEnabled(0)
		self["weiteres"].selectionEnabled(0)
		if self.currenlist == "vorspeisen":
			self["kuchen"].selectionEnabled(1)
			self.currenlist = "kuchen"
			cnt_tmp_ls = len(self.kuchen)
		elif self.currenlist == "hauptspeisen":
			self["weiteres"].selectionEnabled(1)
			self.currenlist = "weiteres"
			cnt_tmp_ls = len(self.weiteres)
		elif self.currenlist == "desserts":
			self["weiteres"].selectionEnabled(1)
			self.currenlist = "weiteres"
			cnt_tmp_ls = len(self.weiteres)
		elif self.currenlist == "kuchen":
			self["vorspeisen"].selectionEnabled(1)
			self.currenlist = "vorspeisen"
			cnt_tmp_ls = len(self.vorspeisen)
		elif self.currenlist == "weiteres":
			self["hauptspeisen"].selectionEnabled(1)
			self.currenlist = "hauptspeisen"
			cnt_tmp_ls = len(self.hauptspeisen)
			
		cnt_tmp_ls = int(cnt_tmp_ls)
		if int(self.cur_idx) < int(cnt_tmp_ls):
			self[self.currenlist].moveToIndex(int(self.cur_idx))
		else:
			idx = int(cnt_tmp_ls) -1
			self[self.currenlist].moveToIndex(int(idx))
			
		auswahl = self[self.currenlist].getCurrent()[0]
		self.title = auswahl
		self['name'].setText(auswahl)
		
	def keyPageUp(self):
		self.cur_idx = self[self.currenlist].getSelectedIndex()
		self["vorspeisen"].selectionEnabled(0)
		self["hauptspeisen"].selectionEnabled(0)
		self["desserts"].selectionEnabled(0)
		self["kuchen"].selectionEnabled(0)
		self["weiteres"].selectionEnabled(0)
		if self.currenlist == "vorspeisen":
			self["kuchen"].selectionEnabled(1)
			self.currenlist = "kuchen"
			cnt_tmp_ls = len(self.kuchen)
		elif self.currenlist == "hauptspeisen":
			self["weiteres"].selectionEnabled(1)
			self.currenlist = "weiteres"
			cnt_tmp_ls = len(self.weiteres)
		elif self.currenlist == "desserts":
			self["weiteres"].selectionEnabled(1)
			self.currenlist = "weiteres"
			cnt_tmp_ls = len(self.weiteres)
		elif self.currenlist == "kuchen":
			self["vorspeisen"].selectionEnabled(1)
			self.currenlist = "vorspeisen"
			cnt_tmp_ls = len(self.vorspeisen)
		elif self.currenlist == "weiteres":
			self["hauptspeisen"].selectionEnabled(1)
			self.currenlist = "hauptspeisen"
			cnt_tmp_ls = len(self.hauptspeisen)
			
		cnt_tmp_ls = int(cnt_tmp_ls)
		if int(self.cur_idx) < int(cnt_tmp_ls):
			self[self.currenlist].moveToIndex(int(self.cur_idx))
		else:
			idx = int(cnt_tmp_ls) -1
			self[self.currenlist].moveToIndex(int(idx))
			
		auswahl = self[self.currenlist].getCurrent()[0]
		self.title = auswahl
		self['name'].setText(auswahl)
		
	def keyOK(self):
		exist = self[self.currenlist].getCurrent()
		if exist == None:
			return
		print self.currenlist
		auswahl = self[self.currenlist].getCurrent()[0]
		print auswahl
		if auswahl == "Salate":
			self.session.open(mahlzeitStreamScreen, "http://mahlzeit.tv/paginate?courses=Vorspeisen&limit=500&offset=0&order_by_key=published_at&type_dishes=Salate")
		elif auswahl == "Suppen":
			self.session.open(mahlzeitStreamScreen, "http://mahlzeit.tv/paginate?courses=Vorspeisen&limit=500&offset=0&order_by_key=published_at&type_dishes=Suppen")
		elif auswahl == "Fleischgerichte":
			self.session.open(mahlzeitStreamScreen, "http://mahlzeit.tv/paginate?courses=Hauptspeisen&limit=500&offset=0&order_by_key=published_at&type_dishes=Fleischgerichte")
		elif auswahl == "Gefluegelgerichte":
			self.session.open(mahlzeitStreamScreen, "http://mahlzeit.tv/paginate?courses=Hauptspeisen&limit=500&offset=0&order_by_key=published_at&type_dishes=Gefl%C3%BCgelgerichte")
		elif auswahl == "Fischgerichte":
			self.session.open(mahlzeitStreamScreen, "http://mahlzeit.tv/paginate?courses=Hauptspeisen&limit=500&offset=0&order_by_key=published_at&type_dishes=Fischgerichte")
		elif auswahl == "Nudelgerichte":
			self.session.open(mahlzeitStreamScreen, "http://mahlzeit.tv/paginate?courses=Hauptspeisen&limit=500&offset=0&order_by_key=published_at&type_dishes=Nudelgerichte")
		elif auswahl == "Meeresfruechte":
			self.session.open(mahlzeitStreamScreen, "http://mahlzeit.tv/paginate?courses=Hauptspeisen&limit=500&offset=0&order_by_key=published_at&type_dishes=Meeresfr%C3%BCchte")
		elif auswahl == "Reisgerichte":
			self.session.open(mahlzeitStreamScreen, "http://mahlzeit.tv/paginate?courses=Hauptspeisen&limit=500&offset=0&order_by_key=published_at&type_dishes=Reisgerichte")
		elif auswahl == "Kartoffelgerichte":
			self.session.open(mahlzeitStreamScreen, "http://mahlzeit.tv/paginate?courses=Hauptspeisen&limit=500&offset=0&order_by_key=published_at&type_dishes=Kartoffelgerichte")
		elif auswahl == "Gemuesegerichte":
			self.session.open(mahlzeitStreamScreen, "http://mahlzeit.tv/paginate?courses=Hauptspeisen&limit=500&offset=0&order_by_key=published_at&type_dishes=Gem%C3%BCsegerichte")
		elif auswahl == "Suesse Desserts":
			self.session.open(mahlzeitStreamScreen, "http://mahlzeit.tv/paginate?courses=Desserts&limit=500&offset=0&order_by_key=published_at&type_dishes=S%C3%BC%C3%9Fe+Desserts")
		elif auswahl == "Kalte Desserts":
			self.session.open(mahlzeitStreamScreen, "http://mahlzeit.tv/paginate?courses=Desserts&limit=500&offset=0&order_by_key=published_at&type_dishes=Kalte+Desserts")
		elif auswahl == "Warme Desserts":
			self.session.open(mahlzeitStreamScreen, "http://mahlzeit.tv/paginate?courses=Desserts&limit=500&offset=0&order_by_key=published_at&type_dishes=Warme+Desserts")
		elif auswahl == "Kuchen":
			self.session.open(mahlzeitStreamScreen, "http://mahlzeit.tv/paginate?courses=Kuchen+%26+Geb%C3%A4ck&limit=500&offset=0&order_by_key=published_at&type_dishes=Kuchen")	
		elif auswahl == "Torten":
			self.session.open(mahlzeitStreamScreen, "http://mahlzeit.tv/paginate?courses=Kuchen+%26+Geb%C3%A4ck&limit=500&offset=0&order_by_key=published_at&type_dishes=Torten")	
		elif auswahl == "Kekse & Plaetzchen":
			self.session.open(mahlzeitStreamScreen, "http://mahlzeit.tv/paginate?courses=Kuchen+%26+Geb%C3%A4ck&limit=500&offset=0&order_by_key=published_at&type_dishes=Kekse+%26+Pl%C3%A4tzchen")	
		elif auswahl == "Tipps & Tricks":
			self.session.open(mahlzeitStreamScreen, "http://mahlzeit.tv/paginate?courses=Tipps+%26+Tricks&limit=500&offset=0&order_by_key=published_at&type_dishes=Tipps+%26+Tricks")	

	def keyCancel(self):
		self.close()

def mahlzeitStreamListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 

class mahlzeitStreamScreen(Screen):
	
	def __init__(self, session, genreLink):
		self.session = session
		self.genreLink = genreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/mahlzeitStreamScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/mahlzeitStreamScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok" : self.keyOK,
			"cancel" : self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft,
		}, -1)
		
		self['title'] = Label("mahlzeit.tv")
		self['coverArt'] = Pixmap()
		self['name'] = Label("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList

		self.keyLocked = False

		self.onLayoutFinish.append(self.loadpage)
		
	def loadpage(self):
		self.keyLocked = True
		self.streamList = []
		ptUrl = self.genreLink
		print ptUrl
		getPage(ptUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.pageData).addErrback(self.dataError)
		
	def pageData(self, data):
		List = re.findall('<div class="vid_figure">.*?<a href="(.*?)" title="(.*?)"><img alt=".*?" src="(.*?)" /></a>.*?<div class="titleWrapper">', data, re.S)
		if List:
			for (Link, Name, Image) in List:
				Link = "http://mahlzeit.tv"+Link
				self.streamList.append((Name, Image, Link))
			self.streamMenuList.setList(map(mahlzeitStreamListEntry, self.streamList))
			self.keyLocked = False
			self.showInfos()

	def showInfos(self):
		if self.keyLocked:
			return
		ptTitle = self['streamlist'].getCurrent()[0][0]
		ptImage = self['streamlist'].getCurrent()[0][1]
		self.ptRead(ptImage)
		self['name'].setText(ptTitle)

	def ptRead(self, stationIconLink):
		downloadPage(stationIconLink, "/tmp/mahlzeitIcon.jpg").addCallback(self.ptCoverShow)
		
	def ptCoverShow(self, picData):
		if fileExists("/tmp/mahlzeitIcon.jpg"):
			self['coverArt'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/mahlzeitIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr.__deref__())
					self['coverArt'].show()
					del self.picload

	def dataError(self, error):
		print error
		
	def keyOK(self):
		if self.keyLocked:
			return
		Link = self['streamlist'].getCurrent()[0][2]
		print Link
		getPage(Link, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.playData).addErrback(self.dataError)
		
	def playData(self, data):
		file = re.findall('},{&quot;src&quot;:&quot;(.*?.mp4)&quot;,&quot;mime_type&quot;:&quot;video/mp4&quot;,&quot;video_codec&quot;:&quot;.*?&quot;,&quot;audio_codec&quot;:&quot;.*?&quot;}', data)
		title = self['streamlist'].getCurrent()[0][0]
		print file
		if file:
			sref = eServiceReference(0x1001, 0, file[0])
			sref.setName(title)
			self.session.open(MoviePlayer, sref)
		
	def keyLeft(self):
		if self.keyLocked:
			return
		self['streamlist'].pageUp()
		self.showInfos()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['streamlist'].pageDown()
		self.showInfos()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['streamlist'].up()
		self.showInfos()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['streamlist'].down()
		self.showInfos()
		
	def keyCancel(self):
		self.close()
