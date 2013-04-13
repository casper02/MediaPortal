from Components.config import config
from Components.ScrollLabel import ScrollLabel
from Plugins.Extensions.mediaportal.resources.imports import *
from Plugins.Extensions.mediaportal.resources.decrypt import *
from Plugins.Extensions.mediaportal.resources.yt_url import *


def youtubeGenreEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry)
		] 

def youtubeFilmeListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 


class youtubeGenreScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/youtubeAuswahl.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/youtubedefaultListeScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['leftContentTitle'] = Label("Videos suchen")
		self['stationIcon'] = Pixmap()
		self['name'] = Label("")
		self['handlung'] = Label("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('mediaportal', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList		
		self.keyLocked = False
		self.suchstring = ' '

		self.streamList.append(('Suchen'))
		self.streamMenuList.setList(map(youtubeGenreEntry, self.streamList))
					

	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		auswahl = self['streamlist'].getCurrent()[0]
		if auswahl == "Suchen":
			self.suchen()
		
	def keyCancel(self):
		self.close()


	def suchen(self):
		self.session.openWithCallback(self.SuchenCallback, VirtualKeyBoard, title = (_("Suchkriterium eingeben")), text = self.suchstring)


	def SuchenCallback(self, callback = None, entry = None):

		if callback is not None and len(callback):
			self.suchstring = callback
			callback = callback.replace(' ', '+')
			streamGenreLink = 'http://gdata.youtube.com/feeds/api/videos?q=' + callback + '&max-results=50&v=2'
			self.session.open(youtubeVideosListeScreen, streamGenreLink)



class youtubeVideosListeScreen(Screen):
	
	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		print self.streamGenreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/youtubedefaultListeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/youtubedefaultListeScreen.xml"
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
			"left" : self.keyLeft
		}, -1)

		self['title'] = Label("Youtube")
		self['name'] = Label("Videos")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.filmliste = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('mediaportal', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['filmList'] = self.streamMenuList		
		self.page = 1
		self['page'] = Label(" ")
		self.videoPrioInt = int(config.mediaportal.youtubeprio.value)
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.loadVideoLinks(self.streamGenreLink)
		
	def loadVideoLinks(self, streamGenreLink):
		self.keyLocked = True
		getPage(streamGenreLink, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadVideoLinksData).addErrback(self.dataError)

	def loadVideoLinksData(self, data):
		videoLinks = re.findall("<media:thumbnail url='(.*?)'.*?default'/>.*?<media:title type='plain'>(.*?)</media:title>.*?<yt:duration seconds='(.*?)'/>.*?<yt:videoid>(.*?)</yt:videoid>", data, re.S)

		if videoLinks:
			print 'videoLinks gefunden'
			self.videoListe = []
			for videoJpg, videoTitel, videoLaengeSek, videoId in videoLinks:
				temp1 = int(videoLaengeSek)
				minutes, seconds= divmod(temp1, 60)
				videoLaenge = '%s min %s sek' % (minutes, seconds)
				self.videoListe.append((decodeHtml(videoTitel), videoJpg, videoLaenge, videoId))
			self.streamMenuList.setList(map(youtubeFilmeListEntry, self.videoListe))
			self.showInfos()
		self.keyLocked = False

	def showInfos(self):
		phRuntime = self['filmList'].getCurrent()[0][2]
		phImage = self['filmList'].getCurrent()[0][1]
		self['name'].setText(phRuntime)
		downloadPage(phImage, "/tmp/phIcon.jpg").addCallback(self.ShowCover)
		
	def ShowCover(self, picData):
		if fileExists("/tmp/phIcon.jpg"):
			self['coverArt'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/phIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr.__deref__())
					self['coverArt'].show()
					del self.picload

	def keyOK(self):
		if self.keyLocked:
			return
		videoId = self['filmList'].getCurrent()[0][3]
		streamName = self['filmList'].getCurrent()[0][0]
		videoStream = youtubeUrl(self.session).getVideoUrl(videoId, self.videoPrioInt)
		if videoStream:
			sref = eServiceReference(0x1001, 0, videoStream)
			sref.setName(streamName)
			self.session.open(MoviePlayer, sref)


	def dataError(self, error):
		print error
		self.keyLocked = False


	def keyLeft(self):
		if self.keyLocked:
			return
		self['filmList'].pageUp()
		self.showInfos()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['filmList'].pageDown()
		self.showInfos()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['filmList'].up()
		self.showInfos()

	def keyDown(self):
		if self.keyLocked:
			return
		self['filmList'].down()
		self.showInfos()
			
	def keyCancel(self):
		self.close()


def main(session, **kwargs):
	session.open(youtubeGenreScreen)
                                                           
def Plugins(**kwargs):
	return PluginDescriptor(name=_("youtube"), description="youtube.de", where = PluginDescriptor.WHERE_PLUGINMENU, icon="plugin.png", fnc=main)