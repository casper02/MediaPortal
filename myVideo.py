from imports import *
from decrypt import *

def myVideoGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

class myVideoGenreScreen(Screen):
	skin = 	"""
		<screen name="MyVideo.de" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="genreList" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,440" size="160,120" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
		</screen>"""

	def __init__(self, session):
		self.session = session
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
	skin = 	"""
		<screen name="MyVideo.de" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="roflList" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="roflPic" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<eLabel text="Page" position="750,420" size="100,25" backgroundColor="#00101214" transparent="1" foregroundColor="#00555556" font="Regular;20" valign="top" />
			<widget name="page" position="850,420" size="30,25" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
			<widget name="handlung" position="205,473" size="680,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
		</screen>"""

	def __init__(self, session, myID):
		self.session = session
		self.myID = myID
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
				#print mvTitle, mvUrl, mvImage
				mvUrl = "http://www.myvideo.de" + mvUrl
				self.mvListe.append((mvTitle, mvUrl, mvImage, mvHandlung, mvRuntime))
			self.chooseMenuList.setList(map(myVideoFilmListEntry, self.mvListe))
			#self.kiListe.append((kiTitle.replace('_',' '),kiUrl,kiImage))
			#self.chooseMenuList.setList(map(kinderKinoListEntry, self.kiListe))
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
