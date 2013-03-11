from imports import *
from decrypt import *

def cczweiListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 580, 25, 0, RT_HALIGN_LEFT, entry[0])
		] 
class cczwei(Screen):
		
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/cczwei.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/cczwei.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
		}, -1)
		
		self['title'] = Label("Cczwei.de")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('mediaportal', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList

		self.keyLocked = False
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		url = "http://www.cczwei.de/index.php?id=tvissuearchive"
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		videos = re.findall('<b>Folge (.*?)</b>.*?<a href="(index.php.*?)">(.*?)</a>', data, re.S)
		if videos:
			for (folge,url,title) in videos:
				title = "Folge %s - %s" % (folge,title)
				url = "http://www.cczwei.de/" + url
				self.streamList.append((title,folge))
			self.streamMenuList.setList(map(cczweiListEntry, self.streamList))
			self.keyLocked = False

	def dataError(self, error):
		print error
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return

		auswahl = self['streamlist'].getCurrent()[0][1]
		print auswahl
		if int(auswahl) < 100:
			test = "http://cczwei.mirror.speedpartner.de/cc2tv/CC2_0%s.avi" % auswahl
		else:
			test = "http://cczwei.mirror.speedpartner.de/cc2tv/CC2_%s.avi" % auswahl
			
		print test
		sref = eServiceReference(0x1001, 0, test)
		self.session.open(MoviePlayer, sref)
				
	def keyCancel(self):
		self.close()
