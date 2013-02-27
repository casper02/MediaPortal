from imports import *
from decrypt import *

from resources.lib.api import XBMC4PlayersApi, NetworkError

api = XBMC4PlayersApi()

def forPlayersGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

class forPlayersGenreScreen(Screen):
	skin = 	"""
		<screen name="4Players" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="selectionList" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
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
		
		self['title'] = Label("4Players")
		self['name'] = Label("Auswahl")
		self['coverArt'] = Pixmap()
		
		self.selectionListe = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['selectionList'] = self.chooseMenuList
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.selectionListe.append(("Aktuelle Videos", "1"))
		self.selectionListe.append(("Populaerste Videos", "2"))
		self.chooseMenuList.setList(map(forPlayersGenreListEntry, self.selectionListe))

	def keyOK(self):
		selectionLink = self['selectionList'].getCurrent()[0][1]
		print selectionLink
		self.session.open(forPlayersVideoScreen, selectionLink)

	def keyCancel(self):
		self.close()

def forPlayersVideoListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]
		
class forPlayersVideoScreen(Screen):
	skin = 	"""
		<screen name="4Players" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="videosList" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="playersPic" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="page" position="850,420" size="30,25" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
		</screen>"""

	def __init__(self, session, selectionLink):
		self.session = session
		self.selectionLink = selectionLink
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up"    : self.keyUp,
			"down"  : self.keyDown,
			"left"  : self.keyLeft,
			"right" : self.keyRight
		}, -1)
		
		self.page = 1
		self['title'] = Label("4Players")
		self['name'] = Label("")
		self['page'] = Label("1")
		self['playersPic'] = Pixmap()
		self.videosListe = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['videosList'] = self.chooseMenuList
		self.onLayoutFinish.append(self.loadVideos)

		
	def loadVideos(self):
		limit = int(80)
		if self.selectionLink == '1':
			videos = api.get_latest_videos(limit)
		elif self.selectionLink == '2':
			videos = api.get_popular_videos(limit)
		for video in videos:
			gameTitle = str(video['game']['title'])
			videoTitle = str(video['video_title'])
			videoStreamUrl = video['streams']['hq']['url']
			videoDate = video['date']
			#videoDuration = self.convDuration(video['duration'])###TODO: Korrektur Zeitanzeige
			videoPic = video['thumb']
			videoTitleConv = gameTitle + ' - ' + videoTitle + ' ' + '(' + videoDate + ')'
			#videoTitleConv = gameTitle + ' - ' + videoTitle + ' ' + '(' + videoDate + ' - ' + str(videoDuration) + ')'
			self.videosListe.append((videoTitleConv, videoStreamUrl, videoPic, videoTitle))
		self.chooseMenuList.setList(map(forPlayersVideoListEntry, self.videosListe))
		self.showPic()
			
#	def convDuration(self, duration):
#		s = duration
#		hours = s // 3600 
#		s = s - (hours * 3600)
#		minutes = s // 60
#		seconds = s - (minutes * 60)
#		return '%s:%s' % (minutes, seconds)
		
	def showPic(self):
		myTitle = self['videosList'].getCurrent()[0][0]
		myPicLink = self['videosList'].getCurrent()[0][2]
		self['name'].setText(str(myTitle))
		self['page'].setText(str(self.page))
		downloadPage(str(myPicLink), "/tmp/myPic.jpg").addCallback(self.playersCoverShow)
		
	def playersCoverShow(self, data):
		if fileExists("/tmp/myPic.jpg"):
			self['playersPic'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['playersPic'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/myPic.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['playersPic'].instance.setPixmap(ptr.__deref__())
					self['playersPic'].show()
					del self.picload

	def keyPageDown(self):
		print "PageDown"
		if not self.page < 2:
			self.page -= 1
			self.loadPage()
		
	def keyPageUp(self):
		print "PageUP"
		self.page += 1
		self.loadPage()
		
	def keyLeft(self):
		self['videosList'].pageUp()
		self.showPic()
		
	def keyRight(self):
		self['videosList'].pageDown()
		self.showPic()
		
	def keyUp(self):
		self['videosList'].up()
		self.showPic()
		
	def keyDown(self):
		self['videosList'].down()
		self.showPic()
		
	def keyOK(self):
		playersUrl = self['videosList'].getCurrent()[0][1]
		streamUrl = str(playersUrl)
		playersTitle = self['videosList'].getCurrent()[0][3]
		playersTitleStr = str(playersTitle)
		print playersUrl
		print streamUrl
		print playersTitle
		if playersUrl:
			sref = eServiceReference(0x1001, 0, streamUrl)
			sref.setName(playersTitleStr)
			self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()
