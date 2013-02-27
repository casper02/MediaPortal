from imports import *

def pornerbrosGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

def pornerbrosStreamListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 

class pornerbrosGenreScreen(Screen):
	skin = 	"""
		<screen name="pornerbros" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
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
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
		</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok" : self.keyOK,
			"cancel" : self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)

		self['title'] = Label("Pornerbros.com")
		self['name'] = Label("Genre Auswahl")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.suchString = ''
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.genreliste.append(("New", "http://www.pornerbros.com/page"))
		self.genreliste.append(("Top Rated", "http://www.pornerbros.com/best/page"))
		self.genreliste.append(("Most Viewed", "http://www.pornerbros.com/popular/page"))
		self.genreliste.append(("Most Discussed", "http://www.pornerbros.com/discussed/page"))
		self.genreliste.append(("Longest", "http://www.pornerbros.com/longest/page"))
		self.genreliste.append(("Creampie", "http://www.pornerbros.com/category/creampie/page"))
		self.genreliste.append(("Cuckolding", "http://www.pornerbros.com/category/cuckolding/page"))
		self.genreliste.append(("Cumshot", "http://www.pornerbros.com/category/cumshot/page"))
		self.genreliste.append(("Double Penetration", "http://www.pornerbros.com/category/dp/page"))
		self.genreliste.append(("Drunk Girls", "http://www.pornerbros.com/category/drunk-girls/page"))
		self.genreliste.append(("Ebony", "http://www.pornerbros.com/category/ebony/page"))
		self.genreliste.append(("Euro", "http://www.pornerbros.com/category/european/page"))
		self.genreliste.append(("Fat Girls", "http://www.pornerbros.com/category/fat/page"))
		self.genreliste.append(("Female Friendly", "http://www.pornerbros.com/category/female-friendly/page"))
		self.genreliste.append(("Femdom", "http://www.pornerbros.com/category/femdom/page"))
		self.genreliste.append(("Fetish", "http://www.pornerbros.com/category/fetish/page"))
		self.genreliste.append(("Fisting", "http://www.pornerbros.com/category/fisting/page"))
		self.genreliste.append(("Gangbang", "http://www.pornerbros.com/category/gang-bang/page"))
		self.genreliste.append(("Gay", "http://www.pornerbros.com/category/gay/page"))
		self.genreliste.append(("Girlfriend", "http://www.pornerbros.com/category/exgf/page"))
		self.genreliste.append(("Granny", "http://www.pornerbros.com/category/granny/page"))
		self.genreliste.append(("Group", "http://www.pornerbros.com/category/group-sex/page"))
		self.genreliste.append(("Hairy Pussy", "http://www.pornerbros.com/category/hairy/page"))
		self.genreliste.append(("Handjob", "http://www.pornerbros.com/category/handjob/page"))
		self.genreliste.append(("Hardcore", "http://www.pornerbros.com/category/hardcore/page"))
		self.genreliste.append(("Hentai", "http://www.pornerbros.com/category/hentai/page"))
		self.genreliste.append(("High Definition", "http://www.pornerbros.com/category/hd/page"))
		self.genreliste.append(("Interracial", "http://www.pornerbros.com/category/interracial/page"))
		self.genreliste.append(("Latina", "http://www.pornerbros.com/category/latina/page"))
		self.genreliste.append(("Lesbian", "http://www.pornerbros.com/category/lesbians/page"))
		self.genreliste.append(("Massage", "http://www.pornerbros.com/category/massage/page"))
		self.genreliste.append(("Masturbation", "http://www.pornerbros.com/category/masturbation/page"))
		self.genreliste.append(("Mature", "http://www.pornerbros.com/category/mature/page"))
		self.genreliste.append(("Midget", "http://www.pornerbros.com/category/midget/page"))
		self.genreliste.append(("MILF", "http://www.pornerbros.com/category/milf/page"))
		self.genreliste.append(("Office", "http://www.pornerbros.com/category/office-sex/page"))
		self.genreliste.append(("Old & Young", "http://www.pornerbros.com/category/old-young/page"))
		self.genreliste.append(("Orgy", "http://www.pornerbros.com/category/orgy/page"))
		self.genreliste.append(("Outdoor", "http://www.pornerbros.com/category/outdoor-sex/page"))
		self.genreliste.append(("POV", "http://www.pornerbros.com/category/pov/page"))
		self.genreliste.append(("Pissing", "http://www.pornerbros.com/category/pissing/page"))
		self.genreliste.append(("Pornstars", "http://www.pornerbros.com/category/pornstars/page"))
		self.genreliste.append(("Pregnant", "http://www.pornerbros.com/category/pregnant/page"))
		self.genreliste.append(("Public", "http://www.pornerbros.com/category/public-sex/page"))
		self.genreliste.append(("Pussy", "http://www.pornerbros.com/category/pussy/page"))
		self.genreliste.append(("Redhead", "http://www.pornerbros.com/category/redhead/page"))
		self.genreliste.append(("Sex Party", "http://www.pornerbros.com/category/sex-party/page"))
		self.genreliste.append(("Shemale", "http://www.pornerbros.com/category/shemale/page"))
		self.genreliste.append(("Solo", "http://www.pornerbros.com/category/solo/page"))
		self.genreliste.append(("Squirting", "http://www.pornerbros.com/category/squirting/page"))
		self.genreliste.append(("Stockings", "http://www.pornerbros.com/category /category/stockings/page"))
		self.genreliste.append(("Teen", "http://www.pornerbros.com/category /category/teens/page"))
		self.genreliste.append(("Threesome", "http://www.pornerbros.com/category/threesome/page"))
		self.genreliste.append(("Toys", "http://www.pornerbros.com/category/toys/page"))
		self.genreliste.append(("Uniform", "http://www.pornerbros.com/category/uniform/page"))
		self.genreliste.append(("Vintage", "http://www.pornerbros.com/category/vintage/page"))
		self.genreliste.append(("Voyeur", "http://www.pornerbros.com/category/voyeur/page"))
		self.genreliste.append(("Webcam", "http://www.pornerbros.com/category/webcam/page"))
		self.chooseMenuList.setList(map(pornerbrosGenreListEntry, self.genreliste))
		
	def keyOK(self):
		streamGenreLink = self['genreList'].getCurrent()[0][1]
		self.session.open(pornerbrosFilmScreen, streamGenreLink)

	def keyLeft(self):
		self['genreList'].pageUp()
		
	def keyRight(self):
		self['genreList'].pageDown()
		
	def keyUp(self):
		self['genreList'].up()
		
	def keyDown(self):
		self['genreList'].down()

	def keyCancel(self):
		self.close()
		
class pornerbrosFilmScreen(Screen):
	skin = 	"""
		<screen name="Pornerbros.com" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="streamlist" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget source="session.CurrentService" render="Label" position="640,420" size="120,40" font="Regular;26" foregroundColor="#00e5b243" backgroundColor="#00101214" halign="right" transparent="1">
				<convert type="ServicePosition">Length</convert>
			</widget>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,440" size="160,120" transparent="1" alphatest="blend" />
			<eLabel text="Views" position="230,470" size="100,25" backgroundColor="#00101214" transparent="1" foregroundColor="#00555556" font="Regular;20" valign="top" />
			<widget name="views" position="330,470" size="580,25" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
			<eLabel text="Runtime" position="230,500" size="100,25" backgroundColor="#00101214" transparent="1" foregroundColor="#00555556" font="Regular;20" valign="top" />
			<widget name="runtime" position="330,500" size="580,25" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
			<eLabel text="Page" position="230,530" size="100,25" backgroundColor="#00101214" transparent="1" foregroundColor="#00555556" font="Regular;20" valign="top" />
			<widget name="page" position="330,530" size="580,25" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
			<widget source="session.CurrentService" render="Label" position="330,70" size="120,24" zPosition="1" font="Regular;24" halign="left" transparent="1">
					<convert type="ServicePosition">Position,ShowHours</convert>
			</widget>
		</screen>"""

	def __init__(self, session, phCatLink):
		self.session = session
		self.phCatLink = phCatLink
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
		
		self['title'] = Label("Pornbros.com")
		self['name'] = Label("Film Auswahl")
		self['views'] = Label("")
		self['runtime'] = Label("")
		self['page'] = Label("1")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.page = 1
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 23))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList

		self.onLayoutFinish.append(self.loadpage)

	def loadpage(self):
		self.keyLocked = True
		self.streamList = []
		self['page'].setText(str(self.page))
		url = "%s%s/" % (self.phCatLink, str(self.page))
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.pageData).addErrback(self.dataError)

	def pageData(self, data):
		xhListe = re.findall('<div class="contents_gallery_item">.*?<a href="(.*?)" title="(.*?)".*?gid="(.*?)".*?data-original="(.*?.jpg)".*?length">(.*?)<.*?views">(.*?)</span>', data, re.S)
		if xhListe:
			for (xhLink, xhName, xhIdnr, xhImage, xhRuntime, xhViews) in xhListe:
				self.streamList.append((xhName, xhLink, xhIdnr, xhImage, xhRuntime, xhViews))
			self.streamMenuList.setList(map(pornerbrosStreamListEntry, self.streamList))
			self.keyLocked = False
			self.showInfos()

	def showInfos(self):
		if self.keyLocked:
			return
		ptTitle = self['streamlist'].getCurrent()[0][0]
		ptImage = self['streamlist'].getCurrent()[0][3]
		ptRuntime = self['streamlist'].getCurrent()[0][4]
		ptViews = self['streamlist'].getCurrent()[0][5]
		ptViews = ptViews.replace(' ','')
		ptViews = ptViews.replace('views','')
		ptViews = ptViews.replace('\r','')
		ptViews = ptViews.replace('\n','')
		ptViews = ptViews.replace('\t','')
		self.ptRead(ptImage)
		self['name'].setText(ptTitle)
		self['runtime'].setText(ptRuntime)
		self['page'].setText(str(self.page))
		self['views'].setText(ptViews)
		
	def ptRead(self, stationIconLink):
		downloadPage(stationIconLink, "/tmp/xhIcon.jpg").addCallback(self.ptCoverShow)

	def ptCoverShow(self, picData):
		if fileExists("/tmp/xhIcon.jpg"):
			self['coverArt'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/xhIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr.__deref__())
					self['coverArt'].show()
					del self.picload

	def dataError(self, error):
		print error
	
	def keyOK(self):
		if self.keyLocked:
			return
                scriptid = self['streamlist'].getCurrent()[0][2]
                xhLink = 'http://www.pornerbros.com/content/%s.js' % scriptid
		xhTitle = self['streamlist'].getCurrent()[0][0]
            	data = urllib.urlopen(xhLink).read()
            	xhStream = re.findall("url.*?escape.*?'(.*?)'", data, re.S)
		
		if xhStream:
			sref = eServiceReference(0x1001, 0, xhStream[0])
			sref.setName(xhTitle)
			self.session.open(MoviePlayer, sref)
            	else:
                	print "no video url found."

	def keyPageNumber(self):
		self.session.openWithCallback(self.callbackkeyPageNumber, VirtualKeyBoard, title = (_("Seitennummer eingeben")), text = str(self.page))

	def callbackkeyPageNumber(self, answer):
		if answer is not None:
			self.page = int(answer)
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
		self.page += 1
		self.loadpage()
		
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
