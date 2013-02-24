from imports import *
from decrypt import *

def xhamsterGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

class xhamsterGenreScreen(Screen):
	skin = 	"""
		<screen name="xHamster.com" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
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
		
		self['title'] = Label("xHamster.com")
		self['name'] = Label("Genre Auswahl")
		self['coverArt'] = Pixmap()
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.genreliste.append(("New", "http://www.xhamster.com/new/"))
		self.genreliste.append(("HD Videos", "http://www.xhamster.com/channels/new-hd_videos-"))
		self.genreliste.append(("Amateur", "http://www.xhamster.com/channels/new-amateur-"))
		self.genreliste.append(("Anal", "http://www.xhamster.com/channels/new-anal-"))
		self.genreliste.append(("Arab", "http://www.xhamster.com/channels/new-arab-"))
		self.genreliste.append(("Asian", "http://www.xhamster.com/channels/new-asian-"))
		self.genreliste.append(("Babes", "http://www.xhamster.com/channels/new-babes-"))
                self.genreliste.append(("Babysitters", "http://www.xhamster.com/channels/new-babysitters-"))
		self.genreliste.append(("BBW", "http://www.xhamster.com/channels/new-bbw-"))
		self.genreliste.append(("BDSM", "http://www.xhamster.com/channels/new-bdsm-"))
		self.genreliste.append(("Beach", "http://www.xhamster.com/channels/new-beach-"))
		self.genreliste.append(("Big Boobs", "http://www.xhamster.com/channels/new-big_boobs-"))
		self.genreliste.append(("Bisexuals", "http://www.xhamster.com/channels/new-bisexuals-"))
		self.genreliste.append(("Black and Ebony", "http://www.xhamster.com/channels/new-ebony-"))
		self.genreliste.append(("Black Gays", "http://www.xhamster.com/channels/new-black_gays-"))
		self.genreliste.append(("Blondes", "http://www.xhamster.com/channels/new-blondes-"))
		self.genreliste.append(("Blowjobs", "http://www.xhamster.com/channels/new-blowjobs-"))
		self.genreliste.append(("Brazilian", "http://www.xhamster.com/channels/new-brazilian-"))
		self.genreliste.append(("British", "http://www.xhamster.com/channels/new-british-"))
		self.genreliste.append(("Brunettes", "http://www.xhamster.com/channels/new-brunettes-"))
		self.genreliste.append(("Bukkake", "http://www.xhamster.com/channels/new-bukkake-"))
		self.genreliste.append(("Cartoons", "http://www.xhamster.com/channels/new-cartoons-"))
		self.genreliste.append(("Celebrities", "http://www.xhamster.com/channels/new-celebs-"))
		self.genreliste.append(("Chinese", "http://www.xhamster.com/channels/new-chinese-"))
		self.genreliste.append(("Close-ups", "http://www.xhamster.com/channels/new-close_ups-"))
		self.genreliste.append(("Cream Pie", "http://www.xhamster.com/channels/new-creampie-"))
		self.genreliste.append(("Cuckold", "http://www.xhamster.com/channels/new-cuckold-"))
		self.genreliste.append(("Cumshots", "http://www.xhamster.com/channels/new-cumshots-"))
		self.genreliste.append(("Czech", "http://www.xhamster.com/channels/new-czech-"))
		self.genreliste.append(("Danish", "http://www.xhamster.com/channels/new-danish-"))
		self.genreliste.append(("Double Penetration", "http://www.xhamster.com/channels/new-double_penetration-"))
		self.genreliste.append(("Emo", "http://www.xhamster.com/channels/new-emo-"))
		self.genreliste.append(("Face Sitting", "http://www.xhamster.com/channels/new-face_sitting-"))
		self.genreliste.append(("Facials", "http://www.xhamster.com/channels/new-facials-"))
		self.genreliste.append(("Female Choice", "http://www.xhamster.com/channels/new-female_choice-"))
		self.genreliste.append(("Femdom", "http://www.xhamster.com/channels/new-femdom-"))
		self.genreliste.append(("Fingering", "http://www.xhamster.com/channels/new-fingering-"))
		self.genreliste.append(("Flashing", "http://www.xhamster.com/channels/new-flashing-"))
		self.genreliste.append(("Foot Fetish", "http://www.xhamster.com/channels/new-foot-fetish-"))
		self.genreliste.append(("French", "http://www.xhamster.com/channels/new-french-"))
		self.genreliste.append(("Funny", "http://www.xhamster.com/channels/new-funny-"))
		self.genreliste.append(("Gangbang", "http://www.xhamster.com/channels/new-gangbang-"))
		self.genreliste.append(("Gaping", "http://www.xhamster.com/channels/new-gaping-"))
		self.genreliste.append(("Gays", "http://www.xhamster.com/channels/new-gays-"))
		self.genreliste.append(("German", "http://www.xhamster.com/channels/new-german-"))
		self.genreliste.append(("Gothic", "http://www.xhamster.com/channels/new-gothic-"))
		self.genreliste.append(("Grannies", "http://www.xhamster.com/channels/new-grannies-"))
		self.genreliste.append(("Group Sex", "http://www.xhamster.com/channels/new-group-"))
		self.genreliste.append(("Hairy", "http://www.xhamster.com/channels/new-hairy-"))
		self.genreliste.append(("Handjobs", "http://www.xhamster.com/channels/new-handjobs-"))
		self.genreliste.append(("Hardcore", "http://www.xhamster.com/channels/new-hardcore-"))
		self.genreliste.append(("Hentai", "http://www.xhamster.com/channels/new-hentai-"))
		self.genreliste.append(("Hidden Cams", "http://www.xhamster.com/channels/new-hidden-"))
		self.genreliste.append(("Hits", "http://www.xhamster.com/channels/new-hits-"))
		self.genreliste.append(("Indian", "http://www.xhamster.com/channels/new-indian-"))
		self.genreliste.append(("Interracial", "http://www.xhamster.com/channels/new-interracial-"))
		self.genreliste.append(("Italian", "http://www.xhamster.com/channels/new-italian-"))
		self.genreliste.append(("Japanese", "http://www.xhamster.com/channels/new-japanese-"))
		self.genreliste.append(("Korean", "http://www.xhamster.com/channels/new-korean-"))
		self.genreliste.append(("Ladyboys", "http://www.xhamster.com/channels/new-ladyboys-"))
		self.genreliste.append(("Latex", "http://www.xhamster.com/channels/new-latex-"))
		self.genreliste.append(("Latin", "http://www.xhamster.com/channels/new-latin-"))
		self.genreliste.append(("Lesbians", "http://www.xhamster.com/channels/new-lesbians-"))
		self.genreliste.append(("Lingerie", "http://www.xhamster.com/channels/new-lingerie-"))
		self.genreliste.append(("Massage", "http://www.xhamster.com/channels/new-massage-"))
		self.genreliste.append(("Masturbation", "http://www.xhamster.com/channels/new-masturbation-"))
		self.genreliste.append(("Matures", "http://www.xhamster.com/channels/new-matures-"))
		self.genreliste.append(("Men", "http://www.xhamster.com/channels/new-men-"))
		self.genreliste.append(("Midgets", "http://www.xhamster.com/channels/new-midgets-"))
		self.genreliste.append(("MILFs", "http://www.xhamster.com/channels/new-milfs-"))
		self.genreliste.append(("Nipples", "http://www.xhamster.com/channels/new-nipples-"))
		self.genreliste.append(("Old+Young", "http://www.xhamster.com/channels/new-old_young-"))
		self.genreliste.append(("Pornstars", "http://www.xhamster.com/channels/new-pornstars-"))
		self.genreliste.append(("POV", "http://www.xhamster.com/channels/new-pov-"))
		self.genreliste.append(("Public Nudity", "http://www.xhamster.com/channels/new-public-"))
		self.genreliste.append(("Redheads", "http://www.xhamster.com/channels/new-redheads-"))
		self.genreliste.append(("Russian", "http://www.xhamster.com/channels/new-russian-"))
		self.genreliste.append(("Sex Toys", "http://www.xhamster.com/channels/new-toys-"))
		self.genreliste.append(("Shemales", "http://www.xhamster.com/channels/new-shemales-"))
		self.genreliste.append(("Showers", "http://www.xhamster.com/channels/new-showers-"))
		self.genreliste.append(("Softcore", "http://www.xhamster.com/channels/new-softcore-"))
		self.genreliste.append(("Spanking", "http://www.xhamster.com/channels/new-spanking-"))
		self.genreliste.append(("Squirting", "http://www.xhamster.com/channels/new-squirting-"))
		self.genreliste.append(("Stockings", "http://www.xhamster.com/channels/new-stockings-"))
		self.genreliste.append(("Strapon", "http://www.xhamster.com/channels/new-strapon-"))
		self.genreliste.append(("Swedish", "http://www.xhamster.com/channels/new-swedish-"))
		self.genreliste.append(("Swingers", "http://www.xhamster.com/channels/new-swingers-"))
		self.genreliste.append(("Teens", "http://www.xhamster.com/channels/new-teens-"))
		self.genreliste.append(("Thai", "http://www.xhamster.com/channels/new-tai-"))
		self.genreliste.append(("Threesomes", "http://www.xhamster.com/channels/new-threesomes-"))
		self.genreliste.append(("Tits", "http://www.xhamster.com/channels/new-tits-"))
		self.genreliste.append(("Turkish", "http://www.xhamster.com/channels/new-turkish-"))
		self.genreliste.append(("Upskirts", "http://www.xhamster.com/channels/new-upskirts-"))
		self.genreliste.append(("Vintage", "http://www.xhamster.com/channels/new-vintage-"))
		self.genreliste.append(("Voyeur", "http://www.xhamster.com/channels/new-voyeur-"))
		self.genreliste.append(("Webcams", "http://www.xhamster.com/channels/new-webcams-"))
		self.chooseMenuList.setList(map(xhamsterGenreListEntry, self.genreliste))

	def keyOK(self):
		streamGenreLink = self['genreList'].getCurrent()[0][1]
		print streamGenreLink
		self.session.open(xhamster, streamGenreLink)

	def keyCancel(self):
		self.close()

def xhamsterstreamListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 

class xhamster(Screen):
	skin = 	"""
		<screen name="xhamster.com" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
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

	def __init__(self, session, genreLink):
		self.session = session
		Screen.__init__(self, session)
		self.genreLink = genreLink
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok" : self.keyOK,
			"cancel" : self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown
		}, -1)
		
		self['title'] = Label("xHamster.com")
		self['coverArt'] = Pixmap()
		self['name'] = Label("")
		self['views'] = Label("")
		self['runtime'] = Label("")
		self['page'] = Label("1")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 23))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList

		self.keyLocked = False
		self.page = 1

		self.onLayoutFinish.append(self.loadpage)
		
	def loadpage(self):
		self.keyLocked = True
		self.streamList = []
		#ptUrl = "http://xhamster.com/new/%s.html" % str(self.page)
		ptUrl = "%s%s.html" % (self.genreLink, str(self.page))
		print ptUrl
		getPage(ptUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.pageData).addErrback(self.dataError)
		
	def pageData(self, data):
		xhListe = re.findall('<a href="(/movies/.*?)" class=\'hRotator\' >.*?<img src=\'(.*?)\'.*?alt="(.*?)"/>.*?<div class="moduleFeaturedDetails">Runtime: (.*?)<BR>Views: (.*?)</div>', data, re.S)
		if xhListe:
			for (xhLink, xhImage, xhName, xhRuntime, xhxhViews) in xhListe:
				xhLink = "http://xhamster.com"+xhLink
				self.streamList.append((xhName, xhImage, xhLink, xhxhViews, xhRuntime))
			self.streamMenuList.setList(map(xhamsterstreamListEntry, self.streamList))
			self.keyLocked = False
			self.showInfos()

	def showInfos(self):
		if self.keyLocked:
			return
		ptTitle = self['streamlist'].getCurrent()[0][0]
		ptImage = self['streamlist'].getCurrent()[0][1]
		ptViews  = self['streamlist'].getCurrent()[0][3]
		ptRuntime = self['streamlist'].getCurrent()[0][4]
		self.ptRead(ptImage)
		self['name'].setText(ptTitle)
		self['views'].setText(ptViews)
		self['runtime'].setText(ptRuntime)
		self['page'].setText(str(self.page))

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
		xhLink = self['streamlist'].getCurrent()[0][2]
		print xhLink
		getPage(xhLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.playData).addErrback(self.dataError)
		
	def playData(self, data):
		xhTitle = self['streamlist'].getCurrent()[0][0]
		xhServer = re.findall("'srv': '(.*?)'", data)
		xhFile = re.findall("'file': '(.*?)'", data)
		if re.match('.*?http%3A', xhFile[0]):
			xhStream = urllib2.unquote(xhFile[0])
			print xhStream
		else:
			xhStream = xhServer[0]+"/key="+xhFile[0]
			print xhStream
		
		if xhStream:
			sref = eServiceReference(0x1001, 0, xhStream)
			sref.setName(xhTitle)
			self.session.open(MoviePlayer, sref)

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
