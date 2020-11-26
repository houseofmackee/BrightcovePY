#!/usr/bin/env python3
from __future__ import print_function
import sys
import csv
import json
import argparse
import time
import queue
import logging
import functools
import pandas
from typing import Callable, Tuple
import requests # pip3 install requests
import boto3 # pip3 install boto3
from threading import Thread
from requests_toolbelt import MultipartEncoder # pip3 install requests_toolbelt
from os.path import expanduser, basename
from abc import ABC, abstractproperty

# disable certificate warnings
requests.urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()

# some globals
oauth = None

# funtion to print to stderr
def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

# decorator for static variables
def static_vars(**kwargs):
	def decorate(func):
		for k in kwargs:
			setattr(func, k, kwargs[k])
		return func
	return decorate

class Base(ABC):

	# every derived class must have a base URL
	@abstractproperty
	def base_url(self):
		pass

	API_VERSION = None
	# generally accepted success responses
	success_responses = [200,201,202,203,204]

	def __init__(self, query=None):
		self.search_query = query
		self.__session = self.__get_session()

	def __get_session(self)  -> requests.Session:
		sess = requests.Session()
		adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
		sess.mount('https://', adapter)
		return sess

	@property
	def search_query(self) -> str:
		return self.__search_query
	
	@search_query.setter
	def search_query(self, query: str):
		self.__search_query = '' if not query else requests.utils.quote(query)

	@property
	def session(self) -> requests.Session:
		return self.__session


class DeliveryRules(Base):
	base_url = 'https://delivery-rules.api.brightcove.com/accounts/{pubid}'

	def __init__(self, oauth):
		self.__oauth = oauth

	def DeliveryRulesEnabled(self, accountID=None):
		return (self.GetDeliveryRules(accountID=accountID).status_code == 200)

	def GetDeliveryRules(self, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliveryRules.base_url).format(pubid=accountID)
		return requests.get(url, headers=headers)

	def GetConditions(self, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliveryRules.base_url+'/conditions').format(pubid=accountID)
		return requests.get(url, headers=headers)

	def UpdateConditions(self, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliveryRules.base_url+'/conditions').format(pubid=accountID)
		return requests.put(url, headers=headers, data=jsonBody)

	def GetActions(self, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliveryRules.base_url+'/actions').format(pubid=accountID)
		return requests.get(url, headers=headers)

	def GetSpecificAction(self, actionID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliveryRules.base_url+'/actions/{action_id}').format(pubid=accountID, action_id=actionID)
		return requests.get(url, headers=headers)

	def CreateAction(self, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliveryRules.base_url+'/actions').format(pubid=accountID)
		return requests.post(url, headers=headers, data=jsonBody)

	def UpdateAction(self, actionID, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliveryRules.base_url+'/actions/{action_id}').format(pubid=accountID, action_id=actionID)
		return requests.put(url, headers=headers, data=jsonBody)

	def DeleteAction(self, actionID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliveryRules.base_url+'/actions/{action_id}').format(pubid=accountID, action_id=actionID)
		return requests.delete(url, headers=headers)

class Social(Base):

	base_url = 'https://edge.social.api.brightcove.com/v1/accounts/{pubid}'

	def __init__(self, oauth, query=None):
		super().__init__(query)
		self.__oauth = oauth

	def ListStatusForVideos(self, searchQuery=None, accountID=None):
		accountID = accountID or self.__oauth.account_id
		searchQuery = searchQuery or self.search_query
		headers = self.__oauth.get_headers()
		url = (Social.base_url+'/videos/status?{query_string}').format(pubid=accountID, query_string=searchQuery)
		return requests.get(url, headers=headers)

	def ListStatusForVideo(self, videoID, searchQuery=None, accountID=None):
		accountID = accountID or self.__oauth.account_id
		searchQuery = searchQuery or self.search_query
		headers = self.__oauth.get_headers()
		url = (Social.base_url+'/videos/{video_id}/status?{query_string}').format(pubid=accountID, video_id=videoID, query_string=searchQuery)
		return requests.get(url, headers=headers)

	def ListHistoryForVideos(self, searchQuery=None, accountID=None):
		accountID = accountID or self.__oauth.account_id
		searchQuery = searchQuery or self.search_query
		headers = self.__oauth.get_headers()
		url = (Social.base_url+'/videos/history?{query_string}').format(pubid=accountID, query_string=searchQuery)
		return requests.get(url, headers=headers)

	def ListHistoryForVideo(self, videoID, searchQuery=None, accountID=None):
		accountID = accountID or self.__oauth.account_id
		searchQuery = searchQuery or self.search_query
		headers = self.__oauth.get_headers()
		url = (Social.base_url+'/videos/{video_id}/history?{query_string}').format(pubid=accountID, video_id=videoID, query_string=searchQuery)
		return requests.get(url, headers=headers)

