from Plugins.Extensions.MediaPortal.resources.imports import *

def gstreaminxxxGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

def gstreaminxxxFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
		
def gstreaminxxxHosterListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 
		
sitechrx = ''

special_headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31',
	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4',
	'Referer': 'http://g-stream.in/'
}

class gstreaminxxxGenreScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/XXXGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/XXXGenreScreen.xml"
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

		self['title'] = Label("G-Stream.in")
		self['name'] = Label("Genre Auswahl")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.suchString = ''
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.get_site_cookie1)
		
	def get_site_cookie1(self):
		self.keyLocked = True
		url = "http://g-stream.in"
		getPage(url, headers=special_headers).addCallback(self.get_site_cookie2).addErrback(self.dataError)
		
	def get_site_cookie2(self, data):
		x = re.search('searchfrm', data, re.S)
		if x:
			self.layoutFinished()
			return
		self.keyLocked = True
		raw = re.findall('javascript"\ssrc="(.*?)">.*?scf\(\'(.*?)\'\+\'(.*?)\'.*?', data, re.S)
		url = "http://g-stream.in" + str(raw[0][0])
		getPage(url, headers=special_headers).addCallback(self.get_site_cookie3, raw[0][1], raw[0][2]).addErrback(self.dataError)
		
	def get_site_cookie3(self, data, cookie1, cookie2):
		raw = re.findall('escape\(hsh.*?"(.*?)"\)', data, re.S)
		global sitechrx
		sitechrx = str(cookie1) + str(cookie2) + str(raw[0])
		print 'sitechrx='+sitechrx
		self.layoutFinished()

	def layoutFinished(self):
		self.genreliste.append(("Newest", "http://g-stream.in/forumdisplay.php?f=661&page="))
		self.genreliste.append(("Amateur", "http://g-stream.in/forumdisplay.php?s=&f=661&page=1&pp=20&sort=lastpost&order=desc&daysprune=-1&prefixid=Amateure1&page="))
		self.genreliste.append(("Anal", "http://g-stream.in/forumdisplay.php?s=&f=661&page=1&pp=20&sort=lastpost&order=desc&daysprune=-1&prefixid=Anal&page="))
		self.genreliste.append(("Asian", "http://g-stream.in/forumdisplay.php?s=&f=661&page=1&pp=20&sort=lastpost&order=desc&daysprune=-1&prefixid=Asia&page="))
		self.genreliste.append(("Big Tits", "http://g-stream.in/forumdisplay.php?s=&f=661&page=1&pp=20&sort=lastpost&order=desc&daysprune=-1&prefixid=GrosseBrueste&page="))
		self.genreliste.append(("Black", "http://g-stream.in/forumdisplay.php?s=&f=661&page=1&pp=20&sort=lastpost&order=desc&daysprune=-1&prefixid=Ebony&page="))
		self.genreliste.append(("Blowjob", "http://g-stream.in/forumdisplay.php?s=&f=661&page=1&pp=20&sort=lastpost&order=desc&daysprune=-1&prefixid=Blowjob&page="))
		self.genreliste.append(("Fetish", "http://g-stream.in/forumdisplay.php?s=&f=661&page=1&pp=20&sort=lastpost&order=desc&daysprune=-1&prefixid=Fetish&page="))
		self.genreliste.append(("Gay", "http://g-stream.in/forumdisplay.php?s=&f=661&page=1&pp=20&sort=lastpost&order=desc&daysprune=-1&prefixid=Gay&page="))
		self.genreliste.append(("German", "http://g-stream.in/forumdisplay.php?s=&f=661&page=1&pp=20&sort=lastpost&order=desc&daysprune=-1&prefixid=Deutsch&page="))
		self.genreliste.append(("Group Sex", "http://g-stream.in/forumdisplay.php?s=&f=661&page=1&pp=20&sort=lastpost&order=desc&daysprune=-1&prefixid=Gruppensex&page="))
		self.genreliste.append(("Hardcore", "http://g-stream.in/forumdisplay.php?s=&f=661&page=1&pp=20&sort=lastpost&order=desc&daysprune=-1&prefixid=Hardcore&page="))
		self.genreliste.append(("Interracial", "http://g-stream.in/forumdisplay.php?s=&f=661&page=1&pp=20&sort=lastpost&order=desc&daysprune=-1&prefixid=International&page="))
		self.genreliste.append(("Lesbian", "http://g-stream.in/forumdisplay.php?s=&f=661&page=1&pp=20&sort=lastpost&order=desc&daysprune=-1&prefixid=Lesben&page="))
		self.genreliste.append(("Masturbation", "http://g-stream.in/forumdisplay.php?s=&f=661&page=1&pp=20&sort=lastpost&order=desc&daysprune=-1&prefixid=Masturbation&page="))
		self.genreliste.append(("Teens", "http://g-stream.in/forumdisplay.php?s=&f=661&page=1&pp=20&sort=lastpost&order=desc&daysprune=-1&prefixid=Teens&page="))
		self.chooseMenuList.setList(map(gstreaminxxxGenreListEntry, self.genreliste))
		self.keyLocked = False

	def dataError(self, error):
		print error

	def keyOK(self):
		if self.keyLocked:
			return
		streamGenreLink = self['genreList'].getCurrent()[0][1]
		self.session.open(gstreaminxxxFilmScreen, streamGenreLink)
		
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

