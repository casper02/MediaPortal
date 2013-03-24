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
#from UltimateStreams import *
from mahlzeitTV import *
from appletrailers import *
from DOKUh import *
from DokuHouse import *
from AllMusicHouse import *
from LiveLeak import *
from DokuStream import *
from ScienceTV import *
from SzeneStreams import *

# mediatheken
from VOXnow import *
from RTLnow import *
from RTLNITROnow import *
from RTL2now import *

# porn
from ahme import *
from amateurporn import *
from beeg import *
from eporner import *
from hdporn import *
from pinkrod import *
from pornerbros import *
from pornHub import *
from pornrabbit import *
from redtube import *
from thenewporn import *
from wetplace import *
from xHamster import *
from x4tube import *
from youporn import *

config.mediaportal = ConfigSubsection()
config.mediaportal.pincode = ConfigPIN(default = 0000)
config.mediaportal.skin = ConfigSelection(default = "original", choices = [("tec", _("tec")),("liquidblue", _("liquidblue")), ("original", _("original"))])
config.mediaportal.ansicht = ConfigSelection(default = "liste", choices = [("liste", _("Liste")),("wall", _("Wall"))])
config.mediaportal.selektor = ConfigSelection(default = "blue", choices = [("blue", _("blau")),("green", _(u"gr\xfcn")),("red", _("rot")),("turkis", _(u"t\xfcrkis"))])
config.mediaportal.useRtmpDump = ConfigYesNo(default = False)
config.mediaportal.storagepath = ConfigText(default="/media/hdd/mediaportal/tmp/", fixed_size=False)
config.mediaportal.filter = ConfigSelection(default = "ALL", choices = [("ALL", ("ALL")), ("Mediathek", ("Mediathek")), ("Grauzone", ("Grauzone")), ("Fun", ("Fun")), ("Sport", ("Sport")), ("Porn", ("Porn"))])
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
# Ustreams deaktiviert.
config.mediaportal.showUstreams = ConfigYesNo(default = False)
config.mediaportal.show4Players = ConfigYesNo(default = True)
config.mediaportal.showMahlzeitTV = ConfigYesNo(default = True)
config.mediaportal.showappletrailers = ConfigYesNo(default = True)
config.mediaportal.showDOKUh = ConfigYesNo(default = True)
config.mediaportal.showDokuHouse = ConfigYesNo(default = True)
config.mediaportal.showAllMusicHouse = ConfigYesNo(default = True)
config.mediaportal.showLiveLeak = ConfigYesNo(default = True)
config.mediaportal.showDokuStream = ConfigYesNo(default = True)
config.mediaportal.showScienceTV = ConfigYesNo(default = True)
config.mediaportal.showSzeneStreams = ConfigYesNo(default = True)

# mediatheken
config.mediaportal.showVoxnow = ConfigYesNo(default = True)
config.mediaportal.showRTLnow = ConfigYesNo(default = True)
config.mediaportal.showRTL2now = ConfigYesNo(default = True)
config.mediaportal.showRTLnitro = ConfigYesNo(default = True)

# porn
config.mediaportal.show4tube = ConfigYesNo(default = False)
config.mediaportal.showahme = ConfigYesNo(default = False)
config.mediaportal.showamateurporn = ConfigYesNo(default = False)
config.mediaportal.showbeeg = ConfigYesNo(default = False)
config.mediaportal.showeporner = ConfigYesNo(default = False)
config.mediaportal.showhdporn = ConfigYesNo(default = False)
config.mediaportal.showM2kPorn = ConfigYesNo(default = False)
config.mediaportal.showpinkrod = ConfigYesNo(default = False)
config.mediaportal.showpornerbros = ConfigYesNo(default = False)
config.mediaportal.showPornhub = ConfigYesNo(default = False)
config.mediaportal.showpornrabbit = ConfigYesNo(default = False)
config.mediaportal.showredtube = ConfigYesNo(default = False)
config.mediaportal.showthenewporn = ConfigYesNo(default = False)
config.mediaportal.showwetplace = ConfigYesNo(default = False)
config.mediaportal.showXhamster = ConfigYesNo(default = False)
config.mediaportal.showyouporn = ConfigYesNo(default = False)

