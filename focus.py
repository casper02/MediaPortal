from imports import *
from decrypt import *

def focusGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

class focusGenre(Screen):
	skin = 	"""
		<screen name="Focus" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="550,20" size="300,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="genreList" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget source="session.CurrentService" render="Label" position="640,420" size="120,40" font="Regular;26" foregroundColor="#00e5b243" backgroundColor="#00101214" halign="right" transparent="1">
				<convert type="ServicePosition">Length</convert>
			</widget>
			<eLabel position="215,460" size="565,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,440" size="160,120" transparent="1" alphatest="blend" />
		</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("Focus.de - VideoPortal")
		self['name'] = Label("Genre Auswahl")
		self['coverArt'] = Pixmap()
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.genreliste.append(("Neuste Videos", "http://www.focus.de/ajax/video/videoplaylist/?playlist_name=newest"))
		self.genreliste.append(("Politik", "http://www.focus.de/ajax/video/videoplaylist/?playlist_name=politik"))
		self.genreliste.append(("Finanzen", "http://www.focus.de/ajax/video/videoplaylist/?playlist_name=finance"))
		self.genreliste.append(("Wissen", "http://www.focus.de/ajax/video/videoplaylist/?playlist_name=knowledge"))
		self.genreliste.append(("Gesundheit", "http://www.focus.de/ajax/video/videoplaylist/?playlist_name=healthiness"))
		self.genreliste.append(("Kultur", "http://www.focus.de/ajax/video/videoplaylist/?playlist_name=culture"))
		self.genreliste.append(("Panorama", "http://www.focus.de/ajax/video/videoplaylist/?playlist_name=panorama"))
		self.genreliste.append(("Sport", "http://www.focus.de/ajax/video/videoplaylist/?playlist_name=sport"))
		self.genreliste.append(("Digital", "http://www.focus.de/ajax/video/videoplaylist/?playlist_name=digital"))
		self.genreliste.append(("Reisen", "http://www.focus.de/ajax/video/videoplaylist/?playlist_name=travel"))
		self.genreliste.append(("Auto", "http://www.focus.de/ajax/video/videoplaylist/?playlist_name=auto"))
		self.chooseMenuList.setList(map(focusGenreListEntry, self.genreliste))

	def keyOK(self):
		streamGenreLink = self['genreList'].getCurrent()[0][1]
		print streamGenreLink
		self.session.open(focus, streamGenreLink)

	def keyCancel(self):
		self.close()
		
def focusListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]
		
class focus(Screen):
	skin = 	"""
		<screen name="Focus" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="600,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="550,20" size="300,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="streamlist" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget source="session.CurrentService" render="Label" position="640,420" size="120,40" font="Regular;26" foregroundColor="#00e5b243" backgroundColor="#00101214" halign="right" transparent="1">
				<convert type="ServicePosition">Length</convert>
			</widget>
			<eLabel position="215,460" size="565,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,440" size="160,120" transparent="1" alphatest="blend" />
			<widget name="handlung" position="205,473" size="680,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
		</screen>"""

	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok" : self.keyOK,
			"cancel" : self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)
		
		self['title'] = Label("Focus.de - VideoPortal")
		self['coverArt'] = Pixmap()
		self['name'] = Label("")
		self['handlung'] = Label("")
		
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
		getPage(self.streamGenreLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.pageData).addErrback(self.dataError)
		
	def pageData(self, data):
		focusVideos = re.findall('<img heig.*?[rel|src]="(.*?.jpg)".*?[alt|title]="(.*?)".*?<a href="(.*?)"', data, re.S|re.I)
		if focusVideos:
			for (Image, Name, Link) in focusVideos:
				self.streamList.append((decodeHtml(Name), Image, Link))
			self.streamMenuList.setList(map(focusListEntry, self.streamList))
			self.keyLocked = False
			self.showInfos()

	def showInfos(self):
		if self.keyLocked:
			return
		Title = self['streamlist'].getCurrent()[0][0]
		Image = self['streamlist'].getCurrent()[0][1]
		print Title, Image.replace('" src="','')
		self['name'].setText(Title)
		self.ReadCover(Image.replace('" src="',''))

	def ReadCover(self, stationIconLink):
		Link = self['streamlist'].getCurrent()[0][2]
		downloadPage(stationIconLink, "/tmp/fIcon.jpg").addCallback(self.ShowCover)
		getPage(Link, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.handlungData).addErrback(self.dataError)

	def handlungData(self, data):
		handlung = re.findall('<meta name="description" content="(.*?)"', data, re.S)
		if handlung:
			self['handlung'].setText(decodeHtml(handlung[0]))
		else:
			self['handlung'].setText("keine infos")

	def ShowCover(self, picData):
		if fileExists("/tmp/fIcon.jpg"):
			self['coverArt'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/fIcon.jpg", 0, 0, False) == 0:
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
		print "ok"
		Link = self['streamlist'].getCurrent()[0][2]
		print Link
		getPage(Link, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.searchStream).addErrback(self.dataError)
	
	def searchStream(self, data):
		Title = self['streamlist'].getCurrent()[0][0]
		streamUrl = re.findall('sVideoURL = "(.*?)"', data, re.S)
		if streamUrl:
			if streamUrl[1]:
				streamUrl = streamUrl[1]
			else:
				streamUrl = streamUrl[0]
				
			sref = eServiceReference(0x1001, 0, streamUrl)
			sref.setName(Title)
			self.session.open(MoviePlayer, sref)
		
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