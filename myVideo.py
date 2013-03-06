from imports import *
from decrypt import *

def myVideoGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

class myVideoGenreScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/myVideoGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/myVideoGenreScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['title'] = Label("MyVideo.de")
		self['name'] = Label("Genre Auswahl")
		self['coverArt'] = Pixmap()
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.genreliste.append(("Alle Filme", "74594"))
		self.genreliste.append(("Comedy", "74588"))
		self.genreliste.append(("Drama", "74589"))
		self.genreliste.append(("Thriller", "74590"))
		self.genreliste.append(("Horror", "74591"))
		self.genreliste.append(("Action", "74592"))
		self.genreliste.append(("Sci-Fi", "74593"))
		self.genreliste.append(("Western", "75189"))
		self.genreliste.append(("Dokumentation", "76116"))
		#self.genreliste.append(("Konzerte", "75833"))
		self.chooseMenuList.setList(map(myVideoGenreListEntry, self.genreliste))

	def keyOK(self):
		streamGenreLink = self['genreList'].getCurrent()[0][1]
		print streamGenreLink
		self.session.open(myVideoFilmScreen, streamGenreLink)

	def keyCancel(self):
		self.close()

def myVideoFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]
		
class myVideoFilmScreen(Screen):
	
	def __init__(self, session, myID):
		self.session = session
		self.myID = myID
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/myVideoFilmScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/myVideoFilmScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up"    : self.keyUp,
			"down"  : self.keyDown,
			"left"  : self.keyLeft,
			"right" : self.keyRight,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown
		}, -1)
		
		self.keyLocked = True
		self.page = 1
		self['title'] = Label("MyVideo.de")
		self['roflPic'] = Pixmap()
		self['name'] = Label("")
		self['page'] = Label("1")
		self['handlung'] = Label("")
		self.mvListe = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['roflList'] = self.chooseMenuList
		
		self.GK = ('WXpnME1EZGhNRGhpTTJNM01XVmhOREU0WldNNVpHTTJOakpt'
			'TW1FMU5tVTBNR05pWkRaa05XRXhNVFJoWVRVd1ptSXhaVEV3'
			'TnpsbA0KTVRkbU1tSTRNdz09')

		self.onLayoutFinish.append(self.loadPage)

	def __md5(self, s):
		return hashlib.md5(s).hexdigest()

	def __rc4crypt(self, data, key):
		x = 0
		box = range(256)
		for i in range(256):
			x = (x + box[i] + ord(key[i % len(key)])) % 256
			box[i], box[x] = box[x], box[i]
		x = 0
		y = 0
		out = []
		for char in data:
			x = (x + 1) % 256
			y = (y + box[x]) % 256
			box[x], box[y] = box[y], box[x]
			out.append(chr(ord(char) ^ box[(box[x] + box[y]) % 256]))
		return ''.join(out)
		
	def loadPage(self):
		self.keyLocked = True
		url = "http://www.myvideo.de/iframe.php?lpage=%s&function=mv_success_box&action=filme_video_list&searchGroup=%s&searchOrder=1" % (str(self.page), self.myID)
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def loadPageData(self, data):
		mvVideo = re.findall("<div class='vThumb vViews'><a href='(.*?)' class='vLink' title='(.*?)'.*?src='(.*?.jpg)' class='vThumb' alt=''/><span class='vViews' id='.*?'>(.*?)</span></a></div><div class='clear'>.*?href='.*?' title='(.*?)'", data, re.S)
		if mvVideo:
			self.mvListe = []
			for (mvUrl,mvHandlung,mvImage,mvRuntime,mvTitle) in mvVideo:
				mvUrl = "http://www.myvideo.de" + mvUrl
				self.mvListe.append((decodeHtml(mvTitle), mvUrl, mvImage, decodeHtml(mvHandlung), mvRuntime))
			self.chooseMenuList.setList(map(myVideoFilmListEntry, self.mvListe))
			self.keyLocked = False
			self.showPic()

	def dataError(self, error):
		print error
		
	def showPic(self):
		myTitle = self['roflList'].getCurrent()[0][0]
		myPicLink = self['roflList'].getCurrent()[0][2]
		myHandlung = self['roflList'].getCurrent()[0][3]
		self['name'].setText(myTitle)
		self['page'].setText(str(self.page))
		self['handlung'].setText(myHandlung)
		downloadPage(myPicLink, "/tmp/myPic.jpg").addCallback(self.roflCoverShow)
		
	def roflCoverShow(self, data):
		if fileExists("/tmp/myPic.jpg"):
			self['roflPic'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['roflPic'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/myPic.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['roflPic'].instance.setPixmap(ptr.__deref__())
					self['roflPic'].show()
					del self.picload

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
		self['roflList'].pageUp()
		self.showPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['roflList'].pageDown()
		self.showPic()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['roflList'].up()
		self.showPic()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['roflList'].down()
		self.showPic()
		
	def keyOK(self):
		if self.keyLocked:
			return
		mvUrl = self['roflList'].getCurrent()[0][1]
		print mvUrl
		id = re.findall('/watch/(.*?)/', mvUrl)
		if id:
			url = "http://www.myvideo.de/dynamic/get_player_video_xml.php?ID=" + id[0]
			getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData, id[0]).addErrback(self.dataError)

	def parseData(self, data, token):
		data = data.replace("_encxml=","")
		kiTitle = self['roflList'].getCurrent()[0][0]
		enc_data_b = unhexlify(data)
		sk = self.__md5(b64decode(b64decode(self.GK)) + self.__md5(str(token)))
		dec_data = self.__rc4crypt(enc_data_b, sk)
		if dec_data:
			url = re.findall("connectionurl='(.*?)'", dec_data, re.S)
			source = re.findall("source='(.*?)'", dec_data, re.S)
			url = unquote(url[0])
			token = re.findall('\\?(.*)', url, re.S)
			source = unquote(source[0])
			vorne = re.findall('(.*?)\.', source, re.S)
			hinten = re.findall('\.(.*[a-zA-Z0-9])', source, re.S)
			string23 = "/%s:%s" % (hinten[0], vorne[0])
			playpath = '%s:%s?%s' % (hinten[0], vorne[0],token[0])
			mvStream = '%s%s playpath=%s' % (url, string23,playpath)
			if mvStream:
				print mvStream
				sref = eServiceReference(0x1001, 0, mvStream)
				sref.setName(kiTitle)
				self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()
