from imports import *
#from decrypt import *

def VoxnowGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]

def VoxnowFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 

def VoxnowHosterListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

class VoxnowGenreScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/VoxnowGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/VoxnowGenreScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)
		
		self['title'] = Label("Voxnow.de")
		self['name'] = Label("Genre Auswahl")
		self['handlung'] = Label("")
		self['Pic'] = Pixmap()
		
		self.genreliste = []
		self.keyLocked = True
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['List'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.keyLocked = True
		url = "http://www.voxnow.de/sendung_a_z.php"
		getPage(url, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def loadPageData(self, data):
		raw = re.findall('(<div class="m03img">.*?<div class="m03play")', data, re.S)
		if raw:
			self.genreliste = []
			genre = []
			for each in raw:
				if re.match('.*?FREE.*?Jetzt ansehen', each, re.S|re.I):
					genre += re.findall('<div class="m03img">.*?<a href="(.*?)" target="_self">\n<img border="0" height="136" width="216" src="(.*?)">\n</a></div>.*?<span class="m03date">FREE.*?<br></span><h2>(.*?)</h2>\n(.*?)</div>', each, re.S|re.I)
		if genre:
			for (url,image,title,handlung) in genre:
					print title
					url = "http://www.voxnow.de/" + url
					self.genreliste.append((title,url,image,handlung))
			self.chooseMenuList.setList(map(VoxnowGenreListEntry, self.genreliste))
			self.loadPic()
			self.keyLocked = False

	def dataError(self, error):
		print error

	def loadPic(self):
		streamName = self['List'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamHandlung = self['List'].getCurrent()[0][3]
		self['handlung'].setText(decodeHtml(streamHandlung))
		streamPic = self['List'].getCurrent()[0][2]
		downloadPage(streamPic, "/tmp/Icon.jpg").addCallback(self.ShowCover)
			
	def ShowCover(self, picData):
		if fileExists("/tmp/Icon.jpg"):
			self['Pic'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['Pic'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/Icon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['Pic'].instance.setPixmap(ptr.__deref__())
					self['Pic'].show()
					del self.picload

	def keyOK(self):
		if self.keyLocked:
			return
		streamGenreLink = self['List'].getCurrent()[0][1]
		self.session.open(VoxnowFilmeListeScreen, streamGenreLink)
		
	def keyLeft(self):
		if self.keyLocked:
			return
		self['List'].pageUp()
		self.loadPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['List'].pageDown()
		self.loadPic()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['List'].up()
		self.loadPic()

	def keyDown(self):
		if self.keyLocked:
			return
		self['List'].down()
		self.loadPic()

	def keyCancel(self):
		self.close()

class VoxnowFilmeListeScreen(Screen):
	
	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/VoxnowFilmeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/VoxnowFilmeScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
			#"up" : self.keyUp,
			#"down" : self.keyDown,
			#"right" : self.keyRight,
			#"left" : self.keyLeft,
			#"red" : self.keyTMDbInfo,
			#"nextBouquet" : self.keyPageUp,
			#"prevBouquet" : self.keyPageDown
		}, -1)

		self['title'] = Label("Voxnow.de")
		self['name'] = Label("Film Auswahl")
		
		self.keyLocked = True
		self.filmliste = []
		self.keckse = {}
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['List'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		getPage(self.streamGenreLink, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		print "daten bekommen"
		free = re.findall('<div class="line linespacer">FREE(.*?)<div class="line linespacer">PAY', data, re.S)
		if free:
			folgen = re.findall('<a href="(.*?)" title="(.*?)">.*?</a> </div>', free[0])
		
		if folgen:
			self.filmliste = []
			for (url,title) in folgen:
				print title
				url = "http://www.voxnow.de" + url.replace('amp;','')
				self.filmliste.append((decodeHtml(title), url))
			self.chooseMenuList.setList(map(VoxnowFilmListEntry, self.filmliste))
			self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return
		self.streamName = self['List'].getCurrent()[0][0]
		link = self['List'].getCurrent()[0][1]
		print link
		getPage(link, agent=std_headers, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.get_xml).addErrback(self.dataError)

	def get_xml(self, data):
		print "xml data"
		stream = re.findall("'playerdata': '(.*?)'", data, re.S)
		if stream:
			print stream[0].replace('amp;',''), self.keckse
			getPage(stream[0].replace('amp;',''), agent=std_headers, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.get_stream).addErrback(self.dataError)
		else:
			print "nix"
			
	def get_stream(self, data):
		print "stream data"
		print data
	
	def keyTMDbInfo(self):
		if TMDbPresent:
			title = self['List'].getCurrent()[0][0]
			self.session.open(TMDbMain, title)
			
	def keyCancel(self):
		self.close()
