# General imports
from imports import *
from decrypt import *
	
# Stream-Sites import
from forPlayers import *
from dokuMe import *
from roflVideos import *
#from streamJunkies import *
from focus import *
#from yourFreeTV import *
from tvKino import *
from filmOn import *
from netzKino import *
from kinoKiste import *
from failTo import *
from sportBild import *
from kinderKino import *
from myVideo import *
from laOla import *
from burningSeries import *
from filmTrailer import *
from firstChannel import *
from radio import *
from ccZwei import *
from basKino import *
from kinoxTo import *
from vuTechTalk import *
from dreamScreenCast import *
from konzertOase import *
from streamOase import *
from autoBild import *
from nhl import *
from spox import *
from tivi import *
from songsTo import *
from myEntertainment import *
from movie2k import *
from iStreamWS import *
from UltimateStreams import *
from mahlzeitTV import *
from appletrailers import *
from DOKUh import *
from DokuHouse import *
from AllMusicHouse import *
# porn
from amateurporn import *
from eporner import *
from hdporn import *
from pornerbros import *
from pornHub import *
from pornrabbit import *
from redtube import *
from xHamster import *
from x4tube import *
from youporn import *

config.mediaportal = ConfigSubsection()
config.mediaportal.pincode = ConfigPIN(default = 0000)
config.mediaportal.skin = ConfigSelection(default = "original", choices = [("tec", _("tec")),("liquidblue", _("liquidblue")), ("original", _("original"))])
config.mediaportal.pornpin = ConfigYesNo(default = True)
config.mediaportal.showDoku = ConfigYesNo(default = True)
config.mediaportal.showRofl = ConfigYesNo(default = True)
config.mediaportal.showFail = ConfigYesNo(default = True)
#config.mediaportal.showStream = ConfigYesNo(default = True)
config.mediaportal.showKinoKiste = ConfigYesNo(default = True)
config.mediaportal.showStreamOase = ConfigYesNo(default = True)
config.mediaportal.showMyvideo = ConfigYesNo(default = True)
config.mediaportal.showFocus = ConfigYesNo(default = True)
#config.mediaportal.showYourfree = ConfigYesNo(default = True)
config.mediaportal.showFilmOn = ConfigYesNo(default = True)
config.mediaportal.showTvkino = ConfigYesNo(default = True)
config.mediaportal.showSpobox = ConfigYesNo(default = True)
config.mediaportal.showNetzKino = ConfigYesNo(default = True)
config.mediaportal.showKinderKino = ConfigYesNo(default = True)
config.mediaportal.showSportBild = ConfigYesNo(default = True)
config.mediaportal.showLaola1 = ConfigYesNo(default = True)
config.mediaportal.showBs = ConfigYesNo(default = True)
config.mediaportal.show1channel = ConfigYesNo(default = True)
config.mediaportal.showRadio = ConfigYesNo(default = True)
config.mediaportal.showCczwei = ConfigYesNo(default = True)
config.mediaportal.showTrailer = ConfigYesNo(default = True)
config.mediaportal.showBaskino = ConfigYesNo(default = True)
config.mediaportal.showKinox = ConfigYesNo(default = True)
config.mediaportal.showVutec = ConfigYesNo(default = True)
config.mediaportal.showDsc = ConfigYesNo(default = True)
config.mediaportal.showKoase = ConfigYesNo(default = True)
config.mediaportal.showAutoBild = ConfigYesNo(default = True)
config.mediaportal.showNhl = ConfigYesNo(default = True)
config.mediaportal.showtivi = ConfigYesNo(default = True)
config.mediaportal.showSongsto = ConfigYesNo(default = True)
config.mediaportal.showMEHD = ConfigYesNo(default = True)
config.mediaportal.showIStream = ConfigYesNo(default = True)
config.mediaportal.showM2k = ConfigYesNo(default = True)
config.mediaportal.showUstreams = ConfigYesNo(default = True)
config.mediaportal.show4Players = ConfigYesNo(default = True)
config.mediaportal.showMahlzeitTV = ConfigYesNo(default = True)
config.mediaportal.showappletrailers = ConfigYesNo(default = True)
config.mediaportal.showDOKUh = ConfigYesNo(default = True)
config.mediaportal.showDokuHouse = ConfigYesNo(default = True)
config.mediaportal.showAllMusicHouse = ConfigYesNo(default = True)
# porn
config.mediaportal.show4tube = ConfigYesNo(default = False)
config.mediaportal.showamateurporn = ConfigYesNo(default = False)
config.mediaportal.showeporner = ConfigYesNo(default = False)
config.mediaportal.showhdporn = ConfigYesNo(default = False)
config.mediaportal.showM2kPorn = ConfigYesNo(default = False)
config.mediaportal.showpornerbros = ConfigYesNo(default = False)
config.mediaportal.showPornhub = ConfigYesNo(default = False)
config.mediaportal.showpornrabbit = ConfigYesNo(default = False)
config.mediaportal.showredtube = ConfigYesNo(default = False)
config.mediaportal.showXhamster = ConfigYesNo(default = False)
config.mediaportal.showyouporn = ConfigYesNo(default = False)

