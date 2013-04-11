#Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/mediaportal/additions/porn/drtuber_url.py
from Plugins.Extensions.mediaportal.resources.imports import *
import hashlib
import base64

class drtuberUrl:

    def __init__(self, session):
        self.session = session

    def getVideoUrl(self, param1, param2, param3, callback):
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3
        hash = hashlib.md5(self.param3 + base64.b64decode('UFQ2bDEzdW1xVjhLODI3')).hexdigest()
        url = 'http://www.drtuber.com/player/config.php?h=%s&t=%s&vkey=%s&pkey=%s&aid=' % (self.param1,
         self.param2,
         self.param3,
         hash)
        got_url = getPage(url, headers={'Content-Type': 'application/x-www-form-urlencoded'}).addCallback(self.getData, callback).addErrback(self.dataError, callback)
        callback(got_url)

    def getData(self, data, callback):
        url = re.findall('video_file.*?(http.*?\\.flv).*?\\/video_file', data, re.S)
        if url:
            url = str(url[0])
            callback(url)

    def dataError(self, error):
        print error