#fake entry fuer die kategorien
config.mediaportal.fake_entry = NoSave(ConfigNothing())

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
		
		self.oldstoragepathvalue = config.mediaportal.storagepath.value

		self.configlist = []
		ConfigListScreen.__init__(self, self.configlist)

		## Allgemein
		self.configlist.append(getConfigListEntry("----- Allgemein -----", config.mediaportal.fake_entry))
		self.configlist.append(getConfigListEntry("Filter:", config.mediaportal.filter))
		self.configlist.append(getConfigListEntry("Pincode:", config.mediaportal.pincode))
		self.configlist.append(getConfigListEntry("XXX-Pincodeabfrage:", config.mediaportal.pornpin))
		self.configlist.append(getConfigListEntry("Selektor-Farbe", config.mediaportal.selektor))
		self.configlist.append(getConfigListEntry("HauptScreen-Ansicht", config.mediaportal.ansicht))
		self.configlist.append(getConfigListEntry("Skinauswahl:", config.mediaportal.skin))
		self.configlist.append(getConfigListEntry("RTMPDump benutzen:", config.mediaportal.useRtmpDump))
		self.configlist.append(getConfigListEntry("RTMPDump Cachepath:", config.mediaportal.storagepath)) 
		
		### Grauzone
		self.configlist.append(getConfigListEntry("----- Grauzone -----", config.mediaportal.fake_entry))
		self.configlist.append(getConfigListEntry("Zeige SzeneStreams:", config.mediaportal.showSzeneStreams))
		self.configlist.append(getConfigListEntry("Zeige Songs.to:", config.mediaportal.showSongsto))
		self.configlist.append(getConfigListEntry("Zeige My-Entertainment:", config.mediaportal.showMEHD))
		self.configlist.append(getConfigListEntry("Zeige IStream:", config.mediaportal.showIStream))
		self.configlist.append(getConfigListEntry("Zeige Baskino:", config.mediaportal.showBaskino))
		self.configlist.append(getConfigListEntry("Zeige KinoKiste:", config.mediaportal.showKinoKiste))
		self.configlist.append(getConfigListEntry("Zeige Stream-Oase:", config.mediaportal.showStreamOase))
		self.configlist.append(getConfigListEntry("Zeige Burning-Series:", config.mediaportal.showBs))
		self.configlist.append(getConfigListEntry("Zeige Kinox:", config.mediaportal.showKinox))
		self.configlist.append(getConfigListEntry("Zeige Movie2k:", config.mediaportal.showM2k))
		self.configlist.append(getConfigListEntry("Zeige Konzert Oase:", config.mediaportal.showKoase))
		self.configlist.append(getConfigListEntry("Zeige 1channel:", config.mediaportal.show1channel))
		#self.configlist.append(getConfigListEntry("Zeige UltimateStreams:", config.mediaportal.showUstreams))
		
		### Sport
		self.configlist.append(getConfigListEntry("----- Sport -----", config.mediaportal.fake_entry))
		self.configlist.append(getConfigListEntry("Zeige NHL:", config.mediaportal.showNhl))		
		self.configlist.append(getConfigListEntry("Zeige Spobox:", config.mediaportal.showSpobox))
		self.configlist.append(getConfigListEntry("Zeige Laola1:", config.mediaportal.showLaola1))
		
		### Fun
		self.configlist.append(getConfigListEntry("----- Fun -----", config.mediaportal.fake_entry))
		self.configlist.append(getConfigListEntry("Zeige Rofl.to:", config.mediaportal.showRofl))
		self.configlist.append(getConfigListEntry("Zeige Fail.to:", config.mediaportal.showFail))
		self.configlist.append(getConfigListEntry("Zeige Radio.de:", config.mediaportal.showRadio))		
		self.configlist.append(getConfigListEntry("Zeige TvKino:", config.mediaportal.showTvkino))
		self.configlist.append(getConfigListEntry("Zeige FilmOn:", config.mediaportal.showFilmOn))
		self.configlist.append(getConfigListEntry("Zeige Focus:", config.mediaportal.showFocus))

		### mediatheken
		self.configlist.append(getConfigListEntry("----- Mediatheken -----", config.mediaportal.fake_entry))
		self.configlist.append(getConfigListEntry("Zeige VOXNOW:", config.mediaportal.showVoxnow))
		self.configlist.append(getConfigListEntry("Zeige RTLNOW:", config.mediaportal.showRTLnow))
		self.configlist.append(getConfigListEntry("Zeige RTL2NOW:", config.mediaportal.showRTL2now))
		self.configlist.append(getConfigListEntry("Zeige RTLNITRONOW:", config.mediaportal.showRTLnitro))
		self.configlist.append(getConfigListEntry("Zeige ScienceTV:", config.mediaportal.showScienceTV))
		self.configlist.append(getConfigListEntry("Zeige Doku.me:", config.mediaportal.showDoku))
		self.configlist.append(getConfigListEntry("Zeige Myvideo:", config.mediaportal.showMyvideo))
		self.configlist.append(getConfigListEntry("Zeige DokuStream:", config.mediaportal.showDokuStream))
		self.configlist.append(getConfigListEntry("Zeige LiveLeak:", config.mediaportal.showLiveLeak))
		self.configlist.append(getConfigListEntry("Zeige 4Players:", config.mediaportal.show4Players))
		self.configlist.append(getConfigListEntry("Zeige mahlzeit.tv:", config.mediaportal.showMahlzeitTV))
		self.configlist.append(getConfigListEntry("Zeige Apple Movie Trailers:", config.mediaportal.showappletrailers))
		self.configlist.append(getConfigListEntry("Zeige DOKUh:", config.mediaportal.showDOKUh))
		self.configlist.append(getConfigListEntry("Zeige DokuHouse:", config.mediaportal.showDokuHouse))
		self.configlist.append(getConfigListEntry("Zeige AllMusicHouse:", config.mediaportal.showAllMusicHouse))
		self.configlist.append(getConfigListEntry("Zeige AutoBild:", config.mediaportal.showAutoBild))
		self.configlist.append(getConfigListEntry("Zeige SportBild:", config.mediaportal.showSportBild))
		self.configlist.append(getConfigListEntry("Zeige Tivi:", config.mediaportal.showtivi))
		self.configlist.append(getConfigListEntry("Zeige KinderKino:", config.mediaportal.showKinderKino))
		self.configlist.append(getConfigListEntry("Zeige Vutechtalk:", config.mediaportal.showVutec))
		self.configlist.append(getConfigListEntry("Zeige Dreamscreencast:", config.mediaportal.showDsc))
		self.configlist.append(getConfigListEntry("Zeige Focus:", config.mediaportal.showFocus))
		self.configlist.append(getConfigListEntry("Zeige CCZwei:", config.mediaportal.showCczwei))
		self.configlist.append(getConfigListEntry("Zeige Filmtrailer:", config.mediaportal.showTrailer))
		self.configlist.append(getConfigListEntry("Zeige NetzKino:", config.mediaportal.showNetzKino))

		### Porn
		self.configlist.append(getConfigListEntry("----- Porn -----", config.mediaportal.fake_entry))
		self.configlist.append(getConfigListEntry("Zeige 4Tube:", config.mediaportal.show4tube))
		self.configlist.append(getConfigListEntry("Zeige Ah-Me:", config.mediaportal.showahme))
		self.configlist.append(getConfigListEntry("Zeige AmateurPorn:", config.mediaportal.showamateurporn))
		self.configlist.append(getConfigListEntry("Zeige beeg:", config.mediaportal.showbeeg))
		self.configlist.append(getConfigListEntry("Zeige Eporner:", config.mediaportal.showeporner))
		self.configlist.append(getConfigListEntry("Zeige HDPorn:", config.mediaportal.showhdporn))
		self.configlist.append(getConfigListEntry("Zeige Movie2k-Porn:", config.mediaportal.showM2kPorn))
		self.configlist.append(getConfigListEntry("Zeige Pinkrod:", config.mediaportal.showpinkrod))
		self.configlist.append(getConfigListEntry("Zeige PornerBros:", config.mediaportal.showpornerbros))
		self.configlist.append(getConfigListEntry("Zeige Pornhub:", config.mediaportal.showPornhub))
		self.configlist.append(getConfigListEntry("Zeige PornRabbit:", config.mediaportal.showpornrabbit))
		self.configlist.append(getConfigListEntry("Zeige RedTube:", config.mediaportal.showredtube))
		self.configlist.append(getConfigListEntry("Zeige TheNewPorn:", config.mediaportal.showthenewporn))
		self.configlist.append(getConfigListEntry("Zeige WetPlace:", config.mediaportal.showwetplace))
		self.configlist.append(getConfigListEntry("Zeige xHamster:", config.mediaportal.showXhamster))
		self.configlist.append(getConfigListEntry("Zeige YouPorn:", config.mediaportal.showyouporn))
		
		#self.configlist.sort(key=lambda t : tuple(t[0].lower()))
		self["config"].setList(self.configlist)

		self['title'] = Label("MediaPortal - Setup - (Version 4.1.0)")
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
		self.l.setFont(0, gFont("mediaportal", 20))
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

		registerFont("/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/mediaportal.ttf", "mediaportal", 100, False)
		
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

		self['title'] = Label("MediaPortal v4.1.0")
		
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
		if config.mediaportal.showSzeneStreams.value:
			self.movies.append(self.hauptListEntry("SzeneStreams", "szenestreams"))
		if config.mediaportal.showVoxnow.value:
			self.movies.append(self.hauptListEntry("VOXNOW", "voxnow"))
		if config.mediaportal.showRTLnow.value:
			self.movies.append(self.hauptListEntry("RTLNOW", "rtlnow"))
		if config.mediaportal.showRTL2now.value:
			self.movies.append(self.hauptListEntry("RTL2NOW", "rtl2now"))
		if config.mediaportal.showRTLnitro.value:
			self.movies.append(self.hauptListEntry("RTLNITRONOW", "rtlnitro"))
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
		if config.mediaportal.showDokuStream.value:
			self.infos.append(self.hauptListEntry("DokuStream", "dokustream"))
		# fun & TV
		if config.mediaportal.showRofl.value:
			self.fun.append(self.hauptListEntry("Rofl.to", "rofl"))
		if config.mediaportal.showFail.value:
			self.fun.append(self.hauptListEntry("Fail.to", "fail"))
		if config.mediaportal.showLiveLeak.value:
			self.fun.append(self.hauptListEntry("LiveLeak", "liveleak"))
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
		if config.mediaportal.showScienceTV.value:
			self.fun.append(self.hauptListEntry("ScienceTV", "sciencetv"))
		# porn
		if config.mediaportal.show4tube.value:
			self.fun.append(self.hauptListEntry("4Tube", "4tube"))
		if config.mediaportal.showahme.value:
			self.fun.append(self.hauptListEntry("Ah-Me", "ahme"))
		if config.mediaportal.showamateurporn.value:
			self.fun.append(self.hauptListEntry("AmateurPorn", "amateurporn"))
		if config.mediaportal.showbeeg.value:
			self.fun.append(self.hauptListEntry("beeg", "beeg"))
		if config.mediaportal.showeporner.value:
			self.fun.append(self.hauptListEntry("Eporner", "eporner"))
		if config.mediaportal.showhdporn.value:
			self.fun.append(self.hauptListEntry("HDPorn", "hdporn"))
		if config.mediaportal.showpinkrod.value:
			self.fun.append(self.hauptListEntry("Pinkrod", "pinkrod"))
		if config.mediaportal.showpornerbros.value:
			self.fun.append(self.hauptListEntry("PornerBros", "pornerbros"))
		if config.mediaportal.showPornhub.value:
			self.fun.append(self.hauptListEntry("Pornhub", "pornhub"))
		if config.mediaportal.showpornrabbit.value:
			self.fun.append(self.hauptListEntry("PornRabbit", "pornrabbit"))
		if config.mediaportal.showredtube.value:
			self.fun.append(self.hauptListEntry("RedTube", "redtube"))
		if config.mediaportal.showthenewporn.value:
			self.fun.append(self.hauptListEntry("TheNewPorn", "thenewporn"))
		if config.mediaportal.showwetplace.value:
			self.fun.append(self.hauptListEntry("WetPlace", "wetplace"))
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
			self.session.openWithCallback(self.restart, hauptScreenSetup)

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
		elif auswahl == "LiveLeak":
			self.session.open(LiveLeakScreen)
		elif auswahl == "DokuStream":
			self.session.open(show_DS_Genre)
		elif auswahl == "ScienceTV":
			self.session.open(scienceTvGenreScreen)
		elif auswahl == "SzeneStreams":
			self.session.open(SzeneStreamsGenreScreen)
		# mediatheken
		elif auswahl == "VOXNOW":
			self.session.open(VOXnowGenreScreen)
		elif auswahl == "RTLNOW":
			self.session.open(RTLnowGenreScreen)
		elif auswahl == "RTL2NOW":
			self.session.open(RTL2nowGenreScreen)
		elif auswahl == "RTLNITRONOW":
			self.session.open(RTLNITROnowGenreScreen)
		# porn
		elif auswahl == "4Tube":
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pin4tube, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				self.session.open(fourtubeGenreScreen)
		elif auswahl == "Ah-Me":
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pinahme, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				self.session.open(ahmeGenreScreen)
		elif auswahl == "AmateurPorn":
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pinamateurporn, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				self.session.open(amateurpornGenreScreen)
		elif auswahl == "beeg":
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pinbeeg, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				self.session.open(beegGenreScreen)
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
		elif auswahl == "Pinkrod":
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pinpinkrod, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				self.session.open(pinkrodGenreScreen)
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
		elif auswahl == "TheNewPorn":
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pinthenewporn, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				self.session.open(thenewpornGenreScreen)
		elif auswahl == "WetPlace":
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pinwetplace, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				self.session.open(wetplaceGenreScreen)
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

	def pinahme(self, pincode):
		if pincode:
			self.session.open(ahmeGenreScreen)

	def pinamateurporn(self, pincode):
		if pincode:
			self.session.open(amateurpornGenreScreen)

	def pinbeeg(self, pincode):
		if pincode:
			self.session.open(beegGenreScreen)

	def pineporner(self, pincode):
		if pincode:
			self.session.open(epornerGenreScreen)

	def pinhdporn(self, pincode):
		if pincode:
			self.session.open(hdpornGenreScreen)

	def pinpinkrod(self, pincode):
		if pincode:
			self.session.open(pinkrodGenreScreen)

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

	def pinthenewporn(self, pincode):
		if pincode:
			self.session.open(thenewpornGenreScreen)

	def pinwetplace(self, pincode):
		if pincode:
			self.session.open(wetplaceGenreScreen)

	def pinxhamster(self, pincode):
		if pincode:
			self.session.open(xhamsterGenreScreen)

	def pinyouporn(self, pincode):
		if pincode:
			self.session.open(youpornGenreScreen)
			
	def keyCancel(self):
		self.close(self.session, True)

	def restart(self):
		self.close(self.session, False)