class SocialSyndication(Base):

	base_url = 'https://social.api.brightcove.com/v1/accounts/{pubid}/mrss/syndications'

	def __init__(self, oauth):
		self.__oauth = oauth

	def GetAllSyndications(self, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (SocialSyndication.base_url).format(pubid=accountID)
		return requests.get(url, headers=headers)

	def GetSyndication(self, syndicationID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (SocialSyndication.base_url+'/{syndicationid}').format(pubid=accountID, syndicationid=syndicationID)
		return requests.get(url, headers=headers)

	def CreateSyndication(self, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (SocialSyndication.base_url).format(pubid=accountID)
		return requests.post(url, headers=headers, data=jsonBody)

	def DeleteSyndication(self, syndicationID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (SocialSyndication.base_url+'/{syndicationid}').format(pubid=accountID, syndicationid=syndicationID)
		return requests.delete(url, headers=headers)

	def UpdateSyndication(self, syndicationID, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (SocialSyndication.base_url+'/{syndicationid}').format(pubid=accountID, syndicationid=syndicationID)
		return requests.patch(url, headers=headers, data=jsonBody)

	def GetTemplate(self, syndicationID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (SocialSyndication.base_url+'/{syndicationid}/template').format(pubid=accountID, syndicationid=syndicationID)
		return requests.get(url, headers=headers)

	def UploadTemplate(self, syndicationID, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (SocialSyndication.base_url+'/{syndicationid}/template').format(pubid=accountID, syndicationid=syndicationID)
		return requests.put(url, headers=headers, data=jsonBody)

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

	def GetPlayerConfiguration(self, playerID, branch, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlayerManagement.base_url+'/players/{playerid}/configuration/{branch}').format(pubid=accountID, playerid=playerID, branch=branch)
		return requests.get(url, headers=headers)

	def UpdatePlayerConfiguration(self, playerID, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlayerManagement.base_url+'/players/{playerid}/configuration').format(pubid=accountID, playerid=playerID)
		return requests.patch(url, headers=headers, data=jsonBody)

	def GetAllPlugins(self, templateVersion=None):
		headers = self.__oauth.get_headers()
		if templateVersion:
			query = '?template_version='+templateVersion
		else:
			query = ''
		url = 'https://players.api.brightcove.com/v2/plugins'+query
		return requests.get(url, headers=headers)

	def GetSinglePlugin(self, pluginID):
		headers = self.__oauth.get_headers()
		if pluginID:
			pluginID = pluginID.replace('@', '%40')
			pluginID = pluginID.replace('/', '%2F')
		else:
			pluginID = ''
		url = 'https://players.api.brightcove.com/v2/plugins/'+pluginID
		return requests.get(url, headers=headers)

	def GetAllEmbeds(self, playerID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlayerManagement.base_url+'/players/{playerid}/embeds').format(pubid=accountID, playerid=playerID)
		return requests.get(url, headers=headers)

	def GetEmbed(self, playerID, embedID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlayerManagement.base_url+'/players/{playerid}/embeds/{embedid}').format(pubid=accountID, playerid=playerID, embedid=embedID)
		return requests.get(url, headers=headers)

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

	def __init__(self, oauth:OAuth, query:str=None):
		super().__init__(query)
		self.__oauth = oauth

	#===========================================
	# get who created a video
	#===========================================
	@staticmethod
	def GetCreatedBy(video:dict) -> str:
		creator = 'Unknown'
		if(video):
			createdBy = video.get('created_by')
			if(createdBy):
				ctype = createdBy.get('type')
				if(ctype=='api_key'):
					creator = 'API'
				elif (ctype=='user'):
					creator = createdBy.get('email')
		return(creator)

	#===========================================
	# get number of videos in an account
	#===========================================
	def GetVideoCount(self, searchQuery=None, accountID=None):
		accountID = accountID or self.__oauth.account_id
		searchQuery = searchQuery or self.search_query
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/count?q={query}').format(pubid=accountID,query=searchQuery)
		r = self.session.get(url, headers=headers)
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
		return self.session.post(url=url, headers=headers, data=jsonBody)

	#===========================================
	# get a video
	#===========================================
	def GetVideo(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}').format(pubid=accountID,videoid=videoID)
		return self.session.get(url=url, headers=headers)

	#===========================================
	# get videos in an account
	#===========================================
	def GetVideos(self, pageSize=20, pageOffset=0, searchQuery=None, accountID=None):
		accountID = accountID or self.__oauth.account_id
		searchQuery = searchQuery or self.search_query
		headers = self.__oauth.get_headers()
		apiRequest = (CMS.base_url+'/videos?limit={pageSize}&offset={offset}&sort=created_at{query}').format(pubid=accountID, pageSize=pageSize, offset=pageOffset, query='&q=' + searchQuery)
		return self.session.get(apiRequest, headers=headers)

	#===========================================
	# get light version of videos in an account
	#===========================================
	def GetLightVideos(self, pageSize=20, pageOffset=0, searchQuery=None, accountID=None):
		accountID = accountID or self.__oauth.account_id
		searchQuery = searchQuery or self.search_query
		headers = self.__oauth.get_headers()
		apiRequest = (CMS.base_url+'/lightvideos?limit={pageSize}&offset={offset}&sort=created_at{query}').format(pubid=accountID, pageSize=pageSize, offset=pageOffset, query='&q=' + searchQuery)
		return self.session.get(apiRequest, headers=headers)

	#===========================================
	# get a video's sources
	#===========================================
	def GetVideoSources(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/sources').format(pubid=accountID,videoid=videoID)
		return self.session.get(url=url, headers=headers)

	#===========================================
	# get a video's images
	#===========================================
	def GetVideoImages(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/images').format(pubid=accountID,videoid=videoID)
		return self.session.get(url=url, headers=headers)

	#===========================================
	# get a video's audio tracks
	#===========================================
	def GetVideoAudioTracks(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/audio_tracks').format(pubid=accountID,videoid=videoID)
		return self.session.get(url=url, headers=headers)

	#===========================================
	# get a specific audio track
	#===========================================
	def GetVideoAudioTrack(self, videoID, trackID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/audio_tracks/{trackid}').format(pubid=accountID,videoid=videoID,trackid=trackID)
		return self.session.get(url=url, headers=headers)

	#===========================================
	# delete a specific audio track
	#===========================================
	def DeleteVideoAudioTrack(self, videoID, trackID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/audio_tracks/{trackid}').format(pubid=accountID,videoid=videoID,trackid=trackID)
		return self.session.delete(url=url, headers=headers)

	#===========================================
	# update a specific audio track
	#===========================================
	def UpdateVideoAudioTrack(self, videoID, trackID, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/audio_tracks/{trackid}').format(pubid=accountID,videoid=videoID,trackid=trackID)
		return self.session.patch(url=url, headers=headers, data=jsonBody)

	#===========================================
	# delete a video
	#===========================================
	def DeleteVideo(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}').format(pubid=accountID,videoid=videoID)
		return self.session.delete(url=url, headers=headers)

	#===========================================
	# get a digital master info
	#===========================================
	def GetDigitalMasterInfo(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/digital_master').format(pubid=accountID,videoid=videoID)
		return self.session.get(url=url, headers=headers)

	#===========================================
	# delete a digital master
	#===========================================
	def DeleteMaster(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/digital_master').format(pubid=accountID,videoid=videoID)
		return self.session.delete(url=url, headers=headers)

	#===========================================
	# update a video
	#===========================================
	def UpdateVideo(self, videoID, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}').format(pubid=accountID,videoid=videoID)
		return self.session.patch(url, headers=headers, data=jsonBody)

	#===========================================
	# get custom fields
	#===========================================
	def GetCustomFields(self, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/video_fields').format(pubid=accountID)
		return self.session.get(url=url, headers=headers)

	#===========================================
	# get ingest job status for a video
	#===========================================
	def GetStatusOfIngestJob(self, videoID, jobID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/ingest_jobs/{jobid}').format(pubid=accountID,videoid=videoID,jobid=jobID)
		return self.session.get(url=url, headers=headers)

	#===========================================
	# get all ingest jobs status for a video
	#===========================================
	def GetStatusOfIngestJobs(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/ingest_jobs').format(pubid=accountID,videoid=videoID)
		return self.session.get(url=url, headers=headers)

	#===========================================
	# variants stuff
	#===========================================
	def GetAllVideoVariants(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/variants').format(pubid=accountID,videoid=videoID)
		return self.session.get(url=url, headers=headers)

	def CreateVideoVariant(self, videoID, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/variants').format(pubid=accountID,videoid=videoID)
		return self.session.post(url=url, headers=headers, data=jsonBody)

	def GetVideoVariant(self, videoID, language, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/variants/{language}').format(pubid=accountID,videoid=videoID, language=language)
		return self.session.get(url=url, headers=headers)

	def UpdateVideoVariant(self, videoID, language, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/variants/{language}').format(pubid=accountID,videoid=videoID, language=language)
		return self.session.patch(url=url, headers=headers, data=jsonBody)

	def DeleteVideoVariant(self, videoID, language, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/variants/{language}').format(pubid=accountID,videoid=videoID, language=language)
		return self.session.delete(url=url, headers=headers)

	#===========================================
	# subscriptions bla bla
	#===========================================
	def GetSubscriptionsList(self, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/subscriptions').format(pubid=accountID)
		return (self.session.get(url, headers=headers))

	def GetSubscription(self, subID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/subscriptions/{subid}').format(pubid=accountID, subid=subID)
		return (self.session.get(url, headers=headers))

	def CreateSubscription(self, callbackURL, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/subscriptions').format(pubid=accountID)
		jsonBody = ('{ "endpoint":"' + callbackURL + '", "events":["video-change"] }')
		return (self.session.post(url, headers=headers, data=jsonBody))

	def DeleteSubscription(self, subID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/subscriptions/{subid}').format(pubid=accountID,subid=subID)
		return (self.session.delete(url, headers=headers))
	
	#===========================================
	# folders stuff
	#===========================================
	def GetFolders(self, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders').format(pubid=accountID)
		return (self.session.get(url, headers=headers))

	def CreateFolder(self, folderName, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders').format(pubid=accountID)
		jsonBody = ('{ "name":"' + folderName + '" }')
		return (self.session.post(url, headers=headers, data=jsonBody))

	def DeleteFolder(self, folderID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders/{folderid}').format(pubid=accountID, folderid=folderID)
		return (self.session.delete(url, headers=headers))

	def GetFolderInformation(self, folderID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders/{folderid}').format(pubid=accountID, folderid=folderID)
		return (self.session.get(url, headers=headers))

	def UpdateFolderName(self, folderID, folderName, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders/{folderid}').format(pubid=accountID, folderid=folderID)
		jsonBody = ('{ "name":"' + folderName + '" }')
		return (self.session.patch(url, headers=headers, data=jsonBody))

	def AddVideoToFolder(self, folderID, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders/{folderid}/videos/{videoid}').format(pubid=accountID, videoid=videoID)
		return (self.session.put(url, headers=headers))

	def RemoveVideoFromFolder(self, folderID, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders/{folderid}/videos/{videoid}').format(pubid=accountID, videoid=videoID)
		return (self.session.delete(url, headers=headers))

	def GetVideosInFolder(self, folderID, pageSize=100, pageOffset=0, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders/{folderid}/videos?limit={limit}&offset={offset}').format(pubid=accountID,folderid=folderID,limit=pageSize, offset=pageOffset)
		return (self.session.get(url, headers=headers))

	#===========================================
	# playlists stuff
	#===========================================
	def GetPlaylistsForVideo(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/references').format(pubid=accountID, videoid=videoID)
		return (self.session.get(url, headers=headers))

	def RemoveVideoFromAllPlaylists(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/references').format(pubid=accountID, videoid=videoID)
		return (self.session.delete(url, headers=headers))

	def GetVideosInPlaylist(self, playlistID, includeDetails=True, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/playlists/{playlistid}/videos?include_details={details}').format(pubid=accountID, playlistid=playlistID, details=('false','true')[includeDetails])
		return (self.session.get(url, headers=headers))

	def GetVideoCountInPlaylist(self, playlistID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/counts/playlists/{playlistid}/videos').format(pubid=accountID, playlistid=playlistID)
		return (self.session.get(url, headers=headers))

	def DeletePlaylist(self, playlistID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/playlists/{playlistid}').format(pubid=accountID, playlistid=playlistID)
		return (self.session.delete(url, headers=headers))

	def UpdatePlaylist(self, playlistID, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/playlists/{playlistid}').format(pubid=accountID, playlistid=playlistID)
		return (self.session.patch(url, headers=headers, data=jsonBody))

	def GetPlaylistByID(self, playlistID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/playlists/{playlistid}').format(pubid=accountID, playlistid=playlistID)
		return (self.session.get(url, headers=headers))

	def GetPlaylistCount(self, searchQuery=None, accountID=None):
		accountID = accountID or self.__oauth.account_id
		searchQuery = searchQuery or self.search_query
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/counts/playlists?q={query}').format(pubid=accountID, query=searchQuery)
		return (self.session.get(url, headers=headers))

	def GetPlaylists(self, sort='-updated_at', searchQuery=None, pageSize=100, pageOffset=0, accountID=None):
		accountID = accountID or self.__oauth.account_id
		searchQuery = searchQuery or self.search_query
		headers = self.__oauth.get_headers()
		if sort not in ['name', 'reference_id', 'created_at', 'published_at', 'updated_at', 'schedule.starts_at', 'schedule.ends_at', 'state', 'plays_total', 'plays_trailing_week', '-name', '-reference_id', '-created_at', '-published_at', '-updated_at', '-schedule.starts_at', '-schedule.ends_at', '-state', '-plays_total', '-plays_trailing_week']:
			sort = '-updated_at'
		url = (CMS.base_url+'/playlists?limit={limit}&offset={offset}&sort={sort}&q={query}').format(pubid=accountID, limit=pageSize, offset=pageOffset, sort=sort, query=searchQuery)
		return (self.session.get(url, headers=headers))

	def CreatePlaylist(self, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/playlists').format(pubid=accountID)
		return (self.session.post(url, headers=headers, data=jsonBody))

	#===========================================
	# Assets stuff
	#===========================================
	def GetDynamicRenditions(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/assets/dynamic_renditions').format(pubid=accountID, videoid=videoID)
		return (self.session.get(url, headers=headers))

	def GetRenditionList(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/assets/renditions').format(pubid=accountID, videoid=videoID)
		return (self.session.get(url, headers=headers))

class EPG(Base):
	base_url ='https://cm.cloudplayout.brightcove.com/accounts/{account_id}'

	def __init__(self, oAuth, query=None) -> None:
		super().__init__(query)
		self.__oauth = oAuth

	def GetAllCPChannels(self, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (EPG.base_url+'/cp_channels').format(account_id=account_id)
		return requests.get(url=url, headers=headers)

	def GetEPG(self, channel_id, query=None, account_id=None):
		# https://sm.cloudplayout.brightcove.com/accounts/{account_id}/channels/{channel_id}/epg
		query = query or self.search_query
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (EPG.base_url+'/channels/{channel_id}/epg?{query}').format(account_id=account_id, channel_id=channel_id, query=query)
		return requests.get(url=url, headers=headers)

class XDR(Base):

	base_url = 'https://data.brightcove.com/v1/xdr/accounts/{pubid}'

	def __init__(self, oAuth):
		self.__oauth = oAuth

	def GetViewerPlayheads(self, viewerID, limit=1000, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		limit = 1000 if (limit>10000 or limit<1) else limit
		url = (XDR.base_url+'/playheads/{viewerid}?limit={limit}').format(pubid=accountID, viewerid=viewerID, limit=limit)
		return requests.get(url=url, headers=headers)

	def GetViewerVideoPlayheads(self, viewerID, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (XDR.base_url+'/playheads/{viewerid}/{videoid}').format(pubid=accountID, viewerid=viewerID, videoid=videoID)
		return requests.get(url=url, headers=headers)

class IngestProfiles(Base):

	base_url = 'https://ingestion.api.brightcove.com/v1/accounts/{pubid}'

	def __init__(self, oAuth):
		super().__init__()
		self.__oauth = oAuth
		# cache for ProfileExists
		self.__previousProfile = None
		self.__previousAccount = None
		# cache for GetDefaultProfile
		self.__defaultProfileResponse = None
		self.__defaultProfileAccount = None
		# cache for GetProfile
		self.__getProfileAccount = None
		self.__getProfileID = None
		self.__getProfileResponse = None

	def GetDefaultProfile(self, accountID=None):
		accountID = accountID or self.__oauth.account_id
		# if it's not the same as before then find it and cache it
		if(accountID != self.__defaultProfileAccount):
			headers = self.__oauth.get_headers()
			url = (IngestProfiles.base_url+'/configuration').format(pubid=accountID)
			self.__defaultProfileResponse = self.session.get(url=url, headers=headers)
			self.__defaultProfileAccount = accountID
		# return cached response
		return self.__defaultProfileResponse
	
	def GetIngestProfile(self, profileID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		# if it's not the same as before then find it and cache it
		if(self.__getProfileAccount != accountID or self.__getProfileID != profileID):
			headers = self.__oauth.get_headers()
			url = (IngestProfiles.base_url+'/profiles/{profileid}').format(pubid=accountID, profileid=profileID)
			self.__getProfileID = profileID
			self.__getProfileAccount = accountID
			self.__getProfileResponse = self.session.get(url=url, headers=headers)
		# return cached response
		return self.__getProfileResponse

	def ProfileExists(self, profileID, accountID=None):
		accountID = accountID or self.__oauth.account_id

		# check if it's a valid cached account/profile combo
		if(self.__previousProfile == profileID and self.__previousAccount == accountID):
			return True

		r = self.GetIngestProfile(accountID=accountID, profileID=profileID)
		if(r.status_code in IngestProfiles.success_responses):
			self.__previousProfile = profileID
			self.__previousAccount = accountID
			return True
		else:
			return False

	def UpdateDefaultProfile(self, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		self.__previousProfile = None
		self.__previousAccount = None
		headers = self.__oauth.get_headers()
		url = (IngestProfiles.base_url+'/configuration').format(pubid=accountID)
		return self.session.put(url=url, headers=headers, data=jsonBody)

	def SetDefaultProfile(self, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		self.__previousProfile = None
		self.__previousAccount = None
		headers = self.__oauth.get_headers()
		url = (IngestProfiles.base_url+'/configuration').format(pubid=accountID)
		return self.session.post(url=url, headers=headers, data=jsonBody)

	def DeleteIngestProfile(self, profileID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		self.__previousProfile = None
		self.__previousAccount = None
		headers = self.__oauth.get_headers()
		url = (IngestProfiles.base_url+'/profiles/{profileid}').format(pubid=accountID,profileid=profileID)
		return self.session.delete(url=url, headers=headers)

	def UpdateIngestProfile(self, profileID, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		self.__previousProfile = None
		self.__previousAccount = None
		headers = self.__oauth.get_headers()
		url = (IngestProfiles.base_url+'/profiles/{profileid}').format(pubid=accountID,profileid=profileID)
		return self.session.put(url=url, headers=headers, data=jsonBody)

	def CreateIngestProfile(self, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (IngestProfiles.base_url+'/profiles').format(pubid=accountID)
		return self.session.post(url=url, headers=headers, data=jsonBody)

	def GetAllIngestProfiles(self, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (IngestProfiles.base_url+'/profiles').format(pubid=accountID)
		return self.session.get(url=url, headers=headers)

class DynamicIngest(Base):

	base_url = 'https://ingest.api.brightcove.com/v1/accounts/{pubid}'

	def __init__(self, oAuth, ingestProfile=None, priorityQueue='normal'):
		super().__init__()
		self.__oauth = oAuth
		self.__previousProfile = None
		self.__previousAccount = None
		self.__ingestProfile = None
		self.__priorityQueue = priorityQueue
		self.__ip = IngestProfiles(oAuth)
		self.SetIngestProfile(ingestProfile)
		self.SetPriorityQueue(priorityQueue)

	def SetIngestProfile(self, profileID):
		if(self.__ip.ProfileExists(accountID=self.__oauth.account_id, profileID=profileID)):
			self.__ingestProfile = profileID
		else:
			self.__ingestProfile = None
		return self.__ingestProfile
	
	def SetPriorityQueue(self, priorityQueue):
		if(priorityQueue in ['low', 'normal', 'high']):
			self.__priorityQueue = priorityQueue
		else:
			self.__priorityQueue = 'normal'
		return self.__priorityQueue
	
	def RetranscodeVideo(self, videoID, profileID=None, captureImages=True, priorityQueue=None, accountID=None):
		accountID = accountID or self.__oauth.account_id

		profile = self.__ingestProfile
		if(profileID and self.__ip.ProfileExists(accountID=accountID, profileID=profileID)):
			profile = profileID
		elif(self.__ingestProfile is None):
			r = self.__ip.GetDefaultProfile(accountID=accountID)
			if r.status_code in DynamicIngest.success_responses:
				profile = r.json().get('default_profile_id')

		priority = priorityQueue or self.__priorityQueue

		headers = self.__oauth.get_headers()
		url = (DynamicIngest.base_url+'/videos/{videoid}/ingest-requests').format(pubid=accountID, videoid=videoID)
		data =	'{ "profile":"'+profile+'", "master": { "use_archived_master": true }, "priority": "'+priority+'","capture-images": '+str(captureImages).lower()+' }'
		return self.session.post(url=url, headers=headers, data=data)

	def SubmitIngest(self, videoID, sourceURL, captureImages=True, priorityQueue=None, callBacks=None, ingestProfile=None, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		profile = self.__ingestProfile

		if(ingestProfile and self.__ip.ProfileExists(accountID=accountID, profileID=ingestProfile)):
			profile = ingestProfile
		elif(self.__ingestProfile is None):
			r = self.__ip.GetDefaultProfile(accountID=accountID)
			if r.status_code in DynamicIngest.success_responses:
				profile = r.json().get('default_profile_id')

		priority = priorityQueue or self.__priorityQueue

		url = (DynamicIngest.base_url+'/videos/{videoid}/ingest-requests').format(pubid=accountID, videoid=videoID)
		data =	'{ "profile":"'+profile+'", "master": { "url": "'+sourceURL+'" }, "priority": "'+priority+'", "capture-images": '+str(captureImages).lower()+' }'
		return self.session.post(url=url, headers=headers, data=data)

	# get_upload_location_and_upload_file first performs an authenticated request to discover
	# a Brightcove-provided location to securely upload a source file
	def UploadFile(self, videoID, fileName, callBack=None, accountID=None):
		accountID = accountID or self.__oauth.account_id
		# Perform an authorized request to obtain a file upload location
		url = (CMS.base_url+'/videos/{videoid}/upload-urls/{sourcefilename}').format(pubid=accountID, videoid=videoID, sourcefilename=fileName)
		r = self.session.get(url=url, headers=self.__oauth.get_headers())
		if(r.status_code in DynamicIngest.success_responses):
			upload_urls_response = r.json()
		else:
			return None

		try:
			# Upload the contents of our local file to the location provided us
			# This example uses the boto3 library to perform a multipart upload
			# This is the recommended method for uploading large source files
			s3 = boto3.resource('s3',
				aws_access_key_id=upload_urls_response.get('access_key_id'),
				aws_secret_access_key=upload_urls_response.get('secret_access_key'),
				aws_session_token=upload_urls_response.get('session_token'))
			
			def emptyCB(muu):
				pass

			if(callBack is None):
				callBack = emptyCB

			s3.Object(upload_urls_response.get('bucket'), upload_urls_response.get('object_key')).upload_file(fileName, Callback=callBack)
			return upload_urls_response
		except Exception as e:
			print (e)
			return None

#===========================================
# read account info from JSON file
#===========================================
def LoadAccountInfo(input_filename:str=None) -> Tuple[str, str, str, dict]:
	"""Function to get information about account from config JSON file

	Args:
		input_filename (str, optional): path and name of the config JSON file. Defaults to None and will use "account_info.json" from the user's home folder.

	Returns:
		Tuple[str, str, str, dict]: account ID, client ID, client secret and the full deserialized JSON object
	"""
	# if no config file was passed we use the default
	input_filename = input_filename or expanduser('~')+'/account_info.json'

	# open the config file
	try:
		with open(input_filename, 'r') as f:
			# read and parse config file
			obj = json.loads( f.read() )
	except:
		eprint(f'Error: unable to open {input_filename}')
		return None, None, None, None

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
# calculates the aspect ratio of w and h
#===========================================
@functools.lru_cache()
def aspect_ratio(width: int , height: int) -> Tuple[int, int]:
	"""Function to calculate aspect ratio for two given values

	Args:
		width (int): width value
		height (int): height value

	Returns:
		Tuple[int, int]: ratio of width to height
	"""
	def gcd(a, b):
		return a if b == 0 else gcd(b, a % b)

	if(width == height):
		return 1,1

	temp = 0
	if(width < height):
		temp = width
		width = height
		height = temp

	divisor = gcd(width, height)

	x = int(width / divisor) if not temp else int(height / divisor)
	y = int(height / divisor) if not temp else int(width / divisor)

	return x,y

class TimeString():

	return_format = '{hh:02}:{mm:02}:{ss:02}'

	@classmethod
	def from_milliseconds(cls, millis:int, fmt:str=None) -> str:
		seconds = int(int(millis)/1000)
		hours, seconds = divmod(seconds, 60*60)
		minutes, seconds = divmod(seconds, 60)
		fmt = fmt if fmt else cls.return_format
		return fmt.format(hh=hours, mm=minutes, ss=seconds)

	@classmethod
	def from_seconds(cls, seconds:int, fmt:str=None) -> str:
		return(cls.from_milliseconds(int(seconds)*1000, fmt))

	@classmethod
	def from_minutes(cls, minutes:int, fmt:str=None) -> str:
		return(cls.from_seconds(int(minutes)*60, fmt))

#===========================================
# returns a DI instance
#===========================================
@static_vars(di=None)
def GetDI(oauth:OAuth=None, ip:str=None, pq:str='normal') -> DynamicIngest:
	if(not GetDI.di and oauth):
		GetDI.di = DynamicIngest(oAuth=oauth, ingestProfile=ip, priorityQueue=pq)
		logging.info('Obtained DI instance')

	return GetDI.di

@static_vars(cms=None)
def GetCMS(oauth:OAuth=None, query:str=None) -> CMS:
	if(not GetCMS.cms and oauth):
		GetCMS.cms = CMS(oauth=oauth, query=query)
		logging.info('Obtained CMS instance')

	return GetCMS.cms

@static_vars(args=None)
def GetArgs(parser=None):
	if(not GetArgs.args and parser):
		GetArgs.args = parser.parse_args()
		logging.info('Obtained arguments')

	return GetArgs.args

@static_vars(session=None)
def GetSession():
	if(not GetArgs.session):
		GetArgs.session = requests.Session()
		logging.info('Obtained Requests Session')

	return GetArgs.session

#===========================================
# test if a value is a valid JSON string
#===========================================
@functools.lru_cache()
def is_json(myjson: str) -> bool:
	"""Function to check if a string is valid JSON

	Args:
		myjson (str): string to check

	Returns:
		bool: true if myjson is valid JSON, false otherwise
	"""
	try:
		_ = json.loads(myjson)
	except Exception as e:
		return False
	return True

#===========================================
# converts asset ID to string
#===========================================
@functools.lru_cache()
def normalize_id(asset_id) -> str:
	"""Converts an asset ID to string

	Args:
		asset_id (any): video or playlist ID

	Returns:
		str: string representation of the ID, None if invalid ID
	"""
	_, response = wrangle_id(asset_id)
	return response

#===========================================
# test if a value is a valid ID
#===========================================
@functools.lru_cache()
def is_valid_id(asset_id) -> bool:
	"""Function to check if a given value is a valid asset ID

	Args:
		asset_id (any): value to check

	Returns:
		bool: True if it's a valid ID, False otherwise
	"""
	response, _ = wrangle_id(asset_id)
	return response

#===========================================
# test if a value is a valid ID and convert
# to string
#===========================================
@functools.lru_cache()
def wrangle_id(asset_id) -> Tuple[bool, str]:
	"""Converts ID to string and checks if it's a valid ID

	Args:
		asset_id (any): asset ID (video or playlist)

	Returns:
		(bool, str): True and string representation of ID if valid, False and None otherwise
	"""
	is_valid = False
	work_id = None

	# is it an int?
	if (type(asset_id) is int and asset_id > 0):
		try:
			work_id = str(asset_id)
		except:
			is_valid = False
		else:
			is_valid = True

	# is it a string?
	elif (type(asset_id) is str):
		if(asset_id.lower().startswith('ref:') and len(asset_id)<=154):
			work_id = asset_id
			is_valid = True
		else:
			try:
				work_id = str(int(asset_id))
			except:
				is_valid = False
			else:
				is_valid = True

	# is it a float?
	elif (type(asset_id) is float):
		if(asset_id.is_integer()):
			work_id = str(int(asset_id))
			is_valid = True
		else:
			is_valid = False

	return is_valid, work_id

#===========================================
# read list of video IDs from XLS/CSV
#===========================================
def videos_from_file(filename:str, column_name:str='video_id', validate:bool=True, unique:bool=True) -> list:
	"""Function to read a list of video IDs from an xls/csv file

	Args:
		filename (str): path and name of file to read from
		column_name (str, optional): name of the column in the file which contains the IDs. Defaults to 'video_id'.
		validate (bool, optional): check IDs to make sure they are valid IDs. Defaults to True.
		unique (bool, optional): makes sure all video IDs in the list are unique. Defaults to True.

	Returns:
		List: List object with the video IDs from the file. None if there was an error processing the file.
	"""
	video_list = None
	try:
		if(filename.lower().endswith('csv')):
			data = pandas.read_csv(filename) 
		else:
			data = pandas.read_excel(filename)
	except Exception as e:
		eprint(f'Error while trying to read {filename}: {e}')
	else:
		try:
			if(validate):
				video_list = [video_id for video_id in data[column_name] if is_valid_id(video_id)]
			else:
				video_list = list(data[column_name])
		except KeyError as e:
			eprint(f'Error while trying to read {filename} -> missing key: "{column_name}"')

	# make list unique
	if(video_list and unique):
		video_list = list(set(video_list))

	return video_list

#===========================================
# write list of rows to CSV file
#===========================================
def list_to_csv(row_list:list, filename:str) -> bool:
	"""Function to write a list of rows to a CSV file

	Args:
		row_list (list): A list of lists (the rows)
		filename (str, optional): Name for the CSV file. Defaults to 'report.csv'.

	Returns:
		bool: True if CSV successfully created, False otherwise
	"""
	result = False
	try:
		with open(filename if filename else 'report.csv', 'w', newline='', encoding='utf-8') as file:
			try:
				writer = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter=',')
				writer.writerows(row_list)
				result = True
			except Exception as e:
				eprint(f'\nError writing CSV data to file: {e}')
	except Exception as e:
		eprint(f'\nError creating outputfile: {e}')
	
	return result

#===========================================
# default processing function
#===========================================
def list_videos(video:dict) -> None:
	print(video.get('id')+', "'+video.get('name')+'"')

#===========================================
# function to fill queue with all videos
# from a Video Cloud account
#===========================================
def process_account(work_queue:queue.Queue, account_id:str, cms_obj:CMS) -> None:
	"""Function to fill a Queue with a list of all video IDs in an account

	Args:
		work_queue (queue.Queue): Queue to be filled with IDs
		cms_obj (CMS): CMS class instance
		account_id (str): Video Cloud account ID
	"""
	# ok, let's process all videos
	# get number of videos in account
	num_videos = cms_obj.GetVideoCount(accountID=account_id)

	if(num_videos <= 0):
		eprint(f'No videos found in account ID {account_id}''s library.')
		return

	eprint(f'Found {num_videos} videos in library. Processing them now.')

	current_offset = 0
	page_size = 50
	retries = 10

	while(current_offset < num_videos):

		response = None
		status = 0
		try:
			response = cms_obj.GetVideos(accountID=account_id, pageSize=page_size, pageOffset=current_offset)
			status = response.status_code
		except Exception as e:
			status = -1

		# good result
		if(status in [200,202]):
			json_data = response.json()
			# make sure we actually got some data
			if(len(json_data) > 0):
				# let's put all videos in a queue
				[ work_queue.put_nowait(video) for video in json_data ]
				# reset retries count and increase page offset
				retries = 10
				current_offset += page_size
				num_videos = cms_obj.GetVideoCount(accountID=account_id)

			# looks like we got an empty response (it can happen)
			else:
				status = -1

		# we hit a retryable error
		if(status == -1):
			code = response.status_code if response else 'unknown'
			if(retries > 0):
				eprint(f'Error: problem during API call ({code}).')
				for remaining in range(5, 0, -1):
					sys.stderr.write(f'\rRetrying in {remaining:2d} seconds.')
					sys.stderr.flush()
					time.sleep(1)

				retries -= 1
				eprint(f'\rRetrying now ({retries} retries left).')

			else:
				eprint(f'Error: fatal failure during API call ({code}).')
				return

#===========================================
# function to process a single video
#===========================================
def process_single_video_id(account_id:str, video_id:str, cms_obj:CMS, process_callback:Callable[[], None]) -> bool:
	"""Function to process a single video using a provided callback function

	Args:
		account_id (str): the account ID
		video_id (str): the video ID
		cms_obj (CMS): CMS class instance
		process_callback (Callable[[], None]): the callback function used for actual processing

	Returns:
		bool: True if there was no error, False otherwise
	"""
	response = None
	try:
		response = cms_obj.GetVideo(accountID=account_id, videoID=video_id)
	except Exception as e:
		response = None

	if(response and response.status_code in CMS.success_responses):
		try:
			process_callback(response.json())
		except Exception as e:
			eprint(f'Error executing callback for video ID {video_id}: {e}')
			return False

	else:
		if(response == None):
			code = 'exception'
		else:
			code = response.status_code
		eprint(f'Error getting information for video ID {video_id} ({code}).')
		return False
	
	return True

# worker class for multithreading
class Worker(Thread):
	def __init__(self, q, cms_obj, account_id, process_callback, *args, **kwargs):
		self.q = q
		self.cms_obj = cms_obj
		self.account_id = account_id
		self.process_callback = process_callback
		super().__init__(*args, **kwargs)

	def run(self):
		keep_working = True
		while keep_working:
			try:
				work = self.q.get()
			except queue.Empty:
				logging.info('Queue empty -> exiting worker thread')
				return
			# is it the exit signal?
			if(work == 'EXIT'):
				logging.info('EXIT found -> exiting worker thread')
				keep_working = False
			# do whatever work you have to do on work
			elif(type(work) == dict):
				self.process_callback(work)
			else:
				process_single_video_id(account_id=self.account_id, 
										video_id=work, 
										cms_obj=self.cms_obj, 
										process_callback=self.process_callback)

			self.q.task_done()

#===========================================
# this is the main loop to process videos
#===========================================
def process_input(inputfile=None, process_callback=list_videos, video_id=None) -> bool:
	global oauth

	# get the account info and credentials
	account_id,b,c,opts = LoadAccountInfo(inputfile)

	if(None in [account_id,b,c,opts]):
		return False

	# update account ID if passed in command line
	account_id = GetArgs().t or account_id

	oauth = OAuth(account_id,b,c)
	GetCMS(oauth=oauth, query=GetArgs().q)
	GetDI(oauth=oauth)

	# if async is enabled use more than one thread
	max_threads = GetArgs().a or 1
	logging.info(f'Using {max_threads} thread(s) for processing')

	#=========================================================
	#=========================================================
	# check if we should process a specific video ID
	#=========================================================
	#=========================================================
	if(video_id):
		print(f'Processing video ID {video_id} now.')
		return process_single_video_id(account_id, video_id, GetCMS(), process_callback)

	# create the work queue because everything below uses it
	work_queue = queue.Queue(maxsize=0)

	#=========================================================
	#=========================================================
	# check if we should process a given list of videos
	#=========================================================
	#=========================================================
	if(GetArgs().x):
		video_list = videos_from_file(GetArgs().x)
	else:
		video_list = opts.get('video_ids')

	if(video_list and video_list[0] != 'all'):
		num_videos = len(video_list)
		eprint(f'Found {num_videos} videos in options file. Processing them now.')
		# let's put all video IDs in a queue
		[ work_queue.put_nowait(video_id) for video_id in video_list ]
		# starting worker threads on queue processing
		num_threads = min(max_threads, num_videos)
		for _ in range(num_threads):
			work_queue.put_nowait("EXIT")
			Worker(	q=work_queue, 
					cms_obj=GetCMS(), 
					account_id=account_id, 
					process_callback=process_callback).start()
		# now we wait until the queue has been processed
		if(not work_queue.empty()):
			work_queue.join()

		return True

	#=========================================================
	#=========================================================
	# here we process the whole account
	#=========================================================
	#=========================================================

	# start thread to fill the queue
	account_page_thread = Thread(target=process_account, args=[work_queue, account_id, GetCMS()])
	account_page_thread.start()

	# starting worker threads on queue processing
	[ Worker(q=work_queue, cms_obj=GetCMS(), account_id=account_id, process_callback=process_callback).start() for _ in range(max_threads) ]

	# first wait for the queue filling thread to finish
	account_page_thread.join()

	# once the queue is filled with videos add exit signals
	[ work_queue.put_nowait("EXIT") for _ in range(max_threads) ]

	# now we wait until the queue has been processed
	if(not work_queue.empty()):
		work_queue.join()

	return True

#===========================================
# parse args and do the thing
#===========================================
def main(process_func:Callable[[], None]) -> None:
	# init the argument parsing
	parser = argparse.ArgumentParser(prog=sys.argv[0])
	parser.add_argument('-i', type=str, help='Name and path of account config information file')
	parser.add_argument('-q', type=str, help='CMS API search query')
	parser.add_argument('-t', type=str, help='Target account ID')
	parser.add_argument('-v', type=str, help='Specific video ID to process')
	parser.add_argument('-o', type=str, help='Output filename')
	parser.add_argument('-x', type=str, help='XLS/CSV input filename')
	parser.add_argument('-a', type=int, const=10, nargs='?', help='Async processing of videos')
	parser.add_argument('-d', action='store_true', default=False, help='Show debug info messages')

	# parse the args
	GetArgs(parser)

	if(GetArgs().d):
		logging.basicConfig(level=logging.INFO, format='[%(levelname)s:%(lineno)d]: %(message)s')
		logging.info('Logging enabled')
	else:
		logging.basicConfig(level=logging.CRITICAL, format='[%(levelname)s:%(lineno)d]: %(message)s')

	# go through the library and do stuff
	process_input(inputfile=GetArgs().i, process_callback=process_func, video_id=GetArgs().v)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(list_videos)
