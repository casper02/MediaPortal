import math
import re
import urllib2
from urllib import unquote
from cookielib import CookieJar

class Flashx(object):

	def __init__(self):
		self.cj = CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		self.opener.addheaders = [('User-agent', 'Mozilla/5.0')]

	def __c(self, c):
		d = ""
		for i in range(0, len(c)):
			if i % 3 == 0:
				d += '%'
			else:
				d += c[i]
		return d

	def __x(self, x, t):
		l = len(x)
		b = 1024
		i = j = p = s = w = 0
		j = math.ceil(l / b)
		r = ""
		while j > 0:
			j -= 1
			i = min(l, b)
			while i > 0:
				i -= 1
				l -= 1
				w |= t[ord(x[p]) - 48] << s
				p += 1
				if s:
					r += chr(165 ^ w & 255)
					w >>= 8
					s -= 2
				else:
					s = 6

		return r

	def __t(self, d):
		data = unquote(d)
		arr = re.findall('Array\((.*?)\)', data)
		if arr:
			t = [int(x) for x in re.findall("\d+", arr[0])]
			return t
		else:
			return []
			
	def __decodeX(self, c, x):
		d = self.__c(c)
		t = self.__t(d)
		html = self.__x(x, t)
		return html
		
	def __getData(self, url, decode=False):
		data = None
		try:
			resp = self.opener.open(url)
			data = resp.read()
		except urllib2.HTTPError, e:
			print "HTTP Error: ",e
		except urllib2.URLError, e:
			print "URL Error: ",e
		
		if not decode:
			return data
		if data != None:
			js = re.findall('<script language=javascript>c="(.*?)";.*?x\("(.*?)"', data)
			if js:
				c = js[0][0]
				x = js[0][1]
				html = self.__decodeX(c,x)
				newurl=resp.geturl()
				return html
					
		return data
		
	def getVidUrl(self, url):
		html = self.__getData(url, True)
		vidUrl = None
		if html:
			js = re.findall('class="auto-style6".*?<a href="(.*?)"', html, re.S)
			if js:
				html = self.__getData(js[0], True)
				if html:
					js = re.findall('player.swf\?config=(.*?)"', html)
					if js:
						html = self.__getData(js[0])
						if html:
							js = re.findall('<file>(.*?)</file>', html)
							if js:
								vidUrl = js[0]
					
		return vidUrl
