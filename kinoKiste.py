from imports import *
from decrypt import *

def kinokisteGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

class kinokisteGenreScreen(Screen):
	skin = 	"""
		<screen name="KinoKiste" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="genreList" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,440" size="160,120" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
		</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		
		self['title'] = Label("KinoKiste")
		self['name'] = Label("Genre Auswahl")
		self['coverArt'] = Pixmap()
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.genreliste.append(("Kinofilme", "http://kkiste.to/aktuelle-kinofilme/"))
		self.genreliste.append(("Filmlisten", "http://kkiste.to/film-index/"))

		self.chooseMenuList.setList(map(kinokisteGenreListEntry, self.genreliste))

	def keyOK(self):
		kkName = self['genreList'].getCurrent()[0][0]
		kkUrl = self['genreList'].getCurrent()[0][1]
		if kkName == "Kinofilme":
			self.session.open(kinokisteKinoScreen)
		else:
			self.session.open(kinokisteFilmlistenScreen)
			
	def keyCancel(self):
		self.close()

def kinokisteKinoListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 

class kinokisteKinoScreen(Screen):
	skin = 	"""
		<screen name="KinoKiste" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="streamlist" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="520,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<eLabel text="Page" position="750,420" size="100,25" backgroundColor="#00101214" transparent="1" foregroundColor="#00555556" font="Regular;20" valign="top" />
			<widget name="page" position="850,420" size="30,25" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
			<widget name="handlung" position="205,473" size="680,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
		</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok" : self.keyOK,
			"cancel" : self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown
		}, -1)
		
		self['title'] = Label("KinoKiste")
		self['name'] = Label("Film Auswahl")
		self['handlung'] = Label("")
		self['page'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.page = 1
		self.filmeliste = []
		self.keyLocked = True
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['streamlist'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadpage)
		
	def loadpage(self):
		self.keyLocked = True
		self.filmeliste = []
		url = "http://kkiste.to/aktuelle-kinofilme/?page=%s" % str(self.page)
		self['page'].setText(str(self.page))
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.filmData).addErrback(self.dataError)
		
	def filmData(self, data):
		kkDaten = re.findall('<a href="(.*?)" title="Jetzt (.*?) Stream ansehen" class="image">\n<img src="(.*?)"', data)
		if kkDaten:
			for (kkUrl,kkTitle,kkImage) in kkDaten:
				kkUrl = "http://www.kkiste.to%s" % kkUrl
				self.filmeliste.append((kkTitle, kkUrl, kkImage))
			self.chooseMenuList.setList(map(kinokisteKinoListEntry, self.filmeliste))
			self.keyLocked = False
			self.showInfos()
			
	def dataError(self, error):
		print error
		
	def showInfos(self):
		kkTitle = self['streamlist'].getCurrent()[0][0]
		self['name'].setText(kkTitle)
		kkUrl = self['streamlist'].getCurrent()[0][1]
		kkImage = self['streamlist'].getCurrent()[0][2]
		kkImageUrl = "http://kkiste.to%s" % kkImage
		print kkImageUrl.replace('_170_120','_145_215')
		downloadPage(kkImageUrl.replace('_170_120','_145_215'), "/tmp/kkIcon.jpg").addCallback(self.kkCoverShow)
		getPage(kkUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getDescription).addErrback(self.dataError)
		
	def getDescription(self, data):
		ddDescription = re.findall('<meta name="description" content="(.*?)"', data, re.S)
		if ddDescription:
			self['handlung'].setText(ddDescription[0])
		else:
			self['handlung'].setText("keine infos.")
			
	def kkCoverShow(self, picData):
		if fileExists("/tmp/kkIcon.jpg"):
			self['coverArt'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/kkIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr.__deref__())
					self['coverArt'].show()
					del self.picload

	def keyOK(self):
		if self.keyLocked:
			return
		kkName = self['streamlist'].getCurrent()[0][0]
		kkUrl = self['streamlist'].getCurrent()[0][1]
		getPage(kkUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getParts).addErrback(self.dataError)
		
	def getParts(self, data):
		kkName = self['streamlist'].getCurrent()[0][0]
		streams = re.findall('<a href="(http://www.ecostream.tv/stream/.*?)"', data, re.S)
		if streams:
			self.session.open(kinokistePartsScreen, streams, kkName)
	
	def keyPageDown(self):
		print "PageDown"
		if self.keyLocked:
			return
		if not self.page < 2:
			self.page -= 1
			self.loadpage()
		
	def keyPageUp(self):
		print "PageUP"
		if self.keyLocked:
			return
		self.page += 1
		self.loadpage()
		
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
		
def kinokistePartsListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

class kinokistePartsScreen(Screen):
	skin = 	"""
		<screen name="KinoKiste" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="genreList" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="160,120" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
		</screen>"""

	def __init__(self, session, parts, stream_name):
		self.session = session
		self.parts = parts
		self.stream_name = stream_name
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("KinoKiste")
		self['name'] = Label("Parts Auswahl")
		self['coverArt'] = Pixmap()
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		self.keyLocked = False
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		print self.parts
		self.parts = list(set(self.parts)) # remove dupes
		self.parts.sort() # sortieren
		self.count_disks = 0
		for part in self.parts:
			self.count_disks += 1
			partsName = "PART %s" % self.count_disks
			print partsName, part
			self.genreliste.append((partsName, part))
		
		self.chooseMenuList.setList(map(kinokistePartsListEntry, self.genreliste))

	def keyOK(self):
		if self.keyLocked:
			return
		kkLink = self['genreList'].getCurrent()[0][1]
		print kkLink
		self.keyLocked = True
		getPage(kkLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.eco_read).addErrback(self.dataError)
		
	def eco_read(self, data):
		post_url = re.findall('<form name="setss" method="post" action="(.*?)">', data, re.S)
		if post_url:
			info = urlencode({'': '1', 'sss': '1'})
			print info
			getPage(post_url[0], method='POST', postdata=info, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.eco_post).addErrback(self.dataError)
			
	def eco_post(self, data):
		url = "http://www.ecostream.tv/assets/js/common.js"
		data2 = urllib.urlopen(url).read()
		post_url = re.findall("url: '(http://www.ecostream.tv/.*?)\?s=", data2, re.S)
		if post_url:
			print post_url
			sPattern = "var t=setTimeout\(\"lc\('([^']+)','([^']+)','([^']+)','([^']+)'\)"
			r = re.findall(sPattern, data)
			if r:
				for aEntry in r:
					sS = str(aEntry[0])
					sK = str(aEntry[1])
					sT = str(aEntry[2])
					sKey = str(aEntry[3])

				print "current keys:", sS, sK, sT, sKey
				sNextUrl = post_url[0]+"?s="+sS+'&k='+sK+'&t='+sT+'&key='+sKey
				print sNextUrl
				info = urlencode({'s': sS, 'k': sK, 't': sT, 'key': sKey})
				print info
				getPage(sNextUrl, method='POST', postdata = info, headers={'Referer':'http://www.ecostream.tv', 'X-Requested-With':'XMLHttpRequest'}).addCallback(self.eco_final).addErrback(self.dataError)
		else:
			print "no post url.."
	
	def eco_final(self, data):
		part = self['genreList'].getCurrent()[0][0]
		stream_url = re.findall('flashvars="file=(.*?)&', data)
		if stream_url:
			kkStreamUrl = "http://www.ecostream.tv"+stream_url[0]+"&start=0"
			kkStreamUrl = urllib2.unquote(kkStreamUrl)
			print kkStreamUrl
			req = urllib2.Request(kkStreamUrl)
			res = urllib2.urlopen(req)
			finalurl = res.geturl()
			print finalurl
			streamname = "%s - %s" % (self.stream_name, part)
			sref = eServiceReference(0x1001, 0, finalurl)
			sref.setName(streamname)
			self.session.open(MoviePlayer, sref)
			
	def dataError(self, error):
		print error
		
	def keyCancel(self):
		self.close()

def kinokisteFilmlistenListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

class kinokisteFilmlistenScreen(Screen):
	skin = 	"""
		<screen name="KinoKiste" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="genreList" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,440" size="160,120" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
		</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("KinoKiste")
		self['name'] = Label("FilmListen Auswahl")
		self['coverArt'] = Pixmap()
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		abc = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9"]
		for letter in abc:
			kkLink = "http://kkiste.to/film-index/%s/" % letter
			self.genreliste.append((letter, kkLink))
		self.chooseMenuList.setList(map(kinokisteFilmlistenListEntry, self.genreliste))

	def keyOK(self):
		kkLink = self['genreList'].getCurrent()[0][1]
		print kkLink
		self.session.open(kinokisteFilmLetterScreen, kkLink)

	def keyCancel(self):
		self.close()		

def kinokisteFilmLetterListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 500, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0]),
		(eListboxPythonMultiContent.TYPE_TEXT, 520, 0, 150, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[1]),
		(eListboxPythonMultiContent.TYPE_TEXT, 670, 0, 150, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[2])
		] 

class kinokisteFilmLetterScreen(Screen):
	skin = 	"""
		<screen name="KinoKiste" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="genreList" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,440" size="160,120" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<eLabel text="Page" position="750,420" size="100,25" backgroundColor="#00101214" transparent="1" foregroundColor="#00555556" font="Regular;20" valign="top" />
			<widget name="page" position="850,420" size="30,25" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
			<widget name="handlung" position="205,473" size="680,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
		</screen>"""

	def __init__(self, session, kkLink):
		self.session = session
		self.kkLink = kkLink
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok" : self.keyOK,
			"cancel" : self.keyCancel,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown
		}, -1)

		self['title'] = Label("KinoKiste")
		self['name'] = Label("Film Auswahl")
		self['page'] = Label("1")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		self.keyLocked = True
		self.page = 1
		
		self.onLayoutFinish.append(self.loadpage)
		
	def loadpage(self):
		self.genreliste = []
		self['page'].setText(str(self.page))
		kkLink = "%s?page=%s" % (self.kkLink, str(self.page))
		print kkLink
		getPage(kkLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.pageData).addErrback(self.dataError)
		
	def pageData(self, data):
		kkMovies = re.findall('<li class="mbox list".*?<a href="(.*?)" title="Jetzt (.*?) Stream ansehen".*?<p class="year">(.*?)</p>\n<p class="genre">(.*?)</p>', data, re.S)
		if kkMovies:
			for (kkUrl,kkTitle,kkYear,kkGenre) in kkMovies:
				kkUrl = "http://kkiste.to%s" % kkUrl
				self.genreliste.append((kkTitle, kkYear, kkGenre, kkUrl))
			self.chooseMenuList.setList(map(kinokisteFilmLetterListEntry, self.genreliste))
			self.keyLocked = False

	def dataError(self, error):
		print error
		
	def keyPageDown(self):
		print "PageDown"
		if self.keyLocked:
			return
		if not self.page < 2:
			self.page -= 1
			self.loadpage()
		
	def keyPageUp(self):
		print "PageUP"
		if self.keyLocked:
			return
		self.page += 1
		self.loadpage()
		
	def keyOK(self):
		if self.keyLocked:
			return
		kkLink = self['genreList'].getCurrent()[0][3]
		print kkLink
		getPage(kkLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getParts).addErrback(self.dataError)
		
	def getParts(self, data):
		kkName = self['genreList'].getCurrent()[0][0]
		streams = re.findall('<a href="(http://www.ecostream.tv/stream/.*?)"', data, re.S)
		print streams
		if streams:
			self.session.open(kinokistePartsScreen, streams, kkName)

	def keyCancel(self):
		self.close()