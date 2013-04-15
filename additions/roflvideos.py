from Plugins.Extensions.mediaportal.resources.imports import *
from Plugins.Extensions.mediaportal.resources.decrypt import *

def auswahlListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]
		
class roflScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/roflScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/roflScreen.xml"
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
		self['title'] = Label("Rofl.to")
		self['roflPic'] = Pixmap()
		self['name'] = Label("")
		self['page'] = Label("1")
		self.roflListe = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['roflList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.keyLocked = True
		url = "http://videos.rofl.to/neue-videos/woche/%s" % str(self.page)
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def loadPageData(self, data):
		roflVideos = re.findall('<a href="(http://videos.rofl.to/clip/.*?)" rel="nofollow" title=".*?"><img src="(http://media.rofl.to/clipshots/.*?)".*?alt="(.*?)" />', data)
		if roflVideos:
			self.roflListe = []
			for roflUrl,roflPic,roflName in roflVideos:
				self.roflListe.append((decodeHtml(roflName), roflUrl, roflPic))
			self.chooseMenuList.setList(map(auswahlListEntry, self.roflListe))
			self.showPic()
			self.keyLocked = False

	def dataError(self, error):
		print error
		
	def showPic(self):
		roflPicLink = self['roflList'].getCurrent()[0][2]
		roflName = self['roflList'].getCurrent()[0][0]
		self['name'].setText(roflName)
		self['page'].setText(str(self.page))
		downloadPage(roflPicLink, "/tmp/roflPic.jpg").addCallback(self.roflCoverShow)
		
	def roflCoverShow(self, data):
		if fileExists("/tmp/roflPic.jpg"):
			self['roflPic'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['roflPic'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/roflPic.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['roflPic'].instance.setPixmap(ptr.__deref__())
					self['roflPic'].show()
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
		roflName = self['roflList'].getCurrent()[0][0]
		roflURL = self['roflList'].getCurrent()[0][1]
		data = urllib.urlopen(roflURL).read()
		roflLink = re.findall('href="(.*?.flv)"', data)
		if roflLink:
			sref = eServiceReference(0x1001, 0, roflLink[0])
			sref.setName(roflName)
			self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()