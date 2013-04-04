from Components.Button import Button
from Components.Label import Label
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from Components.ActionMap import NumberActionMap, ActionMap
from Components.config import config, ConfigInteger, ConfigSelection, getConfigListEntry, ConfigText, ConfigDirectory, ConfigYesNo, configfile, ConfigSelection, ConfigSubsection, ConfigPIN, NoSave, ConfigNothing
from Components.FileList import FileList, FileEntryComponent
from Components.GUIComponent import GUIComponent
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap, MovingPixmap
from Components.PluginList import PluginEntryComponent, PluginList
# All import which are necessary
from Components.AVSwitch import AVSwitch
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmap, MultiContentEntryPixmapAlphaTest
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase

from enigma import gFont, addFont, eTimer, eConsoleAppContainer, ePicLoad, loadPNG, getDesktop, eServiceReference, iPlayableService, eListboxPythonMultiContent, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_VALIGN_CENTER, eListbox
from Plugins.Plugin import PluginDescriptor

from Screens.Screen import Screen
from Screens.ChoiceBox import ChoiceBox
from Screens.MessageBox import MessageBox
from Screens.InputBox import PinInput
from Screens.InfoBarGenerics import InfoBarSeek, InfoBarNotifications
from Screens.InfoBar import MoviePlayer, InfoBar
from twisted.web.client import downloadPage, getPage, error
from twisted.internet import reactor
from twisted.internet import defer
from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS
from Tools.LoadPixmap import LoadPixmap

import re, urllib, urllib2, os, cookielib, time, socket
import sha, cookielib, urllib2, re, shutil, urllib
from jsunpacker import cJsUnpacker
from urllib2 import Request, URLError, urlopen as urlopen2
from socket import gaierror, error
from urllib import quote, unquote_plus, unquote, urlencode
from httplib import HTTPConnection, CannotSendRequest, BadStatusLine, HTTPException
from time import strptime, mktime
from base64 import b64decode
from binascii import unhexlify
from urlparse import parse_qs
from streams import get_stream_link
import sha
import base64
import datetime
import math
import time
import hashlib
from time import *

from Screens.VirtualKeyBoard import VirtualKeyBoard

from Plugins.Extensions.mediaportal.resources import mp_globals

std_headers = {
	'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100627 Firefox/3.6.6',
	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
}
	
def registerFont(file, name, scale, replacement):
		try:
				addFont(file, name, scale, replacement)
		except Exception, ex: #probably just openpli
				addFont(file, name, scale, replacement, 0)

def decodeHtml(text):
	text = text.replace('&auml;','ae')
	text = text.replace('\u00e4','ae')
	text = text.replace('&#228;','ae')

	text = text.replace('&Auml;','Ae')
	text = text.replace('\u00c4','Ae')
	text = text.replace('&#196;','Ae')
	
	text = text.replace('&ouml;','oe')
	text = text.replace('\u00f6','oe')
	text = text.replace('&#246;','oe')
	
	text = text.replace('&ouml;','Oe')
	text = text.replace('\u00d6','Oe')
	text = text.replace('&#214;','Oe')
	
	text = text.replace('&uuml;','ue')
	text = text.replace('\u00fc','ue')
	text = text.replace('&#252;','ue')
	
	text = text.replace('&Uuml;','Ue')
	text = text.replace('\u00dc','Ue')
	text = text.replace('&#220;','Ue')
	
	text = text.replace('&szlig;','ss')
	text = text.replace('\u00df','ss')
	text = text.replace('&#223;','ss')
	
	text = text.replace('&amp;','&')
	text = text.replace('&quot;','\"')
	text = text.replace('&gt;','\'')
	text = text.replace('&apos;',"'")
	text = text.replace('&acute;','\'')
	text = text.replace('&ndash;','-')
	text = text.replace('&bdquo;','"')
	text = text.replace('&rdquo;','"')
	text = text.replace('&ldquo;','"')
	text = text.replace('&lsquo;','\'')
	text = text.replace('&rsquo;','\'')
	text = text.replace('&#038;','&')
	text = text.replace('&#039;','\'')
	text = text.replace('&#160;',' ')
	text = text.replace('&#174;','')
	text = text.replace('&#233;','e')
	text = text.replace('&#8211;',"-")
	text = text.replace('&#8216;',"'")
	text = text.replace('&#8217;',"'")
	text = text.replace('&#8220;',"'")
	text = text.replace('&#8221;','"')
	text = text.replace('&#8222;',',')
	text = text.replace('&#8230;','...')
	return text	