class hauptScreenSetup(Screen, ConfigListScreen):

	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/hauptScreenSetup.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/hauptScreenSetup.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self.configlist = []
		ConfigListScreen.__init__(self, self.configlist)
		self.configlist.append(getConfigListEntry("Zeige Doku.me:", config.mediaportal.showDoku))
		self.configlist.append(getConfigListEntry("Zeige Rofl.to:", config.mediaportal.showRofl))
		self.configlist.append(getConfigListEntry("Zeige Fail.to:", config.mediaportal.showFail))
		self.configlist.append(getConfigListEntry("Zeige Myvideo:", config.mediaportal.showMyvideo))
		self.configlist.append(getConfigListEntry("Zeige AutoBild:", config.mediaportal.showAutoBild))
		self.configlist.append(getConfigListEntry("Zeige SportBild:", config.mediaportal.showSportBild))
		self.configlist.append(getConfigListEntry("Zeige Laola1:", config.mediaportal.showLaola1))
		self.configlist.append(getConfigListEntry("Zeige KinderKino:", config.mediaportal.showKinderKino))
		#self.configlist.append(getConfigListEntry("Zeige Streamjunkies:", config.mediaportal.showStream))
		self.configlist.append(getConfigListEntry("Zeige KinoKiste:", config.mediaportal.showKinoKiste))
		self.configlist.append(getConfigListEntry("Zeige Stream-Oase:", config.mediaportal.showStreamOase))
		self.configlist.append(getConfigListEntry("Zeige Burning-Series:", config.mediaportal.showBs))
		self.configlist.append(getConfigListEntry("Zeige Kinox:", config.mediaportal.showKinox))
		self.configlist.append(getConfigListEntry("Zeige Movie2k:", config.mediaportal.showM2k))
		self.configlist.append(getConfigListEntry("Zeige Konzert Oase:", config.mediaportal.showKoase))
		self.configlist.append(getConfigListEntry("Zeige 1channel:", config.mediaportal.show1channel))
		self.configlist.append(getConfigListEntry("Zeige Focus:", config.mediaportal.showFocus))
		#self.configlist.append(getConfigListEntry("Zeige Yourfree:", config.mediaportal.showYourfree))
		self.configlist.append(getConfigListEntry("Zeige FilmOn:", config.mediaportal.showFilmOn))
		self.configlist.append(getConfigListEntry("Zeige TvKino:", config.mediaportal.showTvkino))
		self.configlist.append(getConfigListEntry("Zeige NetzKino:", config.mediaportal.showNetzKino))
		self.configlist.append(getConfigListEntry("Zeige Spobox:", config.mediaportal.showSpobox))
		self.configlist.append(getConfigListEntry("Zeige Radio.de:", config.mediaportal.showRadio))
		self.configlist.append(getConfigListEntry("Zeige CCZwei:", config.mediaportal.showCczwei))
		self.configlist.append(getConfigListEntry("Zeige Filmtrailer:", config.mediaportal.showTrailer))
		self.configlist.append(getConfigListEntry("Zeige Baskino:", config.mediaportal.showBaskino))
		self.configlist.append(getConfigListEntry("Zeige Vutechtalk:", config.mediaportal.showVutec))
		self.configlist.append(getConfigListEntry("Zeige Dreamscreencast:", config.mediaportal.showDsc))
		self.configlist.append(getConfigListEntry("Zeige NHL:", config.mediaportal.showNhl))
		self.configlist.append(getConfigListEntry("Zeige Tivi:", config.mediaportal.showtivi))
		self.configlist.append(getConfigListEntry("Zeige Songs.to:", config.mediaportal.showSongsto))
		self.configlist.append(getConfigListEntry("Zeige My-Entertainment:", config.mediaportal.showMEHD))
		self.configlist.append(getConfigListEntry("Zeige IStream:", config.mediaportal.showIStream))
		self.configlist.append(getConfigListEntry("Zeige UltimateStreams:", config.mediaportal.showUstreams))
		self.configlist.append(getConfigListEntry("Zeige 4Players:", config.mediaportal.show4Players))
		self.configlist.append(getConfigListEntry("Zeige mahlzeit.tv:", config.mediaportal.showMahlzeitTV))
		self.configlist.append(getConfigListEntry("Zeige Apple Movie Trailers:", config.mediaportal.showappletrailers))
		self.configlist.append(getConfigListEntry("Zeige DOKUh:", config.mediaportal.showDOKUh))
		self.configlist.append(getConfigListEntry("Zeige DokuHouse:", config.mediaportal.showDokuHouse))
		self.configlist.append(getConfigListEntry("Zeige AllMusicHouse:", config.mediaportal.showAllMusicHouse))
		self.configlist.sort(key=lambda t : tuple(t[0].lower()))
		self.configlist.insert(0, ("Skinauswahl:", config.mediaportal.skin))
		self.configlist.insert(0, ("XXX-Pincodeabfrage:", config.mediaportal.pornpin))
		self.configlist.insert(0, ("Pincode:", config.mediaportal.pincode))
		# porn
		self.configlist.append(getConfigListEntry("Zeige 4Tube:", config.mediaportal.show4tube))
		self.configlist.append(getConfigListEntry("Zeige AmateurPorn:", config.mediaportal.showamateurporn))
		self.configlist.append(getConfigListEntry("Zeige Eporner:", config.mediaportal.showeporner))
		self.configlist.append(getConfigListEntry("Zeige HDPorn:", config.mediaportal.showhdporn))
		self.configlist.append(getConfigListEntry("Zeige Movie2k-Porn:", config.mediaportal.showM2kPorn))
		self.configlist.append(getConfigListEntry("Zeige PornerBros:", config.mediaportal.showpornerbros))
		self.configlist.append(getConfigListEntry("Zeige Pornhub:", config.mediaportal.showPornhub))
		self.configlist.append(getConfigListEntry("Zeige PornRabbit:", config.mediaportal.showpornrabbit))
		self.configlist.append(getConfigListEntry("Zeige RedTube:", config.mediaportal.showredtube))
		self.configlist.append(getConfigListEntry("Zeige xHamster:", config.mediaportal.showXhamster))
		self.configlist.append(getConfigListEntry("Zeige YouPorn:", config.mediaportal.showyouporn))
		self["config"].setList(self.configlist)

		self['title'] = Label("MediaPortal - Setup - (Version 3.5.3)")
		self['name'] = Label("Setup")
		self['coverArt'] = Pixmap()
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

	def keyOK(self):
		for x in self["config"].list:
			x[1].save()
		configfile.save()
		self.close()
	
	def keyCancel(self):
		self.close()

