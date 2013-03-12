from imports import *

def LiveLeakEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]
		
class LiveLeakScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/LiveLeakScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/LiveLeakScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['title'] = Label("LiveLeak.com")
		self['Pic'] = Pixmap()
		self['name'] = Label("Genre Auswahl")
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['List'] = self.chooseMenuList

		self.onLayoutFinish.append(self.layoutFinished)

	def layoutFinished(self):
		self.genreliste.append(("Featured Items", "http://www.liveleak.com/rss?featured=1&page="))
		self.genreliste.append(("Recent Items (All)", "http://www.liveleak.com/rss?selection=all&page="))
		self.genreliste.append(("Recent Items (Popular)", "http://www.liveleak.com/rss?selection=popular&page="))
		self.genreliste.append(("Top (Today)", "http://www.liveleak.com/rss?rank_by=day&page="))
		self.genreliste.append(("Top (Week)", "http://www.liveleak.com/rss?rank_by=week&page="))
		self.genreliste.append(("Top (Month)", "http://www.liveleak.com/rss?rank_by=month&page="))
		self.genreliste.append(("Top (All)", "http://www.liveleak.com/rss?rank_by=all_time&page="))
		self.genreliste.append(("Must See", "http://www.liveleak.com/rss?channel_token=9ee_1303244161&page="))
		self.genreliste.append(("Yoursay", "http://www.liveleak.com/rss?channel_token=1b3_1302956579&page="))
		self.genreliste.append(("News", "http://www.liveleak.com/rss?channel_token=04c_1302956196&page="))
		self.genreliste.append(("Entertainment", "http://www.liveleak.com/rss?channel_token=51a_1302956523&page="))
		self.chooseMenuList.setList(map(LiveLeakEntry, self.genreliste))

	def keyOK(self):
		streamGenreLink = self['List'].getCurrent()[0][1]
		print streamGenreLink
		self.session.open(LiveLeakClips, streamGenreLink)

	def keyCancel(self):
		self.close()

class LiveLeakClips(Screen):

	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/LiveLeakScreenClips.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/LiveLeakScreenClips.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up"    : self.keyUp,
			"down"  : self.keyDown,
			"left"  : self.keyLeft,
			"right" : self.keyRight,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown
		}, -1)
		
		self.keyLocked = True
		self.page = 1
		self['title'] = Label("LiveLeak.com")
		self['Pic'] = Pixmap()
		self['name'] = Label("")
		self['page'] = Label("1")
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['List'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.keyLocked = True
		url = "%s%s" % (self.streamGenreLink, str(self.page))
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def loadPageData(self, data):
		rssfeed = re.findall('<title>(.*?)</title>.*?<link>(http://www.liveleak.com/view.*?)</link>.*?<media:thumbnail url="(.*?)"', data, re.S)
		if rssfeed:
			self.feedliste = []
			for (lltitle,llurl,llimage) in rssfeed:
				if not re.match('LiveLeak.com Rss Feed', lltitle, re.S|re.I):
					self.feedliste.append((lltitle,llurl,llimage))
			self.chooseMenuList.setList(map(LiveLeakEntry, self.feedliste))
			self.keyLocked = False
			self.showPic()

	def dataError(self, error):
		print error
		
	def showPic(self):
		llTitle = self['List'].getCurrent()[0][0]
		llPicLink = self['List'].getCurrent()[0][2]
		self['name'].setText(llTitle)
		self['page'].setText(str(self.page))
		downloadPage(llPicLink, "/tmp/Pic.jpg").addCallback(self.ShowImage)
		
	def ShowImage(self, data):
		if fileExists("/tmp/Pic.jpg"):
			self['Pic'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['Pic'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/Pic.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['Pic'].instance.setPixmap(ptr.__deref__())
					self['Pic'].show()
					del self.picload

	def keyPageDown(self):
		print "PageDown"
		if self.keyLocked:
			return
		if not self.page < 2:
			self.page -= 1
			self.loadPage()
		
	def keyPageUp(self):
		print "PageUP"
		if self.keyLocked:
			return
		if not self.page > 2:
			self.page += 1
			self.loadPage()
		
	def keyLeft(self):
		if self.keyLocked:
			return
		self['List'].pageUp()
		self.showPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['List'].pageDown()
		self.showPic()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['List'].up()
		self.showPic()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['List'].down()
		self.showPic()
		
	def keyOK(self):
		if self.keyLocked:
			return
		llUrl = self['List'].getCurrent()[0][1]
		print llUrl
		getPage(llUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)

	def parseData(self, data):
		llTitle = self['List'].getCurrent()[0][0]
		Stream = re.findall('file: "(.*?)"', data, re.S)
		if Stream:
			print Stream
			sref = eServiceReference(0x1001, 0, Stream[0])
			sref.setName(llTitle)
			self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()