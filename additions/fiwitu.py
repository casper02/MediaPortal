from Plugins.Extensions.mediaportal.resources.imports import *

def fiwituGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		]

def fiwituGenre2ListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]
		
def fiwituGenre3ListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]
		
class fiwituGenreScreen(Screen):
	
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

		self['title'] = Label("fiwitu.tv")
		self['name'] = Label("Genre Auswahl")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.genreliste.append(("Muskeltraining", "http://fiwitu.tv/muskeltraining"))
		self.genreliste.append(("Beweglichkeit und Entspannung", "http://fiwitu.tv/beweglichkeit-und-entspannung"))
		self.genreliste.append(("Ausdauersport", "http://fiwitu.tv/ausdauersport"))
		self.genreliste.append(("Tanzsport", "http://fiwitu.tv/tanzsport"))
		self.genreliste.append(("Kampfsport", "http://fiwitu.tv/kampfsport"))
		self.genreliste.append(("Ernaehrung", "http://fiwitu.tv/ernaehrung"))
		self.genreliste.append(("Tipps und Trends", "http://fiwitu.tv/tipps-und-trends"))
		self.chooseMenuList.setList(map(fiwituGenreListEntry, self.genreliste))
		self.keyLocked = False

	def keyOK(self):
		streamGenreLink = self['genreList'].getCurrent()[0][1]
		self.session.open(fiwituGenre2Screen, streamGenreLink)
		
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

class fiwituGenre2Screen(Screen):
	
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

		self['title'] = Label("fiwitu.tv")
		self['name'] = Label("Trainigsauswahl")
		self['views'] = Label("")
		self['runtime'] = Label("")
		self['page'] = Label("")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.page = 1
		self.lastpage = 1
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		self.onLayoutFinish.append(self.loadpage)
		
	def loadpage(self):
		self.keyLocked = True
		#self['name'].setText('Bitte warten...')
		self.filmliste = []
		url = self.phCatLink
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadData).addErrback(self.dataError)
	
	def loadData(self, data):
		genreList = re.findall('<h2 class="label">(.*?)</h2>.*?<a href="(.*?)"', data, re.S)
		for genre, uri in genreList:
			self.filmliste.append((decodeHtml(genre), uri))
		self.chooseMenuList.setList(map(fiwituGenre2ListEntry, self.filmliste))
		self.keyLocked = False

	def dataError(self, error):
		print 'Error Lesen Videos...:', error

	def keyPageDown(self):
		print "PageDown"
		if self.keyLocked:
			return
		if not self.page < 2:
			self.page -= 1
			self.loadpage()
		
	def keyPageUp(self):
		print "PageUP"
		if self.keyLocked:
			return
		if self.page < self.lastpage:
			self.page += 1
			self.loadpage()
		
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
		phTitle = self['genreList'].getCurrent()[0][0]
		phLink = "%s%s" % ("http://fiwitu.tv", self['genreList'].getCurrent()[0][1])
		self.session.open(fiwituGenre3Screen, phTitle, phLink)

	def keyCancel(self):
		self.close()
		
class fiwituGenre3Screen(Screen):
	
	def __init__(self, session, phTitle, phLink):
		self.session = session
		self.ftwTitle = phTitle
		self.ftwLink = phLink
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

		self['title'] = Label("fiwitu.tv")
		self['name'] = Label(self.ftwTitle)
		self['views'] = Label("")
		self['runtime'] = Label("")
		self['page'] = Label("")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.page = 1
		self.lastpage = 1
		self.filmliste = []
		self.mdUrl = ''
		self.sdUrl = ''
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		self.onLayoutFinish.append(self.loadpage)
		
	def loadpage(self):
		self.keyLocked = True
		self['name'].setText('Bitte warten...')
		url = self.ftwLink
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadData).addErrback(self.dataError)
	
	def loadData(self, data):
		allVideos = re.findall('urlTemplate: "(.*?)"', data, re.S)
		allVideosLink =  re.sub(r"limit=[0-9]", "limit=999", allVideos[0])
		print 'Alle Videos Link...:', allVideosLink
		getPage(allVideosLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadAllData).addErrback(self.dataError)

	def loadAllData(self, data):
		print 'loadAllData'
		allVidInfos = re.findall('<div class="vid_figure">.*?<a href="(.*?)" title="(.*?)">', data, re.S)
		for link, title in allVidInfos:
			self.filmliste.append((decodeHtml(title), link))
		self.chooseMenuList.setList(map(fiwituGenre3ListEntry, self.filmliste))
		self.keyLocked = False

	def dataError(self, error):
		print 'Error Lesen Videos...:', error

	def keyPageDown(self):
		print "PageDown"
		if self.keyLocked:
			return
		if not self.page < 2:
			self.page -= 1
			self.loadpage()
		
	def keyPageUp(self):
		print "PageUP"
		if self.keyLocked:
			return
		if self.page < self.lastpage:
			self.page += 1
			self.loadpage()
		
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
		playLink = "%s%s" % ("http://fiwitu.tv", self['genreList'].getCurrent()[0][1])
		getPage(playLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseVideoPage).addErrback(self.dataError)
	def keyCancel(self):
		self.close()

	def parseVideoPage(self, data):
		videoAllInfos = re.findall(r'<object id="sevenload_player".*?data=".*?" data-html5="(.*?)"', data, re.S)
		decodedInfos = decodeHtml(videoAllInfos[0])
		videoUrls = re.findall('"src":"(.*?)","mime_type":"video/mp4"', decodedInfos, re.S)
		if videoUrls:
			if len(videoUrls) == 1:
				self.playVideo(videoUrls[0])
			if len(videoUrls) > 1:
					for videoUrl in videoUrls:
						if re.match('.*?md.*?', videoUrl):
							self.mdUrl = videoUrl
						if re.match('.*?sd.*?', videoUrl):
							self.sdUrl = videoUrl
			if self.mdUrl:
				self.playVideo(self.mdUrl)
			else:
				if self.sdUrl:
					self.playVideo(self.sdUrl)
		
	def keyCancel(self):
		self.close()
		
	def playVideo(self,url):
		title = self['genreList'].getCurrent()[0][0]
		sref = eServiceReference(0x1001, 0, url)
		sref.setName(title)
		self.session.open(MoviePlayer, sref)


