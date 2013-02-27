# General imports
from imports import *
from decrypt import *
	
# Streame-Sites import
from dokuMe import *
from roflVideos import *
from streamJunkies import *
from xHamster import *
from focus import *
from yourFreeTV import *
from tvKino import *
from filmOn import *
from netzKino import *
from kinoKiste import *
from pornHub import *
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
from x4tube import *

config.mediaportal = ConfigSubsection()
config.mediaportal.pincode = ConfigPIN(default = 0000)
config.mediaportal.skin = ConfigSelection(default = "original", choices = [("liquidblue", _("liquidblue")), ("original", _("original"))])
config.mediaportal.showDoku = ConfigYesNo(default = True)
config.mediaportal.showRofl = ConfigYesNo(default = True)
config.mediaportal.showFail = ConfigYesNo(default = True)
config.mediaportal.showStream = ConfigYesNo(default = True)
config.mediaportal.showKinoKiste = ConfigYesNo(default = True)
config.mediaportal.showStreamOase = ConfigYesNo(default = True)
config.mediaportal.showMyvideo = ConfigYesNo(default = True)
config.mediaportal.showFocus = ConfigYesNo(default = True)
config.mediaportal.showYourfree = ConfigYesNo(default = True)
config.mediaportal.showFilmOn = ConfigYesNo(default = True)
config.mediaportal.showTvkino = ConfigYesNo(default = True)
config.mediaportal.showXhamster = ConfigYesNo(default = True)
config.mediaportal.showSpobox = ConfigYesNo(default = True)
config.mediaportal.showPornhub = ConfigYesNo(default = True)
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
config.mediaportal.showtivi = ConfigYesNo(default = True)
config.mediaportal.showSongsto = ConfigYesNo(default = True)
config.mediaportal.showMEHD = ConfigYesNo(default = True)
config.mediaportal.showM2k = ConfigYesNo(default = True)
config.mediaportal.showM2kPorn = ConfigYesNo(default = True)
config.mediaportal.showIStream = ConfigYesNo(default = True)
config.mediaportal.show4tube = ConfigYesNo(default = True)


