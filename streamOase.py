from imports import *
from decrypt import *


def oasetvGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 
class oasetvGenreScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/oasetvGenreScreen.xml" % config.mediaportal.skin.value
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['title'] = Label("Stream-Oase.tv")
		self['name'] = Label("Genre Auswahl")
		self['coverArt'] = Pixmap()
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.genreliste.append(("Neusten", "http://stream-oase.tv/index.php/hd-oase/video/latest?start="))
		self.genreliste.append(("Action", "http://stream-oase.tv/index.php/hd-oase/category/action?start="))
		self.genreliste.append(("Abenteuer", "http://stream-oase.tv/index.php/hd-oase/category/abenteuer?start="))
		self.genreliste.append(("Drama", "http://stream-oase.tv/index.php/hd-oase/category/drama?start="))
		self.genreliste.append(("Krieg", "http://stream-oase.tv/index.php/hd-oase/category/krieg?start="))
		self.genreliste.append(("Thriller", "http://stream-oase.tv/index.php/hd-oase/category/thriller?start="))
		self.genreliste.append(("Horror", "http://stream-oase.tv/index.php/hd-oase/category/horror?start="))
		self.genreliste.append(("Komoedie", "http://stream-oase.tv/index.php/hd-oase/category/komoedie?start="))
		self.genreliste.append(("Zeichentrick", "http://stream-oase.tv/index.php/hd-oase/category/zeichentrick?start="))
		self.genreliste.append(("Sci-fi", "http://stream-oase.tv/index.php/hd-oase/category/sci-fi?start="))
		self.genreliste.append(("Dokus", "http://stream-oase.tv/index.php/hd-oase/category/doku-s?start="))
		self.chooseMenuList.setList(map(oasetvGenreListEntry, self.genreliste))

	def keyOK(self):
		streamGenreLink = self['genreList'].getCurrent()[0][1]
		print streamGenreLink
		self.session.open(oasetvFilmListeScreen, streamGenreLink)

	def keyCancel(self):
		self.close()

def oaseFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
class oasetvFilmListeScreen(Screen):
	
	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/oasetvFilmListeScreen.xml" % config.mediaportal.skin.value
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown
		}, -1)

		self['title'] = Label("Stream-Oase.tv")
		self['name'] = Label("Film Auswahl")
		self['handlung'] = Label("")
		self['page'] = Label("0")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.filmliste = []
		self.keckse = {}
		self.page = 0
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		url = "%s%s" % (self.streamGenreLink, str(self.page))
		print url
		getPage(url, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		print "daten bekommen"
		raw = re.findall('<div id="system-message-container">(.*?)<div style="clear:both"></div>', data, re.S)
		if raw:
			filme = re.findall('<a ondragstart="return false;" href="(/index.php/hd-oase/.*?)".*?<img ondragstart="return false;" class="image" src="(.*?)".*?title="Click to View : (.*?)"', raw[0], re.S)
			if filme:
				self.filmliste = []
				for (url,image,title) in filme:
					url = "http://stream-oase.tv" + url
					self.filmliste.append((decodeHtml(title), url, image))
				self.chooseMenuList.setList(map(oaseFilmListEntry, self.filmliste))
				self.keyLocked = False
				self.loadPic()

	def loadPic(self):
		streamName = self['filmList'].getCurrent()[0][0]
		streamFilmLink = self['filmList'].getCurrent()[0][1]
		self['name'].setText(streamName)
		if int(self.page) == 0:
			self['page'].setText("0")
		else:
			pagenr = (int(self.page) / 56)
			self['page'].setText(str(pagenr))
		streamPic = self['filmList'].getCurrent()[0][2]
		downloadPage(streamPic, "/tmp/oatvIcon.jpg").addCallback(self.ShowCover)
		getPage(streamFilmLink, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageInfos).addErrback(self.dataError)
		
	def loadPageInfos(self, data):
		if re.match('.*?<strong>Inhalt:</strong></p>\r\n<p>', data, re.S):
			handlung = re.findall('<strong>Inhalt:</strong></p>\r\n<p>(.*?)</p>', data, re.S|re.I)
			if handlung:
				self['handlung'].setText(decodeHtml(handlung[0]))
			else:
				self['handlung'].setText("keine infos")
		else:
			self['handlung'].setText("keine infos")
	
	def ShowCover(self, picData):
		if fileExists("/tmp/oatvIcon.jpg"):
			self['coverArt'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/oatvIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr.__deref__())
					self['coverArt'].show()
					del self.picload

	def keyOK(self):
		if self.keyLocked:
			return
		streamLink = self['filmList'].getCurrent()[0][1]
		print streamLink
		self.keyLocked = True
		getPage(streamLink, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.findStream).addErrback(self.dataError)

	def findStream(self, data):
		stream_list = []
		stream_name = self['filmList'].getCurrent()[0][0]
		get_embed = re.findall('http://180upload.com/embed-(.*?)-', data, re.S)
		if get_embed:
			url = "http://180upload.com/" + get_embed[0]
			print url
			stream_list.append(("180upload", url))
		get_wupfile = re.findall('(http://wupfile.com.*?)"', data, re.S)
		if get_wupfile:
			print get_wupfile[0]
			stream_list.append(("Wupfile", get_wupfile[0]))
		mighty = re.findall('(http://www.mightyupload.com/embed.*?)"', data, re.S)
		if mighty:
			print mighty[0]
			stream_list.append(("MightyUpload", mighty[0]))

		self.keyLocked = False
		self.session.open(oasetvCDListeScreen, stream_list, stream_name)

	def keyLeft(self):
		if self.keyLocked:
			return
		self['filmList'].pageUp()
		self.loadPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['filmList'].pageDown()
		self.loadPic()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['filmList'].up()
		self.loadPic()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['filmList'].down()
		self.loadPic()
		
	def keyPageDown(self):
		print "PageDown"
		if self.keyLocked:
			return
		if not self.page < 56:
			self.page -= 56
			self.loadPage()
			
	def keyPageUp(self):
		print "PageUp"
		if self.keyLocked:
			return
		self.page += 56 
		self.loadPage()
			
	def keyCancel(self):
		self.close()

def oasetvCDListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 
class oasetvCDListeScreen(Screen):
	
	def __init__(self, session, parts, stream_name):
		self.session = session
		self.streamParts = parts
		self.stream_name = stream_name
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/oasetvCDListeScreen.xml" % config.mediaportal.skin.value
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("Stream-Oase.tv")
		self['name'] = Label("Part Auswahl")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = False
		self.keckse = {}
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		for (name,url) in self.streamParts:
			print name, url
			self.filmliste.append((name, url))
		self.chooseMenuList.setList(map(oasetvCDListEntry, self.filmliste))		
		
	def keyOK(self):
		if self.keyLocked:
			return
			
		name = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]
		self.keyLocked = True
		if name == "180upload":
			getPage(streamLink, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.readPostData, streamLink).addErrback(self.dataError)
		elif name == "Wupfile":
			getPage(streamLink, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.postData).addErrback(self.dataError)
		elif name == "MightyUpload":
			getPage(streamLink, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.postData2).addErrback(self.dataError)
		
	def readPostData(self, data, url):
		form_values = {}
		for i in re.finditer('<input.*?name="(.*?)".*?value="(.*?)">', data):
			form_values[i.group(1)] = i.group(2)
				
		form_values = urllib.urlencode(form_values)
		getPage(url, agent=std_headers, method='POST', postdata=form_values, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.postData).addErrback(self.dataError)

	def postData(self, data):
		get_packedjava = re.findall("<script type=.text.javascript.>eval.function(.*?)</script>", data, re.S|re.DOTALL)
		if get_packedjava:
			sUnpacked = cJsUnpacker().unpackByString(get_packedjava[1])
		if sUnpacked:
			stream_url = re.findall("'file','(.*?)'", sUnpacked)
			if stream_url:
				print stream_url[0]
				sref = eServiceReference(0x1001, 0, stream_url[0])
				sref.setName(self.stream_name)
				self.session.open(MoviePlayer, sref)
		else:
			message = self.session.open(MessageBox, _("Stream not found."), MessageBox.TYPE_INFO, timeout=3)
			
	def postData2(self, data):
		get_packedjava = re.findall("<script type=.text.javascript.>eval.function(.*?)</script>", data, re.S|re.DOTALL)
		if get_packedjava:
			sUnpacked = cJsUnpacker().unpackByString(get_packedjava[1])
		if sUnpacked:
			stream_url = re.findall("'file','(.*?)'", sUnpacked)
			if stream_url:
				print stream_url[0]
				sref = eServiceReference(0x1001, 0, stream_url[0])
				sref.setName(self.stream_name)
				self.session.open(MoviePlayer, sref)
		else:
			message = self.session.open(MessageBox, _("Stream not found."), MessageBox.TYPE_INFO, timeout=3)
			
		self.keyLocked = False

	def dataError(self, error):
		self.keyLocked = False
		print error
		
	def keyCancel(self):
		self.close()