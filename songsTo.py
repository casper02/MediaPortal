from imports import *
from decrypt import *

def SongstoListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 0, 0, 800, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 
class showSongstoGenre(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/showSongstoGenre.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/showSongstoGenre.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "MoviePlayerActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self["title"] = Label("Songs.to Music Player - Auswahl")
		self["coverArt"] = Pixmap()
		self["songtitle"] = Label ("")
		self["artist"] = Label ("")
		self["album"] = Label ("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.streamMenuList.l.setItemHeight(25)
		self["streamlist"] = self.streamMenuList

		self.keyLocked = False
		self.playing = False
		self.lastservice = session.nav.getCurrentlyPlayingServiceReference()
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.keyLocked = True
		scGenre = [("Songs Top 500", "http://songs.to/json/songlist.php?top=all"),
			("Singles Top 100", "http://songs.to/json/songlist.php?charts=music_single_de"),
			("Dance Top 50", "http://songs.to/json/songlist.php?charts=music_dance_de"),
			("Black Top 40", "http://songs.to/json/songlist.php?charts=music_black_de"),
			("Singles US Top 40", "http://songs.to/json/songlist.php?charts=music_single_us"),
			("Singles UK Top 40", "http://songs.to/json/songlist.php?charts=music_single_uk"),
			("Metal-Rock Top 15", "http://songs.to/json/songlist.php?charts=music_album_mrc"),
			("Schlager Top 30", "http://songs.to/json/songlist.php?charts=music_schlager_de"),
			("Singles Jahr 2011", "http://songs.to/json/songlist.php?charts=music_year2011_de"),
			("Singles Jahr 2012", "http://songs.to/json/songlist.php?charts=music_year2012_de")]
					
		for (scName, scUrl) in scGenre:
			self.streamList.append((scName, scUrl))
		self.streamMenuList.setList(map(SongstoListEntry, self.streamList))
		self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return
		scName = self['streamlist'].getCurrent()[0][0]
		scUrl = self['streamlist'].getCurrent()[0][1]
		if scName == "Songs Top 500":
			print scName, "showAll"
			self.session.open(showSongstoAll, scUrl, scName)
		else:
			print scName, "showTop"
			self.session.open(showSongstoTop, scUrl, scName)
			
	def keyCancel(self):
		self.close()

class showSongstoAll(Screen, InfoBarBase, InfoBarSeek):
	
	def __init__(self, session, link, name):
		self.session = session
		self.scLink = link
		self.scGuiName = name
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/showSongstoAll.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/showSongstoAll.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		InfoBarBase.__init__(self)
		InfoBarSeek.__init__(self)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok" : self.keyOK,
			"cancel" : self.keyCancel,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)
		
		self["title"] = Label("Songs.to Music Player %s" % self.scGuiName)
		self["coverArt"] = Pixmap()
		self["songtitle"] = Label ("")
		self["artist"] = Label ("")
		self["album"] = Label ("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.streamMenuList.l.setItemHeight(25)
		self["streamlist"] = self.streamMenuList

		self.keyLocked = False
		self.playing = False
		self.lastservice = session.nav.getCurrentlyPlayingServiceReference()
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.keyLocked = True
		getPage(self.scLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.scData).addErrback(self.dataError)
		
	def scData(self, data):
		findSongs = re.findall('"hash":"(.*?)","title":"(.*?)","artist":"(.*?)","album":"(.*?)".*?"cover":"(.*?)"', data, re.S)
		if findSongs:
			for (scHash,scTitle,scArtist,scAlbum,scCover) in findSongs:
				self.streamList.append((scTitle, scArtist, scAlbum, scCover, scHash))
			self.streamMenuList.setList(map(self.streamListEntry, self.streamList))
			self.keyLocked = False
			
	def streamListEntry(self, entry):
		title = entry[1] + " - " + entry[0]
		return [entry,
			(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 800, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, decodeHtml(title))
			] 
				
	def dataError(self, error):
		print error

	def scRead(self, stationIconLink):
		downloadPage(stationIconLink, "/tmp/scIcon.jpg").addCallback(self.scCoverShow)
		
	def scCoverShow(self, picData):
		if fileExists("/tmp/scIcon.jpg"):
			self['coverArt'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/scIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr.__deref__())
					self['coverArt'].show()
					del self.picload
	
	def doEofInternal(self, playing):
		print "ENDEEEEE"
		self['streamlist'].down()
		self.keyOK()

	def lockShow(self):
		pass
		
	def unlockShow(self):
		pass

	def keyLeft(self):
		if self.keyLocked:
			return
		self['streamlist'].pageUp()
			
	def keyRight(self):
		if self.keyLocked:
			return
		self['streamlist'].pageDown()
		
	def keyOK(self):
		if self.keyLocked:
			print self.keyLocked
			return
		scTitle = self['streamlist'].getCurrent()[0][0]
		if scTitle:
			self["songtitle"].setText(scTitle)
			
		scArtist = self['streamlist'].getCurrent()[0][1]
		if scArtist:
			self["artist"].setText(scArtist)
		
		scAlbum = self['streamlist'].getCurrent()[0][2]
		if scAlbum:
			self["album"].setText(scAlbum)
		
		scHash = self['streamlist'].getCurrent()[0][4]
		if scHash:
			#scStream = "http://s.songs.to/data.php?id="+scHash
			#print scHash
			scStream = "http://s.songs.to/data.php?id="+scHash
			print scStream
			sref = eServiceReference(0x1001, 0, scStream)
			self.session.nav.playService(sref)
			self.playing = True
			
		scCover = self['streamlist'].getCurrent()[0][3]
		if scCover:
			scCoverUrl = "http://songs.to/covers/"+scCover
			self.scRead(scCoverUrl)

	def keyCancel(self):
		if self.playing:
			self.session.nav.stopService()
			self.session.nav.playService(self.lastservice)
			self.playing = False
		self.close()
	
class showSongstoTop(Screen, InfoBarBase, InfoBarSeek):
	
	def __init__(self, session, link, name):
		self.session = session
		self.scLink = link
		self.scGuiName = name
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/showSongstoTop.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/showSongstoTop.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		InfoBarSeek.__init__(self)
		InfoBarBase.__init__(self)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok" : self.keyOK,
			"cancel" : self.keyCancel,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)
		
		self["title"] = Label("Songs.to Music Player - %s" % self.scGuiName)
		self["coverArt"] = Pixmap()
		self["songtitle"] = Label ("")
		self["artist"] = Label ("")
		self["album"] = Label ("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.streamMenuList.l.setItemHeight(25)
		self["streamlist"] = self.streamMenuList

		self.keyLocked = False
		self.playing = False
		self.lastservice = session.nav.getCurrentlyPlayingServiceReference()
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.keyLocked = True
		getPage(self.scLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.scDataGet).addErrback(self.dataError)
		
	def scDataGet(self, data):
		findSongs = re.findall('name1":"(.*?)","name2":"(.*?)"', data, re.S)
		if findSongs:
			for (scTitle,scArtist) in findSongs:
				self.streamList.append((scTitle, scArtist))
			self.streamMenuList.setList(map(self.streamListEntry, self.streamList))
			self.keyLocked = False
			
	def streamListEntry(self, entry):
		title = entry[1] + " - " + entry[0]
		return [entry,
			(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 800, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, decodeHtml(title))
			] 
				
	def dataError(self, error):
		print error

	def scRead(self, stationIconLink):
		downloadPage(stationIconLink, "/tmp/scIcon.jpg").addCallback(self.scCoverShow)
		
	def scCoverShow(self, picData):
		if fileExists("/tmp/scIcon.jpg"):
			self['coverArt'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/scIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr.__deref__())
					self['coverArt'].show()
					del self.picload
	
	def doEofInternal(self, playing):
		print "ENDEEEEE"
		self['streamlist'].down()
		self.keyOK()

	def lockShow(self):
		pass
		
	def unlockShow(self):
		pass

	def keyLeft(self):
		if self.keyLocked:
			return
		self['streamlist'].pageUp()
			
	def keyRight(self):
		if self.keyLocked:
			return
		self['streamlist'].pageDown()

	def keyOK(self):
		if self.keyLocked:
			return
		scArtist = self['streamlist'].getCurrent()[0][0]
		scTitle = self['streamlist'].getCurrent()[0][1]
		title = urllib2.quote(scTitle.encode("utf8"))
		artist = urllib2.quote(scArtist.encode("utf8"))
		url = "http://songs.to/json/songlist.php?quickplay=1"
		dataPost = "data=%7B%22data%22%3A%5B%7B%22artist%22%3A%22"+artist+"%22%2C%20%22album%22%3A%22%22%2C%20%22title%22%3A%22"+title+"%22%7D%5D%7D"
		getPage(url, method='POST', postdata=dataPost, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.scDataPost).addErrback(self.dataError)
			
	def scDataPost(self, data):
		print data
		print "drin."
		self.found = False
		findSongs = re.findall('"hash":"(.*?)","title":"(.*?)","artist":"(.*?)","album":"(.*?)".*?"cover":"(.*?)"', data)
		if findSongs:
			print findSongs
			(scHash, scTitle, scArtist, scAlbum, scCover) = findSongs[0]
			
			if scTitle:
				self["songtitle"].setText(scTitle)
			if scArtist:
				self["artist"].setText(scArtist)
			if scAlbum:
				self["album"].setText(scAlbum)
			if scHash:
				scStream = "http://s.songs.to/data.php?id="+scHash
				print scHash
				sref = eServiceReference(0x1001, 0, scStream)
				self.session.nav.playService(sref)
				self.playing = True
				self.found = True
			if scCover:
				scCoverUrl = "http://songs.to/covers/"+scCover
				self.scRead(scCoverUrl)

		if not self.found:
			findSongs = re.findall('"hash":"(.*?)","title":"(.*?)","artist":"(.*?)","album":"(.*?)"', data)
			if findSongs:
				print findSongs
				(scHash, scTitle, scArtist, scAlbum) = findSongs[0]
				
				if scTitle:
					self["songtitle"].setText(scTitle)
				if scArtist:
					self["artist"].setText(scArtist)
				if scAlbum:
					self["album"].setText(scAlbum)
				if scHash:
					scStream = "http://s.songs.to/data.php?id="+scHash
					print scHash
					sref = eServiceReference(0x1001, 0, scStream)
					self.session.nav.playService(sref)
					self.playing = True

	def keyCancel(self):
		if self.playing:
			self.session.nav.stopService()
			self.session.nav.playService(self.lastservice)
			self.playing = False
		self.close()