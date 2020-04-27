#!/usr/bin/env python3
import sys
import json
import argparse
import time
import requests # pip3 install requests
import boto3 # pip3 install boto3
from requests_toolbelt import MultipartEncoder # pip3 install requests_toolbelt
from os.path import expanduser
from os.path import basename

# provide abstract class functionality for Python 2 and 3
import abc
ABC = abc.ABCMeta('ABC', (object,), {})

class Base(ABC):

	# every derived class must have a base URL
	@abc.abstractproperty
	def base_url(self):
		pass

	API_VERSION = None
	# generally accepted success responses
	success_responses = [200,201,202,203,204]

	def __init__(self):
		pass

class PlayerManagement(Base):

	base_url = 'https://players.api.brightcove.com/v2/accounts/{pubid}'

	def __init__(self, oauth):
		self.__oauth = oauth

	def GetListOfPlayers(self, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlayerManagement.base_url+'/players').format(pubid=accountID)
		return requests.get(url, headers=headers)

	def GetSinglePlayer(self, accountID=None, playerID='default'):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlayerManagement.base_url+'/players/{playerid}').format(pubid=accountID, playerid=playerID)
		return requests.get(url, headers=headers)

	def CreatePlayer(self, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlayerManagement.base_url+'/players').format(pubid=accountID)
		return requests.post(url, headers=headers, data=jsonBody)

	def DeletePlayer(self, playerID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlayerManagement.base_url+'/players/{playerid}').format(pubid=accountID, playerid=playerID)
		return requests.delete(url, headers=headers)

	def PublishPlayer(self, playerID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlayerManagement.base_url+'/players/{playerid}/publish').format(pubid=accountID, playerid=playerID)
		return requests.post(url, headers=headers)

	def UpdatePlayer(self, playerID, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlayerManagement.base_url+'/players/{playerid}').format(pubid=accountID, playerid=playerID)
		return requests.patch(url, headers=headers, data=jsonBody)

class OAuth(Base):
	base_url = 'https://oauth.brightcove.com/v4/access_token'

	def __init__(self, account_id, client_id, client_secret):
		self.account_id = account_id
		self.client_id = client_id
		self.client_secret = client_secret
		self.__access_token = None
		self.__request_time = None
		self.__token_life = 240

	def __get_access_token(self):
		access_token = None
		r = requests.post(url=OAuth.base_url, params='grant_type=client_credentials', auth=(self.client_id, self.client_secret))
		if(r.status_code == 200):
			access_token = r.json().get('access_token')
			self.__request_time = time.time()

		return access_token

	def get_access_token(self):
		if(self.__access_token == None):
			self.__access_token = self.__get_access_token()
		elif( (time.time()-self.__request_time) > self.__token_life ):
			self.__access_token = self.__get_access_token()
		return self.__access_token

	def get_headers(self):
		access_token = self.get_access_token()
		headers = { 'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json' }
		return headers