class hauptScreenSetup(Screen, ConfigListScreen):
     
            if config.mediaportal.skin.value == "original":
                    skin =  """
                            <screen name="MediaPortal_Setup" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
                                    <eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
                                    <widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
                                    <widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
                                            <convert type="ClockToText">Format:%-H:%M</convert>
                                    </widget>
                                    <widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
                                            <convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
                                    </widget>
                                    <widget name="config" position="0,60" size="900,350" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
                                    <eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
                                    <widget name="coverArt" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,440" size="160,120" transparent="1" alphatest="blend" />
                                    <widget name="name" position="230,420" size="560,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
                            </screen>"""
            else:
                    path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/haupt_Screen.xml" % config.mediaportal.skin.value
                    with open(path, "r") as f:
                    self.skin = f.read()
                    f.close()


	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		
		self.configlist = []
		ConfigListScreen.__init__(self, self.configlist)
		self.configlist.append(getConfigListEntry("Pincode:", config.mediaportal.pincode))
		self.configlist.append(getConfigListEntry("Skinauswahl:", config.mediaportal.skin))
		self.configlist.append(getConfigListEntry("Zeige Doku:", config.mediaportal.showDoku))
		self.configlist.append(getConfigListEntry("Zeige Rofl:", config.mediaportal.showRofl))
		self.configlist.append(getConfigListEntry("Zeige Fail:", config.mediaportal.showFail))
		self.configlist.append(getConfigListEntry("Zeige Myvideo:", config.mediaportal.showMyvideo))
		self.configlist.append(getConfigListEntry("Zeige AutoBild:", config.mediaportal.showAutoBild))
		self.configlist.append(getConfigListEntry("Zeige SportBild:", config.mediaportal.showSportBild))
		self.configlist.append(getConfigListEntry("Zeige Laola1:", config.mediaportal.showLaola1))
		self.configlist.append(getConfigListEntry("Zeige KinderKino:", config.mediaportal.showKinderKino))
		self.configlist.append(getConfigListEntry("Zeige Streamjunkies:", config.mediaportal.showStream))
		self.configlist.append(getConfigListEntry("Zeige KinoKiste:", config.mediaportal.showKinoKiste))
		self.configlist.append(getConfigListEntry("Zeige Stream-Oase:", config.mediaportal.showStreamOase))
		self.configlist.append(getConfigListEntry("Zeige Burning Series:", config.mediaportal.showBs))
		self.configlist.append(getConfigListEntry("Zeige Kinox:", config.mediaportal.showKinox))
		self.configlist.append(getConfigListEntry("Zeige Movie2k:", config.mediaportal.showM2k))
		self.configlist.append(getConfigListEntry("Zeige Movie2k-Porn:", config.mediaportal.showM2kPorn))
		self.configlist.append(getConfigListEntry("Zeige Konzert Oase:", config.mediaportal.showKoase))
		self.configlist.append(getConfigListEntry("Zeige 1channel:", config.mediaportal.show1channel))
		self.configlist.append(getConfigListEntry("Zeige Focus:", config.mediaportal.showFocus))
		self.configlist.append(getConfigListEntry("Zeige Yourfree:", config.mediaportal.showYourfree))
		self.configlist.append(getConfigListEntry("Zeige FilmeOn:", config.mediaportal.showFilmOn))
		self.configlist.append(getConfigListEntry("Zeige TvKino:", config.mediaportal.showTvkino))
		self.configlist.append(getConfigListEntry("Zeige NetzKino:", config.mediaportal.showNetzKino))
		self.configlist.append(getConfigListEntry("Zeige xHamster:", config.mediaportal.showXhamster))
		self.configlist.append(getConfigListEntry("Zeige Spobox:", config.mediaportal.showSpobox))
		self.configlist.append(getConfigListEntry("Zeige Pornhub:", config.mediaportal.showPornhub))
		self.configlist.append(getConfigListEntry("Zeige Radio:", config.mediaportal.showRadio))
		self.configlist.append(getConfigListEntry("Zeige Cczwei:", config.mediaportal.showCczwei))
		self.configlist.append(getConfigListEntry("Zeige Filmtrailer:", config.mediaportal.showTrailer))
		self.configlist.append(getConfigListEntry("Zeige Baskino:", config.mediaportal.showBaskino))
		self.configlist.append(getConfigListEntry("Zeige Vutechtalk:", config.mediaportal.showVutec))
		self.configlist.append(getConfigListEntry("Zeige Dreamscreencast:", config.mediaportal.showDsc))
		self.configlist.append(getConfigListEntry("Zeige NHL:", config.mediaportal.showNhl))
		self.configlist.append(getConfigListEntry("Zeige Tivi:", config.mediaportal.showtivi))
		self.configlist.append(getConfigListEntry("Zeige Songsto:", config.mediaportal.showSongsto))
		self.configlist.append(getConfigListEntry("Zeige My-Entertainment:", config.mediaportal.showMEHD))
		self.configlist.append(getConfigListEntry("Zeige IStream:", config.mediaportal.showIStream))
		self.configlist.append(getConfigListEntry("Zeige 4tube:", config.mediaportal.show4tube))
		self["config"].setList(self.configlist)

		self['title'] = Label("MediaPortal - Setup - (version 3.5.1)")
		self['name'] = Label("Setup")
		self['coverArt'] = Pixmap()
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

	def keyOK(self):
		for x in self["config"].list:
			x[1].save()
		self.close()
	
	def keyCancel(self):
		self.close()

class chooseMenuList(MenuList):
	def __init__(self, list):
		MenuList.__init__(self, list, True, eListboxPythonMultiContent)
		self.l.setFont(0, gFont("Regular", 20))
		self.l.setItemHeight(40)

