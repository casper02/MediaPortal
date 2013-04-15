from Plugins.Extensions.MediaPortal.resources.imports import *
from Plugins.Extensions.MediaPortal.resources.decrypt import *

def filmonListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 

class filmON(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/filmON.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/filmON.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("Filmon.com - Watch Live TV")
		self['name'] = Label("Sender Auswahl")
		self['coverArt'] = Pixmap()
		
		self.senderliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.keyLocked = False
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.keyLocked = True
		url = "http://www.filmon.com"
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.pageData).addErrback(self.dataError)
	
	def pageData(self, data):
		foSender = re.findall('<li chat-keyword=.*?tags="(.*?)".*?><img.*?href="(/channel/.*?)"', data, re.S)
		if foSender:
			for (foName,foUrl) in foSender:
				foUrl = "http://www.filmon.com" + foUrl
				print foUrl
				foName = foName.replace('featured ', 'Most Watched: ')
				foName = foName.replace(' Live TV ', ': ')
				foName = foName.replace(' Video On Demand ', ' VoD: ')
				self.senderliste.append((foName, foUrl))
			self.chooseMenuList.setList(map(filmonListEntry, self.senderliste))
			self.keyLocked = False

	def dataError(self, error):
		print error
		
	def keyOK(self):
		if self.keyLocked:
			return
		foTitle = self['genreList'].getCurrent()[0][0]
		foLink = self['genreList'].getCurrent()[0][1]
		print foTitle, foLink
		getPage(foLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.streamerData).addErrback(self.dataError)
		
	def streamerData(self, data):
		foTitle = self['genreList'].getCurrent()[0][0]
		streamDaten = re.findall('var channel_high_quality_stream = "(.*?)".*?var stream_url = "(.*?)"', data, re.S)
		if streamDaten:
			(rtmpFile, rtmpServer) = streamDaten[0]
			streamUrl = "%s/%s" % (rtmpServer, rtmpFile)
			sref = eServiceReference(0x1001, 0, streamUrl)
			sref.setName(foTitle)
			self.session.open(MoviePlayer, sref)		
		
	def keyCancel(self):
		self.close()