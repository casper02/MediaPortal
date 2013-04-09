from Plugins.Extensions.mediaportal.resources.imports import *
from Components.config import config
from Plugins.Extensions.mediaportal.resources.playrtmpmovie import PlayRtmpMovie

def auditvGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

def auditvFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
		
class auditvGenreScreen(Screen):
	
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

		self['title'] = Label("Audi.tv")
		self['name'] = Label("Kanal Auswahl")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.suchString = ''
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.genreliste.append(("Deutsch", "1"))
		self.genreliste.append(("Englisch", "2"))
		self.chooseMenuList.setList(map(auditvGenreListEntry, self.genreliste))
		self.chooseMenuList.moveToIndex(0)
		self.keyLocked = False

	def dataError(self, error):
		print error

	def keyOK(self):
		streamGenreName = self['genreList'].getCurrent()[0][0]
		streamGenreLink = self['genreList'].getCurrent()[0][1]		
		self.session.open(auditvFilmScreen, streamGenreLink, streamGenreName)
			
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

	def keyCancel(self):
		self.close()

class auditvFilmScreen(Screen):
	
	def __init__(self, session, phCatLink, catName):
		self.session = session
		self.phCatLink = phCatLink
		self.catName = catName
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

		self['title'] = Label("Titel Auswahl")
		self['name'] = Label("")
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
		self['name'].setText(self.catName)
		self.filmliste = []
		url = "http://tv.audi.com/tvnext/services/epg/?channelId=%s&showRunning=true" % (self.phCatLink)
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadData).addErrback(self.dataError)
	
	def loadData(self, data):
		phMovies = re.findall('<item>.*?<title><\!\[CDATA\[(.*?)\]\]></title>.*?<cms_id>(.*?)</cms_id>', data, re.S)
		if phMovies:
			for (phTitle, phId) in phMovies:
				self.filmliste.append((decodeHtml(phTitle), phId))
		self.filmliste = list(set(self.filmliste))
		self.filmliste.sort()
		self.chooseMenuList.setList(map(auditvFilmListEntry, self.filmliste))
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
		phId = self['genreList'].getCurrent()[0][1]
		url = 'http://tv.audi.com/embedData/%s' % phId
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getVideoUrl).addErrback(self.dataError)

	def getVideoUrl(self, data):
		parse = re.findall('high.*?streamName":"(.*?high.mp4)".*?akamaiStreamingUrl":"(.*?)"', data, re.S)
		if parse:
			playpath = str(parse[0][0]).replace('\/','/')
			host = str(parse[0][1]).replace('\/','/')
			if config.mediaportal.useRtmpDump.value:
				final = "%s' --swfVfy=1 --playpath=mp4:%s --pageUrl=http://tv.audi.de/#/01 --swfUrl=http://tv.audi.de/auditv/portal.swf?version=1348653342'" % (host, playpath)
				print final
				title = self['genreList'].getCurrent()[0][0]
				movieinfo = [final, title]
				self.session.open(PlayRtmpMovie, movieinfo, title)
			else:
				url = "%s swfUrl=http://tv.audi.de/auditv/portal.swf?version=1348653342 pageurl=http://tv.audi.de/#/01 playpath=mp4:%s swfVfy=1" % (host, playpath)
				self.keyLocked = False
				self.play(url)

	def play(self,file):
		xxxtitle = self['genreList'].getCurrent()[0][0]
		sref = eServiceReference(0x1001, 0, file)
		sref.setName(xxxtitle)
		self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()
