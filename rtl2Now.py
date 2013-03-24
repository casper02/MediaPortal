from imports import *
from Components.config import config
from PlayRtmpMovie import PlayRtmpMovie

def rtl2AuswahlListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]

def rtl2SerieListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]

class rtl2Screen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/rtl2Screen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/rtl2Screen.xml"
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
		
		self['title'] = Label("RTL2Now.de")
		self['name'] = Label("Sendung Auswahl")
		self['handlung'] = Label("")
		self.rtl2Liste = []
		self.keyLocked = True
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['rtl2List'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.keyLocked = True
		url = "http://rtl2now.rtl2.de"
		getPage(url, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def loadPageData(self, data):
		rtl2FreeVideos = re.findall('<div class="seriennavi_free" style=""><a href="(.*?)".*?>FREE.*?</div>.*?<div style="" class="seriennavi_link">.*?">(.*?)</a>.*?</div>', data, re.S)
		if rtl2FreeVideos:
			self.rtl2Liste = []
			for vidUrl, vidName in rtl2FreeVideos:
				url = "http://rtl2now.rtl2.de/" + vidUrl
				self.rtl2Liste.append((vidName, vidUrl))
			self.chooseMenuList.setList(map(rtl2AuswahlListEntry, self.rtl2Liste))
			self.keyLocked = False
		
	def dataError(self, error):
		print error
		self.rtl2Liste.append(('Keine RTL2-Serien gefunden', ''))
		self.chooseMenuList.setList(map(rtl2AuswahlListEntry, self.rtl2Liste))
		
	def keyOK(self):
		if self.keyLocked:
			return
		rtl2SerieUrl = self['rtl2List'].getCurrent()[0][1]
		print 'serienurl:...', rtl2SerieUrl
		self.session.open(rtl2SerieScreen, rtl2SerieUrl)
		
	def keyLeft(self):
		if self.keyLocked:
			return
		self['rtl2List'].pageUp()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['rtl2List'].pageDown()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['rtl2List'].up()

	def keyDown(self):
		if self.keyLocked:
			return
		self['rtl2List'].down()

	def keyCancel(self):
		self.close()

class rtl2SerieScreen(Screen):
	
	def __init__(self, session, rtl2SerieLink):
		self.session = session
		self.rtl2SerieLink = rtl2SerieLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/rtl2SerieScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/rtl2SerieScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("RTL2Now")
		self['name'] = Label("Sendung Auswahl")
		self.keyLocked = True
		self.rtl2SerieListe = []
		self.keckse = {}
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['rtl2SerieList'] = self.chooseMenuList
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		url = "http://rtl2now.rtl2.de" + self.rtl2SerieLink
		getPage(url, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def dataError(self, error):
		print error
		self.rtl2SerieListe.append(('Keine RTL2-Serien gefunden', ''))
		self.chooseMenuList.setList(map(rtl2SerieListEntry, self.rtl2SerieListe))
		
	def loadPageData(self, data):
		print "daten bekommen"
		serien = re.compile('<div class="line (even|odd)"><div onclick="link\(\'(.*?)\'\); return false;".*?<a href=".*?" title=".*?">(.*?)</a>.*?class="time">.*?</div>.*?class="minibutton">(.*?)</a></div></div>', re.DOTALL).findall(data)
		if serien:
			for filler, link, title, pay in serien:
				if pay == "kostenlos":
					link = "http://rtl2now.rtl2.de" + link.replace('amp;','')
					
					self.rtl2SerieListe.append((decodeHtml(title), link))
			self.chooseMenuList.setList(map(rtl2SerieListEntry, self.rtl2SerieListe))
			self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return
		self.sendungName = self['rtl2SerieList'].getCurrent()[0][0]
		self.sendungUrl = self['rtl2SerieList'].getCurrent()[0][1]
		print self.sendungUrl
		getPage(self.sendungUrl, agent=std_headers, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.get_xml).addErrback(self.dataError)

	def get_xml(self, data):
		print "xml data"
		self.stream = re.findall("'playerdata': '(.*?)'", data, re.S)
		if self.stream:
			print self.stream[0].replace('amp;',''), self.keckse
			getPage(self.stream[0].replace('amp;',''), agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.get_stream).addErrback(self.dataError)
		else:
			print "nix"
			
	def get_stream(self, data):
		print "stream data"
		rtmpe_data = re.findall('<filename.*?><!\[CDATA\[(rtmpe://.*?rtl2now/)(.*?)\]\]></filename>', data, re.S|re.I)
		if rtmpe_data:
			print rtmpe_data, self.sendungUrl
			(host, playpath) = rtmpe_data[0]
			print host, playpath
			if config.mediaportal.useRtmpDump.value:
				final = "%s' --swfVfy=1 --playpath=mp4:%s --app=rtl2now/_definst_ --pageUrl=http://rtl2now.rtl2.de/ --swfUrl=http://rtl2now.rtl2.de/includes/vodplayer.swf'" % (host, playpath)
				print final
				movieinfo = [final,self.sendungName+'.f4v']
				self.session.open(PlayRtmpMovie, movieinfo, self.sendungName)
			else:
				final = "%s swfUrl=http://www.rtl2now.rtl2.de/includes/vodplayer.swf pageurl=%s playpath=mp4:%s swfVfy=1" % (host, self.sendungUrl, playpath)
				print final
				sref = eServiceReference(0x1001, 0, final)
				sref.setName(self.sendungName)
				self.session.open(MoviePlayer, sref)
	
	def keyTMDbInfo(self):
		if TMDbPresent:
			title = self['List'].getCurrent()[0][0]
			self.session.open(TMDbMain, title)
			
	def keyCancel(self):
		self.close()
