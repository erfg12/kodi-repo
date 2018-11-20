import sys
import urllib
import urllib2,cookielib,re
import StringIO
import urlparse
import xbmc
import xbmcgui
import xbmcplugin
import HTMLParser
import xbmcaddon
import os
import json
import webbrowser

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')
__addon__        = xbmcaddon.Addon()
__addonname__    = __addon__.getAddonInfo('id')
dataroot = xbmc.translatePath('special://profile/addon_data/%s' % __addonname__ ).decode('utf-8')
cookie_file = os.path.join( dataroot,'cookies.lwp')

if not os.path.exists(dataroot):
	os.makedirs(dataroot)

def build_url(query):
	return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

if mode is None:
	response = urllib.urlopen('https://newagetv.stream/rest.api.php').read()
	data = json.loads(response)
	for i in data:
		url = build_url({'mode': 'channel', 'chanID': i['id']})
		#xbmcgui.Dialog().ok(__addonname__, str(i))
		li = xbmcgui.ListItem(i['name'], iconImage=i['icon'])
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
	
	xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'channel':
	response = urllib.urlopen('https://newagetv.stream/rest.api.php?chan=1').read()
	data = json.loads(response)
	pl=xbmc.PlayList(1)
	pl.clear()
	jumpTime = 0
	for i in data:
		if jumpTime <= 0:
			jumpTime = i['seek']
		url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=" + i['vid_id']
		pl.add(url)
	xbmc.Player().play(pl)
	xbmc.log('seeking to ' + str(jumpTime))
	#xbmc.executebuiltin("Seek(%s)" % jumpTime)
	xbmc.Player().seekTime(float(jumpTime))