class gstreaminxxxFilmScreen(Screen):
	
	def __init__(self, session, phCatLink):
		self.session = session
		self.phCatLink = phCatLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/XXXFilmScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/XXXFilmScreen.xml"
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

		self['title'] = Label("G-Stream.in")
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
		url = "%s%s" % (self.phCatLink, str(self.page))
		print url
		getPage(url, agent=special_headers, headers={'Cookie': 'sitechrx='+sitechrx}).addCallback(self.loadData).addErrback(self.dataError)
	
	def loadData(self, data):
		lastp = re.findall('normal">Seite.*?von\s(.*?)</td>', data, re.S)
		if lastp:
			lastp = lastp[0]
			print lastp
			self.lastpage = int(lastp)
		else:
			self.lastpage = 1
		self['page'].setText(str(self.page) + ' / ' + str(self.lastpage))	
		phMovies = re.findall('class="p1"\shref="(.*?)".*?class="large"\ssrc="(.*?)".*?thread_title_[0-9]+".*?>(.*?)</a>', data, re.S)
		if phMovies:
			for (phUrl, phImage, phTitle) in phMovies:
				phUrl = phUrl.replace('&amp;','&')
				phUrl = 'http://g-stream.in/' + phUrl
				if re.search('images-box.com|rapidimg.org|your-imag.es|pics-traderz.org|imgload.biz|lulzimg.com|shareimage.me|pic.ms', str(phImage), re.S):
					phImage = None
				self.filmliste.append((decodeHtml(phTitle), phUrl, phImage))
			self.chooseMenuList.setList(map(gstreaminxxxFilmListEntry, self.filmliste))
			self.chooseMenuList.moveToIndex(0)
			self.keyLocked = False
			self.showInfos()

	def dataError(self, error):
		print error

	def showInfos(self):
		phTitle = self['genreList'].getCurrent()[0][0]
		phImage = self['genreList'].getCurrent()[0][2]
		self['name'].setText(phTitle)
		print phImage
		if not phImage == None:
			downloadPage(phImage, "/tmp/Icon.jpg").addCallback(self.ShowCover)
		else:
			self.ShowCoverNone()		

	def ShowCover(self, picData):
		picPath = "/tmp/Icon.jpg"
		self.ShowCoverFile(picPath)

	def ShowCoverNone(self):
		picPath = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/images/no_coverArt.png" % config.mediaportal.skin.value
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
		self.session.open(gstreaminxxxStreamListeScreen, phLink, phTitle)

	def keyCancel(self):
		self.close()

