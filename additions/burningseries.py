from Plugins.Extensions.MediaPortal.resources.imports import *
from Plugins.Extensions.MediaPortal.resources.decrypt import *

ck = {}

def bsListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT, entry[0])
		]	
def mainListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER, entry[0])
		]	
		
class bsMain(Screen, ConfigListScreen):
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/bsMain.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/bsMain.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['title'] = Label("Burning-seri.es")
		self['leftContentTitle'] = Label("M e n u")
		self['stationIcon'] = Pixmap()
		self['stationInfo'] = Label("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('mediaportal', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = False
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.keyLocked = True
		self.streamList.append(("Serien von A-Z","serien"))
		self.streamList.append(("Watchlist","watchlist"))
		self.streamMenuList.setList(map(mainListEntry, self.streamList))
		self.keyLocked = False
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
			
		auswahl = self['streamlist'].getCurrent()[0][1]
		if auswahl == "serien":
			self.session.open(bsSerien)
		else:
			self.session.open(bsWatchlist)
			
	def keyCancel(self):
		self.close()

class bsSerien(Screen, ConfigListScreen):
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/bsSerien.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/bsSerien.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"green" : self.keyAdd
		}, -1)
		
		self['title'] = Label("Burning-seri.es")
		self['leftContentTitle'] = Label("Serien A-Z")
		self['stationIcon'] = Pixmap()
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('mediaportal', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		url = "http://www.burning-seri.es/serie-alphabet"
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		serien_raw = re.findall('<ul id=\'serSeries\'>(.*?)</ul>', data, re.S)
		if serien_raw:
			serien = re.findall('<li><a.*?href="(.*?)">(.*?)</a></li>', serien_raw[0], re.S)
			if serien:
				for (bsUrl,bsTitle) in serien:
					bsUrl = "http://www.burning-seri.es/" + bsUrl
					self.streamList.append((decodeHtml(bsTitle),bsUrl))
					self.streamMenuList.setList(map(bsListEntry, self.streamList))
				self.keyLocked = False

	def dataError(self, error):
		print error
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return

		auswahl = self['streamlist'].getCurrent()[0][1]
		print auswahl
		self.session.open(bsStaffeln, auswahl)

	def keyAdd(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		muTitle = self['streamlist'].getCurrent()[0][0]
		muID = self['streamlist'].getCurrent()[0][1]
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/resources/bs_watchlist"
		if fileExists(path):
			writePlaylist = open(path,"a")
			writePlaylist.write('"%s" "%s"\n' % (muTitle, muID))
			writePlaylist.close()
			message = self.session.open(MessageBox, _("Serie wurde zur watchlist hinzugefuegt."), MessageBox.TYPE_INFO, timeout=3)
				
	def keyCancel(self):
		self.close()

class bsWatchlist(Screen, ConfigListScreen):
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/bsWatchlist.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/bsWatchlist.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"red" : self.keyDel
		}, -1)
		
		self['title'] = Label("Burning-seri.es")
		self['leftContentTitle'] = Label("Watchlist")
		self['stationIcon'] = Pixmap()
		self['handlung'] = Label("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('mediaportal', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPlaylist)

	def loadPlaylist(self):
		self.streamList = []
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/resources/bs_watchlist"	
		if fileExists(path):
			readStations = open(path,"r")
			for rawData in readStations.readlines():
				data = re.findall('"(.*?)" "(.*?)"', rawData, re.S)
				if data:
					(stationName, stationLink) = data[0]
					self.streamList.append((stationName, stationLink))
			print "Reload Playlist"
			self.streamList.sort()
			self.streamMenuList.setList(map(bsListEntry, self.streamList))
			readStations.close()
			self.keyLocked = False
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return

		auswahl = self['streamlist'].getCurrent()[0][1]
		print auswahl
		self.session.open(bsStaffeln, auswahl)
			
	def keyDel(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		
		selectedName = self['streamlist'].getCurrent()[0][0]
		pathTmp = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/resources/bs_watchlist.tmp"
		writeTmp = open(pathTmp,"w")	
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/resources/bs_watchlist"
		if fileExists(path):
			readStations = open(path,"r")
			for rawData in readStations.readlines():
				data = re.findall('"(.*?)" "(.*?)"', rawData, re.S)
				if data:
					(stationName, stationLink) = data[0]
					if stationName != selectedName:
						writeTmp.write('"%s" "%s"\n' % (stationName, stationLink))
			readStations.close()
			writeTmp.close()
			shutil.move(pathTmp, path)
			self.loadPlaylist()
				
	def keyCancel(self):
		self.close()

class bsStaffeln(Screen, ConfigListScreen):
	def __init__(self, session, serienUrl):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/bsStaffeln.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/bsStaffeln.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		self.serienUrl = serienUrl
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"green" : self.keyAdd,
		}, -1)
		
		self['title'] = Label("Burning-seri.es")
		self['leftContentTitle'] = Label("Staffel Auswahl")
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
		print self.serienUrl
		getPage(self.serienUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		details = re.findall('<strong>Beschreibung</strong>.*?<p>(.*?)</p>.*?<img\ssrc="(.*?)"\salt="Cover"\s{0,2}/>', data, re.S)
		staffeln_raw = re.findall('<ul class="pages">(.*?)</ul>', data, re.S)
		if staffeln_raw:
			staffeln = re.findall('<li class=".*?"><a.*?href="(serie/.*?)">(.*?)</a></li>', staffeln_raw[0], re.S)		
			if staffeln:
				for (bsUrl,bsStaffel) in staffeln:
					bsUrl = "http://www.burning-seri.es/" + bsUrl
					bsStaffel = "Staffel %s" % bsStaffel
					bsStaffel = bsStaffel.replace('Staffel Film(e)','Film(e)')
					self.streamList.append((bsStaffel,bsUrl))
				self.streamMenuList.setList(map(bsListEntry, self.streamList))
				self.keyLocked = False
			if details:
				(handlung,cover) = details[0]
				self['handlung'].setText(decodeHtml(handlung))
				coverUrl = "http://www.burning-seri.es/" + cover
				print coverUrl
				downloadPage(coverUrl, "/tmp/bsIcon.jpg").addCallback(self.ShowCover)
		
	def ShowCover(self, picData):
		if fileExists("/tmp/bsIcon.jpg"):
			self['stationIcon'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['stationIcon'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/bsIcon.jpg", 0, 0, False) == 0:
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

		staffel = self['streamlist'].getCurrent()[0][0]
		staffel = staffel.replace('Staffel ','').replace('Film(e)','0')
		auswahl = self['streamlist'].getCurrent()[0][1]
		print auswahl, staffel
		self.session.open(bsEpisoden, auswahl, staffel)

	def keyAdd(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		muTitle = self['streamlist'].getCurrent()[0][0]
		muID = self['streamlist'].getCurrent()[0][1]
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/resources/bs_watchlist"
		if fileExists(path):
			writePlaylist = open(path,"a")
			writePlaylist.write('"%s" "%s"\n' % (muTitle, muID))
			writePlaylist.close()
			self.loadPlaylist()
				
	def keyCancel(self):
		self.close()

class bsEpisoden(Screen, ConfigListScreen):
	def __init__(self, session, serienUrl, bsStaffel):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/bsEpisoden.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/bsEpisoden.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
		
		self.serienUrl = serienUrl
		self.bsStaffel = bsStaffel
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['title'] = Label("Burning-seri.es")
		self['leftContentTitle'] = Label("Episoden Auswahl")
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
		print self.serienUrl
		getPage(self.serienUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		episoden = re.findall('<tr>.*?<td>(\d+)</td>.*?<td><a href="(serie/.*?)">', data, re.S)
		details = re.findall('<strong>Beschreibung</strong>.*?<p>(.*?)</p>.*?<img\ssrc="(.*?)"\salt="Cover"\s{0,2}/>', data, re.S)
		bsStaffel2 = self.bsStaffel
		if int(bsStaffel2) < 10:
			bsStaffel3 = "S0"+str(bsStaffel2)
		else:
			bsStaffel3 = "S"+str(bsStaffel2)
		if episoden:
			for (bsEpisode,bsUrl) in episoden:
				bsTitle = re.findall('/\d+/\d+-(.*[0-9a-z]+)', bsUrl, re.S|re.I)
				bsUrl = "http://www.burning-seri.es/" + bsUrl
				if int(bsEpisode) < 10:
					bsEpisode2 = "E0"+str(bsEpisode)
				else:
					bsEpisode2 = "E"+str(bsEpisode)
				bsEpisode = "%s%s - %s" % (bsStaffel3, bsEpisode2, decodeHtml(bsTitle[0].replace('_',' ').replace('-',' ')))
				self.streamList.append((bsEpisode,bsUrl))
			self.streamMenuList.setList(map(bsListEntry, self.streamList))
			self.keyLocked = False
		if details:
			(handlung,cover) = details[0]
			self['handlung'].setText(decodeHtml(handlung))
			coverUrl = "http://www.burning-seri.es/" + cover
			print coverUrl
			downloadPage(coverUrl, "/tmp/bsIcon.jpg").addCallback(self.ShowCover)

	def ShowCover(self, picData):
		if fileExists("/tmp/bsIcon.jpg"):
			self['stationIcon'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['stationIcon'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/bsIcon.jpg", 0, 0, False) == 0:
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
		title = self['streamlist'].getCurrent()[0][0]
		print auswahl
		self.session.open(bsStreams, auswahl, title)
				
	def keyCancel(self):
		self.close()
		
class bsStreams(Screen, ConfigListScreen):
	
	def __init__(self, session, serienUrl, title):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/bsStreams.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/bsStreams.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		self.serienUrl = serienUrl
		self.streamname = title
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['title'] = Label("Burning-seri.es")
		self['leftContentTitle'] = Label("Stream Auswahl")
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
		print self.serienUrl
		getPage(self.serienUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		streams = re.findall('<li><a href="(serie/.*?)"><span\n            class="icon.(.*?)"></span>', data)
		details = re.findall('id="desc_spoiler">\s{0,10}(.*?)</div>.*?<img\ssrc="(.*?)"\salt="Cover"\s{0,2}/>', data, re.S)
		if streams:
			for (bsUrl,bsStream) in streams:
				bsUrl = "http://www.burning-seri.es/" + bsUrl
				if re.match('.*?(Ecostream|Sockshare|Streamcloud|Putlocker|Filenuke|MovShare|Novamov|DivxStage|UploadC|NowVideo|VideoWeed|Flashx|FileNuke|BitShare)',bsStream,re.I):
					self.streamList.append((bsStream,bsUrl))
			self.streamMenuList.setList(map(bsListEntry, self.streamList))
			self.keyLocked = False
		if details:
			(handlung,cover) = details[0]
			self['handlung'].setText(decodeHtml(handlung))
			coverUrl = "http://www.burning-seri.es/" + cover
			print coverUrl
			downloadPage(coverUrl, "/tmp/bsIcon.jpg").addCallback(self.ShowCover)
			
	def ShowCover(self, picData):
		if fileExists("/tmp/bsIcon.jpg"):
			self['stationIcon'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['stationIcon'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/bsIcon.jpg", 0, 0, False) == 0:
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
		getPage(auswahl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.findStream).addErrback(self.dataError)

	def playfile(self, link):
		print link
		sref = eServiceReference(0x1001, 0, link)
		sref.setName(self.streamname)
		self.session.open(MoviePlayer, sref)
		
	def findStream(self, data):
		#print data
		
		#test = re.findall('<a href="(.*?)" target="_blank">', data, re.S)
		
		if re.match(".*?<iframe.*?src=",data, re.S|re.I):
			test = re.findall('<iframe.*?src=["|\'](http://.*?)["|\']', data, re.S|re.I)
		else:
			test = re.findall('<a target=["|\']_blank["|\'] href=["|\'](http://.*?)["|\']', data, re.S|re.I)
		print test
		
		get_stream_link(self.session).check_link(test[0], self.got_link, False)
		
	def got_link(self, stream_url):
		if stream_url == None:
			message = self.session.open(MessageBox, _("Stream not found, try another Stream Hoster."), MessageBox.TYPE_INFO, timeout=3)
		else:
			self.playfile(stream_url.replace('&amp;','&'))
	
	def keyCancel(self):
		self.close()
