from imports import *
from decrypt import *

def youpornGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

def youpornFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
		
class youpornGenreScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/youpornGenreScreen.xml" % config.mediaportal.skin.value
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok" : self.keyOK,
			"cancel" : self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)

		self['title'] = Label("YouPorn.com")
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
		self.genreliste.append(("--- Search ---", "callSuchen"))
		self.genreliste.append(("New", "http://www.youporn.com/?page="))
		self.genreliste.append(("Top Rated", "http://www.youporn.com/top_rated/?page="))
		self.genreliste.append(("Most Viewed", "http://www.youporn.com/most_viewed/?page="))
		self.genreliste.append(("Most Favorited", "http://www.youporn.com/most_favorited/?page="))
		self.genreliste.append(("Most Discussed", "http://www.youporn.com/most_discussed/?page="))
		self.genreliste.append(("Amateur", "http://www.youporn.com/category/1/amateur/?page="))
		self.genreliste.append(("Anal", "http://www.youporn.com/category/2/anal/?page="))
		self.genreliste.append(("Asian", "http://www.youporn.com/category/3/asian/?page="))
		self.genreliste.append(("BBW", "http://www.youporn.com/category/4/bbw/?page="))
		self.genreliste.append(("Big Butt", "http://www.youporn.com/category/6/big-butt/?page="))
		self.genreliste.append(("Big Tits", "http://www.youporn.com/category/7/big-tits/?page="))
		self.genreliste.append(("Bisexual", "http://www.youporn.com/category/5/bisexual/?page="))
		self.genreliste.append(("Blonde", "http://www.youporn.com/category/51/blonde/?page="))
		self.genreliste.append(("Blowjob", "http://www.youporn.com/category/9/blowjob/?page="))
		self.genreliste.append(("Brunette", "http://www.youporn.com/category/52/brunette/?page="))
		self.genreliste.append(("Coed", "http://www.youporn.com/category/10/coed/?page="))
		self.genreliste.append(("Compilation", "http://www.youporn.com/category/11/compilation/?page="))
		self.genreliste.append(("Couples", "http://www.youporn.com/category/12/couples/?page="))
		self.genreliste.append(("Creampie", "http://www.youporn.com/category/13/creampie/?page="))
		self.genreliste.append(("Cumshots", "http://www.youporn.com/category/37/cumshots/?page="))
		self.genreliste.append(("Cunnilingus", "http://www.youporn.com/category/15/cunnilingus/?page="))
		self.genreliste.append(("DP", "http://www.youporn.com/category/16/dp/?page="))
		self.genreliste.append(("Dildos/Toys", "http://www.youporn.com/category/44/dildos-toys/?page="))
		self.genreliste.append(("Ebony", "http://www.youporn.com/category/8/ebony/?page="))
		self.genreliste.append(("European", "http://www.youporn.com/category/48/european/?page="))
		self.genreliste.append(("Facial", "http://www.youporn.com/category/17/facial/?page="))
		self.genreliste.append(("Fantasy", "http://www.youporn.com/category/42/fantasy/?page="))
		self.genreliste.append(("Fetish", "http://www.youporn.com/category/18/fetish/?page="))
		self.genreliste.append(("Fingering", "http://www.youporn.com/category/62/fingering/?page="))
		self.genreliste.append(("Funny", "http://www.youporn.com/category/19/funny/?page="))
		self.genreliste.append(("Gay", "http://www.youporn.com/category/20/gay/?page="))
		self.genreliste.append(("German", "http://www.youporn.com/category/58/german/?page="))
		self.genreliste.append(("Gonzo", "http://www.youporn.com/category/50/gonzo/?page="))
		self.genreliste.append(("Group Sex", "http://www.youporn.com/category/21/group-sex/?page="))
		self.genreliste.append(("Hairy", "http://www.youporn.com/category/46/hairy/?page="))
		self.genreliste.append(("Handjob", "http://www.youporn.com/category/22/handjob/?page="))
		self.genreliste.append(("Hentai", "http://www.youporn.com/category/23/hentai/?page="))
		self.genreliste.append(("Instructional", "http://www.youporn.com/category/24/instructional/?page="))
		self.genreliste.append(("Interracial", "http://www.youporn.com/category/25/interracial/?page="))
		self.genreliste.append(("Interview", "http://www.youporn.com/category/41/interview/?page="))
		self.genreliste.append(("Kissing", "http://www.youporn.com/category/40/kissing/?page="))
		self.genreliste.append(("Latina", "http://www.youporn.com/category/49/latina/?page="))
		self.genreliste.append(("Lesbian", "http://www.youporn.com/category/26/lesbian/?page="))
		self.genreliste.append(("MILF", "http://www.youporn.com/category/29/milf/?page="))
		self.genreliste.append(("Massage", "http://www.youporn.com/category/64/massage/?page="))
		self.genreliste.append(("Masturbate", "http://www.youporn.com/category/55/masturbate/?page="))
		self.genreliste.append(("Mature", "http://www.youporn.com/category/28/mature/?page="))
		self.genreliste.append(("POV", "http://www.youporn.com/category/36/pov/?page="))
		self.genreliste.append(("Panties", "http://www.youporn.com/category/56/panties/?page="))
		self.genreliste.append(("Pantyhose", "http://www.youporn.com/category/57/pantyhose/?page="))
		self.genreliste.append(("Public", "http://www.youporn.com/category/30/public/?page="))
		self.genreliste.append(("Redhead", "http://www.youporn.com/category/53/redhead/?page="))
		self.genreliste.append(("Rimming", "http://www.youporn.com/category/43/rimming/?page="))
		self.genreliste.append(("Romantic", "http://www.youporn.com/category/61/romantic/?page="))
		self.genreliste.append(("Shaved", "http://www.youporn.com/category/54/shaved/?page="))
		self.genreliste.append(("Shemale", "http://www.youporn.com/category/31/shemale/?page="))
		self.genreliste.append(("Solo Male", "http://www.youporn.com/category/60/solo-male/?page="))
		self.genreliste.append(("Solo Girl", "http://www.youporn.com/category/27/solo-girl/?page="))
		self.genreliste.append(("Squirting", "http://www.youporn.com/category/39/squirting/?page="))
		self.genreliste.append(("Strt Sex", "http://www.youporn.com/category/47/strt-sex/?page="))
		self.genreliste.append(("Swallow", "http://www.youporn.com/category/59/swallow/?page="))
		self.genreliste.append(("Teen", "http://www.youporn.com/category/32/teen/?page="))
		self.genreliste.append(("Threesome", "http://www.youporn.com/category/38/threesome/?page="))
		self.genreliste.append(("Vintage", "http://www.youporn.com/category/33/vintage/?page="))
		self.genreliste.append(("Voyeur", "http://www.youporn.com/category/34/voyeur/?page="))
		self.genreliste.append(("Webcam", "http://www.youporn.com/category/35/webcam/?page="))
		self.genreliste.append(("Young/Old", "http://www.youporn.com/category/45/young-old/?page="))
		self.genreliste.append(("3D", "http://www.youporn.com/category/63/3d/?page="))
		self.chooseMenuList.setList(map(youpornGenreListEntry, self.genreliste))

	def keyOK(self):
		streamGenreName = self['genreList'].getCurrent()[0][0]
		if streamGenreName == "--- Search ---":
			self.suchen()

		else:
			streamGenreLink = self['genreList'].getCurrent()[0][1]
			self.session.open(youpornFilmScreen, streamGenreLink)
		
	def suchen(self):
		self.session.openWithCallback(self.SuchenCallback, VirtualKeyBoard, title = (_("Suchkriterium eingeben")), text = self.suchString)

	def SuchenCallback(self, callback = None, entry = None):
		if callback is not None and len(callback):
			self.suchString = callback.replace(' ', '+')
			streamGenreLink = 'http://www.youporn.com/search/?query=%s&page=' % (self.suchString)
			self.session.open(youpornFilmScreen, streamGenreLink)

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

