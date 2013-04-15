from Plugins.Extensions.MediaPortal.resources.imports import *

def sportBildListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]
		
class sportBildScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/sportBildScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/sportBildScreen.xml"
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
		self.page = 0
		self['title'] = Label("SportBild.de")
		self['roflPic'] = Pixmap()
		self['name'] = Label("")
		self['page'] = Label("1")
		self['runtime'] = Label("")
		self['date'] = Label("")
		self.spListe = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['roflList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.keyLocked = True
		url = "http://sportbild.bild.de/SPORT/video/clip/video-home/teaser-alle-videos,templateId=renderVideoChannelList,page=%s,rootDocumentId=13275342.html" % str(self.page)
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def loadPageData(self, data):
		spVideos = re.findall('<a href="(/SPORT/video.*?)" target="btobody"><img src="(.*?.jpg)".*?<div class="bdeVideoDachzeile">(.*?)</div>.*?<div class="bdeVideoTeaser11 bdeVideoTime">(.*?)</div>.*?<div class="bdeVideoTeaser11 bdeVideoDate">(.*?)</div>', data, re.S)
		print spVideos
		if spVideos:
			self.spListe = []
			for (spUrl,spImage,spTitle,spRuntime,spDate) in spVideos:
				spImage = "http://sportbild.bild.de" + spImage
				self.spListe.append((decodeHtml(spTitle), spUrl, spImage, spRuntime, spDate))
			self.chooseMenuList.setList(map(sportBildListEntry, self.spListe))
			self.keyLocked = False
			self.showPic()

	def dataError(self, error):
		print error
		
	def showPic(self):
		spTitle = self['roflList'].getCurrent()[0][0]
		spPicLink = self['roflList'].getCurrent()[0][2]
		spRuntime = self['roflList'].getCurrent()[0][3]
		spDate = self['roflList'].getCurrent()[0][4]
		self['name'].setText(spTitle)
		self['page'].setText(str(self.page))
		self['date'].setText(spDate)
		self['runtime'].setText(spRuntime)
		downloadPage(spPicLink, "/tmp/spPic.jpg").addCallback(self.roflCoverShow)
		
	def roflCoverShow(self, data):
		if fileExists("/tmp/spPic.jpg"):
			self['roflPic'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['roflPic'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/spPic.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['roflPic'].instance.setPixmap(ptr.__deref__())
					self['roflPic'].show()
					del self.picload

	def keyPageDown(self):
		print "PageDown"
		if self.keyLocked:
			return
		if not self.page < 1:
			self.page -= 1
			self.loadPage()
		
	def keyPageUp(self):
		print "PageUP"
		if self.keyLocked:
			return
		self.page += 1
		self.loadPage()
		
	def keyLeft(self):
		if self.keyLocked:
			return
		self['roflList'].pageUp()
		self.showPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['roflList'].pageDown()
		self.showPic()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['roflList'].up()
		self.showPic()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['roflList'].down()
		self.showPic()
		
	def keyOK(self):
		if self.keyLocked:
			return
		spUrl = self['roflList'].getCurrent()[0][1]
		spUrl = re.sub('seite=.*?html','templateId=renderJavaScript,layout=17,startvideo=true.js',spUrl)
		#url = "http://sportbild.bild.de" + spUrl.replace('seite=*.html','templateId=renderJavaScript,layout=17,startvideo=true.js')
		url = "http://sportbild.bild.de" + spUrl
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)

	def parseData(self, data):
		spTitle = self['roflList'].getCurrent()[0][0]
		spStream = re.findall('src="(http://.*?[mp4|flv])"', data, re.S)
		if spStream:
			print spStream
			sref = eServiceReference(0x1001, 0, spStream[0])
			sref.setName(spTitle)
			self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()
