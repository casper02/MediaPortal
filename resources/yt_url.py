#	-*-	coding:	utf-8	-*-

from imports import *

class youtubeUrl:

  def __init__(self, session):
	self.callBack = None
	self.errBack = None
	self.session = session
	self.error = ""

  def addCallback(self, cbFunc):
	self.callBack = cbFunc
  
  def addErrback(self, errFunc):
	self.errBack = errFunc
		
  def errReturn(self, url):
	print self.error
	#print url
	if self.errBack == None:
		self.session.open(MessageBox,str(self.error), MessageBox.TYPE_INFO, timeout=10)
		return url
	else:
		self.errBack(self.error)
  
  def getVideoUrl(self, url, videoPrio=2):
	# this part is from mtube plugin
	print "got url:", url
	if videoPrio == 0:
		VIDEO_FMT_PRIORITY_MAP = {
			'38' : 5, #MP4 Original (HD)
			'37' : 6, #MP4 1080p (HD)
			'22' : 4, #MP4 720p (HD)
			'18' : 3, #MP4 360p
			'35' : 2, #FLV 480p
			'34' : 1, #FLV 360p
		}
	elif videoPrio == 1:
		VIDEO_FMT_PRIORITY_MAP = {
			'38' : 4, #MP4 Original (HD)
			'37' : 5, #MP4 1080p (HD)
			'22' : 2, #MP4 720p (HD)
			'18' : 3, #MP4 360p
			'35' : 1, #FLV 480p
			'34' : 2, #FLV 360p
		}
	elif videoPrio == 2:
		VIDEO_FMT_PRIORITY_MAP = {
			'38' : 2, #MP4 Original (HD)
			'37' : 3, #MP4 1080p (HD)
			'22' : 1, #MP4 720p (HD)
			'18' : 4, #MP4 360p
			'35' : 5, #FLV 480p
			'34' : 6, #FLV 360p
		}
	else:
		VIDEO_FMT_PRIORITY_MAP = {
			'38' : 1, #MP4 Original (HD)
			'37' : 2, #MP4 1080p (HD)
			'22' : 3, #MP4 720p (HD)
			'18' : 4, #MP4 360p
			'35' : 5, #FLV 480p
			'34' : 6, #FLV 360p
		}
		
	video_url = None
	video_id = url

	# Getting video webpage
	#URLs for YouTube video pages will change from the format http://www.youtube.com/watch?v=ylLzyHk54Z0 to http://www.youtube.com/watch#!v=ylLzyHk54Z0.
	watch_url = 'http://www.youtube.com/watch?v=%s&gl=US&hl=en' % video_id
	watchrequest = Request(watch_url, None, std_headers)
	try:
		print "[youtubeUrl] trying to find out if a HD Stream is available",watch_url
		watchvideopage = urlopen2(watchrequest).read()
	except (URLError, HTTPException, socket.error), err:
		self.error = "Error: Unable to retrieve watchpage - Error code: %s" % str(err)
		self.errReturn(video_url)
		return video_url
		
		# Get video info
	for el in ['&el=embedded', '&el=detailpage', '&el=vevo', '']:
		info_url = ('http://www.youtube.com/get_video_info?&video_id=%s%s&ps=default&eurl=&gl=US&hl=en' % (video_id, el))
		request = Request(info_url, None, std_headers)
		try:
			infopage = urlopen2(request).read()
			videoinfo = parse_qs(infopage)
			if ('url_encoded_fmt_stream_map' or 'fmt_url_map') in videoinfo:
				break
		except (URLError, HTTPException, socket.error), err:
			self.error = "Error: unable to download video infopage - %s" % str(err)
			self.errReturn(video_url)
			return video_url
			
	if ('url_encoded_fmt_stream_map' or 'fmt_url_map') not in videoinfo:
		# Attempt to see if YouTube has issued an error message
		if 'reason' not in videoinfo:
			self.error = 'Error: unable to extract "fmt_url_map" or "url_encoded_fmt_stream_map" parameter for unknown reason'
		else:
			reason = unquote_plus(videoinfo['reason'][0])
			self.error = 'Error: YouTube said: %s' % reason.decode('utf-8')

		self.errReturn(video_url)
		return video_url

	video_fmt_map = {}
	fmt_infomap = {}
	if videoinfo.has_key('url_encoded_fmt_stream_map'):
		tmp_fmtUrlDATA = videoinfo['url_encoded_fmt_stream_map'][0].split(',')
	else:
		tmp_fmtUrlDATA = videoinfo['fmt_url_map'][0].split(',')
	for fmtstring in tmp_fmtUrlDATA:
		fmturl = fmtid = fmtsig = ""
		if videoinfo.has_key('url_encoded_fmt_stream_map'):
			try:
				for arg in fmtstring.split('&'):
					if arg.find('=') >= 0:
						print arg.split('=')
						key, value = arg.split('=')
						if key == 'itag':
							if len(value) > 3:
								value = value[:2]
							fmtid = value
						elif key == 'url':
							fmturl = value
						elif key == 'sig':
							fmtsig = value
								
				if fmtid != "" and fmturl != "" and fmtsig != ""  and VIDEO_FMT_PRIORITY_MAP.has_key(fmtid):
					video_fmt_map[VIDEO_FMT_PRIORITY_MAP[fmtid]] = { 'fmtid': fmtid, 'fmturl': unquote_plus(fmturl), 'fmtsig': fmtsig }
					fmt_infomap[int(fmtid)] = "%s&signature=%s" %(unquote_plus(fmturl), fmtsig)
				fmturl = fmtid = fmtsig = ""

			except:
				self.error = "error parsing fmtstring: %s" % fmtstring
				self.errReturn(video_url)
				return video_url
					
		else:
			(fmtid,fmturl) = fmtstring.split('|')
		if VIDEO_FMT_PRIORITY_MAP.has_key(fmtid) and fmtid != "":
			video_fmt_map[VIDEO_FMT_PRIORITY_MAP[fmtid]] = { 'fmtid': fmtid, 'fmturl': unquote_plus(fmturl) }
			fmt_infomap[int(fmtid)] = unquote_plus(fmturl)
	print "[youtubeUrl] got",sorted(fmt_infomap.iterkeys())
	if video_fmt_map and len(video_fmt_map):
		print "[youtubeUrl] found best available video format:",video_fmt_map[sorted(video_fmt_map.iterkeys())[0]]['fmtid']
		best_video = video_fmt_map[sorted(video_fmt_map.iterkeys())[0]]
		video_url = "%s&signature=%s" %(best_video['fmturl'].split(';')[0], best_video['fmtsig'])
		print "[youtubeUrl] found best available video url:",video_url

	if self.callBack == None:
		return video_url
	else:
		self.callBack(video_url)
