from imports import *
from decrypt import *

ck = {}

def bsListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT, entry[0])
		]	
def mainListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER, entry[0])
		]	
		
class bsMain(Screen, ConfigListScreen):
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/bsMain.xml" % config.mediaportal.skin.value
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['title'] = Label("Burning-seri.es")
		self['leftContentTitle'] = Label("M e n u")
		self['stationIcon'] = Pixmap()
		self['stationInfo'] = Label("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = False
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.keyLocked = True
		self.streamList.append(("Serien von A-Z","serien"))
		self.streamList.append(("Watchlist","watchlist"))
		self.streamMenuList.setList(map(mainListEntry, self.streamList))
		self.keyLocked = False
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
			
		auswahl = self['streamlist'].getCurrent()[0][1]
		if auswahl == "serien":
			self.session.open(bsSerien)
		else:
			self.session.open(bsWatchlist)
			
	def keyCancel(self):
		self.close()

class bsSerien(Screen, ConfigListScreen):
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/bsSerien.xml" % config.mediaportal.skin.value
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"green" : self.keyAdd
		}, -1)
		
		self['title'] = Label("Burning-seri.es")
		self['leftContentTitle'] = Label("Serien A-Z")
		self['stationIcon'] = Pixmap()
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		url = "http://www.burning-seri.es/serie-alphabet"
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		serien_raw = re.findall('<ul id=\'serSeries\'>(.*?)</ul>', data, re.S)
		if serien_raw:
			serien = re.findall('<li><a.*?href="(.*?)">(.*?)</a></li>', serien_raw[0], re.S)
			if serien:
				for (bsUrl,bsTitle) in serien:
					bsUrl = "http://www.burning-seri.es/" + bsUrl
					self.streamList.append((decodeHtml(bsTitle),bsUrl))
					self.streamMenuList.setList(map(bsListEntry, self.streamList))
				self.keyLocked = False

	def dataError(self, error):
		print error
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return

		auswahl = self['streamlist'].getCurrent()[0][1]
		print auswahl
		self.session.open(bsStaffeln, auswahl)

	def keyAdd(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		muTitle = self['streamlist'].getCurrent()[0][0]
		muID = self['streamlist'].getCurrent()[0][1]
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/bs_watchlist"
		if fileExists(path):
			writePlaylist = open(path,"a")
			writePlaylist.write('"%s" "%s"\n' % (muTitle, muID))
			writePlaylist.close()
			message = self.session.open(MessageBox, _("Serie wurde zur watchlist hinzugefuegt."), MessageBox.TYPE_INFO, timeout=3)
				
	def keyCancel(self):
		self.close()

class bsWatchlist(Screen, ConfigListScreen):
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/bsWatchlist.xml" % config.mediaportal.skin.value
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"red" : self.keyDel
		}, -1)
		
		self['title'] = Label("Burning-seri.es")
		self['leftContentTitle'] = Label("Watchlist")
		self['stationIcon'] = Pixmap()
		self['handlung'] = Label("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPlaylist)

	def loadPlaylist(self):
		self.streamList = []
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/bs_watchlist"	
		if fileExists(path):
			readStations = open(path,"r")
			for rawData in readStations.readlines():
				data = re.findall('"(.*?)" "(.*?)"', rawData, re.S)
				if data:
					(stationName, stationLink) = data[0]
					self.streamList.append((stationName, stationLink))
			print "Reload Playlist"
			self.streamList.sort()
			self.streamMenuList.setList(map(bsListEntry, self.streamList))
			readStations.close()
			self.keyLocked = False
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return

		auswahl = self['streamlist'].getCurrent()[0][1]
		print auswahl
		self.session.open(bsStaffeln, auswahl)
			
	def keyDel(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		
		selectedName = self['streamlist'].getCurrent()[0][0]
		pathTmp = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/bs_watchlist.tmp"
		writeTmp = open(pathTmp,"w")	
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/bs_watchlist"
		if fileExists(path):
			readStations = open(path,"r")
			for rawData in readStations.readlines():
				data = re.findall('"(.*?)" "(.*?)"', rawData, re.S)
				if data:
					(stationName, stationLink) = data[0]
					if stationName != selectedName:
						writeTmp.write('"%s" "%s"\n' % (stationName, stationLink))
			readStations.close()
			writeTmp.close()
			shutil.move(pathTmp, path)
			self.loadPlaylist()
				
	def keyCancel(self):
		self.close()

class bsStaffeln(Screen, ConfigListScreen):
	def __init__(self, session, serienUrl):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/bsStaffeln.xml" % config.mediaportal.skin.value
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		self.serienUrl = serienUrl
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"green" : self.keyAdd,
		}, -1)
		
		self['title'] = Label("Burning-seri.es")
		self['leftContentTitle'] = Label("Staffel Auswahl")
		self['stationIcon'] = Pixmap()
		self['handlung'] = Label("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		print self.serienUrl
		getPage(self.serienUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		staffeln = re.findall('<li class=".*?"><a href="(serie/.*?)">(.*?)</a></li>', data, re.S)
		details = re.findall('<strong>Beschreibung</strong>.*?<p>(.*?)</p>.*?<img src="(.*?)" alt="Cover"/>', data, re.S)
		if staffeln:
			for (bsUrl,bsStaffel) in staffeln:
				bsUrl = "http://www.burning-seri.es/" + bsUrl
				bsStaffel = "Staffel %s" % bsStaffel
				self.streamList.append((bsStaffel,bsUrl))
			self.streamMenuList.setList(map(bsListEntry, self.streamList))
			self.keyLocked = False
		if details:
			(handlung,cover) = details[0]
			self['handlung'].setText(decodeHtml(handlung))
			coverUrl = "http://www.burning-seri.es/" + cover
			print coverUrl
			downloadPage(coverUrl, "/tmp/bsIcon.jpg").addCallback(self.ShowCover)
		
	def ShowCover(self, picData):
		if fileExists("/tmp/bsIcon.jpg"):
			self['stationIcon'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['stationIcon'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/bsIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['stationIcon'].instance.setPixmap(ptr.__deref__())
					self['stationIcon'].show()
					del self.picload

	def dataError(self, error):
		print error
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return

		staffel = self['streamlist'].getCurrent()[0][0]
		staffel = staffel.replace('Staffel ','')
		auswahl = self['streamlist'].getCurrent()[0][1]
		print auswahl, staffel
		self.session.open(bsEpisoden, auswahl, staffel)

	def keyAdd(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		muTitle = self['streamlist'].getCurrent()[0][0]
		muID = self['streamlist'].getCurrent()[0][1]
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/bs_watchlist"
		if fileExists(path):
			writePlaylist = open(path,"a")
			writePlaylist.write('"%s" "%s"\n' % (muTitle, muID))
			writePlaylist.close()
			self.loadPlaylist()
				
	def keyCancel(self):
		self.close()

class bsEpisoden(Screen, ConfigListScreen):
	def __init__(self, session, serienUrl, bsStaffel):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/bsEpisoden.xml" % config.mediaportal.skin.value
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
		
		self.serienUrl = serienUrl
		self.bsStaffel = bsStaffel
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['title'] = Label("Burning-seri.es")
		self['leftContentTitle'] = Label("Episoden Auswahl")
		self['stationIcon'] = Pixmap()
		self['handlung'] = Label("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		print self.serienUrl
		getPage(self.serienUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		episoden = re.findall('<tr>.*?<td>(\d+)</td>.*?<td><a href="(serie/.*?)">', data, re.S)
		details = re.findall('<strong>Beschreibung</strong>.*?<p>(.*?)</p>.*?<img src="(.*?)" alt="Cover"/>', data, re.S)
		if episoden:
			for (bsEpisode,bsUrl) in episoden:
				bsTitle = re.findall('/\d+/\d+-(.*[0-9a-z]+)', bsUrl, re.S|re.I)
				bsUrl = "http://www.burning-seri.es/" + bsUrl
				bsEpisode = "S%sE%s - %s" % (self.bsStaffel, bsEpisode, decodeHtml(bsTitle[0].replace('_',' ').replace('-',' ')))
				self.streamList.append((bsEpisode,bsUrl))
			self.streamMenuList.setList(map(bsListEntry, self.streamList))
			self.keyLocked = False
		if details:
			(handlung,cover) = details[0]
			self['handlung'].setText(decodeHtml(handlung))
			coverUrl = "http://www.burning-seri.es/" + cover
			print coverUrl
			downloadPage(coverUrl, "/tmp/bsIcon.jpg").addCallback(self.ShowCover)

	def ShowCover(self, picData):
		if fileExists("/tmp/bsIcon.jpg"):
			self['stationIcon'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['stationIcon'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/bsIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['stationIcon'].instance.setPixmap(ptr.__deref__())
					self['stationIcon'].show()
					del self.picload
					
	def dataError(self, error):
		print error
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return

		auswahl = self['streamlist'].getCurrent()[0][1]
		print auswahl
		self.session.open(bsStreams, auswahl)
				
	def keyCancel(self):
		self.close()
		
class bsStreams(Screen, ConfigListScreen):
	
	def __init__(self, session, serienUrl):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/bsStreams.xml" % config.mediaportal.skin.value
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		self.serienUrl = serienUrl
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['title'] = Label("Burning-seri.es")
		self['leftContentTitle'] = Label("Stream Auswahl")
		self['stationIcon'] = Pixmap()
		self['handlung'] = Label("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		print self.serienUrl
		getPage(self.serienUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		streams = re.findall('<li><a href="(serie/.*?)"><span\n            class="icon.(.*?)"></span>', data)
		details = re.findall('<strong>Beschreibung</strong>.*?<p>(.*?)</p>.*?<img src="(.*?)" alt="Cover"/>', data, re.S)
		if streams:
			for (bsUrl,bsStream) in streams:
				bsUrl = "http://www.burning-seri.es/" + bsUrl
				if re.match('.*?(Ecostream|Sockshare|Streamcloud|Putlocker|Filenuke|Ecostream)',bsStream,re.I):
					self.streamList.append((bsStream,bsUrl))
			self.streamMenuList.setList(map(bsListEntry, self.streamList))
			self.keyLocked = False
		if details:
			(handlung,cover) = details[0]
			self['handlung'].setText(decodeHtml(handlung))
			coverUrl = "http://www.burning-seri.es/" + cover
			print coverUrl
			downloadPage(coverUrl, "/tmp/bsIcon.jpg").addCallback(self.ShowCover)
			
	def ShowCover(self, picData):
		if fileExists("/tmp/bsIcon.jpg"):
			self['stationIcon'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['stationIcon'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/bsIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['stationIcon'].instance.setPixmap(ptr.__deref__())
					self['stationIcon'].show()
					del self.picload

	def dataError(self, error):
		print error
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return

		auswahl = self['streamlist'].getCurrent()[0][1]
		print auswahl
		getPage(auswahl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.findStream).addErrback(self.dataError)

	def playfile(self, link):
		print link
		sref = eServiceReference(0x1001, 0, link)
		#sref.setName(self.filmname)
		self.session.open(MoviePlayer, sref)
		
	def findStream(self, data):
		if re.match(".*?http://www.sockshare.com/", data, re.S):
			link = re.findall("(http://www.sockshare.com/.*?)'", data, re.S)
		elif re.match(".*?http://www.putlocker.com/", data, re.S):
			link = re.findall("(http://www.putlocker.com/.*?)'", data, re.S)	
		elif re.match(".*?http://streamcloud.eu/", data, re.S):
			link = re.findall("(http://streamcloud.eu/.*?)'", data, re.S)
		elif re.match(".*?http://www.uploadc.com/", data, re.S):
			link = re.findall("(http://www.uploadc.com/.*?)'", data, re.S)
		elif re.match(".*?http://www.filenuke.com", data, re.S):
			link = re.findall("(http://www.filenuke.com/.*?)'", data, re.S)
		elif re.match(".*?http://www.ecostream.tv", data, re.S):
			link = re.findall("(http://www.ecostream.tv/.*?)'", data, re.S)			
			
		if link:
			link = link[0]
			print link
			if re.match(".*?putlocker.com/(file|embed)/", link, re.S):
				link = link.replace('file','embed')
				print "url:", link
				if link:
					getPage(link, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.streamPutlockerSockshare, link, "putlocker").addErrback(self.dataError)

			elif re.match(".*?sockshare.com/(file|embed)/", link, re.S):
				link = link.replace('file','embed')
				print "url:", link
				if link:
					getPage(link, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.streamPutlockerSockshare, link, "sockshare").addErrback(self.dataError)
	
			elif re.match(".*?streamcloud.eu/", link, re.S):
				if link:
					print "url", link
					getPage(link, cookies=ck, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.streamcloud).addErrback(self.dataError)

			elif re.match('.*?filenuke.com', link, re.S):
				if link:
					print "url:", link
					getPage(link, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.filenuke, link).addErrback(self.dataError)
					
			elif re.match('.*?ecostream.tv', link, re.S):
				if link:
					print "url:", link
					getPage(link, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.eco_read).addErrback(self.dataError)

	def filenuke(self, data, url):
		id = re.findall('<input type="hidden" name="id".*?value="(.*?)">', data)
		fname = re.findall('<input type="hidden" name="fname".*?alue="(.*?)">', data)
		post_data = urllib.urlencode({'op': 'download1', 'usr_login': '', 'id': id[0], 'fname': fname[0], 'referer': '', 'method_free': 'Free'})
		print post_data
		getPage(url, method='POST', postdata=post_data, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.filenuke_data).addErrback(self.dataError)

	def filenuke_data(self, data):
		print "drin"
		get_packedjava = re.findall("<script type=.text.javascript.>eval.function(.*?)</script>", data, re.S|re.DOTALL)
		if get_packedjava:
			#print get_packedjava
			sJavascript = get_packedjava[1]
			sUnpacked = cJsUnpacker().unpackByString(sJavascript)
			if sUnpacked:
				stream_url = re.findall("'file','(.*?)'", sUnpacked)
				if stream_url:
					print stream_url[0]
					self.playfile(stream_url[0])		
				else:
					self.stream_not_found()
			else:
				self.stream_not_found()
		else:
			self.stream_not_found()

	def streamPutlockerSockshare(self, data, url, provider):
		if re.match('.*?File Does not Exist', data, re.S):
			message = self.session.open(MessageBox, "File Does not Exist, or Has Been Removed", MessageBox.TYPE_INFO, timeout=5)
		elif re.match('.*?Encoding to enable streaming is in progresss', data, re.S):
			message = self.session.open(MessageBox, "Encoding to enable streaming is in progresss. Try again soon.", MessageBox.TYPE_INFO, timeout=5)			
		else:
			print "provider:", provider
			enter = re.findall('<input type="hidden" value="(.*?)" name="fuck_you">', data)
			print "enter:", enter
			values = {'fuck_you': enter[0], 'confirm': 'Close+Ad+and+Watch+as+Free+User'}
			user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
			headers = { 'User-Agent' : user_agent}
			cookiejar = cookielib.LWPCookieJar()
			cookiejar = urllib2.HTTPCookieProcessor(cookiejar)
			opener = urllib2.build_opener(cookiejar)
			urllib2.install_opener(opener)
			data = urlencode(values)
			req = urllib2.Request(url, data, headers)
			try:
				response = urllib2.urlopen(req)
			except urllib2.HTTPError, e:
				print e.code
				self.stream_not_found()
			except urllib2.URLError, e:
				print e.args
				self.stream_not_found()
			else:
				link = response.read()
				if link:
					print "found embed data"
					embed = re.findall("get_file.php.stream=(.*?)'\,", link, re.S)
					if embed:
						req = urllib2.Request('http://www.%s.com/get_file.php?stream=%s' %(provider, embed[0]))
						req.add_header('User-Agent', user_agent)
						try:
							response = urllib2.urlopen(req)
						except urllib2.HTTPError, e:
							print e.code
							self.stream_not_found()
						except urllib2.URLError, e:
							print e.args
							self.stream_not_found()
						else:
							link = response.read()
							if link:
								stream_url = re.findall('<media:content url="(.*?)"', link, re.S)
								print stream_url[1].replace('&amp;','&')
								self.playfile(stream_url[1].replace('&amp;','&'))
							else:
								self.stream_not_found()
					else:
						self.stream_not_found()
				else:
					self.stream_not_found()

	def streamcloud(self, data):
		id = re.findall('<input type="hidden" name="id".*?value="(.*?)">', data)
		fname = re.findall('<input type="hidden" name="fname".*?alue="(.*?)">', data)
		hash = re.findall('<input type="hidden" name="hash" value="(.*?)">', data)
		if id and fname and hash:
			url = "http://streamcloud.eu/%s" % id[0]
			post_data = urllib.urlencode({'op': 'download2', 'usr_login': '', 'id': id[0], 'fname': fname[0], 'referer': '', 'hash': hash[0], 'imhuman':'Weiter+zum+Video'})
			getPage(url, method='POST', cookies=ck, postdata=post_data, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.streamcloud_data).addErrback(self.dataError)
		else:
			self.stream_not_found()

	def streamcloud_data(self, data):
		stream_url = re.findall('file: "(.*?)"', data)
		if stream_url:
			print stream_url
			self.playfile(stream_url[0])
		else:
			self.stream_not_found()
			
	def eco_read(self, data):
		post_url = re.findall('<form name="setss" method="post" action="(.*?)">', data, re.S)
		if post_url:
			info = urlencode({'': '1', 'sss': '1'})
			print info
			getPage(post_url[0], method='POST', postdata=info, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.eco_post).addErrback(self.dataError)
			
	def eco_post(self, data):
		url = "http://www.ecostream.tv/assets/js/common.js"
		data2 = urllib.urlopen(url).read()
		post_url = re.findall("url: '(http://www.ecostream.tv/.*?)\?s=", data2, re.S)
		if post_url:
			print post_url
			sPattern = "var t=setTimeout\(\"lc\('([^']+)','([^']+)','([^']+)','([^']+)'\)"
			r = re.findall(sPattern, data)
			if r:
				for aEntry in r:
					sS = str(aEntry[0])
					sK = str(aEntry[1])
					sT = str(aEntry[2])
					sKey = str(aEntry[3])

				print "current keys:", sS, sK, sT, sKey
				sNextUrl = post_url[0]+"?s="+sS+'&k='+sK+'&t='+sT+'&key='+sKey
				print sNextUrl
				info = urlencode({'s': sS, 'k': sK, 't': sT, 'key': sKey})
				print info
				getPage(sNextUrl, method='POST', postdata = info, headers={'Referer':'http://www.ecostream.tv', 'X-Requested-With':'XMLHttpRequest'}).addCallback(self.eco_final).addErrback(self.dataError)
				
	def eco_final(self, data):
		print data
		stream_url = re.findall('flashvars="file=(.*?)&', data)
		if stream_url:
			kkStreamUrl = "http://www.ecostream.tv"+stream_url[0]
			print kkStreamUrl
			self.playfile(kkStreamUrl)
			
	def stream_not_found(self):
		message = self.session.open(MessageBox, _("Stream wurde nicht gefunden."), MessageBox.TYPE_INFO, timeout=3)
		
	def keyCancel(self):
		self.close()
