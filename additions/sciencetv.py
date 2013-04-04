from Plugins.Extensions.mediaportal.resources.imports import *
from Plugins.Extensions.mediaportal.resources.decrypt import *

STV_Version = "Science-Tv.com v0.91"

STV_siteEncoding = 'utf-8'

def scienceTvGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[1])
		] 
		
class scienceTvGenreScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"
		
		path = "%s/%s/defaultGenreScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/defaultGenreScreen.xml"

		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		
		self['title'] = Label(STV_Version)
		self['ContentTitle'] = Label("M e n ü")
		self['name'] = Label("")
		self['F1'] = Label("")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.genreliste.append((1,'Aktuelles Programm', 'http://www.science-tv.com/c/mid,2668,aktuelles_Programm/'))
		self.genreliste.append((2,'Filme auf Abruf', 'http://www.science-tv.com/c/mid,2671,Filme_auf_Abruf/'))
		self.genreliste.append((3,'TV-Programmvorschau', 'http://www.science-tv.com/c/mid,2670,TV-Programmvorschau/'))
		self.chooseMenuList.setList(map(scienceTvGenreListEntry, self.genreliste))
	
	def genreData(self, data):
		stvStream = re.findall('<video src="(.*?)"', data)
		if stvStream:
			print "S-TV stream found"
			stvLink = stvStream[0]
			stvTitle = 'Science-TV - aktuelles Programm'
			sref = eServiceReference(0x1001, 0, stvLink)
			sref.setName(stvTitle)
			self.session.open(MoviePlayer, sref)
			
	def dataError(self, error):
		print error
		
	def keyOK(self):
		genreID = self['genreList'].getCurrent()[0][0]
		genre = self['genreList'].getCurrent()[0][1]
		stvLink = self['genreList'].getCurrent()[0][2]
		if genreID == 1:
			getPage(stvLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.genreData).addErrback(self.dataError)
		else:
			self.session.open(scienceTvListScreen, genreID, stvLink, genre)

	def keyCancel(self):
		self.close()

def scienceTvListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 50, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0]+entry[1])
		] 
		
class scienceTvListScreen(Screen):
	
	def __init__(self, session, genreID, stvLink, stvGenre):
		self.session = session
		self.genreID = genreID
		self.stvLink = stvLink
		self.genreName = stvGenre
		
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"
		
		path = "%s/%s/scienceTvListScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/scienceTvListScreen.xml"

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

		self['title'] = Label(STV_Version)
		self['leftContentTitle'] = Label(self.genreName)
		self.keyLocked = True
		self.baseUrl = "http://www.science-tv.com"
		
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(50)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.keyLocked = True
		print "getPage: ",self.stvLink
		getPage(self.stvLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.genreData).addErrback(self.dataError)
	
	def genreData(self, data):
		print "genreData:"
		if self.genreID == 2:
			stvDaten = re.findall('<a href="\?v=(.*?)" title="(.*?)".*?<img src="(.*?)".*?_time">(.*?)<', data)
			if stvDaten:
				print "Movies found"
				for (href,title,img,dura) in stvDaten:
					self.filmliste.append(('',title.replace(' - ','\n')+' ['+dura+']',href,img))
				self.keyLocked = False
			else:
				self.filmliste.append(('Keine Filme gefunden !','','',''))
			
			self.chooseMenuList.setList(map(scienceTvListEntry, self.filmliste))
			self.showInfos()
		elif self.genreID == 3:
			m = re.search('<div id="bx_main_c">(.*?)</div>', data, re.S)
			if m:
				stvDaten = re.findall('<td .*?<strong>(.*?)</strong></td>.*?title="(.*?)"><img src="(.*?)".*?onclick=', m.group(1), re.S)
				
			if stvDaten:
				print "EPG Data found"
				for (ptime,title,img) in stvDaten:
					title = title.replace(' - ','\n\t')
					self.filmliste.append((ptime+'\t',title,'',img))
				self.keyLocked = False
			else:
				self.filmliste.append(('Keine Programmdaten gefunden !','','',''))
			
			self.chooseMenuList.setList(map(scienceTvListEntry, self.filmliste))
			self.showInfos()
		else:
			print "Wrong genre"

	def dataError(self, error):
		print "dataError: ",error

	def showInfos(self):
		#stvTitle = self['genreList'].getCurrent()[0][1]
		stvImage = self['genreList'].getCurrent()[0][3]
		print stvImage
		#self['name'].setText(stvTitle)
		#if stvImage != '' and self.genreID == 3:
		#	downloadPage(self.baseUrl+stvImage, "/tmp/stvIcon.jpg").addCallback(self.ShowCover)
		
	def ShowCover(self, picData):
		if fileExists("/tmp/stvIcon.jpg"):
			self['coverArt'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/stvIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr.__deref__())
					self['coverArt'].show()
					del self.picload
	
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
		if self.genreID == 2:
			stvLink = "http://www.science-tv.com/inc/mod/video/play.php/vid,%s/q,mp4/typ,ondemand/file.mp4"\
						% self['genreList'].getCurrent()[0][2]
			stvTitle = self['genreList'].getCurrent()[0][1]
			sref = eServiceReference(0x1001, 0, stvLink)
			sref.setName(stvTitle)
			self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()