class HelpScreen(Screen):

	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/help.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/help.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

	def keyOK(self):
		self.close()
	
	def keyCancel(self):
		self.close()
		
class chooseMenuList(MenuList):
	def __init__(self, list):
		MenuList.__init__(self, list, True, eListboxPythonMultiContent)
		self.l.setFont(0, gFont("Regular", 20))
		self.l.setItemHeight(40)

class haupt_Screen(Screen, ConfigListScreen):
	def __init__(self, session):
		self.session = session

		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/haupt_Screen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/haupt_Screen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "HelpActions"], {
			"ok"    : self.keyOK,
			"up"    : self.keyUp,
			"down"  : self.keyDown,
			"cancel": self.keyCancel,
			"left"  : self.keyLeft,
			"right" : self.keyRight,
			"menu" : self.keySetup,
			"displayHelp" : self.keyHelp
		}, -1)

		self['title'] = Label("MediaPortal v3.5.3")
		
		self['name'] = Label("Plugin Auswahl")
		
		self['infos'] = chooseMenuList([])
		self['Infos'] = Label("Info / More")
		
		self['fun'] = chooseMenuList([])
		self['Fun'] = Label("Fun / TV")
		
		self['movies'] = chooseMenuList([])
		self['Movies'] = Label("Filme / Serien")
		self.showM2kPorn = False
	
		self.currenlist = "movies"
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.movies = []
		self.infos = []
		self.fun = []	
		
		# movies
		if config.mediaportal.showMyvideo.value:
			self.movies.append(self.hauptListEntry("MyVideo", "myvideo"))
		if config.mediaportal.showKinderKino.value:
			self.movies.append(self.hauptListEntry("KinderKino", "kinderkino"))
		#if config.mediaportal.showStream.value:
		#	self.movies.append(self.hauptListEntry("Streamjunkies", "streamjunkies"))
		if config.mediaportal.showKinoKiste.value:
			self.movies.append(self.hauptListEntry("KinoKiste", "kinokiste"))
		if config.mediaportal.showBs.value:
			self.movies.append(self.hauptListEntry("Burning-Series", "burningseries"))
		if config.mediaportal.show1channel.value:
			self.movies.append(self.hauptListEntry("1channel", "1channel"))
		if config.mediaportal.showNetzKino.value:
			self.movies.append(self.hauptListEntry("NetzKino", "netzkino"))
		if config.mediaportal.showBaskino.value:
			self.movies.append(self.hauptListEntry("Baskino", "baskino"))
		if config.mediaportal.showKinox.value:
			self.movies.append(self.hauptListEntry("Kinox", "kinox"))
		if config.mediaportal.showStreamOase.value:
			self.movies.append(self.hauptListEntry("StreamOase", "streamoase"))
		if config.mediaportal.showtivi.value:
			self.movies.append(self.hauptListEntry("Tivi", "tivi"))
		if config.mediaportal.showMEHD.value:
			self.movies.append(self.hauptListEntry("My-Entertainment", "mehd"))
		if config.mediaportal.showUstreams.value:
			self.movies.append(self.hauptListEntry("UltimateStreams", "ustreams"))
		if config.mediaportal.showM2k.value:
			self.movies.append(self.hauptListEntry("Movie2k", "movie2k"))
		if config.mediaportal.showM2kPorn.value:
			self.showM2KPorn = True
		else:
			self.showM2KPorn = False
		if config.mediaportal.showIStream.value:
			self.movies.append(self.hauptListEntry("IStream", "istream"))
		# info
		if config.mediaportal.showDoku.value:
			self.infos.append(self.hauptListEntry("Doku.me", "doku"))		
		if config.mediaportal.showSportBild.value:
			self.infos.append(self.hauptListEntry("SportBild", "sportbild"))
		if config.mediaportal.showAutoBild.value:
			self.infos.append(self.hauptListEntry("AutoBild", "autobild"))
		if config.mediaportal.showLaola1.value:
			self.infos.append(self.hauptListEntry("Laola1 Live", "laola1"))
		if config.mediaportal.showFocus.value:
			self.infos.append(self.hauptListEntry("Focus", "focus"))
		if config.mediaportal.showCczwei.value:
			self.infos.append(self.hauptListEntry("CCZwei", "cczwei"))
		if config.mediaportal.showTrailer.value:
			self.infos.append(self.hauptListEntry("Filmtrailer", "trailer"))
		if config.mediaportal.showVutec.value:
			self.infos.append(self.hauptListEntry("Vutechtalk", "vutechtalk"))
		if config.mediaportal.showDsc.value:
			self.infos.append(self.hauptListEntry("Dreamscreencast", "dreamscreencast"))
		if config.mediaportal.showKoase.value:
			self.infos.append(self.hauptListEntry("Konzert Oase", "koase"))
		if config.mediaportal.showNhl.value:
			self.infos.append(self.hauptListEntry("NHL", "nhl"))
		if config.mediaportal.show4Players.value:
			self.infos.append(self.hauptListEntry("4Players", "4players"))
		if config.mediaportal.showMahlzeitTV.value:
			self.infos.append(self.hauptListEntry("mahlzeit.tv", "mahlzeit"))
		if config.mediaportal.showappletrailers.value:
			self.infos.append(self.hauptListEntry("AppleTrailer", "appletrailers"))
		if config.mediaportal.showDOKUh.value:
			self.infos.append(self.hauptListEntry("DOKUh", "dokuh"))
		if config.mediaportal.showDokuHouse.value:
			self.infos.append(self.hauptListEntry("DokuHouse", "dokuhouse"))
		if config.mediaportal.showAllMusicHouse.value:
			self.infos.append(self.hauptListEntry("AllMusicHouse", "allmusichouse"))
		# fun & TV
		if config.mediaportal.showRofl.value:
			self.fun.append(self.hauptListEntry("Rofl.to", "rofl"))
		if config.mediaportal.showFail.value:
			self.fun.append(self.hauptListEntry("Fail.to", "fail"))
		#if config.mediaportal.showYourfree.value:
		#	self.fun.append(self.hauptListEntry("YourfreeTv", "yourfreetv"))
		if config.mediaportal.showFilmOn.value:
			self.fun.append(self.hauptListEntry("FilmOn", "filmon"))
		if config.mediaportal.showTvkino.value:
			self.fun.append(self.hauptListEntry("TV-Kino", "tvkino"))
		if config.mediaportal.showRadio.value:
			self.fun.append(self.hauptListEntry("Radio.de", "radiode"))
		if config.mediaportal.showSpobox.value:
			self.fun.append(self.hauptListEntry("Spobox", "spobox"))
		if config.mediaportal.showSongsto.value:
			self.fun.append(self.hauptListEntry("Songs.to", "songsto"))
		# porn
		if config.mediaportal.show4tube.value:
			self.fun.append(self.hauptListEntry("4Tube", "4tube"))
		if config.mediaportal.showamateurporn.value:
			self.fun.append(self.hauptListEntry("AmateurPorn", "amateurporn"))
		if config.mediaportal.showeporner.value:
			self.fun.append(self.hauptListEntry("Eporner", "eporner"))
		if config.mediaportal.showhdporn.value:
			self.fun.append(self.hauptListEntry("HDPorn", "hdporn"))
		if config.mediaportal.showpornerbros.value:
			self.fun.append(self.hauptListEntry("PornerBros", "pornerbros"))
		if config.mediaportal.showPornhub.value:
			self.fun.append(self.hauptListEntry("Pornhub", "pornhub"))
		if config.mediaportal.showpornrabbit.value:
			self.fun.append(self.hauptListEntry("PornRabbit", "pornrabbit"))
		if config.mediaportal.showredtube.value:
			self.fun.append(self.hauptListEntry("RedTube", "redtube"))
		if config.mediaportal.showXhamster.value:
			self.fun.append(self.hauptListEntry("xHamster", "xhamster"))
		if config.mediaportal.showyouporn.value:
			self.fun.append(self.hauptListEntry("YouPorn", "youporn"))

		self.movies.sort(key=lambda t : tuple(t[0][0].lower()))
		self.infos.sort(key=lambda t : tuple(t[0][0].lower()))
		self.fun.sort(key=lambda t : tuple(t[0][0].lower()))		

		self["movies"].setList(self.movies)
		self["movies"].l.setItemHeight(42)
		self["infos"].setList(self.infos)
		self["infos"].l.setItemHeight(42)
		self["fun"].setList(self.fun)
		self["fun"].l.setItemHeight(42)
		self.keyRight()
		
	def hauptListEntry(self, name, jpg):
		res = [(name, jpg)]
		icon = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/icons/%s.png" % jpg
		if fileExists(icon):
			res.append(MultiContentEntryPixmapAlphaTest(pos=(0, 1), size=(100, 40), png=loadPNG(icon)))	
		res.append(MultiContentEntryText(pos=(110, 1), size=(160, 40), font=0, text=name, flags=RT_HALIGN_LEFT))
		return res
	
	def keySetup(self):
		print config.mediaportal.pincode.value
		self.session.openWithCallback(self.pinok, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
	
	def keyHelp(self):
		self.session.open(HelpScreen)

	def getTriesEntry(self):
		return config.ParentalControl.retries.setuppin
		
	def pinok(self, pincode):
		if pincode:
			self.session.openWithCallback(self.layoutFinished, hauptScreenSetup)

	def keyUp(self):
		exist = self[self.currenlist].getCurrent()
		if exist == None:
			return
		self[self.currenlist].up()
		auswahl = self[self.currenlist].getCurrent()[0][0]
		self.title = auswahl
		self['name'].setText(auswahl)
		
	def keyDown(self):
		exist = self[self.currenlist].getCurrent()
		if exist == None:
			return
		self[self.currenlist].down()
		auswahl = self[self.currenlist].getCurrent()[0][0]
		self.title = auswahl
		self['name'].setText(auswahl)

	def keyRight(self):
		self.cur_idx = self[self.currenlist].getSelectedIndex()
		self["infos"].selectionEnabled(0)
		self["fun"].selectionEnabled(0)
		self["movies"].selectionEnabled(0)
		if self.currenlist == "infos":
			self["fun"].selectionEnabled(1)
			self.currenlist = "fun"
			cnt_tmp_ls = len(self.fun)
		elif self.currenlist == "fun":
			self["movies"].selectionEnabled(1)
			self.currenlist = "movies"
			cnt_tmp_ls = len(self.movies)
		elif self.currenlist == "movies":
			self["infos"].selectionEnabled(1)
			self.currenlist = "infos"
			cnt_tmp_ls = len(self.infos)
			
		cnt_tmp_ls = int(cnt_tmp_ls)
		if int(self.cur_idx) < int(cnt_tmp_ls):
			self[self.currenlist].moveToIndex(int(self.cur_idx))
		else:
			idx = int(cnt_tmp_ls) -1
			self[self.currenlist].moveToIndex(int(idx))
			
		auswahl = self[self.currenlist].getCurrent()[0][0]
		self.title = auswahl
		self['name'].setText(auswahl)
		
	def keyLeft(self):
		self.cur_idx = self[self.currenlist].getSelectedIndex()
		self["infos"].selectionEnabled(0)
		self["fun"].selectionEnabled(0)
		self["movies"].selectionEnabled(0)
		if self.currenlist == "movies":
			self["fun"].selectionEnabled(1)
			self.currenlist = "fun"
			cnt_tmp_ls = len(self.fun)
		elif self.currenlist == "fun":
			self["infos"].selectionEnabled(1)
			self.currenlist = "infos"
			cnt_tmp_ls = len(self.infos)
		elif self.currenlist == "infos":
			self["movies"].selectionEnabled(1)
			self.currenlist = "movies"
			cnt_tmp_ls = len(self.movies)
	
		cnt_tmp_ls = int(cnt_tmp_ls)
		print self.cur_idx, cnt_tmp_ls
		if int(self.cur_idx) < int(cnt_tmp_ls):
			self[self.currenlist].moveToIndex(int(self.cur_idx))
		else:
			idx = int(cnt_tmp_ls) -1
			self[self.currenlist].moveToIndex(int(idx))

		auswahl = self[self.currenlist].getCurrent()[0][0]
		self.title = auswahl
		self['name'].setText(auswahl)
		
	def keyOK(self):
		exist = self[self.currenlist].getCurrent()
		if exist == None:
			return
		print self.currenlist
		auswahl = self[self.currenlist].getCurrent()[0][0]
		print auswahl
		if auswahl == "Doku.me":
			self.session.open(dokuScreen)
		elif auswahl == "Rofl.to":
			self.session.open(roflScreen)
		elif auswahl == "Fail.to":
			self.session.open(failScreen)
		elif auswahl == "KinderKino":
			self.session.open(kinderKinoScreen)
		elif auswahl == "MyVideo":
			self.session.open(myVideoGenreScreen)
		elif auswahl == "SportBild":
			self.session.open(sportBildScreen)
		elif auswahl == "Laola1 Live":
			self.session.open(laolaScreen)
		#elif auswahl == "Streamjunkies":
		#	self.session.open(streamGenreScreen)
		elif auswahl == "KinoKiste":
			self.session.open(kinokisteGenreScreen)
		elif auswahl == "Burning-Series":
			self.session.open(bsMain)
		elif auswahl == "1channel":
			self.session.open(chMain)
		elif auswahl == "Focus":
			self.session.open(focusGenre)
		#elif auswahl == "YourfreeTv":
		#	self.session.open(yourFreeTv)
		elif auswahl == "FilmOn":
			self.session.open(filmON)
		elif auswahl == "NetzKino":
			self.session.open(netzKinoGenreScreen)
		elif auswahl == "Spobox":
			self.session.open(spoboxGenreScreen)
		elif auswahl == "Radio.de":
			self.session.open(Radiode)
		elif auswahl == "CCZwei":
			self.session.open(cczwei)
		elif auswahl == "Filmtrailer":
			self.session.open(trailer)
		elif auswahl == "Baskino":
			self.session.open(baskino)
		elif auswahl == "Kinox":
			self.session.open(kxMain) 
		elif auswahl == "Vutechtalk":
			self.session.open(vutechtalk)
		elif auswahl == "Dreamscreencast":
			self.session.open(dreamscreencast)
		elif auswahl == "TV-Kino":
			self.session.open(tvkino)
		elif auswahl == "Konzert Oase":
			self.session.open(oaseGenreScreen)
		elif auswahl == "StreamOase":
			self.session.open(oasetvGenreScreen)
		elif auswahl == "AutoBild":
			self.session.open(autoBildGenreScreen)
		elif auswahl == "NHL":
			self.session.open(nhlGenreScreen)
		elif auswahl == "4Players":
			self.session.open(forPlayersGenreScreen)
		elif auswahl == "Tivi":
			self.session.open(tiviGenreListeScreen)
		elif auswahl == "My-Entertainment":
			self.session.open(showMEHDGenre)
		elif auswahl == "Songs.to":
			self.session.open(showSongstoGenre)
		elif auswahl == "Movie2k":
			self.session.open(m2kGenreScreen, self.showM2KPorn)
		elif auswahl == "IStream":
			self.session.open(showIStreamGenre)
		elif auswahl == "UltimateStreams":
			self.session.open(showUSGenre)
		elif auswahl == "mahlzeit.tv":
			self.session.open(mahlzeitMainScreen)
		elif auswahl == "AppleTrailer":
			self.session.open(appletrailersGenreScreen)
		elif auswahl == "DOKUh":
			self.session.open(showDOKUHGenre)
		elif auswahl == "DokuHouse":
			self.session.open(show_DH_Genre)
		elif auswahl == "AllMusicHouse":
			self.session.open(show_AMH_Genre)
		# porn
		elif auswahl == "4Tube":
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pin4tube, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				self.session.open(fourtubeGenreScreen)
		elif auswahl == "AmateurPorn":
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pinamateurporn, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				self.session.open(amateurpornGenreScreen)
		elif auswahl == "Eporner":
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pineporner, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				self.session.open(epornerGenreScreen)
		elif auswahl == "HDPorn":
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pinhdporn, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				self.session.open(hdpornGenreScreen)
		elif auswahl == "PornerBros":
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pinpornerbros, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				self.session.open(pornerbrosGenreScreen)
		elif auswahl == "Pornhub":
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pinpornhub, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				self.session.open(pornhubGenreScreen)
		elif auswahl == "PornRabbit":
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pinpornrabbit, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				self.session.open(pornrabbitGenreScreen)
		elif auswahl == "RedTube":
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pinredtube, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				self.session.open(redtubeGenreScreen)
		elif auswahl == "xHamster":
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pinxhamster, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				self.session.open(xhamsterGenreScreen)
		elif auswahl == "YouPorn":
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pinyouporn, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				self.session.open(youpornGenreScreen)

	def pin4tube(self, pincode):
		if pincode:
			self.session.open(fourtubeGenreScreen)

	def pinamateurporn(self, pincode):
		if pincode:
			self.session.open(amateurpornGenreScreen)

	def pineporner(self, pincode):
		if pincode:
			self.session.open(epornerGenreScreen)

	def pinhdporn(self, pincode):
		if pincode:
			self.session.open(hdpornGenreScreen)

	def pinpornerbros(self, pincode):
		if pincode:
			self.session.open(pornerbrosGenreScreen)

	def pinpornhub(self, pincode):
		if pincode:
			self.session.open(pornhubGenreScreen)

	def pinpornrabbit(self, pincode):
		if pincode:
			self.session.open(pornrabbitGenreScreen)

	def pinredtube(self, pincode):
		if pincode:
			self.session.open(redtubeGenreScreen)

	def pinxhamster(self, pincode):
		if pincode:
			self.session.open(xhamsterGenreScreen)

	def pinyouporn(self, pincode):
		if pincode:
			self.session.open(youpornGenreScreen)
			
	def keyCancel(self):
		self.close()

def main(session, **kwargs):
	session.open(haupt_Screen)

def Plugins(**kwargs):
	return PluginDescriptor(name=_("MediaPortal"), description="MediaPortal", where = [PluginDescriptor.WHERE_PLUGINMENU, PluginDescriptor.WHERE_EXTENSIONSMENU], icon="plugin.png", fnc=main)
