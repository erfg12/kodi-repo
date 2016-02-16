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

# REFERENCE http://hbenjamin.com/blog/2013/10/24/tutorial-yt-api/

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
	searchUrl = 'https://www.googleapis.com/youtube/v3/search'
	params = {'q': 'NewAge Soldier', 'key': 'AIzaSyC7YrCyuR9fccM3aSpGcfZhAvVynfyc53k', 'part': 'snippet', 'type': 'channel'}
	url = '%s?%s' % (searchUrl, urllib.urlencode(params))
	response = urllib.urlopen(url).read()
	data = json.loads(response)

	#print url
	#print data
	
	for i in data['items']:
		url = build_url({'mode': 'channel', 'chanID': i['id']['channelId']})
		li = xbmcgui.ListItem(i['snippet']['title'], iconImage=i['snippet']['thumbnails']['default']['url'])
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
		break

	params = {'q': 'goonnoodles', 'key': 'AIzaSyC7YrCyuR9fccM3aSpGcfZhAvVynfyc53k', 'part': 'snippet', 'type': 'channel'}
	url = '%s?%s' % (searchUrl, urllib.urlencode(params))
	response = urllib.urlopen(url).read()
	data = json.loads(response)

	for i in data['items']:
		url = build_url({'mode': 'channel', 'chanID': i['id']['channelId']})
		li = xbmcgui.ListItem(i['snippet']['title'], iconImage=i['snippet']['thumbnails']['default']['url'])
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
		break
	
	url = build_url({'mode': 'visitWebsite'})
	li = xbmcgui.ListItem('Visit NewAgeSoldier.com', iconImage='DefaultHardDisk.png')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
	
	xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'visitWebsite':
	new = 1
	url = "http://newagesoldier.com"
	webbrowser.open(url,new=new)

elif mode[0] == 'channel':

	#xbmcgui.Dialog().ok('DEBUG', grabContent[0])

	playlistUrl = 'https://www.googleapis.com/youtube/v3/playlists'
	params = {'key': 'AIzaSyC7YrCyuR9fccM3aSpGcfZhAvVynfyc53k', 'part': 'snippet', 'channelId': args['chanID'][0]}
	url = '%s?%s' % (playlistUrl, urllib.urlencode(params))
	response = urllib.urlopen(url).read()
	data = json.loads(response)

	for i in data['items']:
		PLAYLIST_ID = i['id']
		url = build_url({'mode': 'pl_info', 'plID': PLAYLIST_ID})
		li = xbmcgui.ListItem(i['snippet']['title'], iconImage=i['snippet']['thumbnails']['default']['url'])
		li.setInfo('video', { 'title': i['snippet']['title'] })
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

	xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'pl_info':

	pItemsUrl = 'https://www.googleapis.com/youtube/v3/playlistItems'
	params = {'key': 'AIzaSyC7YrCyuR9fccM3aSpGcfZhAvVynfyc53k', 'playlistId': args['plID'][0], 'part': 'snippet', 'maxResults': 50}
	url = '%s?%s' % (pItemsUrl, urllib.urlencode(params))
	res = urllib.urlopen(url).read()
	data = json.loads(res)

	#print url
	#print data

	for i in data['items']:
		vID = i['snippet']['resourceId']['videoId']
		url = build_url({'mode': 'play_video', 'videoID': vID})
		#print i['snippet']['title']
		if i['snippet']['title'] == 'Private video':
			continue
		else:
			thumb = i['snippet']['thumbnails']['default']['url']
		li = xbmcgui.ListItem(i['snippet']['title'], iconImage=thumb)
		li.setInfo('video', { 'title': i['snippet']['title'] })
		#url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=" + args['videoID'][0]
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
	xbmcplugin.endOfDirectory(addon_handle)
		#tmp['id'] = i['snippet']['resourceId']['videoId']

elif mode[0] == 'play_video':
	url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=" + args['videoID'][0]
	xbmc.Player().play(url)
