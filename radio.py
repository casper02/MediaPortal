from imports import *
from decrypt import *

def radiostreamListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 580, 25, 0, RT_HALIGN_LEFT, entry[0])
		]
def radioplayListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 580, 25, 0, RT_HALIGN_LEFT, entry[0])
		]

class Radiode(Screen):
	skin = 	"""
		<screen name="Radio.de" position="center,center" size="900,580" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,80" backgroundColor="#00242424"/>
			<widget name="title" position="25,15" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;26" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="730,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;26" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="580,20" size="300,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;18" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="leftContentTitle" position="0,80" size="440,26" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center"/>
			<widget name="streamlist" position="0,106" size="440,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<widget name="rightContentTitle" position="460,80" size="440,26" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center"/>		
			<widget name="playlist" position="460,106" size="440,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<widget name="stationIcon" position="20,465" zPosition="1" size="60,60" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png"/>
			<eLabel text="Play" position="120,470" size="120,25" backgroundColor="#00101214" transparent="1" foregroundColor="#00555556" font="Regular;20" valign="top"/>
			<widget name="stationInfo" position="240,470" size="450,25" backgroundColor="#00101214" foregroundColor="#00e5b243" transparent="1" font="Regular;20" valign="top"/>
			<widget source="session.CurrentService" render="Label" position="750,470" size="120,25" font="Regular;20" foregroundColor="#00e5b243" backgroundColor="#00101214" halign="right" valign="top" transparent="1">
				<convert type="ServicePosition">Position</convert>
			</widget>
			<eLabel text="Info" position="120,500" size="120,25" backgroundColor="#00101214" foregroundColor="#00555556" transparent="1" font="Regular;20" valign="top"/>
			<widget name="stationDesc" position="240,500" zPosition="1" size="640,60" backgroundColor="#00101214" transparent="1" font="Regular;19" halign="left" valign="top"/>		
	        </screen>
		"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up"    : self.keyUp,
			"down"  : self.keyDown,
			"left"  : self.keyLeft,
			"right" : self.keyRight,
			"leavePlayer" : self.keyStop,
			"nextBouquet" : self.keySwitchList,
			"prevBouquet" : self.keySwitchList,
			"green" : self.keyAdd,
			"red" : self.keyDel
		}, -1)
		
		self['title'] = Label("Radio.de - Radio online hoeren")
		self['leftContentTitle'] = Label("S e n d e r l i s t e")
		self['rightContentTitle'] = Label("P l a y l i s t")
		self['stationIcon'] = Pixmap()
		self['stationInfo'] = Label("")
		self['stationDesc'] = Label("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.playList = []
		self.playMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.playMenuList.l.setFont(0, gFont('Regular', 24))
		self.playMenuList.l.setItemHeight(25)
		self['playlist'] = self.playMenuList
		
		self.currentList = "playlist"
		self.keyLocked = False
		self.playing = False
		self.lastservice = session.nav.getCurrentlyPlayingServiceReference()
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.keyLocked = True
		self.loadStations("streamlist")
		self.loadStations("playlist")
		self["streamlist"].selectionEnabled(0)
		self["playlist"].selectionEnabled(1)
		
	def loadStations(self, list):
		print list
		if list == "streamlist":
			self.streamList = []
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/radiode_sender"
		else:
			self.playList = []
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/radiode_playlist"
			
		if fileExists(path):
			readStations = open(path,"r")
			for rawData in readStations.readlines():
				data = re.findall('"(.*?)" "(.*?)" "(.*?)" "(.*?)"', rawData, re.S)
				if data:
					(stationName, stationLink, stationImage, stationDesc) = data[0]
					if list == "streamlist":
						self.streamList.append((stationName, stationLink, stationImage, stationDesc))
					else:
						self.playList.append((stationName, stationLink, stationImage, stationDesc))
			if list == "streamlist":
				self.streamList.sort()
				self.streamMenuList.setList(map(radiostreamListEntry, self.streamList))
			else:
				self.playList.sort()
				self.playMenuList.setList(map(radioplayListEntry, self.playList))
				
			readStations.close()

			exist = self[list].getCurrent()
			if exist != None:
				stationImage = self[list].getCurrent()[0][2]
				self.stationIconRead(stationImage)
				stationDesc = self[list].getCurrent()[0][3]
				self['stationDesc'].setText(stationDesc)
				
			self.keyLocked = False


	def stationIconRead(self, stationIconLink):
		downloadPage(stationIconLink, "/tmp/stationIcon.jpg").addCallback(self.statonIconShow)
		
	def statonIconShow(self, picData):
		if fileExists("/tmp/stationIcon.jpg"):
			self['stationIcon'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['stationIcon'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/stationIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['stationIcon'].instance.setPixmap(ptr.__deref__())
					self['stationIcon'].show()
					del self.picload

	def keySwitchList(self):
		if self.currentList == "streamlist":
			self["streamlist"].selectionEnabled(0)
			self["playlist"].selectionEnabled(1)
			self.currentList = "playlist"
		else:
			self["playlist"].selectionEnabled(0)
			self["streamlist"].selectionEnabled(1)
			self.currentList = "streamlist"
			
	def keyLeft(self):
		exist = self[self.currentList].getCurrent()
		if self.keyLocked or exist == None:
			return
		self[self.currentList].pageUp()
		stationName = self[self.currentList].getCurrent()[0][0]
		self['stationInfo'].setText(stationName)
		stationImage = self[self.currentList].getCurrent()[0][2]
		self.stationIconRead(stationImage)
		stationDesc = self[self.currentList].getCurrent()[0][3]
		self['stationDesc'].setText(decodeHtml(stationDesc))
		
	def keyRight(self):
		exist = self[self.currentList].getCurrent()
		if self.keyLocked or exist == None:
			return
		self[self.currentList].pageDown()
		stationName = self[self.currentList].getCurrent()[0][0]
		self['stationInfo'].setText(stationName)
		stationImage = self[self.currentList].getCurrent()[0][2]
		self.stationIconRead(stationImage)
		stationDesc = self[self.currentList].getCurrent()[0][3]
		self['stationDesc'].setText(decodeHtml(stationDesc))
		
	def keyUp(self):
		exist = self[self.currentList].getCurrent()
		if self.keyLocked or exist == None:
			return
		self[self.currentList].up()
		stationName = self[self.currentList].getCurrent()[0][0]
		self['stationInfo'].setText(stationName)
		stationImage = self[self.currentList].getCurrent()[0][2]
		self.stationIconRead(stationImage)
		stationDesc = self[self.currentList].getCurrent()[0][3]
		self['stationDesc'].setText(decodeHtml(stationDesc))
		
	def keyDown(self):
		exist = self[self.currentList].getCurrent()
		if self.keyLocked or exist == None:
			return
		self[self.currentList].down()
		stationName = self[self.currentList].getCurrent()[0][0]
		self['stationInfo'].setText(stationName)
		stationImage = self[self.currentList].getCurrent()[0][2]
		self.stationIconRead(stationImage)
		stationDesc = self[self.currentList].getCurrent()[0][3]
		self['stationDesc'].setText(decodeHtml(stationDesc))

	def keyOK(self):
		exist = self[self.currentList].getCurrent()
		if self.keyLocked or exist == None:
			return
			
		stationUrl = self[self.currentList].getCurrent()[0][1]
		print stationUrl
		getPage(stationUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getStreamTOmp3).addErrback(self.dataError)

	def dataError(self, error):
		print error
		
	def getStreamTOmp3(self, data):
		#data = urllib.urlopen(stationUrl).read()
		if re.match('.*?"stream"', data, re.S):
			pattern = re.compile('"stream":"(.*?)"')
			stationStream = pattern.findall(data, re.S)
			if stationStream:
				print stationStream[0]
				stationName = self['streamlist'].getCurrent()[0][0]
				sref = eServiceReference(0x1001, 0, stationStream[0])
				sref.setName(stationName)
				self.session.nav.playService(sref)
				self.playing = True

	def keyAdd(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None or self.currentList == "playlist":
			return
		stationName = self['streamlist'].getCurrent()[0][0]
		stationLink = self['streamlist'].getCurrent()[0][1]
		stationImage = self['streamlist'].getCurrent()[0][2]
		stationDesc = self['streamlist'].getCurrent()[0][3]

		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/radiode_playlist"
		if fileExists(path):
			writePlaylist = open(path,"a")
			writePlaylist.write('"%s" "%s" "%s" "%s"\n' % (stationName, stationLink, stationImage, stationDesc))
			writePlaylist.close()
			self.loadStations("playlist")

	def keyDel(self):
		exist = self['playlist'].getCurrent()
		if self.keyLocked or exist == None or self.currentList == "streamlist":
			self["playlist"].selectionEnabled(0)
			self["streamlist"].selectionEnabled(1)
			self.currentList = "streamlist"
			return
		
		selectedName = self['playlist'].getCurrent()[0][0]
		
		pathTmp = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/radiode_playlist.tmp"
		writeTmp = open(pathTmp,"w")
		
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/radiode_playlist"
		if fileExists(path):
			readStations = open(path,"r")
			for rawData in readStations.readlines():
				data = re.findall('"(.*?)" "(.*?)" "(.*?)" "(.*?)"', rawData, re.S)
				if data:
					(stationName, stationLink, stationImage, stationDesc) = data[0]
					if stationName != selectedName:
						writeTmp.write('"%s" "%s" "%s" "%s"\n' % (stationName, stationLink, stationImage, stationDesc))
			readStations.close()
			writeTmp.close()
			shutil.move(pathTmp, path)
			self.loadStations("playlist")
			exist = self['playlist'].getCurrent()
			if exist == None:
				self["playlist"].selectionEnabled(0)
				self["streamlist"].selectionEnabled(1)
				self.currentList = "streamlist"
			
	def keyStop(self):
		if self.playing:
			self.session.nav.stopService()
			self.session.nav.playService(self.lastservice)
			self.playing = False
				
	def keyCancel(self):
		if self.playing:
			self.session.nav.stopService()
			self.session.nav.playService(self.lastservice)
			self.playing = False
		self.close()