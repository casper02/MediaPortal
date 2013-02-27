from imports import *
from decrypt import *

def kinderKinoListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]
		
class kinderKinoScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/kinderKinoScreen.xml" % config.mediaportal.skin.value
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
		self['title'] = Label("KinderKino.de")
		self['roflPic'] = Pixmap()
		self['name'] = Label("")
		self['page'] = Label("1")
		self.kiListe = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['roflList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.keyLocked = True
		url = "http://www.kinderkino.de/kostenlos/page/%s/" % str(self.page)
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def loadPageData(self, data):
		kiVideos = re.findall('<a href="(http://www.kinderkino.de/kostenlos/kinderfilme/.*?)">.*?<figure class="thumbImg"><img.*?src="(.*?)".*?title="(.*?)[-| ].*?"', data, re.S)
		if kiVideos:
			self.kiListe = []
			for (kiUrl,kiImage,kiTitle) in kiVideos:
				self.kiListe.append((kiTitle.replace('_',' '),kiUrl,kiImage))
			self.chooseMenuList.setList(map(kinderKinoListEntry, self.kiListe))
			self.keyLocked = False
			self.showPic()

	def dataError(self, error):
		print error
		
	def showPic(self):
		kiTitle = self['roflList'].getCurrent()[0][0]
		kiPicLink = self['roflList'].getCurrent()[0][2]
		self['name'].setText(kiTitle)
		self['page'].setText(str(self.page))
		downloadPage(kiPicLink, "/tmp/kiPic.jpg").addCallback(self.roflCoverShow)
		
	def roflCoverShow(self, data):
		if fileExists("/tmp/kiPic.jpg"):
			self['roflPic'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['roflPic'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/kiPic.jpg", 0, 0, False) == 0:
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
		if not self.page > 2:
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
		kiUrl = self['roflList'].getCurrent()[0][1]
		print kiUrl
		getPage(kiUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)

	def parseData(self, data):
		kiTitle = self['roflList'].getCurrent()[0][0]
		kiStream = re.findall("file: '(http://.*?)'", data)
		if kiStream:
			print kiStream
			sref = eServiceReference(0x1001, 0, kiStream[0])
			sref.setName(kiTitle)
			self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()