from Plugins.Extensions.mediaportal.resources.imports import *
from Plugins.Extensions.mediaportal.resources.yt_url import *

def putpattvGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

def putpattvFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
		
class putpattvGenreScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/XXXGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/XXXGenreScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok" : self.keyOK,
			"cancel" : self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)

		self['title'] = Label("putpat.tv")
		self['name'] = Label("Kanal Auswahl")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.genreliste.append(("Charts", "2"))
		self.genreliste.append(("Heimat", "3"))
		self.genreliste.append(("Retro", "4"))
		self.genreliste.append(("2Rock", "5"))
		self.genreliste.append(("Vibes", "6"))
		self.genreliste.append(("Hooray!", "7"))
		self.genreliste.append(("INTRO TV", "9"))
		self.genreliste.append(("This is JAZZthing.TV", "11"))
		self.genreliste.append(("Festival Guide", "12"))
		self.genreliste.append(("SchuelerVZ", "14"))
		self.genreliste.append(("StudiVZ", "15"))
		self.genreliste.append(("MeinVZ", "16"))
		self.genreliste.append(("Rockalarm", "27"))
		self.genreliste.append(("MELT Festival", "29"))
		self.genreliste.append(("Splash! Festival", "30"))
		self.genreliste.append(("Berlin Festival", "31"))
		self.genreliste.append(("Flux TV", "34"))
		self.genreliste.append(("Rockalarm", "35"))
		self.genreliste.append(("Introducing", "36"))
		self.genreliste.append(("20 Jahre Intro", "38"))
		self.genreliste.append(("Pop10 Studioshow", "39"))
		self.genreliste.append(("Rock Hard", "41"))
		self.chooseMenuList.setList(map(putpattvGenreListEntry, self.genreliste))
		self.chooseMenuList.moveToIndex(0)
		self.keyLocked = False
		self.showInfos()

	def dataError(self, error):
		print error

	def showInfos(self):
		phTitle = self['genreList'].getCurrent()[0][0]
		phImage = self['genreList'].getCurrent()[0][1]
		if phTitle == "Flux TV" or phTitle == "Rock Hard" or phTitle == "20 Jahre Intro" or phTitle == "INTRO TV":
			phImage = 'http://files.putpat.tv/artwork/channelgraphics/%s/channellogo_invert_500.png' % phImage
		else:
			phImage = 'http://files.putpat.tv/artwork/channelgraphics/%s/channellogo_500.png' % phImage
		print phImage
		if not phImage == None:
			downloadPage(phImage, "/tmp/phIcon.jpg").addCallback(self.ShowCover)
		else:
			self.ShowCoverNone()

	def ShowCover(self, picData):
		picPath = "/tmp/phIcon.jpg"
		self.ShowCoverFile(picPath)
		
	def ShowCoverNone(self):
		picPath = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/images/no_coverArt.png" % config.mediaportal.skin.value
		self.ShowCoverFile(picPath)
		
	def ShowCoverFile(self, picPath):
		if fileExists(picPath):
			self['coverArt'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode(picPath, 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr.__deref__())
					self['coverArt'].show()
					del self.picload

	def keyOK(self):
		streamGenreLink = self['genreList'].getCurrent()[0][1]
		self.session.open(putpattvFilmScreen, streamGenreLink)
		
	def keyLeft(self):
		if self.keyLocked:
			return
		self['genreList'].pageUp()
		self.showInfos()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['genreList'].pageDown()
		self.showInfos()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['genreList'].up()
		self.showInfos()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['genreList'].down()
		self.showInfos()

	def keyCancel(self):
		self.close()

class putpattvFilmScreen(Screen):
	
	def __init__(self, session, phCatLink):
		self.session = session
		self.phCatLink = phCatLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/XXXFilmScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/XXXFilmScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok" : self.keyOK,
			"cancel" : self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)

		self['title'] = Label("putpat.tv")
		self['name'] = Label("Titel Auswahl")
		self['views'] = Label("")
		self['runtime'] = Label("")
		self['page'] = Label("")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.page = 1
		
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadpage)
		
	def loadpage(self):
		self.keyLocked = True
		self['name'].setText('Bitte warten...')
		self.filmliste = []
		url = "http://www.putpat.tv/ws.xml?method=Channel.clips&partnerId=1&client=putpatplayer&maxClips=500&channelId=%s&streamingId=tvrl&streamingMethod=http" % (self.phCatLink)
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadData).addErrback(self.dataError)
	
	def loadData(self, data):
		print data
		phMovies = re.findall('<clip>.*?<medium>(.*?)</medium>.*?<title>(.*?)</title>.*?<display-artist-title>(.*?)</display-artist-title>', data, re.S)
		if phMovies:
			for (phUrl, phTitle, phArtist) in phMovies:
				phTitle = phArtist + ' - ' + phTitle
				phUrl = phUrl.replace('&amp;','&')
				self.filmliste.append((phTitle, phUrl))
			self.chooseMenuList.setList(map(putpattvFilmListEntry, self.filmliste))
			self.chooseMenuList.moveToIndex(0)
			self.keyLocked = False

	def dataError(self, error):
		print error

	def keyLeft(self):
		if self.keyLocked:
			return
		self['genreList'].pageUp()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['genreList'].pageDown()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['genreList'].up()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['genreList'].down()
		
	def keyOK(self):
		if self.keyLocked:
			return
		url = self['genreList'].getCurrent()[0][1]
		self.keyLocked = False
		self.play(url)
					
	def play(self,file):
		xxxtitle = self['genreList'].getCurrent()[0][0]
		sref = eServiceReference(0x1001, 0, file)
		sref.setName(xxxtitle)
		self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()