class youpornFilmScreen(Screen):
	
	def __init__(self, session, phCatLink):
		self.session = session
		self.phCatLink = phCatLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/youpornFilmScreen.xml" % config.mediaportal.skin.value
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
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

		self['title'] = Label("YouPorn.com")
		self['name'] = Label("Film Auswahl")
		self['views'] = Label("")
		self['runtime'] = Label("")
		self['page'] = Label("1")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.page = 1
		
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadpage)
		
	def loadpage(self):
		self.keyLocked = True
		self.filmliste = []
		self['page'].setText(str(self.page))
		url = "%s%s" % (self.phCatLink, str(self.page))
		print url
		getPage(url, headers={'Cookie': 'age_verified=1', 'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadData).addErrback(self.dataError)
	
	def loadData(self, data):
		phMovies = re.findall('class="wrapping-video-box">.*?<a href="(.*?)">.*?<img src="(.*?)" alt="(.*?)".*?class="duration">(.*?)<span>length.*?views">(.*?)<span>views', data, re.S)
		if phMovies:
			for (phUrl, phImage, phTitle, phRuntime, phViews) in phMovies:
				self.filmliste.append((decodeHtml(phTitle), phUrl, phImage, phRuntime, phViews))
			self.chooseMenuList.setList(map(youpornFilmListEntry, self.filmliste))
			self.showInfos()
		self.keyLocked = False

	def dataError(self, error):
		print error

	def showInfos(self):
		phTitle = self['genreList'].getCurrent()[0][0]
		phImage = self['genreList'].getCurrent()[0][2]
		phRuntime = self['genreList'].getCurrent()[0][3]
		phViews = self['genreList'].getCurrent()[0][4]
		self['name'].setText(phTitle)
		self['runtime'].setText(phRuntime)
		self['views'].setText(phViews)
		downloadPage(phImage, "/tmp/Icon.jpg").addCallback(self.ShowCover)
		
	def ShowCover(self, picData):
		if fileExists("/tmp/Icon.jpg"):
			self['coverArt'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/Icon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr.__deref__())
					self['coverArt'].show()
					del self.picload

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
		self['genreList'].pageUp()
		self.showInfos()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['genreList'].pageDown()
		self.showInfos()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['genreList'].up()
		self.showInfos()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['genreList'].down()
		self.showInfos()
		
	def keyOK(self):
		if self.keyLocked:
			return
		phTitle = self['genreList'].getCurrent()[0][0]
		phLink = 'http://www.youporn.com' + self['genreList'].getCurrent()[0][1]
		self.keyLocked = True
		getPage(phLink, headers={'Cookie': 'age_verified=1', 'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getVideoPage).addErrback(self.dataError)

	def getVideoPage(self, data):
		videoPage = re.findall('video src="(.*?)" width', data, re.S)
		if videoPage:
			for (phurl) in videoPage:
				url = '%s' % (phurl)
				videos = urllib.unquote(url)
				videos = videos.replace('&amp;','&')
				self.keyLocked = False
				self.play(videos)
		
	def play(self,file):
		xxxtitle = self['genreList'].getCurrent()[0][0]
		sref = eServiceReference(0x1001, 0, file)
		sref.setName(xxxtitle)
		self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()
