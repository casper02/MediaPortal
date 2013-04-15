#	-*-	coding:	utf-8	-*-

from Plugins.Extensions.MediaPortal.resources.imports import *
from Plugins.Extensions.MediaPortal.resources.yt_url import *

YT_Version = "Youtube Search v0.90 (experimental)"

YT_siteEncoding = 'utf-8'

def YT_menuListentry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 
		
class youtubeGenreScreen(Screen):

	def __init__(self, session):
		self.session = session
		
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"
		
		path = "%s/%s/ytSearchScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/ytSearchScreen.xml"

		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"] = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up"	: self.keyUp,
			"down"	: self.keyDown,
			"left"	: self.keyLeft,
			"right"	: self.keyRight,
			"red"	: self.keyRed,
			"green"	: self.keyGreen,
			"yellow": self.keyYellow
		}, -1)

		self['title'] = Label(YT_Version)
		self['ContentTitle'] = Label("VIDEOSUCHE")
		self['name'] = Label("")
		self['F1'] = Label("Parameter")
		self['F2'] = Label("")
		self['F3'] = Label("Edit")
		self['F4'] = Label("")
		self['Query'] = Label("Suchanfrage")
		self['query'] = Label("")
		self['Time'] = Label("Zeitbereich")
		self['time'] = Label("")
		self['Metalang'] = Label("Suchsprache")
		self['metalang'] = Label("")
		self['Regionid'] = Label("Suchregion")
		self['regionid'] = Label("")
		self['Author'] = Label("")
		self['author'] = Label("")
		self['Keywords'] = Label("")
		self['keywords'] = Label("")
		self['Parameter'] = Label("Parameter")
		self['ParameterToEdit'] = Label("Edit:")
		self['parametertoedit'] = Label("")
		
		self.param_qr = ""
		self.param_lr_idx = 0
		self.param_kw = ""
		self.param_regionid_idx = 0
		self.param_time_idx = 0
		self.param_meta_idx = 0
		self.paramListIdx = 0
		self.param_author = ""
		
		self.menuLevel = 0
		self.menuMaxLevel = 2
		self.menuIdx = [0,0,0]
		self.keyLocked = True
		self.genreSelected = False
		self.menuListe = []
		self.baseUrl = "http://gdata.youtube.com/feeds/api"
		self.genreName = ["","","",""]
		self.genreUrl = ["","","",""]
		self.genreBase = ""
		self.genreTitle = ""
		#self.keckse = {}
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		#self.param_restriction = ['restriction=DE']
		self.param_safesearch = ['&safeSearch=none']
		self.param_format = '&format=5'
		
		self.subCat = [
			('Keine Kategorie', ''),
			('Autos & Fahrzeuge', 'Autos'),
			('Bildung', 'Education'),
			('Comedy', 'Comedy'),
			('Film & Animation', 'Film'),
			('Hilfen / Anleitungen', 'Howto'),
			('Musik', 'Music'),
			('Nachrichten & Politik', 'News'),
			('Leute & Blogs', 'People'),
			('Reisen & Veranstaltungen', 'Travel'),
			('Sport', 'Sports'),
			('Tiere', 'Pets'),
			('Unterhaltung', 'Entertainment'),
			('Wissenschaft & Technik', 'Tech')
			]
			
		self.subGenre_0 = [
			("Top bewertet", "/top_rated"),
			("Top Favoriten", "/top_favorites"),
			("Meist populär", "/most_popular"),
			("Meist diskutiert", "/most_discussed"),
			("Meist geantwortet", "/most_responded"),
			("Meist gesehen", "/most_viewed")
			]

		self.param_time = [
			("Alle", "time=all_time"),
			("Diese Woche", "time=this_week"),
			("Diesen Monat", "time=this_month"),
			("Heute", "time=today")
			]

		self.param_metalang = [
			('Deutsch', '&lr=de'),
			('Englisch', '&lr=en'),
			('Französisch', '&lr=fr'),
			('Italienisch', '&lr=it'),
			('Alle', '')
			]
			
		self.param_regionid = [
			('Ganze Welt', ''),
			('Deutschland', '/DE'),
			('England', '/EN'),
			('Frankreich', '/FR'),
			('Italien', '/IT')
			]
			
		self.paramList = [
			('Suchanfrage', self.paraQuery),
			('Zeitbereich', self.paraTime),
			('Suchsprache', self.paraMeta),
			('Suchregion', self.paraRegionID)
			#('Author', self.paraAuthor),
			#('Schlüsselworte', self.paraKey)
			]
			
		self.genreMenu = [
			[
			('Standard feeds', '/standardfeeds'),
			('Video feeds', '/videos/-')
			],
			[
			self.subGenre_0, self.subCat
			],
			[
			[self.subCat,self.subCat,self.subCat,self.subCat,self.subCat,self.subCat],
			[None,None,None,None,None,None,None,None,None,None,None,None,None,None]
			]
			]

		"""
			[
			self.param_time,self.param_time,self.param_time2,self.param_time,self.param_time,self.param_time,self.param_time,self.param_time
			],
			[None]
			]
		"""

		self.onLayoutFinish.append(self.loadMenu)

	def paraQuery(self):
		self.session.openWithCallback(self.cb_paraQuery, VirtualKeyBoard, title = (_("Suchanfrage")), text = self.param_qr)
		
	def cb_paraQuery(self, callback = None, entry = None):
		if callback != None:
			self.param_qr = callback.strip()
			self.showParams()
		
	def paraTime(self):
		self.param_time_idx += 1
		if self.param_time_idx not in range(0, len(self.param_time)):
			self.param_time_idx = 0
		
	def paraMeta(self):
		self.param_meta_idx += 1
		if self.param_meta_idx not in range(0, len(self.param_metalang)):
			self.param_meta_idx = 0
		
	def paraRegionID(self):
		self.param_regionid_idx += 1
		if self.param_regionid_idx not in range(0, len(self.param_regionid)):
			self.param_regionid_idx = 0
	
	def paraAuthor(self):
		self.session.openWithCallback(self.cb_paraAuthor, VirtualKeyBoard, title = (_("Author")), text = self.param_author)
	
	def cb_paraAuthor(self, callback = None, entry = None):
		if callback != None:
			self.param_author = callback.strip()
			self.showParams()
		
	def paraKey(self):
		self.session.openWithCallback(self.cb_paraKey, VirtualKeyBoard, title = (_("Suchschlüssel")), text = self.param_kw)
	
	def cb_paraKey(self, callback = None, entry = None):
		if callback != None:
			self.param_kw = callback.strip()
			self.showParams()
		
	def showParams(self):
		self['query'].setText(self.param_qr)
		self['time'].setText(self.param_time[self.param_time_idx][0])
		self['metalang'].setText(self.param_metalang[self.param_meta_idx][0])
		self['regionid'].setText(self.param_regionid[self.param_regionid_idx][0])
		self['author'].setText(self.param_author)
		self['keywords'].setText(self.param_kw)
		self['parametertoedit'].setText(self.paramList[self.paramListIdx][0])
	
	def setGenreStrTitle(self):
		genreName = self['genreList'].getCurrent()[0][0]
		genreLink = self['genreList'].getCurrent()[0][1]
		if self.menuLevel in range(self.menuMaxLevel+1):
			if self.menuLevel == 0:
				self.genreName[self.menuLevel] = genreName
			else:
				self.genreName[self.menuLevel] = ':'+genreName
				
			self.genreUrl[self.menuLevel] = genreLink
			
		self.genreTitle = "%s%s%s" % (self.genreName[0],self.genreName[1],self.genreName[2])
		self['name'].setText("Genre: "+self.genreTitle)
		
		if self.genreSelected:
			print "Genre selected"
			self['F2'].setText("Start")
		else:
			self['F2'].setText("")

	def loadMenu(self):
		print "Youtube:"
		self.showParams()
		self.setMenu(0, True)
		self.keyLocked = False

	def keyRed(self):
		self.paramListIdx += 1
		if self.paramListIdx not in range(0, len(self.paramList)):
			self.paramListIdx = 0
		self.showParams()

	def keyGreen(self):
		if self.genreSelected:
			print "Genre selected"
			qr = '&q='+urllib.quote(self.param_qr)
			tm = self.param_time[self.param_time_idx][1]
			lr = self.param_metalang[self.param_meta_idx][1]
			regionid = self.param_regionid[self.param_regionid_idx][1]
			#at = '&author='+self.param_author
			#self.param_kw
			
			if re.match('Standard', self.genreTitle):
				stdGenre = self.genreUrl[2]
				if stdGenre != '':
					stdGenre = '_'+stdGenre
				genreurl = self.baseUrl+self.genreUrl[0]+regionid+self.genreUrl[1]+stdGenre+'?'+tm+lr+qr+self.param_format+self.param_safesearch[0]
			else:
				genreurl = self.baseUrl+self.genreUrl[0]+'/'+self.genreUrl[1]+'?'+tm+lr+qr+self.param_format+self.param_safesearch[0]
			
			#print "genreurl: ", genreurl
			self.session.open(YT_ListScreen, genreurl, self.genreTitle)

	def keyYellow(self):
		self.paramList[self.paramListIdx][1]()
		self.showParams()
	
	def keyUp(self):
		self['genreList'].up()
		self.menuIdx[self.menuLevel] = self['genreList'].getSelectedIndex()
		self.setGenreStrTitle()
		
	def keyDown(self):
		self['genreList'].down()
		self.menuIdx[self.menuLevel] = self['genreList'].getSelectedIndex()
		self.setGenreStrTitle()
		
	def keyMenuUp(self):
		print "keyMenuUp:"
		if self.keyLocked:
			return
		self.menuIdx[self.menuLevel] = self['genreList'].getSelectedIndex()
		self.setMenu(-1)

	def keyRight(self):
		self['genreList'].pageDown()
		self.menuIdx[self.menuLevel] = self['genreList'].getSelectedIndex()
		self.setGenreStrTitle()
		
	def keyLeft(self):
		self['genreList'].pageUp()
		self.menuIdx[self.menuLevel] = self['genreList'].getSelectedIndex()
		self.setGenreStrTitle()
		
	def keyOK(self):
		print "keyOK:"
		if self.keyLocked:
			return
			
		self.menuIdx[self.menuLevel] = self['genreList'].getSelectedIndex()
		self.setMenu(1)
		
		#if self.genreSelected:
		#	print "Genre selected"
		#	self['F2'].setText("Start")

	def setMenu(self, levelIncr, menuInit=False):
		print "setMenu: ",levelIncr
		self.genreSelected = False
		if (self.menuLevel+levelIncr) in range(self.menuMaxLevel+1):
			if levelIncr < 0:
				self.genreName[self.menuLevel] = ""
			
			self.menuLevel += levelIncr
			
			if levelIncr > 0 or menuInit:
				self.menuIdx[self.menuLevel] = 0
			
			if self.menuLevel == 0:
				print "level-0"
				if self.genreMenu[0] != None:
					self.menuListe = []
					for (Name,Url) in self.genreMenu[0]:
						self.menuListe.append((Name,Url))
					self.chooseMenuList.setList(map(YT_menuListentry, self.menuListe))
					self['genreList'].moveToIndex(self.menuIdx[0])
				else:
					self.genreName[self.menuLevel] = ""
					self.genreUrl[self.menuLevel] = ""
					print "No menu entrys!"
			elif self.menuLevel == 1:
				print "level-1"
				if self.genreMenu[1][self.menuIdx[0]] != None:
					self.menuListe = []
					for (Name,Url) in self.genreMenu[1][self.menuIdx[0]]:
						self.menuListe.append((Name,Url))
					self.chooseMenuList.setList(map(YT_menuListentry, self.menuListe))
					self['genreList'].moveToIndex(self.menuIdx[1])
				else:
					self.genreName[self.menuLevel] = ""
					self.genreUrl[self.menuLevel] = ""
					self.menuLevel -= levelIncr
					self.genreSelected = True
					print "No menu entrys!"
			elif self.menuLevel == 2:
				print "level-2"
				if self.genreMenu[2][self.menuIdx[0]][self.menuIdx[1]] != None:
					self.menuListe = []
					for (Name,Url) in self.genreMenu[2][self.menuIdx[0]][self.menuIdx[1]]:
						self.menuListe.append((Name,Url))
					self.chooseMenuList.setList(map(YT_menuListentry, self.menuListe))
					self['genreList'].moveToIndex(self.menuIdx[2])
				else:
					self.genreName[self.menuLevel] = ""
					self.genreUrl[self.menuLevel] = ""
					self.menuLevel -= levelIncr
					self.genreSelected = True
					print "No menu entrys!"
		else:
			print "Entry selected"
			self.genreSelected = True
				
		print "menuLevel: ",self.menuLevel
		print "mainIdx: ",self.menuIdx[0]
		print "subIdx_1: ",self.menuIdx[1]
		print "subIdx_2: ",self.menuIdx[2]
		print "genreSelected: ",self.genreSelected
		print "menuListe: ",self.menuListe
		print "genreUrl: ",self.genreUrl
		
		self.setGenreStrTitle()		
		
	def keyCancel(self):
		if self.menuLevel == 0:
			self.close()
		else:
			self.keyMenuUp()

		