class JWT(Base):

	base_url = 'https://playback-auth.api.brightcove.com/v1/accounts/{pubid}'

	def __init__(self, oauth):
		self.__oauth = oauth

	def RegisterKey(self, keyData, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (JWT.base_url+'/keys').format(pubid=accountID)
		jsonBody = '{ "value":"'+keyData+'" }'
		return requests.post(url, headers=headers, data=jsonBody)

	def ListKeys(self, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (JWT.base_url+'/keys').format(pubid=accountID)
		return requests.get(url, headers=headers)

	def GetKey(self, keyID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (JWT.base_url+'/keys/{keyid}').format(pubid=accountID,keyid=keyID)
		return requests.get(url, headers=headers)

	def DeleteKey(self, keyID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (JWT.base_url+'/keys/{keyid}').format(pubid=accountID,keyid=keyID)
		return requests.delete(url, headers=headers)

class PlaybackRights(Base):

	base_url ='https://playback-rights.api.brightcove.com/v1/accounts/{pubid}'

	def __init__(self, oauth):
		self.__oauth = oauth

	def CreatePlaybackRight(self, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlaybackRights.base_url+'/playback_rights').format(pubid=accountID)
		return requests.post(url=url, headers=headers, data=jsonBody)

	def GetPlaybackRights(self, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlaybackRights.base_url+'/playback_rights').format(pubid=accountID)
		return requests.get(url=url, headers=headers)

	def GetPlaybackRight(self, epaID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlaybackRights.base_url+'/playback_rights/{epaid}').format(pubid=accountID, epaid=epaID)
		return requests.get(url=url, headers=headers)

	def UpdatePlaybackRight(self, epaID, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlaybackRights.base_url+'/playback_rights/{epaid}').format(pubid=accountID, epaid=epaID)
		return requests.put(url=url, headers=headers, data=jsonBody)

	def DeletePlaybackRight(self, epaID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlaybackRights.base_url+'/playback_rights/{epaid}').format(pubid=accountID, epaid=epaID)
		return requests.delete(url=url, headers=headers)

	def GetAllUserDevices(self, userID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlaybackRights.base_url+'/users/{userid}/devices').format(pubid=accountID, userid=userID)
		return requests.get(url=url, headers=headers)

	def DeleteAllUserDevices(self, userID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlaybackRights.base_url+'/users/{userid}/devices').format(pubid=accountID, userid=userID)
		return requests.delete(url=url, headers=headers)

	def DeleteUserDevice(self, userID, deviceID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlaybackRights.base_url+'/users/{userid}/devices/{deviceid}').format(pubid=accountID, userid=userID, deviceid=deviceID)
		return requests.delete(url=url, headers=headers)

class DeliverySystem(Base):

	base_url = 'https://repos.api.brightcove.com/v1/accounts/{pubid}/repos'

	def __init__(self, oauth):
		self.__oauth = oauth

	def ListRepositories(self, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliverySystem.base_url).format(pubid=accountID)
		return requests.get(url=url, headers=headers)

	def GetRepositoryDetails(self, repoName, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliverySystem.base_url+'/{reponame}').format(pubid=accountID,reponame=repoName)
		return requests.get(url, headers=headers)

	def DeleteRepository(self, repoName, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliverySystem.base_url+'/{reponame}').format(pubid=accountID,reponame=repoName)
		return requests.delete(url, headers=headers)

	def CreateRepository(self, repoName, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliverySystem.base_url+'/{reponame}').format(pubid=accountID,reponame=repoName)
		return requests.put(url, headers=headers)

	def ListFilesInRepository(self, repoName, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliverySystem.base_url+'/{reponame}/files').format(pubid=accountID,reponame=repoName)
		return requests.get(url, headers=headers)

	def DeleteFileInRepository(self, repoName, fileName, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliverySystem.base_url+'/{reponame}/files/{filename}').format(pubid=accountID,reponame=repoName,filename=fileName)
		return requests.delete(url, headers=headers)

	def AddFileToRepository(self, repoName, fileName, accountID=None):
		accountID = accountID or self.__oauth.account_id
		url = (DeliverySystem.base_url+'/{reponame}/files/{filename}').format(pubid=accountID,reponame=repoName,filename=basename(fileName))
		m = MultipartEncoder( fields={'contents': (None, open(fileName, 'rb'), 'text/plain')} )
		access_token = self.__oauth.get_access_token()
		headers = { 'Authorization': 'Bearer ' + access_token, 'Content-Type': m.content_type }
		return requests.put(url, headers=headers, data=m)

class CMS(Base):
	base_url = 'https://cms.api.brightcove.com/v1/accounts/{pubid}'

	def __init__(self, oauth):
		self.__oauth = oauth

	#===========================================
	# get number of videos in an account
	#===========================================
	def GetVideoCount(self, searchQuery='', accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/count?q={query}').format(pubid=accountID,query=searchQuery)
		r = requests.get(url, headers=headers)
		if(r.status_code == 200):
			return r.json().get('count')
		return -1

	#===========================================
	# create new video object in an account
	#===========================================
	def CreateVideo(self, videoTitle='Video Title', jsonBody=None, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/').format(pubid=accountID)
		if(not jsonBody):
			jsonBody = '{"name": "' + videoTitle + '"}'
		return requests.post(url=url, headers=headers, data=jsonBody)

	#===========================================
	# get a video
	#===========================================
	def GetVideo(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}').format(pubid=accountID,videoid=videoID)
		return requests.get(url=url, headers=headers)

	#===========================================
	# get videos in an account
	#===========================================
	def GetVideos(self, pageSize=20, pageOffset=0, searchQuery='', accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		apiRequest = (CMS.base_url+'/videos?limit={pageSize}&offset={offset}&sort=created_at{query}').format(pubid=accountID, pageSize=pageSize, offset=pageOffset, query='&q=' + searchQuery)
		return requests.get(apiRequest, headers=headers)

	#===========================================
	# get a video's sources
	#===========================================
	def GetVideoSources(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/sources').format(pubid=accountID,videoid=videoID)
		return requests.get(url=url, headers=headers)

	#===========================================
	# get a video's images
	#===========================================
	def GetVideoImages(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/images').format(pubid=accountID,videoid=videoID)
		return requests.get(url=url, headers=headers)

	#===========================================
	# get a video's audio tracks
	#===========================================
	def GetVideoAudioTracks(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/audio_tracks').format(pubid=accountID,videoid=videoID)
		return requests.get(url=url, headers=headers)

	#===========================================
	# get a specific audio track
	#===========================================
	def GetVideoAudioTrack(self, videoID, trackID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/audio_tracks/{trackid}').format(pubid=accountID,videoid=videoID,trackid=trackID)
		return requests.get(url=url, headers=headers)

	#===========================================
	# delete a specific audio track
	#===========================================
	def DeleteVideoAudioTrack(self, videoID, trackID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/audio_tracks/{trackid}').format(pubid=accountID,videoid=videoID,trackid=trackID)
		return requests.delete(url=url, headers=headers)

	#===========================================
	# update a specific audio track
	#===========================================
	def UpdateVideoAudioTrack(self, videoID, trackID, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/audio_tracks/{trackid}').format(pubid=accountID,videoid=videoID,trackid=trackID)
		return requests.patch(url=url, headers=headers, data=jsonBody)

	#===========================================
	# delete a video
	#===========================================
	def DeleteVideo(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}').format(pubid=accountID,videoid=videoID)
		return requests.delete(url=url, headers=headers)

	#===========================================
	# get a digital master info
	#===========================================
	def GetDigitalMasterInfo(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/sources').format(pubid=accountID,videoid=videoID)
		return requests.get(url=url, headers=headers)

	#===========================================
	# delete a digital master
	#===========================================
	def DeleteMaster(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/digital_master').format(pubid=accountID,videoid=videoID)
		return requests.delete(url=url, headers=headers)

	#===========================================
	# update a video
	#===========================================
	def UpdateVideo(self, videoID, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}').format(pubid=accountID,videoid=videoID)
		return requests.patch(url, headers=headers, data=jsonBody)

	#===========================================
	# get custom fields
	#===========================================
	def GetCustomFields(self, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/video_fields').format(pubid=accountID)
		return requests.get(url=url, headers=headers)

	#===========================================
	# get ingest job status for a video
	#===========================================
	def GetStatusOfIngestJob(self, videoID, jobID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/ingest_jobs/{jobid}').format(pubid=accountID,videoid=videoID,jobid=jobID)
		return requests.get(url=url, headers=headers)

	#===========================================
	# get all ingest jobs status for a video
	#===========================================
	def GetStatusOfIngestJobs(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/ingest_jobs').format(pubid=accountID,videoid=videoID)
		return requests.get(url=url, headers=headers)

	#===========================================
	# variants stuff
	#===========================================
	def GetAllVideoVariants(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/variants').format(pubid=accountID,videoid=videoID)
		return requests.get(url=url, headers=headers)

	def CreateVideoVariant(self, videoID, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/variants').format(pubid=accountID,videoid=videoID)
		return requests.post(url=url, headers=headers, data=jsonBody)

	def GetVideoVariant(self, videoID, language, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/variants/{language}').format(pubid=accountID,videoid=videoID, language=language)
		return requests.get(url=url, headers=headers)

	def UpdateVideoVariant(self, videoID, language, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/variants/{language}').format(pubid=accountID,videoid=videoID, language=language)
		return requests.patch(url=url, headers=headers, data=jsonBody)

	def DeleteVideoVariant(self, videoID, language, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/variants/{language}').format(pubid=accountID,videoid=videoID, language=language)
		return requests.delete(url=url, headers=headers)

	#===========================================
	# subscriptions bla bla
	#===========================================
	def GetSubscriptionsList(self, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/subscriptions').format(pubid=accountID)
		return (requests.get(url, headers=headers))

	def GetSubscription(self, subID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/subscriptions/{subid}').format(pubid=accountID, subid=subID)
		return (requests.get(url, headers=headers))

	def CreateSubscription(self, callbackURL, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/subscriptions').format(pubid=accountID)
		jsonBody = ('{ "endpoint":"' + callbackURL + '", "events":["video-change"] }')
		return (requests.post(url, headers=headers, data=jsonBody))

	def DeleteSubscription(self, subID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/subscriptions/{subid}').format(pubid=accountID,subid=subID)
		return (requests.delete(url, headers=headers))
	
	#===========================================
	# folders stuff
	#===========================================
	def GetFolders(self, pageSize=100, pageOffset=0, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders?limit={limit}&offset={offset}').format(pubid=accountID,limit=pageSize, offset=pageOffset)
		return (requests.get(url, headers=headers))

	def CreateFolder(self, folderName, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders').format(pubid=accountID)
		jsonBody = ('{ "name":"' + folderName + '" }')
		return (requests.post(url, headers=headers, data=jsonBody))

	def DeleteFolder(self, folderID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders/{folderid}').format(pubid=accountID, folderid=folderID)
		return (requests.delete(url, headers=headers))

	def GetFolderInformation(self, folderID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders/{folderid}').format(pubid=accountID, folderid=folderID)
		return (requests.get(url, headers=headers))

	def UpdateFolderName(self, folderID, folderName, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders/{folderid}').format(pubid=accountID, folderid=folderID)
		jsonBody = ('{ "name":"' + folderName + '" }')
		return (requests.patch(url, headers=headers, data=jsonBody))

	def AddVideoToFolder(self, folderID, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders/{folderid}/videos/{videoid}').format(pubid=accountID, videoid=videoID)
		return (requests.put(url, headers=headers))

	def RemoveVideoFromFolder(self, folderID, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders/{folderid}/videos/{videoid}').format(pubid=accountID, videoid=videoID)
		return (requests.delete(url, headers=headers))

	def GetVideosInFolder(self, folderID, pageSize=100, pageOffset=0, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders/{folderid}/videos?limit={limit}&offset={offset}').format(pubid=accountID,folderid=folderID,limit=pageSize, offset=pageOffset)
		return (requests.get(url, headers=headers))

	#===========================================
	# playlists stuff
	#===========================================
	def GetPlaylistsForVideo(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/references').format(pubid=accountID, videoid=videoID)
		return (requests.get(url, headers=headers))

	def RemoveVideoFromAllPlaylists(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/references').format(pubid=accountID, videoid=videoID)
		return (requests.delete(url, headers=headers))

	def GetVideosInPlaylist(self, playlistID, includeDetails=True, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/playlists/{playlistid}/videos?include_details={details}').format(pubid=accountID, playlistid=playlistID, details=('false','true')[includeDetails])
		print(url)
		return (requests.get(url, headers=headers))

	def GetVideoCountInPlaylist(self, playlistID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/counts/playlists/{playlistid}/videos').format(pubid=accountID, playlistid=playlistID)
		return (requests.get(url, headers=headers))

	def DeletePlaylist(self, playlistID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/playlists/{playlistid}').format(pubid=accountID, playlistid=playlistID)
		return (requests.delete(url, headers=headers))

	def UpdatePlaylist(self, playlistID, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/playlists/{playlistid}').format(pubid=accountID, playlistid=playlistID)
		return (requests.patch(url, headers=headers, data=jsonBody))

	def GetPlaylistByID(self, playlistID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/playlists/{playlistid}').format(pubid=accountID, playlistid=playlistID)
		return (requests.get(url, headers=headers))

	def GetPlaylistCount(self, searchQuery='', accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		if(searchQuery != ''):
			searchQuery = requests.utils.quote(searchQuery)
		url = (CMS.base_url+'/counts/playlists?q={query}').format(pubid=accountID, query=searchQuery)
		return (requests.get(url, headers=headers))

	def GetPlaylists(self, sort='-updated_at', searchQuery='', pageSize=100, pageOffset=0, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		if sort not in ['name', 'reference_id', 'created_at', 'published_at', 'updated_at', 'schedule.starts_at', 'schedule.ends_at', 'state', 'plays_total', 'plays_trailing_week', '-name', '-reference_id', '-created_at', '-published_at', '-updated_at', '-schedule.starts_at', '-schedule.ends_at', '-state', '-plays_total', '-plays_trailing_week']:
			sort = '-updated_at'

		if(searchQuery != ''):
			searchQuery = requests.utils.quote(searchQuery)

		url = (CMS.base_url+'/playlists?limit={limit}&offset={offset}&sort={sort}&q={query}').format(pubid=accountID, limit=pageSize, offset=pageOffset, sort=sort, query=searchQuery)
		return (requests.get(url, headers=headers))

	def CreatePlaylist(self, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/playlists').format(pubid=accountID)
		return (requests.post(url, headers=headers, data=jsonBody))

class DynamicIngest(Base):

	base_url = 'https://ingestion.api.brightcove.com/v1/accounts/{pubid}'

	def __init__(self, oAuth, ingestProfile=None, priorityQueue=None):
		self.__oauth = oAuth
		self.SetIngestProfile(ingestProfile)
		self.SetPriorityQueue(priorityQueue)

	def SetIngestProfile(self, profileID):
		if(self.ProfileExists(accountID=self.__oauth.account_id, profileID=profileID)):
			self.__ingestProfile = profileID
		else:
			self.__ingestProfile = None
		return self.__ingestProfile
	
	def SetPriorityQueue(self, priorityQueue):
		if(priorityQueue in ['low', 'normal', 'high']):
			self.__priorityQueue = priorityQueue
		else:
			self.__priorityQueue = None
		return self.__priorityQueue

	def GetDefaultProfiles(self, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DynamicIngest.base_url+'/configuration').format(pubid=accountID)
		return requests.get(url=url, headers=headers)
	
	def GetProfile(self, profileID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DynamicIngest.base_url+'/profiles/{profileid}').format(pubid=accountID, profileid=profileID)
		return requests.get(url=url, headers=headers)

	def ProfileExists(self, profileID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		r = self.GetProfile(accountID=accountID, profileID=profileID)
		if(r.status_code in DynamicIngest.success_responses):
			return True
		else:
			return False
	
	def RetranscodeVideo(self, videoID, profileID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		if(self.ProfileExists(accountID=accountID, profileID=profileID) is False):
			return None
		headers = self.__oauth.get_headers()
		url = ('https://ingest.api.brightcove.com/v1/accounts/{pubid}/videos/{videoid}/ingest-requests').format(pubid=accountID, videoid=videoID)
		data =	'{ "profile":"'+profileID+'", "master": { "use_archived_master": true } }'
		return requests.post(url=url, headers=headers, data=data)

	def SubmitIngest(self, videoID, sourceURL, priorityQueue=None, callBacks=None, ingestProfile=None, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		profile = ''
		priority = 'normal'

		if(ingestProfile is not None):
			profile = ingestProfile
		elif(self.__ingestProfile is None):
			r = self.GetDefaultProfiles(accountID=accountID)
			if r.status_code in DynamicIngest.success_responses:
				profile = r.json()['default_profile_id']
		else:
			profile = self.__ingestProfile

		if(priorityQueue is not None):
			priority = priorityQueue
		elif(self.__priorityQueue is not None):
			priority = self.__priorityQueue

		url = ('https://ingest.api.brightcove.com/v1/accounts/{pubid}/videos/{videoid}/ingest-requests').format(pubid=accountID, videoid=videoID)
		data =	'{ "profile":"'+profile+'", "master": { "url": "'+sourceURL+'" }, "priority": "'+priority+'" }'
		return requests.post(url=url, headers=headers, data=data)

	# get_upload_location_and_upload_file first performs an authenticated request to discover
	# a Brightcove-provided location to securely upload a source file
	def UploadFile(self, videoID, fileName, callBack=None, accountID=None):
		accountID = accountID or self.__oauth.account_id
		# Perform an authorized request to obtain a file upload location
		url = ('https://cms.api.brightcove.com/v1/accounts/{pubid}/videos/{videoid}/upload-urls/{sourcefilename}').format(pubid=accountID, videoid=videoID, sourcefilename=fileName)
		r = requests.get(url=url, headers=self.__oauth.get_headers())
		if(r.status_code in DynamicIngest.success_responses):
			upload_urls_response = r.json()
		else:
			return None

		try:
			# Upload the contents of our local file to the location provided us
			# This example uses the boto3 library to perform a multipart upload
			# This is the recommended method for uploading large source files
			s3 = boto3.resource('s3',
				aws_access_key_id=upload_urls_response['access_key_id'],
				aws_secret_access_key=upload_urls_response['secret_access_key'],
				aws_session_token=upload_urls_response['session_token'])
			
			def emptyCB(muu):
				pass

			if(callBack is None):
				callBack = emptyCB

			s3.Object(upload_urls_response['bucket'], upload_urls_response['object_key']).upload_file(fileName, Callback=callBack)
			return upload_urls_response
		except Exception as e:
			print (e)
			return None

#===========================================
# read account info from JSON file
#===========================================
def GetAccountInfo(input_filename=None):
	# if no config file was passed we use the default
	if(not input_filename):
		input_filename = expanduser('~')+'/account_info.json'

	# open the config file
	try:
		myfile = open(input_filename, 'r')
	except:
		print(('Error: unable to open {filename}').format(filename=input_filename))
		return None, None, None, None

	# read and parse config file
	obj = json.loads( myfile.read() )

	# grab data, make it strings and strip it
	account = obj.get('account_id')
	if(account):
		account = str(account).strip()

	client = obj.get('client_id')
	if(client):
		client = str(client).strip()

	secret = obj.get('client_secret')
	if(secret):
		secret = str(secret).strip()

	# return the object just in case it's needed later
	return(account, client, secret, obj)

#===========================================
# default processing function
#===========================================
def list_videos(video):
	print(video['id']+', "'+video['name']+'"')

#===========================================
# this is the main loop to process videos
#===========================================
def process_video(inputfile, processVideo=list_videos, searchQuery=None, vidID=None):
	global oauth
	global cms
	global opts
	# get the account info and credentials
	accountID,b,c,opts = GetAccountInfo(inputfile)

	if(None in [accountID,b,c,opts]):
		return False
	
	oauth = OAuth(accountID,b,c)
	cms = CMS(oauth)

	# check if we should process a specific video ID
	if(vidID):
		print(('Processing video ID {videoid} now.').format(videoid=vidID))
		video = cms.GetVideo(accountID=accountID, videoID=vidID)
		if(video.status_code in CMS.success_responses):
			processVideo(video.json())
			return True
		else:
			print(('Error getting information for video ID {videoid}.').format(videoid=vidID))
			return False

	# check if we should process a given list of videos
	videoList = opts.get('video_ids')
	if(videoList and videoList[0] != 'all'):
		print(('Found {numVideos} videos in options file. Processing them now.').format(numVideos=len(videoList)))
		for videoID in videoList:
			#if(videoID=='all'): # not needed?
			#	continue
			video = cms.GetVideo(accountID=accountID, videoID=videoID)
			if(video.status_code in CMS.success_responses):
				processVideo(video.json())
			else:
				print(('Error getting information for video ID {videoid}.').format(videoid=videoID))

		return True

	# if a query was passed along URI encode it
	if(not searchQuery):
		searchQuery = ''
	else:
		searchQuery = requests.utils.quote(searchQuery)

	# ok, let's process all videos
	# get number of videos in account
	numVideos = cms.GetVideoCount(searchQuery=searchQuery)

	if(numVideos>0):
		print(('Found {numVideos} videos in library. Processing them now.').format(numVideos=numVideos))
	else:
		print(('No videos found in account ID {pubid}''s library.').format(pubid=oauth.account_id))
		return False

	currentOffset = 0
	pageSize = 20
	retries = 10

	while(currentOffset<numVideos):
		r = cms.GetVideos(pageSize=pageSize, pageOffset=currentOffset, searchQuery=searchQuery)
		# good result
		if (r.status_code in [200,202]):
			json_data = json.loads(r.text)
			# make sure we actually got some data
			if(len(json_data) > 0):
				for video in json_data:
					processVideo(video)
				retries = 10
				currentOffset += pageSize
			# looks like we got an empty response (it can happen)
			else:
				if(retries>0):
					print('Error: empty API response received.')
					for remaining in range(10, 0, -1):
						sys.stdout.write('\rRetrying in {:2d} seconds.'.format(remaining))
						sys.stdout.flush()
						time.sleep(1)

					retries -= 1
					sys.stdout.write('\rRetrying now ({retries} retries left).\n'.format(retries))

				else:
					print('Error: failed to get non-empty API response.')
					return False

		# token probably expired
		elif(r.status_code == 401):
			if(retries>0):
				retries -= 1
			else:
				print('Error: possible problem with OAuth token:')
				print(r.content)
				return False

		# we received an unexpected status code, let's get out of here
		else:
			print('Error: Received unexpected status code {status}:'.format(r.status_code))
			print(r.json())
			return False

	return True

#===========================================
# parse args and do the thing
#===========================================
def main(process_func):
	# init the argument parsing
	parser = argparse.ArgumentParser(prog=sys.argv[0])
	parser.add_argument('-i', type=str, help='Name and path of account config information file')
	parser.add_argument('-q', type=str, help='CMS API search query')
	parser.add_argument('-v', type=str, help='Specific video ID to process')

	# parse the args
	args = parser.parse_args()

	# go through the library and do stuff
	process_video(inputfile=args.i, processVideo=process_func, searchQuery=args.q, vidID=args.v)

#===========================================
# only run code if it's not imported
#===========================================

# disable certificate warnings
requests.urllib3.disable_warnings()

if __name__ == '__main__':
	main(list_videos)