class haupt_Screen(Screen, ConfigListScreen):
	skin = 	"""
		<screen name="MediaPortal" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="Infos" position="30,60" size="260,25" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center"/>
			<widget name="infos" position="30,85" size="260,480" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<widget name="Fun" position="320,60" size="260,25" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center"/>
			<widget name="fun" position="320,85" size="260,480" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<widget name="Movies" position="610,60" size="260,25" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center"/>
			<widget name="movies" position="610,85" size="260,480" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<widget name="name" position="0,580" size="900,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;28" valign="top" halign="center"/>
		</screen>"""

class haupt_Screen:

path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/haupt_Scre
en.xml" % config.mediaportal.skin.value
with open(path, "r") as f:
self.skin = f.read()
f.close()		

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"up"    : self.keyUp,
			"down"  : self.keyDown,
			"cancel": self.keyCancel,
			"left"  : self.keyLeft,
			"right" : self.keyRight,
			"menu" : self.keySetup
		}, -1)

		self['title'] = Label("MediaPortal v3.5.1")
		
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
			self.movies.append(self.hauptListEntry("BurningSeries", "burningseries"))
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
			self.movies.append(self.hauptListEntry("My-Entertain", "mehd"))
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
			self.infos.append(self.hauptListEntry("Cczwei", "cczwei"))
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
			
		#fun & TV
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
			self.fun.append(self.hauptListEntry("Radio", "radiode"))
		if config.mediaportal.showXhamster.value:
			self.fun.append(self.hauptListEntry("xHamster", "xhamster"))
		if config.mediaportal.showSpobox.value:
			self.fun.append(self.hauptListEntry("Spobox", "spobox"))
		if config.mediaportal.showPornhub.value:
			self.fun.append(self.hauptListEntry("PornHub", "pornhub"))
		if config.mediaportal.showSongsto.value:
			self.fun.append(self.hauptListEntry("Songsto", "songsto"))
		if config.mediaportal.show4tube.value:
			self.fun.append(self.hauptListEntry("4tube", "4tube"))

		self.movies.sort()
		self.infos.sort()
		self.fun.sort()		

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
		elif auswahl == "Streamjunkies":
			self.session.open(streamGenreScreen)
		elif auswahl == "KinoKiste":
			self.session.open(kinokisteGenreScreen)
		elif auswahl == "BurningSeries":
			self.session.open(bsMain)
		elif auswahl == "1channel":
			self.session.open(chMain)
		elif auswahl == "Focus":
			self.session.open(focusGenre)
		elif auswahl == "YourfreeTv":
			self.session.open(yourFreeTv)
		elif auswahl == "FilmOn":
			self.session.open(filmON)
		elif auswahl == "NetzKino":
			self.session.open(netzKinoGenreScreen)
		elif auswahl == "xHamster":
			self.session.open(xhamsterGenreScreen)
		elif auswahl == "Spobox":
			self.session.open(spoboxGenreScreen)
		elif auswahl == "PornHub":
			self.session.open(pornhubGenreScreen)
		elif auswahl == "Radio":
			self.session.open(Radiode)
		elif auswahl == "Cczwei":
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
		elif auswahl == "Tivi":
			self.session.open(tiviGenreListeScreen)
		elif auswahl == "My-Entertain":
			self.session.open(showMEHDGenre)
		elif auswahl == "Songsto":
			self.session.open(showSongstoGenre)
		elif auswahl == "Movie2k":
			self.session.open(m2kGenreScreen, self.showM2KPorn)
		elif auswahl == "IStream":
			self.session.open(showIStreamGenre)
		elif auswahl == "4tube":
			self.session.open(fourtubeGenreScreen)

	def keyCancel(self):
		self.close()


def main(session, **kwargs):
	session.open(haupt_Screen)

def Plugins(**kwargs):
	return PluginDescriptor(name=_("MediaPortal"), description="MediaPortal", where = PluginDescriptor.WHERE_PLUGINMENU, icon="plugin.png", fnc=main)