def YT_ListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0]+entry[1])
		] 
		
class YT_ListScreen(Screen):
	
	def __init__(self, session, stvLink, stvGenre):
		self.session = session
		self.stvLink = stvLink
		self.genreName = stvGenre
		
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"
		
		path = "%s/%s/dokuListScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/dokuListScreen.xml"

		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok" 		: self.keyOK,
			"cancel"	: self.keyCancel,
			"up" 		: self.keyUp,
			"down" 		: self.keyDown,
			"right" 	: self.keyRight,
			"left" 		: self.keyLeft,
			"nextBouquet": self.keyPageUpFast,
			"prevBouquet": self.keyPageDownFast,
			"red" 		:  self.keyTxtPageUp,
			"blue" 		:  self.keyTxtPageDown,
			"yellow"	: self.keyYellow,
			"1" 		: self.key_1,
			"3" 		: self.key_3,
			"4" 		: self.key_4,
			"6" 		: self.key_6,
			"7" 		: self.key_7,
			"9" 		: self.key_9
		}, -1)

		self['title'] = Label(YT_Version)
		self['ContentTitle'] = Label(self.genreName)
		self['name'] = Label("")
		self['handlung'] = ScrollLabel("")
		self['page'] = Label("")
		self['F1'] = Label("Text-")
		self['F2'] = Label("")
		self['F3'] = Label("VidPrio")
		self['F4'] = Label("Text+")
		self['VideoPrio'] = Label("")
		self['vPrio'] = Label("")
		self['Page'] = Label("Page")
		self['coverArt'] = Pixmap()

		self.keyLocked = True
		self.baseUrl = "http://www.youtube.com"

		self.videoPrio = int(config.mediaportal.youtubeprio.value)-1
		self.videoPrioS = ['L','M','H']
		self.setVideoPrio()
		
		self.keckse = {}
		self.filmliste = []
		self.start_idx = 1
		self.max_res = 12
		self.total_res = 0
		self.pages = 0
		self.page = 0
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['liste'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.loadPageData()
		
	def loadPageData(self):
		self.keyLocked = True
		print "getPage: ",self.stvLink
		
		self.filmliste = []
		self.filmliste.append(('Bitte warten...','','','',''))
		self.chooseMenuList.setList(map(YT_ListEntry, self.filmliste))
		
		url = self.stvLink+"&start-index=%d&max-results=%d&v=2" % (self.start_idx, self.max_res)
		print "YT-Url: ",url
		getPage(url, cookies=self.keckse, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.genreData).addErrback(self.dataError)

	def genreData(self, data):
		print "genreData:"
		if not self.pages:
			m = re.search('totalResults>(.*?)</', data)
			if m:
				a = int(m.group(1))
				self.pages = a // self.max_res
				if a % self.max_res:
					self.pages += 1
				if self.pages > 999:
					self.pages = 999
				self.page = 1
		
		a = 0
		l = len(data)
		self.filmliste = []
		while a < l:
			mg = re.search('<media:group>(.*?)</media:group>', data[a:], re.S)
			if mg:
				a += mg.end()
				m1 = re.search('description type=\'plain\'>(.*?)</', mg.group(1), re.S)
				if m1:
					desc = decodeHtml(m1.group(1))
					desc = urllib.unquote(desc)
				else:
					desc = "Keine weiteren Info's vorhanden."
					
				m2 = re.search('<media:player url=.*?/watch\?v=(.*?)&amp;feature=youtube_gdata_player.*?'\
					'<media:thumbnail url=\'(.*?)\'.*?<media:title type=\'plain\'>(.*?)</.*?<yt:duration seconds=\'(.*?)\'', mg.group(1), re.S)
				if m2:
					vid = m2.group(1)
					img = m2.group(2)
					dura = int(m2.group(4))
					vtim = str(datetime.timedelta(seconds=dura))
					title = decodeHtml(m2.group(3))
					self.filmliste.append((vtim+' ', title, vid, img, desc))
			else:
				a = l
				
		if len(self.filmliste) == 0:
			print "No video found!"
			self.pages = 0
			self.filmliste.append(('Keine Videos gefunden !','','','',''))
		else:
			#self.filmliste.sort(key=lambda t : t[0].lower())
			menu_len = len(self.filmliste)
			print "Videos found: ",menu_len
			
		self.chooseMenuList.setList(map(YT_ListEntry, self.filmliste))
		self.keyLocked = False
		self.showInfos()
		
	def dataError(self, error):
		print "dataError: ",error
		self['handlung'].setText("Lesefehler !\n"+str(error))

	def dataErrorP(self, error):
		print "dataError:"
		print error
		self.ShowCoverNone()
		
	def showInfos(self):
		self['page'].setText("%d / %d" % (self.page,self.pages))
		stvTitle = self['liste'].getCurrent()[0][1]
		stvImage = self['liste'].getCurrent()[0][3]
		desc = self['liste'].getCurrent()[0][4]
		print "Img: ",stvImage
		self['name'].setText(stvTitle)
		self['handlung'].setText(desc)
		if stvImage != '':
			url = stvImage
			print "Img: ",url
			downloadPage(url, "/tmp/Icon.jpg").addCallback(self.ShowCover).addErrback(self.dataErrorP)
		else:
			self.ShowCoverNone()
		
	def ShowCover(self, picData):
		print "ShowCover:"
		picPath = "/tmp/Icon.jpg"
		self.ShowCoverFile(picPath)
		
	def ShowCoverNone(self):
		print "ShowCoverNone:"
		picPath = self.plugin_path + "/images/no_coverArt.png"
		self.ShowCoverFile(picPath)
	
	def ShowCoverFile(self, picPath):
		print "showCoverFile:"
		if fileExists(picPath):
			print "picpath: ",picPath
			self['coverArt'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode(picPath, 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr.__deref__())
					self['coverArt'].show()
					del self.picload

	def youtubeErr(self, error):
		print "youtubeErr: ",error
		self['handlung'].setText("Das Video kann leider nicht abgespielt werden !\n"+str(error))

	def setVideoPrio(self):
		if self.videoPrio+1 > 2:
			self.videoPrio = 0
		else:
			self.videoPrio += 1
			
		self['vPrio'].setText(self.videoPrioS[self.videoPrio])

	def keyLeft(self):
		if self.keyLocked:
			return
		self['liste'].pageUp()
		self.showInfos()

	def keyRight(self):
		if self.keyLocked:
			return
		self['liste'].pageDown()
		self.showInfos()

	def keyUp(self):
		if self.keyLocked:
			return
		i = self['liste'].getSelectedIndex()
		if not i:
			self.keyPageDownFast()
			
		self['liste'].up()
		self.showInfos()

	def keyDown(self):
		if self.keyLocked:
			return
		i = self['liste'].getSelectedIndex()
		l = len(self.filmliste) - 1
		#print "i, l: ",i,l
		if l == i:
			self.keyPageUpFast()
			
		self['liste'].down()
		self.showInfos()

	def keyTxtPageUp(self):
		self['handlung'].pageUp()

	def keyTxtPageDown(self):
		self['handlung'].pageDown()

	def keyPageUpFast(self,step=1):
		if self.keyLocked:
			return
		#print "keyPageUp: "
		oldpage = self.page
		if (self.page + step) <= self.pages:
			self.page += step
			self.start_idx += self.max_res * step
		else:
			self.page = 1
			self.start_idx = 1
		#print "Page %d/%d" % (self.page,self.pages)
		if oldpage != self.page:
			self.loadPageData()

	def keyPageDownFast(self,step=1):
		if self.keyLocked:
			return
		print "keyPageDown: "
		oldpage = self.page
		if (self.page - step) >= 1:
			self.page -= step
			self.start_idx -= self.max_res * step
		else:
			self.page = self.pages
			self.start_idx = self.max_res * (self.pages - 1) + 1
		#print "Page %d/%d" % (self.page,self.pages)
		if oldpage != self.page:
			self.loadPageData()

	def keyYellow(self):
		self.setVideoPrio()

	def key_1(self):
		#print "keyPageDownFast(2)"
		self.keyPageDownFast(2)
		
	def key_4(self):
		#print "keyPageDownFast(5)"
		self.keyPageDownFast(5)
		
	def key_7(self):
		#print "keyPageDownFast(10)"
		self.keyPageDownFast(10)
		
	def key_3(self):
		#print "keyPageUpFast(2)"
		self.keyPageUpFast(2)
		
	def key_6(self):
		#print "keyPageUpFast(5)"
		self.keyPageUpFast(5)
		
	def key_9(self):
		#print "keyPageUpFast(10)"
		self.keyPageUpFast(10)

	def keyOK(self):
		if self.keyLocked:
			return
		dhTitle = self['liste'].getCurrent()[0][1]
		dhVideoId = self['liste'].getCurrent()[0][2]
		print "Title: ",dhTitle
		#print "VideoId: ",dhVideoId
		y = youtubeUrl(self.session)
		y.addErrback(self.youtubeErr)
		dhLink = y.getVideoUrl(dhVideoId, self.videoPrio)
		if dhLink:
			print dhLink
			sref = eServiceReference(0x1001, 0, dhLink)
			sref.setName(dhTitle)
			self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()