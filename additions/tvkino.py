from Plugins.Extensions.mediaportal.resources.imports import *
from Plugins.Extensions.mediaportal.resources.decrypt import *

def tvkinoGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

class tvkino(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/tvkino.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/tvkino.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("TV-Kino.net - Watch Live TV")
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
		url = "http://www.tv-kino.net/"
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.pageData).addErrback(self.dataError)
	
	def pageData(self, data):
		sender = re.findall('<div class="portfolio-thumbnail">.*?<a title="(.*?)" href="(/stream/live/.*?)">', data, re.S)
		if sender:
			for (name, url) in sender:
				url = "http://www.tv-kino.net" + url
				print name
				self.senderliste.append((name.replace(' Online TV Live Stream',''), url))
			self.chooseMenuList.setList(map(tvkinoGenreListEntry, self.senderliste))
			self.keyLocked = False

	def dataError(self, error):
		print error
		
	def keyOK(self):
		if self.keyLocked:
			return
		name = self['genreList'].getCurrent()[0][0]
		url = self['genreList'].getCurrent()[0][1]
		print url
		self.keyLocked = True
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.streamData).addErrback(self.dataError)
		
	def streamData(self, data):
		stream_raw = re.findall('name="flashvars" value="(.*?)"', data, re.S)
		if stream_raw:
			name = self['genreList'].getCurrent()[0][0]
			self.keyLocked = False
			sender = re.findall('file=(.*?)\&', stream_raw[0])
			stream = re.findall('streamer=(rtmp.*?)\&', stream_raw[0])
			print sender, stream
			streamUrl = "%s/%s swfUrl=http://stream.tv-kino.net/player.swf" % (stream[0], sender[0])
			if streamUrl:
				print streamUrl
				sref = eServiceReference(0x1001, 0, streamUrl)
				sref.setName(name)
				self.session.open(MoviePlayer, sref)
		
	def keyCancel(self):
		self.close()