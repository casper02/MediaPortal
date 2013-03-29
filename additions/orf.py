from Plugins.Extensions.mediaportal.resources.imports import *
from Components.config import config
from Plugins.Extensions.mediaportal.resources.playrtmpmovie import PlayRtmpMovie

def ORFGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]

def ORFFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 

class ORFGenreScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/RTLnowGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/RTLnowGenreScreen.xml"
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
		
		self['title'] = Label("ORF.de")
		self['name'] = Label("Auswahl der Sendung")
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
		url = "http://tvthek.orf.at/"
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def loadPageData(self, data):
		parse = re.search('<form\sid="programs"\saction="/programs/az"(.*)</form>', data, re.S)
		sendungen = re.findall('<option\svalue=".*?(/programs/.*?)">(.*?)</option>', parse.group(1), re.S)
		if sendungen:
			self.genreliste = []
			for (url,title) in sendungen:
				url = "http://tvthek.orf.at%s" % url
				self.genreliste.append((decodeHtml(title),url))
			self.genreliste.sort()
			self.chooseMenuList.setList(map(ORFGenreListEntry, self.genreliste))
			self.keyLocked = False

	def dataError(self, error):
		print error

	def keyOK(self):
		if self.keyLocked:
			return
		self.streamGenreLink = self['List'].getCurrent()[0][1]
		getPage(self.streamGenreLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.check_xml).addErrback(self.dataError)

	def dataError(self, error):
		print error
		
	def check_xml(self,data):
		if re.match('.*?<span>Weitere Folgen</span>', data, re.S):
			print "mehrere Folgen"
			self.session.open(ORFFilmeListeScreen, self.streamGenreLink)
		elif re.search('Keine\saktuellen\sSendungen\svorhanden', data, re.S):
			print "keine Folge"
			message = self.session.open(MessageBox, _("Aus der von Ihnen gewaehlten Kategorie kann derzeit leider keine Sendung in der TVthek angeboten werden."), MessageBox.TYPE_INFO, timeout=5)
			return
		else:
			print "eine Folge"
			xml = re.findall("ORF.flashXML = '.*?Items(.*?)'", data, re.S)
			if xml:
				data = urllib.unquote(xml[0])
				self.session.open(ORFStreamListeScreen, data)
		
	def keyLeft(self):
		self['List'].pageUp()
		
	def keyRight(self):
		self['List'].pageDown()
		
	def keyUp(self):
		self['List'].up()

	def keyDown(self):
		self['List'].down()

	def keyCancel(self):
		self.close()

class ORFFilmeListeScreen(Screen):
	
	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/RTLnowFilmeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/RTLnowFilmeScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("ORF.de")
		self['name'] = Label("Folgen Auswahl")
		
		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['List'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		getPage(self.streamGenreLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		self.filmliste = []
		folgen = re.findall('<li.*?><a href="#" class="nolink">(.*?)</a>.*?<li><a href="(.*?)">(.*?)</a></li>', data, re.S)
		if folgen:
			for (datum,url,title) in folgen:
				url = "http://tvthek.orf.at%s" % url
				title = "%s - %s" % (datum, title)
				self.filmliste.append((decodeHtml(title),url))
			self.chooseMenuList.setList(map(ORFFilmListEntry, self.filmliste))
			self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return
		streamName = self['List'].getCurrent()[0][0]
		url = self['List'].getCurrent()[0][1]
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.get_xml).addErrback(self.dataError)

	def get_xml(self, data):
			xml = re.findall("ORF.flashXML = '.*?Items(.*?)'", data, re.S)
			if xml:
				data = urllib.unquote(xml[0])
				self.session.open(ORFStreamListeScreen, data)

	def keyCancel(self):
		self.close()
		
class ORFStreamListeScreen(Screen):
	
	def __init__(self, session, data_raw):
		self.session = session
		self.data_raw = data_raw
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/RTLnowFilmeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/RTLnowFilmeScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("ORF.de")
		self['name'] = Label("Folgen Auswahl")
		
		self.keyLocked = True
		self.streamliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['List'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		print "hole daten"
		folgen = re.findall('<Title><!\[CDATA\[(.*?)\]\]></Title>.*?<VideoUrl><!\[CDATA\[(.*?mp4)\]\]></VideoUrl>', self.data_raw, re.S)
		if folgen:
			self.streamliste = []
			for (title,rtmp_link) in folgen:
					print title
					self.streamliste.append((decodeHtml(title),rtmp_link))
			self.chooseMenuList.setList(map(ORFFilmListEntry, self.streamliste))
			self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return
		title = self['List'].getCurrent()[0][0]
		url = self['List'].getCurrent()[0][1]
		if config.mediaportal.useRtmpDump.value:
			movieinfo = [url,title]
			self.session.open(PlayRtmpMovie, movieinfo, title)
		else:
			final = "%s" % url
			print final
			sref = eServiceReference(0x1001, 0, final)
			sref.setName(title)
			self.session.open(MoviePlayer, sref)
		
	def keyCancel(self):
		self.close()
