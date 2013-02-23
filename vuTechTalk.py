from imports import *
from decrypt import *

def vutechtalkListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 830, 25, 0, RT_HALIGN_LEFT, entry[0])
		]

class vutechtalk(Screen):
	skin = 	"""
		<screen name="Vutechtalk.com" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="leftContentTitle" position="0,60" size="900,25" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center"/>
			<widget name="streamlist" position="0,85" size="900,325" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="stationIcon" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="520,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="205,473" size="680,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />		
			</screen>
		"""
		
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)
		
		self['title'] = Label("Vutechtalk.com")
		self['leftContentTitle'] = Label("Videos:")
		self['stationIcon'] = Pixmap()
		self['name'] = Label("")
		self['handlung'] = Label("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.streamList = []
		url = "http://vutechtalk.com/feed/"
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		videos = re.findall('<item>.*?<title>(.*?)</title>.*?<link>(.*?)</link>.*?<enclosure url="(.*?)".*?<itunes:summary>(.*?)<',data, re.S)
		if videos:
			for (title,url,stream,handlung) in videos:
				print title
				if title != "VU Techtalk":
					self.streamList.append((decodeHtml(title),url,handlung,stream))
			self.streamMenuList.setList(map(vutechtalkListEntry, self.streamList))
			self.keyLocked = False
			self.showInfos()
					
	def dataError(self, error):
		print error
			
	def showInfos(self):
		self.Dscname = self['streamlist'].getCurrent()[0][0]
		handlung = self['streamlist'].getCurrent()[0][2]
		url = self['streamlist'].getCurrent()[0][1]
		self['handlung'].setText(decodeHtml(handlung))
		self['name'].setText(self.Dscname)
		if url:
			print url
			getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getImage).addErrback(self.dataError)
			
	def getImage(self, data):
		image = re.findall('<img class="postimg" src=".*?src=(.*?.png)', data, re.S)
		if image:
			print image[0]
			downloadPage(image[0], "/tmp/dscIcon.jpg").addCallback(self.showCover)
		
	def showCover(self, picData):
		if fileExists("/tmp/dscIcon.jpg"):
			self['stationIcon'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['stationIcon'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/dscIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['stationIcon'].instance.setPixmap(ptr.__deref__())
					self['stationIcon'].show()
					del self.picload			

	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		stream = self['streamlist'].getCurrent()[0][3]
		if stream:
			print stream
			sref = eServiceReference(0x1001, 0, stream)
			sref.setName(self.Dscname)
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