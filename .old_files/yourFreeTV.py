from imports import *
from decrypt import *

def yourFreeTvListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 

class yourFreeTv(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/skins/%s/yourFreeTv.xml" % config.mediaportal.skin.value
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("YourFreeTv.net - Watch Live TV")
		self['name'] = Label("Sender Auswahl")
		self['coverArt'] = Pixmap()
		
		self.senderliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.keyLocked = False
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.keyLocked = True
		url = "http://www.youfreetv.net/index.php?section=channel&value=pro7"
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.pageData).addErrback(self.dataError)
	
	def pageData(self, data):
		yftSender = re.findall('<li id=".*?"><a href="(.*?)"><img src=".(.*?)" alt="" border="" title="" />(.*?)</a></li(> !-->|>)', data, re.S)
		if yftSender:
			for (yftUrl,yftImage,yftTitle,yftCheck) in yftSender:
				yftUrl = "http://www.youfreetv.net/" + yftUrl
				print yftTitle, yftUrl
				if yftCheck == ">":
					self.senderliste.append((yftTitle, yftUrl))
			self.chooseMenuList.setList(map(yourFreeTvListEntry, self.senderliste))
			self.keyLocked = False

	def dataError(self, error):
		print error
		
	def keyOK(self):
		if self.keyLocked:
			return
		yftTitle = self['genreList'].getCurrent()[0][0]
		yftLink = self['genreList'].getCurrent()[0][1]
		print yftLink
		#getPage(yftLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.streamData).addErrback(self.dataError)
		getName = re.findall('value=(.*?)$', yftLink)
		if getName:
			print getName[0]
			streamUrl = "rtmp://cdn.youfreetv.net/tvstream//%s.stream swfUrl=http://www.youfreetv.net/medien/player.php?file=swf" % getName[0]
			#streamUrl = "rtmp://megaserver.youfreetv.net/live//%s.stream swfUrl=http://www.youfreetv.net/medien/player.php?file=swf" % getName[0]
			sref = eServiceReference(0x1001, 0, streamUrl)
			sref.setName(yftTitle)
			self.session.open(MoviePlayer, sref)		
		
	def streamData(self, data):
		self.keyLocked = False
		yftTitle = self['genreList'].getCurrent()[0][0]
		yftInfo = re.findall("streamer: '(.*?)'.*?file: '(.*?)'", data, re.S)
		if yftInfo:
			streamUrl = "%s//%s swfUrl=http://www.youfreetv.net/medien/player.php?file=swf" % (yftInfo[0][0], yftInfo[0][1])
			if streamUrl:
				sref = eServiceReference(0x1001, 0, streamUrl)
				sref.setName(yftTitle)
				self.session.open(MoviePlayer, sref)
		
	def keyCancel(self):
		self.close()