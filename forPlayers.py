##Thanks to Tristan Fischer for XBMC-API (sphere@dersphere.de)
from imports import *
from decrypt import *

from resources.lib.api import VuBox4PlayersApi, NetworkError, SYSTEMS

api = VuBox4PlayersApi()

def forPlayersGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

class forPlayersGenreScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/forPlayersGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/forPlayersGenreScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
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
		self.selectionListe.append(("Meistgesehene Videos", "2"))
		self.selectionListe.append(("Letzte Reviews", "3"))
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
	
	def __init__(self, session, selectionLink):
		self.session = session
		self.selectionLink = selectionLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/forPlayersVideoScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/forPlayersVideoScreen.xml"
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
			"info"  : self.keyInfo,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown
		}, -1)
		
		self.page = 1
		self['title'] = Label("4Players")
		self['name'] = Label("")
		self['page'] = Label("1")
		self['playersPic'] = Pixmap()
		self.juengstTS = ''
		self.page = 1
		self.videosListe = []
		self.videosQueue = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['videosList'] = self.chooseMenuList
		self.onLayoutFinish.append(self.loadVideos)
		
	def loadVideos(self):
		if self.selectionLink == '1':
			try:
				limit = int(50)
				api.set_systems(SYSTEMS)#Videos zu allen Systeme
				videos = api.get_latest_videos(limit)
				self.videosQueue.append((self.page, videos))
				self.juengstTS = min((v['ts'] for v in videos))
				self.showData(videos)
			except NetworkError:
				print 'Fehler API-Call...'
				self.videosListe.append(('4Players nicht verfuegbar....', "", "", ""))
				self.chooseMenuList.setList(map(forPlayersVideoListEntry, self.videosListe))
		elif self.selectionLink == '2':
			try:
				limit = int(150)
				api.set_systems(SYSTEMS)#Videos zu allen Systeme
				videos = api.get_popular_videos(limit)
				self.showData(videos)
			except NetworkError:
				print 'Fehler API-Call...'
				self.videosListe.append(('4Players nicht verfuegbar....', "", "", ""))
				self.chooseMenuList.setList(map(forPlayersVideoListEntry, self.videosListe))
		elif self.selectionLink == '3':
			try:
				limit = int(150)
				api.set_systems(SYSTEMS)#Videos zu allen Systeme
				videos = api.get_latest_reviews(older_than=0)
				self.showData(videos)
			except NetworkError:
				print 'Fehler API-Call...'
				self.videosListe.append(('4Players nicht verfuegbar....', "", "", ""))
				self.chooseMenuList.setList(map(forPlayersVideoListEntry, self.videosListe))
				
	def showData(self, videos):
		for video in videos:
			gameTitle = str(video['game']['title'])
			videoTitle = str(video['video_title'])
			videoStreamUrl = video['streams']['hq']['url']
			videoDate = video['date']
			videoPic = video['thumb']
			gameId = video['game']['id']
			gameStudio = video['game']['studio']
			videoTitleConv = gameTitle + ' - ' + videoTitle + ' ' + '(' + videoDate + ')'
			self.videosListe.append((videoTitleConv, videoStreamUrl, videoPic, videoTitle, gameId, gameStudio, gameTitle))
		self.chooseMenuList.setList(map(forPlayersVideoListEntry, self.videosListe))
		self.showPic()
		
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

	def loadPage(self):
		if self.selectionLink == '1':
			self.videosListe = []
			self.queuedVideoList = []
			for queuedEntry in self.videosQueue:
				if queuedEntry[0] == self.page:
					self.queuedVideoList = queuedEntry[1]
			if self.queuedVideoList:
				self.showData(self.queuedVideoList)
			else:
				try:
						api.set_systems(SYSTEMS)#Videos zu allen Systeme
						videos = api.get_latest_videos(older_than=self.juengstTS)
						self.juengstTS = min((v['ts'] for v in videos))
						self.videosQueue.append((self.page, videos))
						self.showData(videos)
				except NetworkError:
						print 'Fehler API-Call...'
						self.videosListe.append(('4Players nicht verfuegbar....', "", "", ""))
						self.chooseMenuList.setList(map(forPlayersVideoListEntry, self.videosListe))

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
		
	def keyInfo(self):
		text = []
		gameStudio = self['videosList'].getCurrent()[0][5]
		gameId = self['videosList'].getCurrent()[0][4]
		gameTitle = self['videosList'].getCurrent()[0][6]
		gameInfoCol = api._get_game_info(gameId)
		text.append('Titel: ' + str(gameTitle))
		text.append('\n')
		text.append('Studion: ' + str(gameStudio))
		text.append('\n')
		for info in gameInfoCol:
			gamePub = info['publisher']
			text.append('Publisher: ' + str(gamePub))
			text.append('\n')
			for system in info['systeme']:
				gameSys = system['system']
				text.append('Plattform: ' + str(gameSys))
				text.append('\n')
				text.append('Release: ' + str(system['releasetag']) + '.' + str(system['releasemonat']) + '.' + str(system['releasejahr']))
				text.append('\n')
				text.append('USK: ' + str(system['usk']))
				text.append('\n')
		sText = ''.join(text)
		print sText
		self.session.open(MessageBox,_(sText), MessageBox.TYPE_INFO)
		
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
