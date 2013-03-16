from imports import *
from decrypt import *

def failListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]
		
class failScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/failScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/failScreen.xml"
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
			"prevBouquet" : self.keyPageDown,
			"green" : self.keyPageNumber
		}, -1)
		
		self.keyLocked = True
		self.page = 1
		self['title'] = Label("Fail.to")
		self['roflPic'] = Pixmap()
		self['name'] = Label("")
		self['page'] = Label("1")
		self.flListe = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['roflList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.keyLocked = True
		url = "http://www.fail.to/genre/1-videos/p-%s" % str(self.page)
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def loadPageData(self, data):
		parse = re.search('<body>(.*?)Fan werden', data, re.S)
		flVideos = re.findall('class="entry">.*?</span><a href="(.*?)" title=".*?">(.*?)</a></h3>.*?class="preview".*?<img src="(.*?)"', parse.group(1), re.S)
		if flVideos:
			self.flListe = []
			for (flUrl, flTitle, flImage) in flVideos:
				flUrl = "http://www.fail.to" + flUrl
				flImage = "http://www.fail.to" + flImage
				self.flListe.append((flTitle, flUrl, flImage))
			self.chooseMenuList.setList(map(failListEntry, self.flListe))
			self.keyLocked = False
			self.showPic()

	def dataError(self, error):
		print error
		
	def showPic(self):
		flTitle = self['roflList'].getCurrent()[0][0]
		flPicLink = self['roflList'].getCurrent()[0][2]
		self['name'].setText(flTitle)
		self['page'].setText(str(self.page))
		downloadPage(flPicLink, "/tmp/flPic.jpg").addCallback(self.roflCoverShow)
		
	def roflCoverShow(self, data):
		if fileExists("/tmp/flPic.jpg"):
			self['roflPic'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['roflPic'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/flPic.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['roflPic'].instance.setPixmap(ptr.__deref__())
					self['roflPic'].show()
					del self.picload

	def keyPageNumber(self):
		self.session.openWithCallback(self.callbackkeyPageNumber, VirtualKeyBoard, title = (_("Seitennummer eingeben")), text = str(self.page))

	def callbackkeyPageNumber(self, answer):
		if answer is not None:
			self.page = int(answer)
			self.loadPage()

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
		flURL = self['roflList'].getCurrent()[0][1]
		getPage(flURL, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)

	def parseData(self, data):
		flTitle = self['roflList'].getCurrent()[0][0]
		flStream = re.findall("'file': '(.*?)'", data)
		if flStream:
			rflStream = "http://www.fail.to" + flStream[0]
			print rflStream
			sref = eServiceReference(0x1001, 0, rflStream)
			sref.setName(flTitle)
			self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()