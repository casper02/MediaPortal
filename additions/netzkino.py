from Plugins.Extensions.mediaportal.resources.imports import *
from Plugins.Extensions.mediaportal.resources.decrypt import *

def netzKinoGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[1])
		] 
		
class netzKinoGenreScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/netzKinoGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/netzKinoGenreScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		
		self['title'] = Label("Netzkino.de")
		self['name'] = Label("Genre Auswahl")
		self['coverArt'] = Pixmap()
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.genreliste.append(('81', 'Neu bei Netzkino'))
		self.genreliste.append(('61', 'HD-Kino'))
		self.genreliste.append(('39', 'Starkino'))
		self.genreliste.append(('1', 'Actionkino'))
		self.genreliste.append(('4', 'Dramakino'))
		self.genreliste.append(('32', 'Thrillerkino'))
		self.genreliste.append(('18', 'Liebesfilmkino'))
		self.genreliste.append(('6', 'Scifikino'))
		self.genreliste.append(('51', 'Arthousekino'))
		self.genreliste.append(('31', 'Queerkino'))
		self.genreliste.append(('3', 'Spasskino'))
		self.genreliste.append(('10', 'Asiakino'))
		self.genreliste.append(('5', 'Horrorkino'))
		self.genreliste.append(('33', 'Klassikerkino'))
		self.genreliste.append(('34', 'Westernkino'))
		self.genreliste.append(('71', 'Kino ab 18'))
		self.chooseMenuList.setList(map(netzKinoGenreListEntry, self.genreliste))

	def keyOK(self):
		genreID = self['genreList'].getCurrent()[0][0]
		self.session.open(netzKinoFilmeScreen, genreID)

	def keyCancel(self):
		self.close()

def netzKinoFilmeListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
		
class netzKinoFilmeScreen(Screen):
	
	def __init__(self, session, genreID):
		self.session = session
		self.genreID = genreID
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/netzKinoFilmeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/netzKinoFilmeScreen.xml"
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
			"left" : self.keyLeft
		}, -1)

		self['title'] = Label("Netzkino.de")
		self['name'] = Label("Film Auswahl")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.keyLocked = True
		url = "http://www.netzkino.de/capi/get_category_posts?id=%s&count=500&custom_fields=Streaming" % self.genreID
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.genreData).addErrback(self.dataError)
	
	def genreData(self, data):
		nkDaten = re.findall('"title_plain":"(.*?)".*?"images":."full":."url":"(.*?)".*?"custom_fields":\{(.*?\})', data, re.S|re.I)
		if nkDaten:
			for (nkTitle,nkImage,nkStream) in nkDaten:
				nkImage = nkImage.replace('\\','')
				nkUrl = re.findall('"Streaming":."(.*?)"', nkStream)
				if nkUrl:
					nkUrl = "http://dl.netzkinotv.c.nmdn.net/netzkino_tv/%s.mp4" % nkUrl[0].replace('\\','').replace('\\','')
					self.filmliste.append((decodeHtml(nkTitle),nkImage,nkUrl))
				self.chooseMenuList.setList(map(netzKinoFilmeListEntry, self.filmliste))
			self.keyLocked = False
			self.showInfos()

	def dataError(self, error):
		print error

	def showInfos(self):
		nkTitle = self['genreList'].getCurrent()[0][0]
		nkImage = self['genreList'].getCurrent()[0][1]
		print nkImage
		self['name'].setText(nkTitle)
		downloadPage(nkImage, "/tmp/nkIcon.jpg").addCallback(self.ShowCover)
		
	def ShowCover(self, picData):
		if fileExists("/tmp/nkIcon.jpg"):
			self['coverArt'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/nkIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr.__deref__())
					self['coverArt'].show()
					del self.picload
	
	def keyLeft(self):
		if self.keyLocked:
			return
		self['genreList'].pageUp()
		self.showInfos()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['genreList'].pageDown()
		self.showInfos()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['genreList'].up()
		self.showInfos()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['genreList'].down()
		self.showInfos()
		
	def keyOK(self):
		if self.keyLocked:
			return
		nkLink = self['genreList'].getCurrent()[0][2]
		nkTitle = self['genreList'].getCurrent()[0][0]
		sref = eServiceReference(0x1001, 0, nkLink)
		sref.setName(nkTitle)
		self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()