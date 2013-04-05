from Plugins.Extensions.mediaportal.resources.imports import *
from Plugins.Extensions.mediaportal.resources.yt_url import *

def gigatvGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

def gigatvFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
		
class gigatvGenreScreen(Screen):
	
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

		self['title'] = Label("GIGA.de")
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
		self.genreliste.append(("Alle Videos", "http://www.giga.de/tv/alle-videos/", None))
		self.genreliste.append(("G-Log","http://www.giga.de/games/videos/g-log/", "http://media2.giga.de/2012/12/g-log2-150x95.jpg"))
		self.genreliste.append(("GIGA Failplays","http://www.giga.de/games/channel/giga-failplays/", "http://media2.giga.de/2013/04/failplay-teaser-150x95.jpg"))
		self.genreliste.append(("GIGA Gameplay","http://www.giga.de/games/videos/giga-gameplay/", "http://media2.giga.de/2012/12/gameplay2-150x95.jpg"))
		self.genreliste.append(("GIGA Live","http://www.giga.de/games/videos/giga-live/", "http://media2.giga.de/2012/12/gigatvlive-teaser-150x95.jpg"))
		self.genreliste.append(("GIGA Top Montag","http://www.giga.de/mac/channel/giga-top-montag/", "http://media2.giga.de/2013/04/topmontag-teaser-150x95.jpg"))
		self.genreliste.append(("Jonas liest","http://www.giga.de/games/videos/jonas-liest/", "http://media2.giga.de/2012/12/jonasliest-teaser-150x95.jpg"))
		self.genreliste.append(("NostalGIGA","http://www.giga.de/games/videos/nostalgiga/", "http://media2.giga.de/2012/12/nostalgiga-150x95.jpg"))
		self.genreliste.append(("Radio GIGA","http://www.giga.de/games/videos/radio-giga/", "http://media2.giga.de/2012/12/radiogiga-150x95.jpg"))
		self.genreliste.append(("Specials","http://www.giga.de/games/videos/specials/", None))
		self.genreliste.append(("Top 100 Filme","http://www.giga.de/games/videos/top-100-filme/", "http://media2.giga.de/2012/12/top100filme-teaser-150x95.jpg"))
		self.genreliste.append(("Top 100 Games","http://www.giga.de/games/videos/top-100-games/", "http://media2.giga.de/2012/12/top100spiele-teaser-150x95.jpg"))
		self.genreliste.append(("Top 100 Momente","http://www.giga.de/android/channel/top-100-spielemomente/", "http://media2.giga.de/2013/04/top100spielemomente-teaser-150x95.jpg"))
		self.genreliste.append(("Top 100 Serien","http://www.giga.de/games/videos/top-100-tv-serien/", "http://media2.giga.de/2012/12/top100serien-teaser-150x95.jpg"))
		self.chooseMenuList.setList(map(gigatvGenreListEntry, self.genreliste))
		self.chooseMenuList.moveToIndex(0)
		self.keyLocked = False
		self.showInfos()

	def dataError(self, error):
		print error

	def showInfos(self):
		phImage = self['genreList'].getCurrent()[0][2]
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
		self.session.open(gigatvFilmScreen, streamGenreLink)
		
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

class gigatvFilmScreen(Screen):
	
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
			"left" : self.keyLeft,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown,
			"green" : self.keyPageNumber
		}, -1)

		self['title'] = Label("GIGA.de")
		self['name'] = Label("Film Auswahl")
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
		self['name'].setText('Bitte warten...')
		self.filmliste = []
		if self.page > 1:
			url = "%s%s/" % (self.phCatLink, str(self.page))
		else:
			url = "%s" % (self.phCatLink)
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadData).addErrback(self.dataError)
	
	def loadData(self, data):
		lastparse = re.search('<ul\sclass="sequences\shlist">(.*?)</ul>', data, re.S)
		if lastparse:
			lastp = re.findall('<a\shref=".*>.*?([0-9]+)', lastparse.group(1), re.S)
			if lastp:
				self.lastpage = int(lastp[0])
			else:
				self.lastpage = 1
		else:
			self.lastpage = 1
		self['page'].setText(str(self.page) + ' / ' + str(self.lastpage))
		phMovies = re.findall('<article\sclass="videos\ssmallimg">.*?<a\shref="(.*?)".*?>(.*?)</a>.*?<img\ssrc="(.*?)"', data, re.S)
		if phMovies:
			for (phUrl, phTitle, phImage) in phMovies:
				phTitle = phTitle.replace('<b>','').replace('</b>','')
				self.filmliste.append((decodeHtml(phTitle), phUrl, phImage))
			self.chooseMenuList.setList(map(gigatvFilmListEntry, self.filmliste))
			self.chooseMenuList.moveToIndex(0)
			self.keyLocked = False
			self.showInfos()

	def dataError(self, error):
		print error

	def showInfos(self):
		phTitle = self['genreList'].getCurrent()[0][0]
		phImage = self['genreList'].getCurrent()[0][2]
		self['name'].setText(phTitle)
		downloadPage(phImage, "/tmp/Icon.jpg").addCallback(self.ShowCover)
		
	def ShowCover(self, picData):
		if fileExists("/tmp/Icon.jpg"):
			self['coverArt'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/Icon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr.__deref__())
					self['coverArt'].show()
					del self.picload

	def keyPageNumber(self):
		self.session.openWithCallback(self.callbackkeyPageNumber, VirtualKeyBoard, title = (_("Seitennummer eingeben")), text = str(self.page))

	def callbackkeyPageNumber(self, answer):
		if answer is not None:
			answer = re.findall('\d+', answer)
		else:
			return
		if answer:
			if int(answer[0]) < self.lastpage + 1:
				self.page = int(answer[0])
				self.loadpage()
			else:
				self.page = self.lastpage
				self.loadpage()

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
		
	def keyOK(self):
		if self.keyLocked:
			return
		phTitle = self['genreList'].getCurrent()[0][0]
		phLink = self['genreList'].getCurrent()[0][1]
		self.keyLocked = True
		print phLink
		getPage(phLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getVideoPage).addErrback(self.dataError)

	def getVideoPage(self, data):
		videoPage = re.findall('rel="media:video".*?="(.*?)-normal.mp4"', data, re.S)
		if videoPage:
			for phurl in videoPage:
				print phurl
				url = phurl + '-hd.mp4'
				print url
				self.keyLocked = False
				self.play(url)
		else:
			videoPage = re.findall('"http://www.youtube.com/(v|embed)/(.*?)\?.*?"', data, re.S)
			if videoPage:
				print videoPage
				url = youtubeUrl(self.session).getVideoUrl(videoPage[0][1], 2)
				if url:
					self.play(url)
			else:
				message = self.session.open(MessageBox, _("Dieses Video ist nicht verfuegbar."), MessageBox.TYPE_INFO, timeout=5)
		self.keyLocked = False
					
	def play(self,file):
		xxxtitle = self['genreList'].getCurrent()[0][0]
		sref = eServiceReference(0x1001, 0, file)
		sref.setName(xxxtitle)
		self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()