class haupt_Screen_Wall(Screen, ConfigListScreen):
	def __init__(self, session, filter):
		self.session = session
		#config.mediaportal.filter.value = filter

		self.plugin_liste = []
		if config.mediaportal.showMyvideo.value:
			self.plugin_liste.append(("MyVideo", "myvideo", "Mediathek"))
		if config.mediaportal.showKinderKino.value:
			self.plugin_liste.append(("KinderKino", "kinderkino", "Mediathek"))
		if config.mediaportal.showKinoKiste.value:
			self.plugin_liste.append(("KinoKiste", "kinokiste", "Grauzone"))
		if config.mediaportal.showBs.value:
			self.plugin_liste.append(("Burning-Series", "burningseries", "Grauzone"))
		if config.mediaportal.show1channel.value:
			self.plugin_liste.append(("1channel", "1channel", "Grauzone"))
		if config.mediaportal.showNetzKino.value:
			self.plugin_liste.append(("NetzKino", "netzkino", "Mediathek"))
		if config.mediaportal.showBaskino.value:
			self.plugin_liste.append(("Baskino", "baskino", "Grauzone"))
		if config.mediaportal.showKinox.value:
			self.plugin_liste.append(("Kinox", "kinox", "Grauzone"))
		if config.mediaportal.showStreamOase.value:
			self.plugin_liste.append(("StreamOase", "streamoase", "Grauzone"))
		if config.mediaportal.showtivi.value:
			self.plugin_liste.append(("Tivi", "tivi", "Mediathek"))
		if config.mediaportal.showMEHD.value:
			self.plugin_liste.append(("My-Entertainment", "mehd", "Grauzone"))
		if config.mediaportal.showUstreams.value:
			self.plugin_liste.append(("UltimateStreams", "ustreams", "Grauzone"))
		if config.mediaportal.showM2k.value:
			self.plugin_liste.append(("Movie2k", "movie2k", "Grauzone"))
		if config.mediaportal.showM2kPorn.value:
			self.showM2KPorn = True
		else:
			self.showM2KPorn = False
		if config.mediaportal.showIStream.value:
			self.plugin_liste.append(("IStream", "istream", "Grauzone"))
		if config.mediaportal.showSzeneStreams.value:
			self.plugin_liste.append(("SzeneStreams", "szenestreams", "Grauzone"))
		if config.mediaportal.showDoku.value:
			self.plugin_liste.append(("Doku.me", "doku", "Mediathek"))		
		if config.mediaportal.showSportBild.value:
			self.plugin_liste.append(("SportBild", "sportbild", "Mediathek"))
		if config.mediaportal.showAutoBild.value:
			self.plugin_liste.append(("AutoBild", "autobild", "Mediathek"))
		if config.mediaportal.showLaola1.value:
			self.plugin_liste.append(("Laola1 Live", "laola1", "Sport"))
		if config.mediaportal.showFocus.value:
			self.plugin_liste.append(("Focus", "focus", "Mediathek"))
		if config.mediaportal.showCczwei.value:
			self.plugin_liste.append(("CCZwei", "cczwei", "Mediathek"))
		if config.mediaportal.showTrailer.value:
			self.plugin_liste.append(("Filmtrailer", "trailer", "Mediathek"))
		if config.mediaportal.showVutec.value:
			self.plugin_liste.append(("Vutechtalk", "vutechtalk", "Mediathek"))
		if config.mediaportal.showDsc.value:
			self.plugin_liste.append(("Dreamscreencast", "dreamscreencast", "Mediathek"))
		if config.mediaportal.showKoase.value:
			self.plugin_liste.append(("Konzert Oase", "koase", "Grauzone"))
		if config.mediaportal.showNhl.value:
			self.plugin_liste.append(("NHL", "nhl", "Sport"))
		if config.mediaportal.show4Players.value:
			self.plugin_liste.append(("4Players", "4players", "Mediathek"))
		if config.mediaportal.showMahlzeitTV.value:
			self.plugin_liste.append(("mahlzeit.tv", "mahlzeit", "Mediathek"))
		if config.mediaportal.showappletrailers.value:
			self.plugin_liste.append(("AppleTrailer", "appletrailers", "Mediathek"))
		if config.mediaportal.showDOKUh.value:
			self.plugin_liste.append(("DOKUh", "dokuh", "Mediathek"))
		if config.mediaportal.showDokuHouse.value:
			self.plugin_liste.append(("DokuHouse", "dokuhouse", "Mediathek"))
		if config.mediaportal.showAllMusicHouse.value:
			self.plugin_liste.append(("AllMusicHouse", "allmusichouse", "Fun"))
		if config.mediaportal.showRofl.value:
			self.plugin_liste.append(("Rofl.to", "rofl", "Fun"))
		if config.mediaportal.showFail.value:
			self.plugin_liste.append(("Fail.to", "fail", "Fun"))
		if config.mediaportal.showFilmOn.value:
			self.plugin_liste.append(("FilmOn", "filmon", "Fun"))
		if config.mediaportal.showTvkino.value:
			self.plugin_liste.append(("TV-Kino", "tvkino", "Fun"))
		if config.mediaportal.showRadio.value:
			self.plugin_liste.append(("Radio.de", "radiode", "Fun"))
		if config.mediaportal.showSpobox.value:
			self.plugin_liste.append(("Spobox", "spobox", "Sport"))
		if config.mediaportal.showSongsto.value:
			self.plugin_liste.append(("Songs.to", "songsto", "Fun"))
		if config.mediaportal.showLiveLeak.value:
			self.plugin_liste.append(("LiveLeak", "liveleak", "Fun"))
		if config.mediaportal.showDokuStream.value:
			self.plugin_liste.append(("DokuStream", "dokustream", "Mediathek"))
		if config.mediaportal.showScienceTV.value:
			self.plugin_liste.append(("ScienceTV", "sciencetv", "Mediathek"))
			
		### mediatheken	
		if config.mediaportal.showVoxnow.value:
			self.plugin_liste.append(("VOXNOW", "voxnow", "Mediathek"))
		if config.mediaportal.showRTLnow.value:
			self.plugin_liste.append(("RTLNOW", "rtlnow", "Mediathek"))
		if config.mediaportal.showRTL2now.value:
			self.plugin_liste.append(("RTL2NOW", "rtl2now", "Mediathek"))
		if config.mediaportal.showRTLnitro.value:
			self.plugin_liste.append(("RTLNITRONOW", "rtlnitro", "Mediathek"))
			
		### porn
		if config.mediaportal.show4tube.value:
			self.plugin_liste.append(("4Tube", "4tube", "Porn"))
		if config.mediaportal.showahme.value:
			self.plugin_liste.append(("Ah-Me", "ahme", "Porn"))
		if config.mediaportal.showamateurporn.value:
			self.plugin_liste.append(("AmateurPorn", "amateurporn", "Porn"))
		if config.mediaportal.showbeeg.value:
			self.plugin_liste.append(("beeg", "beeg", "Porn"))
		if config.mediaportal.showeporner.value:
			self.plugin_liste.append(("Eporner", "eporner", "Porn"))
		if config.mediaportal.showhdporn.value:
			self.plugin_liste.append(("HDPorn", "hdporn", "Porn"))
		if config.mediaportal.showpinkrod.value:
			self.plugin_liste.append(("Pinkrod", "pinkrod", "Porn"))
		if config.mediaportal.showpornerbros.value:
			self.plugin_liste.append(("PornerBros", "pornerbros", "Porn"))
		if config.mediaportal.showPornhub.value:
			self.plugin_liste.append(("Pornhub", "pornhub", "Porn"))
		if config.mediaportal.showpornrabbit.value:
			self.plugin_liste.append(("PornRabbit", "pornrabbit", "Porn"))
		if config.mediaportal.showredtube.value:
			self.plugin_liste.append(("RedTube", "redtube", "Porn"))
		if config.mediaportal.showthenewporn.value:
			self.plugin_liste.append(("TheNewPorn", "thenewporn", "Porn"))
		if config.mediaportal.showwetplace.value:
			self.plugin_liste.append(("WetPlace", "wetplace", "Porn"))
		if config.mediaportal.showXhamster.value:
			self.plugin_liste.append(("xHamster", "xhamster", "Porn"))
		if config.mediaportal.showyouporn.value:
			self.plugin_liste.append(("YouPorn", "youporn", "Porn"))
			
		skincontent = ""
		
		posx = 20
		posy = 210
		for x in range(1,len(self.plugin_liste)+1):
			skincontent += "<widget name=\"zeile" + str(x) + "\" position=\"" + str(posx) + "," + str(posy) + "\" size=\"150,80\" zPosition=\"1\" transparent=\"0\" alphatest=\"blend\" />"
			posx += 155
			if x == 8 or x == 16 or x == 24 or x == 32 or x == 48 or x == 56 or x == 64 or x == 72:
				posx = 20
				posy += 85
			elif x == 40 or x == 80:
				posx = 20
				posy = 210
				
		self.skin_dump = ""
		self.skin_dump += "<widget name=\"frame\" position=\"20,210\" size=\"150,80\" pixmap=\"/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/icons_wall/Selektor_%s.png\" zPosition=\"2\" transparent=\"0\" alphatest=\"blend\" />" % config.mediaportal.selektor.value
		self.skin_dump += skincontent
		self.skin_dump += "</screen>"
		
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/hauptScreenWall.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/original/hauptScreenWall.xml"
		with open(path, "r") as f:
			self.skin_dump2 = f.read()
			self.skin_dump2 += self.skin_dump
			self.skin = self.skin_dump2
			f.close()
		
		Screen.__init__(self, session)

		registerFont("/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/mediaportal.ttf", "mediaportal", 100, False)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions", "HelpActions"], {
			"ok"    : self.keyOK,
			"up"    : self.keyUp,
			"down"  : self.keyDown,
			"cancel": self.keyCancel,
			"left"  : self.keyLeft,
			"right" : self.keyRight,
			"nextBouquet" :	self.page_next,
			"prevBouquet" :	self.page_back,
			"menu" : self.keySetup,
			"displayHelp" : self.keyHelp,
			"blue" : self.chFilter
		}, -1)
		
		self['name'] = Label("Plugin Auswahl")
		self['blue'] = Label("")
		self['page'] = Label("")
		self["frame"] = MovingPixmap()
		for x in range(1,len(self.plugin_liste)+1):
			self["zeile"+str(x)] = Pixmap()
			self["zeile"+str(x)].show()
		
		self.selektor_index = 1
		self.select_list = 0
		self.onFirstExecBegin.append(self._onFirstExecBegin)
		
	def _onFirstExecBegin(self):
		# load plugin icons
		print "Set Filter:", config.mediaportal.filter.value
		self['blue'].setText(config.mediaportal.filter.value)
		if config.mediaportal.filter.value != "ALL":
			dump_liste = self.plugin_liste
			self.plugin_liste = []
			self.plugin_liste = [x for x in dump_liste if config.mediaportal.filter.value == x[2]]
			self.plugin_liste.sort(key=lambda t : tuple(t[0].lower()))
			if self.check_empty_list():
				return
				
			for each in self.plugin_liste:
				print each

		for x in range(1,len(self.plugin_liste)+1):
			postername = self.plugin_liste[int(x)-1][1]
			poster_path = "%s/%s.png" % ("/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/icons_wall", postername)
			if not fileExists(poster_path):
				poster_path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/icons_wall/no_icon.png"

			self["zeile"+str(x)].instance.setPixmap(None)
			self["zeile"+str(x)].hide()
			pic = LoadPixmap(cached=True, path=poster_path)
			if pic != None:
				self["zeile"+str(x)].instance.setPixmap(pic)
				if x <= 40:
					self["zeile"+str(x)].show()
					
		# erstelle mainlist
		self.widget_list()
				
	def widget_list(self):
		count = 1
		counting = 1
		self.mainlist = []
		list_dummy = []
		self.plugin_counting = len(self.plugin_liste)
		
		for x in range(1,int(self.plugin_counting)+1):
			if count == 40:
				count += 1
				counting += 1
				list_dummy.append(x)
				self.mainlist.append(list_dummy)
				count = 1
				list_dummy = []
			else:
				count += 1
				counting += 1
				list_dummy.append(x)
				if int(counting) == int(self.plugin_counting)+1:
					self.mainlist.append(list_dummy)
					
		print self.mainlist
		pageinfo = "%s / %s" % (self.select_list+1, len(self.mainlist))
		self['page'].setText(pageinfo)
		select_nr = self.mainlist[int(self.select_list)][int(self.selektor_index)-1]
		plugin_name = self.plugin_liste[int(select_nr)-1][0]
		self['name'].setText(plugin_name)		
				
	def move_selector(self):
		select_nr = self.mainlist[int(self.select_list)][int(self.selektor_index)-1]
		plugin_name = self.plugin_liste[int(select_nr)-1][0]
		self['name'].setText(plugin_name)
		position = self["zeile"+str(self.selektor_index)].instance.position()
		self["frame"].moveTo(position.x(), position.y(), 1)
		self["frame"].show()
		self["frame"].startMoving()
		
	def keyOK(self):
		if self.check_empty_list():
			return
		
		select_nr = self.mainlist[int(self.select_list)][int(self.selektor_index)-1]
		auswahl = self.plugin_liste[int(select_nr)-1][0]
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
		elif auswahl == "LiveLeak":
			self.session.open(LiveLeakScreen)
		elif auswahl == "DokuStream":
			self.session.open(show_DS_Genre)
		elif auswahl == "ScienceTV":
			self.session.open(scienceTvGenreScreen)
		elif auswahl == "SzeneStreams":
			self.session.open(SzeneStreamsGenreScreen)
		# mediatheken
		elif auswahl == "VOXNOW":
			self.session.open(VOXnowGenreScreen)
		elif auswahl == "RTLNOW":
			self.session.open(RTLnowGenreScreen)
		elif auswahl == "RTL2NOW":
			self.session.open(RTL2nowGenreScreen)
		elif auswahl == "RTLNITRONOW":
			self.session.open(RTLNITROnowGenreScreen)
		# porn
		elif auswahl == "4Tube":
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pin4tube, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				self.session.open(fourtubeGenreScreen)
		elif auswahl == "Ah-Me":
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pinahme, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				self.session.open(ahmeGenreScreen)
		elif auswahl == "AmateurPorn":
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pinamateurporn, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				self.session.open(amateurpornGenreScreen)
		elif auswahl == "beeg":
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pinbeeg, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				self.session.open(beegGenreScreen)
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
		elif auswahl == "Pinkrod":
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pinpinkrod, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				self.session.open(pinkrodGenreScreen)
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
		elif auswahl == "TheNewPorn":
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pinthenewporn, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				self.session.open(thenewpornGenreScreen)
		elif auswahl == "WetPlace":
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pinwetplace, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				self.session.open(wetplaceGenreScreen)
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

	def pinahme(self, pincode):
		if pincode:
			self.session.open(ahmeGenreScreen)

	def pinamateurporn(self, pincode):
		if pincode:
			self.session.open(amateurpornGenreScreen)

	def pinbeeg(self, pincode):
		if pincode:
			self.session.open(beegGenreScreen)

	def pineporner(self, pincode):
		if pincode:
			self.session.open(epornerGenreScreen)

	def pinhdporn(self, pincode):
		if pincode:
			self.session.open(hdpornGenreScreen)

	def pinpinkrod(self, pincode):
		if pincode:
			self.session.open(pinkrodGenreScreen)

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

	def pinthenewporn(self, pincode):
		if pincode:
			self.session.open(thenewpornGenreScreen)

	def pinwetplace(self, pincode):
		if pincode:
			self.session.open(wetplaceGenreScreen)

	def pinxhamster(self, pincode):
		if pincode:
			self.session.open(xhamsterGenreScreen)

	def pinyouporn(self, pincode):
		if pincode:
			self.session.open(youpornGenreScreen)
	
	def	keyLeft(self):
		if self.check_empty_list():
			return
		if self.selektor_index > 1: 
			self.selektor_index -= 1
			self.move_selector()
		else:
			self.page_back()

	def	keyRight(self):
		if self.check_empty_list():
			return
		if self.selektor_index < 40 and self.selektor_index != len(self.mainlist[int(self.select_list)]):
			self.selektor_index += 1
			self.move_selector()
		else:
			self.page_next()
			
	def keyUp(self):
		if self.check_empty_list():
			return
		if self.selektor_index-8 > 1:
			self.selektor_index -=8
			self.move_selector()
		else:
			self.selektor_index = 1
			self.move_selector()

	def keyDown(self):
		if self.check_empty_list():
			return
			
		if self.selektor_index+8 <= len(self.mainlist[int(self.select_list)]):
			self.selektor_index +=8
			self.move_selector()
		else:
			self.selektor_index = len(self.mainlist[int(self.select_list)])
			self.move_selector()
			
	def page_next(self):
		if self.check_empty_list():
			return
			
		if self.select_list < len(self.mainlist)-1:
			self.paint_hide()
			self.select_list += 1
			self.paint_new()
	
	def page_back(self):
		if self.check_empty_list():
			return
			
		if self.select_list > 0:
			self.paint_hide()
			self.select_list -= 1
			self.paint_new_last()

	def check_empty_list(self):
		if len(self.plugin_liste) == 0:
			self['name'].setText('Keine Plugins der Kategorie %s aktiviert !' % config.mediaportal.filter.value)
			self["frame"].hide()
			return True
		else:
			return False
			
	def paint_hide(self):
		for x in self.mainlist[int(self.select_list)]:
			self["zeile"+str(x)].hide()
	
	def paint_new_last(self):
		pageinfo = "%s / %s" % (self.select_list+1, len(self.mainlist))
		self['page'].setText(pageinfo)
		self.selektor_index = self.mainlist[int(self.select_list)][-1]
		print self.selektor_index
		self.move_selector()
		for x in self.mainlist[int(self.select_list)]:
			self["zeile"+str(x)].show()
			
	def paint_new(self):
		pageinfo = "%s / %s" % (self.select_list+1, len(self.mainlist))
		self['page'].setText(pageinfo)
		self.selektor_index = 1
		self.move_selector()
		for x in self.mainlist[int(self.select_list)]:
			self["zeile"+str(x)].show()
	
	def keySetup(self):
		print config.mediaportal.pincode.value
		self.session.openWithCallback(self.pinok, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
	
	def keyHelp(self):
		self.session.open(HelpScreen)

	def getTriesEntry(self):
		return config.ParentalControl.retries.setuppin
		
	def pinok(self, pincode):
		if pincode:
			self.session.openWithCallback(self.restart, hauptScreenSetup)
			
	def chFilter(self):
		print config.mediaportal.filter.value
		if config.mediaportal.filter.value == "ALL":
			config.mediaportal.filter.value = "Mediathek"
		elif config.mediaportal.filter.value == "Mediathek":
			config.mediaportal.filter.value = "Grauzone"
		elif config.mediaportal.filter.value == "Grauzone":
			config.mediaportal.filter.value = "Sport"
		elif config.mediaportal.filter.value == "Sport":
			config.mediaportal.filter.value = "Fun"
		elif config.mediaportal.filter.value == "Fun":
			config.mediaportal.filter.value = "Porn"
		elif config.mediaportal.filter.value == "Porn":
			config.mediaportal.filter.value = "ALL"

		print "Filter:", config.mediaportal.filter.value
		self.restart()
		
	def keyCancel(self):
		config.mediaportal.filter.save()
		configfile.save()
		self.close(self.session, True)

	def restart(self):
		config.mediaportal.filter.save()
		configfile.save()
		self.close(self.session, False)

def exit(session, result):
	if not result:
		if config.mediaportal.ansicht.value == "liste":
			session.openWithCallback(exit, haupt_Screen)
		else:
			session.openWithCallback(exit, haupt_Screen_Wall, config.mediaportal.filter.value)		
	
def main(session, **kwargs):
	if config.mediaportal.ansicht.value == "liste":
		session.openWithCallback(exit, haupt_Screen)
	else:
		session.openWithCallback(exit, haupt_Screen_Wall, config.mediaportal.filter.value)
	
def Plugins(**kwargs):
	return PluginDescriptor(name=_("MediaPortal"), description="MediaPortal", where = [PluginDescriptor.WHERE_PLUGINMENU, PluginDescriptor.WHERE_EXTENSIONSMENU], icon="plugin.png", fnc=main)