class gstreaminxxxStreamListeScreen(Screen):
	
	def __init__(self, session, streamFilmLink, streamName):
		self.session = session
		self.streamFilmLink = streamFilmLink
		self.streamName = streamName

		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/XXXGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/XXXGenreScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("G-Stream.in")
		self['name'] = Label('Bitte warten...')
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		getPage(self.streamFilmLink, agent=special_headers, headers={'Cookie': 'sitechrx='+sitechrx}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		print "daten bekommen"
		raw = re.findall('<table\sid="post[0-9]+"(.*?)</table>', data, re.S)
		streams = re.findall('"(http://.*?(g-stream.in\/secure\/.*?\/|flashx|[w]+.putlocker|.).*?)"', raw[0], re.S)
		if streams:
			for (stream, hostername) in streams:
				if re.match('.*?(putlocker|sockshare|streamclou|xvidstage|filenuke|movreel|nowvideo|xvidstream|uploadc|vreer|MonsterUploads|Novamov|Videoweed|Divxstage|Ginbig|Flashstrea|Movshare|yesload|faststream|Vidstream|PrimeShare|flashx|Divxmov|Putme|Zooupload|Wupfile)', hostername.strip(' '), re.S|re.I):
					print hostername, stream
					if hostername == 'flashx':
						hostername = 'Flashx'
					if hostername == 'www.putlocker':
						hostername = 'Putlocker'
					hostername = hostername.replace('g-stream.in/secure/streamcloud.eu/', 'Streamcloud (Secure)')
					hostername = hostername.replace('g-stream.in/secure/flashx.tv/', 'Flashx (Secure)')
					hostername = hostername.replace('g-stream.in/secure/www.putlocker.com/', 'Putlocker (Secure)')
					self.filmliste.append((hostername, stream))
		if len(self.filmliste) < 1:
			self.filmliste.append(('Keine Streams gefunden.', None))
		self.filmliste = list(set(self.filmliste))
		self.filmliste.sort()
		self.chooseMenuList.setList(map(gstreaminxxxHosterListEntry, self.filmliste))
		self['name'].setText(self.streamName)
		self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return
		streamLink = self['genreList'].getCurrent()[0][1]
		streamHoster = self['genreList'].getCurrent()[0][0]
		if streamLink == None:
			return
		url = streamLink
		url = url.replace('&amp;','&')
		print 'Hoster: ' + streamHoster
		print 'URL: ' + url
		self['name'].setText('Bitte warten...')
		if streamHoster == 'Flashx':
			print 'Direct Play'
			self.get_stream(url)
		elif streamHoster == 'Putlocker':
			print 'Direct Play'
			self.get_stream(url)
		else:
			print 'Secured Play'
			getPage(streamLink, agent=special_headers, headers={'Cookie': 'sitechrx='+sitechrx}).addCallback(self.getVideoPage).addErrback(self.dataError)

	def getVideoPage(self, data):
		# secured streamcloud url
		videoPage = re.findall('<script.*?src="http://meta.streamcloud.eu/agever.php\?detect=1&ref=.*?src=(.*?)"></script>', data, re.S)
		if not videoPage:
			# secured flashx url
			videoPage = re.findall('<meta\sproperty="og:video"\scontent=\'(.*?)\'>', data, re.S)
		if not videoPage:
			# secured putlocker url
			videoPage = re.findall('src=".*?smarterdownloads.*file=(.*?)\&subid', data, re.S)
		if videoPage:
			for phurl in videoPage:
				url = unquote(phurl)
				self.get_stream(url)

	def get_stream(self,url):
		get_stream_link(self.session).check_link(url, self.got_link)

	def got_link(self, stream_url):
		self['name'].setText(self.streamName)
		if stream_url == None:
			message = self.session.open(MessageBox, _("Stream not found, try another Stream Hoster."), MessageBox.TYPE_INFO, timeout=3)
		else:
			sref = eServiceReference(0x1001, 0, stream_url)
			sref.setName(self.streamName)
			self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()