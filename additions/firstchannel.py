from Plugins.Extensions.MediaPortal.resources.imports import *
from Plugins.Extensions.MediaPortal.resources.decrypt import *

ck = {}

def chListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT, entry[0])
		]
def chStreamListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER, entry[0])
		]
def chMainListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER, entry[0])
		]
		
class chMain(Screen, ConfigListScreen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/chMain.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/chMain.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['title'] = Label("1channel.ch")
		self['leftContentTitle'] = Label("M e n u")
		self['stationIcon'] = Pixmap()
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('mediaportal', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = False
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.keyLocked = True
		self.streamList.append(("Featured Movies", "http://www.1channel.ch/index.php?sort=featured&page="))
		self.streamList.append(("TV Shows","http://www.1channel.ch/index.php?tv=&sort=views&page="))
		self.streamMenuList.setList(map(chMainListEntry, self.streamList))
		self.keyLocked = False
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		auswahl = self['streamlist'].getCurrent()[0][0]
		url = self['streamlist'].getCurrent()[0][1]
		print auswahl
		if auswahl == "Featured Movies":
			self.session.open(chFeatured, url)
		elif auswahl == "TV Shows":
			self.session.open(chTVshows, url)
			
	def keyCancel(self):
		self.close()

class chFeatured(Screen, ConfigListScreen):
	
	def __init__(self, session, chGotLink):
		self.chGotLink = chGotLink
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/chFeatured.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/chFeatured.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown
		}, -1)
		
		self['title'] = Label("1channel.ch")
		self['leftContentTitle'] = Label("Featured Movies")
		self['stationIcon'] = Pixmap()
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('mediaportal', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		self.page = 1
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.streamList = []
		#url = "http://www.1channel.ch/index.php?sort=featured&page=%s" % self.page
		url = "%s%s" % (self.chGotLink, str(self.page)) 
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		chMovies = re.findall('<div class="index_item index_item_ie"><a href="(.*?)" title="Watch.(.*?)"><img src="(.*?)"', data, re.S)
		if chMovies:
			for (chUrl,chTitle,chImage) in chMovies:
				chUrl = "http://www.1channel.ch" + chUrl
				self.streamList.append((decodeHtml(chTitle),chUrl,chImage))
				self.streamMenuList.setList(map(chListEntry, self.streamList))
			self.keyLocked = False
			self.showInfos()

	def showInfos(self):
		coverUrl = self['streamlist'].getCurrent()[0][2]
		if coverUrl:
			downloadPage(coverUrl, "/tmp/chIcon.jpg").addCallback(self.showCover)
		
	def showCover(self, picData):
		if fileExists("/tmp/chIcon.jpg"):
			self['stationIcon'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['stationIcon'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/chIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['stationIcon'].instance.setPixmap(ptr.__deref__())
					self['stationIcon'].show()
					del self.picload
					
	def dataError(self, error):
		print error
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		auswahl = self['streamlist'].getCurrent()[0][1]
		print auswahl
		self.session.open(chStreams, auswahl)

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

class chTVshows(Screen, ConfigListScreen):
	
	def __init__(self, session, chGotLink):
		self.chGotLink = chGotLink
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/chTVshows.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/chTVshows.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown
		}, -1)
		
		self['title'] = Label("1channel.ch")
		self['leftContentTitle'] = Label("TV Shows")
		self['stationIcon'] = Pixmap()
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('mediaportal', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		self.page = 1
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.streamList = []
		#url = "http://www.1channel.ch/index.php?sort=featured&page=%s" % self.page
		url = "%s%s" % (self.chGotLink, str(self.page)) 
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		chMovies = re.findall('<div class="index_item index_item_ie"><a href="(.*?)" title="Watch.(.*?)"><img src="(.*?)"', data, re.S)
		if chMovies:
			for (chUrl,chTitle,chImage) in chMovies:
				chUrl = "http://www.1channel.ch" + chUrl
				self.streamList.append((decodeHtml(chTitle),chUrl,chImage))
				self.streamMenuList.setList(map(chListEntry, self.streamList))
			self.keyLocked = False
			self.showInfos()

	def showInfos(self):
		coverUrl = self['streamlist'].getCurrent()[0][2]
		if coverUrl:
			downloadPage(coverUrl, "/tmp/chIcon.jpg").addCallback(self.showCover)
		
	def showCover(self, picData):
		if fileExists("/tmp/chIcon.jpg"):
			self['stationIcon'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['stationIcon'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/chIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['stationIcon'].instance.setPixmap(ptr.__deref__())
					self['stationIcon'].show()
					del self.picload
					
	def dataError(self, error):
		print error
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		auswahl = self['streamlist'].getCurrent()[0][1]
		print auswahl
		self.session.open(chTVshowsEpisode, auswahl)

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
		
class chTVshowsEpisode(Screen, ConfigListScreen):
		
	def __init__(self, session, chGotLink):
		self.chGotLink = chGotLink
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/chTVshowsEpisode.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/chTVshowsEpisode.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
		}, -1)
		
		self['title'] = Label("1channel.ch")
		self['leftContentTitle'] = Label("Season Episode")
		self['stationIcon'] = Pixmap()
		self['handlung'] = Label("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('mediaportal', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		self.page = 1
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.streamList = []
		#url = "http://www.1channel.ch/index.php?sort=featured&page=%s" % self.page
		url = "%s%s" % (self.chGotLink, str(self.page)) 
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		episoden = re.findall('<div class="tv_episode_ite.*?"> <a href="(.*?)">.*?<span class="tv_episode_name">(.*?)</span>', data, re.S)
		if episoden:
			for (url,title) in episoden:
				episode = re.findall('season-(.*?)-episode-(.*?)$',url, re.S)
				season_episode_label = "Season %s Episode %s %s" % (episode[0][0], episode[0][1], title)
				url = "http://www.1channel.ch" + url
				self.streamList.append((decodeHtml(season_episode_label),url))
				self.streamMenuList.setList(map(chListEntry, self.streamList))
			self.keyLocked = False
			
		details = re.findall('<meta name="description" content="Watch.(.*?)">.*?<meta property="og:image" content="(.*?)"/>', data, re.S)
		if details:
			(handlung,image) = details[0]
			self['handlung'].setText(decodeHtml(handlung))
			self.showInfos(image)

	def showInfos(self, coverUrl):
		downloadPage(coverUrl, "/tmp/chIcon.jpg").addCallback(self.showCover)
		
	def showCover(self, picData):
		if fileExists("/tmp/chIcon.jpg"):
			self['stationIcon'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['stationIcon'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/chIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['stationIcon'].instance.setPixmap(ptr.__deref__())
					self['stationIcon'].show()
					del self.picload
					
	def dataError(self, error):
		print error
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		auswahl = self['streamlist'].getCurrent()[0][1]
		print auswahl
		self.session.open(chStreams, auswahl)

	def keyCancel(self):
		self.close()
		
class chStreams(Screen, ConfigListScreen):
	
	def __init__(self, session, movielink):
		self.session = session
		self.movielink = movielink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/chStreams.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/chStreams.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
		}, -1)
		
		self['title'] = Label("1channel.ch")
		self['leftContentTitle'] = Label("Streams")
		self['stationIcon'] = Pixmap()
		self['handlung'] = Label("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('mediaportal', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		print self.movielink
		getPage(self.movielink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
	
	def parseData(self, data):
		streams = re.findall('<a href="/external.php.*?url=(.*?)&.*?document.writeln\(\'(.*?)\'\)',data, re.S)
		if streams:
			for (chCode, chStreamHoster) in streams:
				chUrl = base64.urlsafe_b64decode(chCode + '=' * (4 - len(chCode) % 4))
				print chStreamHoster, chUrl
				if re.match('.*?(putlocker|sockshare|filenuke|videoweed|movshare|novamov|divxstage|uploadc|sharesix)', chStreamHoster, re.S):
					self.streamList.append((chStreamHoster, chUrl))
			self.streamMenuList.setList(map(chStreamListEntry, self.streamList))
			self.keyLocked = False
		details = re.findall('<meta name="description" content="Watch.(.*?)">.*?<meta property="og:image" content="(.*?)"/>', data, re.S)
		if details:
			(handlung,image) = details[0]
			self['handlung'].setText(decodeHtml(handlung))
			self.showInfos(image)

	def dataError(self, error):
		print error
		
	def showInfos(self,coverUrl):
		print coverUrl
		downloadPage(coverUrl, "/tmp/chIcon.jpg").addCallback(self.showCover)
		
	def showCover(self, picData):
		if fileExists("/tmp/chIcon.jpg"):
			self['stationIcon'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['stationIcon'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/chIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['stationIcon'].instance.setPixmap(ptr.__deref__())
					self['stationIcon'].show()
					del self.picload
					
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		auswahl = self['streamlist'].getCurrent()[0][1]
		print auswahl
		get_stream_link(self.session).check_link(auswahl, self.got_link)
		
	def got_link(self, stream_url):
		print stream_url
		sref = eServiceReference(0x1001, 0, stream_url)
		self.session.open(MoviePlayer, sref)
		
	def keyCancel(self):
		self.close()