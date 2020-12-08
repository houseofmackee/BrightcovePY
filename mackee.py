#!/usr/bin/env python3
from __future__ import print_function
import sys
import csv
import json
import argparse
import time
import logging
import functools
from queue import Queue, Empty
from typing import Callable, Tuple, Union, Optional, Dict, Any
from threading import Thread, Lock
from os.path import expanduser, basename, getsize
from abc import ABC, abstractproperty
from requests.adapters import Response
from requests_toolbelt import MultipartEncoder # type: ignore # pip3 install requests_toolbelt
from dataclasses import dataclass
import requests # pip3 install requests
import boto3 # pip3 install boto3
import pandas

mac_logger = logging.getLogger()

# disable certificate warnings
requests.urllib3.disable_warnings()

# function to print to stderr
def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

# decorator for static variables
def static_vars(**kwargs):
	def decorate(func):
		for k in kwargs:
			setattr(func, k, kwargs[k])
		return func
	return decorate

class ProgressPercentage(object):
	"""
	Class to provide a simple progress indicator
	"""
	def __init__(self, filename=None, target=0):
		self._filename = filename
		self._size = int(getsize(filename)) if filename else target
		self._seen_so_far = 0
		self._lock = Lock()

	def __call__(self, bytes_amount, add_info=''):
		# To simplify, assume this is hooked up to a single filename
		with self._lock:
			self._seen_so_far += bytes_amount
			percentage = (self._seen_so_far / self._size) * 100
			sys.stdout.write("\rProgress: %s / %s  (%.2f%%)%s\r" % (self._seen_so_far, self._size, percentage, add_info))
			sys.stdout.flush()

class Base(ABC):

	# every derived class must have a base URL
	@abstractproperty
	def base_url(self):
		pass

	API_VERSION = None
	# generally accepted success responses
	success_responses = [200,201,202,203,204]

	def __init__(self, query:Optional[str]=None) -> None:
		self.search_query:Optional[str] = query
		self.__session = self._get_session()

	@staticmethod
	def _get_session() -> requests.Session:
		sess = requests.Session()
		adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
		sess.mount('https://', adapter)
		return sess

	@staticmethod
	def _json_to_string(json_object:Union[str, dict]) -> Optional[str]:
		"""
		If json_object is a dict convert to str.
		If json_object is a str validate it.
		Returns str if it's valid JSON, None otherwise.
		"""
		if isinstance(json_object, dict):
			return json.dumps(json_object)
		elif isinstance(json_object, str):
			try:
				_ = json.loads(json_object)
				return json_object
			except:
				pass
		return None

	@property
	def search_query(self) -> Optional[str]:
		return self.__search_query

	@search_query.setter
	def search_query(self, query: Optional[str]) -> None:
		self.__search_query = '' if not query else requests.utils.quote(query)

	@property
	def session(self) -> requests.Session:
		return self.__session


class DeliveryRules(Base):
	base_url = 'https://delivery-rules.api.brightcove.com/accounts/{account_id}'

	def __init__(self, oauth):
		self.__oauth = oauth

	def DeliveryRulesEnabled(self, account_id=None):
		return self.GetDeliveryRules(account_id=account_id).status_code == 200

	def GetDeliveryRules(self, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliveryRules.base_url).format(account_id=account_id)
		return requests.get(url, headers=headers)

	def GetConditions(self, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliveryRules.base_url+'/conditions').format(account_id=account_id)
		return requests.get(url, headers=headers)

	def UpdateConditions(self, json_body, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliveryRules.base_url+'/conditions').format(account_id=account_id)
		return requests.put(url, headers=headers, data=self._json_to_string(json_body))

	def GetActions(self, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliveryRules.base_url+'/actions').format(account_id=account_id)
		return requests.get(url, headers=headers)

	def GetSpecificAction(self, action_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliveryRules.base_url+'/actions/{action_id}').format(account_id=account_id, action_id=action_id)
		return requests.get(url, headers=headers)

	def CreateAction(self, json_body, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliveryRules.base_url+'/actions').format(account_id=account_id)
		return requests.post(url, headers=headers, data=self._json_to_string(json_body))

	def UpdateAction(self, action_id, json_body, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliveryRules.base_url+'/actions/{action_id}').format(account_id=account_id, action_id=action_id)
		return requests.put(url, headers=headers, data=self._json_to_string(json_body))

	def DeleteAction(self, action_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliveryRules.base_url+'/actions/{action_id}').format(account_id=account_id, action_id=action_id)
		return requests.delete(url, headers=headers)

class Social(Base):

	base_url = 'https://edge.social.api.brightcove.com/v1/accounts/{account_id}'

	def __init__(self, oauth, query=None):
		super().__init__(query)
		self.__oauth = oauth

	def ListStatusForVideos(self, search_query=None, account_id=None):
		account_id = account_id or self.__oauth.account_id
		search_query = search_query or self.search_query
		headers = self.__oauth.get_headers()
		url = (Social.base_url+'/videos/status?{query_string}').format(account_id=account_id, query_string=search_query)
		return self.session.get(url, headers=headers)

	def ListStatusForVideo(self, video_id, search_query=None, account_id=None):
		account_id = account_id or self.__oauth.account_id
		search_query = search_query or self.search_query
		headers = self.__oauth.get_headers()
		url = (Social.base_url+'/videos/{video_id}/status?{query_string}').format(account_id=account_id, video_id=video_id, query_string=search_query)
		return self.session.get(url, headers=headers)

	def ListHistoryForVideos(self, search_query=None, account_id=None):
		account_id = account_id or self.__oauth.account_id
		search_query = search_query or self.search_query
		headers = self.__oauth.get_headers()
		url = (Social.base_url+'/videos/history?{query_string}').format(account_id=account_id, query_string=search_query)
		return self.session.get(url, headers=headers)

	def ListHistoryForVideo(self, video_id, search_query=None, account_id=None):
		account_id = account_id or self.__oauth.account_id
		search_query = search_query or self.search_query
		headers = self.__oauth.get_headers()
		url = (Social.base_url+'/videos/{video_id}/history?{query_string}').format(account_id=account_id, video_id=video_id, query_string=search_query)
		return self.session.get(url, headers=headers)

class SocialSyndication(Base):

	base_url = 'https://social.api.brightcove.com/v1/accounts/{account_id}/mrss/syndications'

	def __init__(self, oauth):
		self.__oauth = oauth

	def GetAllSyndications(self, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (SocialSyndication.base_url).format(account_id=account_id)
		return requests.get(url, headers=headers)

	def GetSyndication(self, syndication_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (SocialSyndication.base_url+'/{syndicationid}').format(account_id=account_id, syndicationid=syndication_id)
		return requests.get(url, headers=headers)

	def CreateSyndication(self, json_body, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (SocialSyndication.base_url).format(account_id=account_id)
		return requests.post(url, headers=headers, data=self._json_to_string(json_body))

	def DeleteSyndication(self, syndication_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (SocialSyndication.base_url+'/{syndicationid}').format(account_id=account_id, syndicationid=syndication_id)
		return requests.delete(url, headers=headers)

	def UpdateSyndication(self, syndication_id, json_body, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (SocialSyndication.base_url+'/{syndicationid}').format(account_id=account_id, syndicationid=syndication_id)
		return requests.patch(url, headers=headers, data=self._json_to_string(json_body))

	def GetTemplate(self, syndication_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (SocialSyndication.base_url+'/{syndicationid}/template').format(account_id=account_id, syndicationid=syndication_id)
		return requests.get(url, headers=headers)

	def UploadTemplate(self, syndication_id, json_body, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (SocialSyndication.base_url+'/{syndicationid}/template').format(account_id=account_id, syndicationid=syndication_id)
		return requests.put(url, headers=headers, data=self._json_to_string(json_body))

class PlayerManagement(Base):

	base_url = 'https://players.api.brightcove.com/v2/accounts/{account_id}'

	def __init__(self, oauth):
		super().__init__()
		self.__oauth = oauth

	def GetListOfPlayers(self, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlayerManagement.base_url+'/players').format(account_id=account_id)
		return self.session.get(url, headers=headers)

	def GetSinglePlayer(self, account_id=None, player_id=None):
		account_id = account_id or self.__oauth.account_id
		player_id = player_id or 'default'
		headers = self.__oauth.get_headers()
		url = (PlayerManagement.base_url+'/players/{playerid}').format(account_id=account_id, playerid=player_id)
		return self.session.get(url, headers=headers)

	def CreatePlayer(self, json_body, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlayerManagement.base_url+'/players').format(account_id=account_id)
		return self.session.post(url, headers=headers, data=self._json_to_string(json_body))

	def DeletePlayer(self, player_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlayerManagement.base_url+'/players/{playerid}').format(account_id=account_id, playerid=player_id)
		return self.session.delete(url, headers=headers)

	def PublishPlayer(self, player_id=None, account_id=None):
		account_id = account_id or self.__oauth.account_id
		player_id = player_id or 'default'
		headers = self.__oauth.get_headers()
		url = (PlayerManagement.base_url+'/players/{playerid}/publish').format(account_id=account_id, playerid=player_id)
		return self.session.post(url, headers=headers)

	def UpdatePlayer(self, player_id, json_body, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlayerManagement.base_url+'/players/{playerid}').format(account_id=account_id, playerid=player_id)
		return self.session.patch(url, headers=headers, data=self._json_to_string(json_body))

	def GetPlayerConfiguration(self, player_id, branch, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlayerManagement.base_url+'/players/{playerid}/configuration/{branch}').format(account_id=account_id, playerid=player_id, branch=branch)
		return self.session.get(url, headers=headers)

	def UpdatePlayerConfiguration(self, player_id, json_body, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlayerManagement.base_url+'/players/{playerid}/configuration').format(account_id=account_id, playerid=player_id)
		return self.session.patch(url, headers=headers, data=self._json_to_string(json_body))

	def GetAllPlugins(self, template_version=None):
		headers = self.__oauth.get_headers()
		if template_version:
			query = '?template_version='+template_version
		else:
			query = ''
		url = 'https://players.api.brightcove.com/v2/plugins'+query
		return self.session.get(url, headers=headers)

	def GetSinglePlugin(self, plugin_id):
		headers = self.__oauth.get_headers()
		if plugin_id:
			plugin_id = plugin_id.replace('@', '%40')
			plugin_id = plugin_id.replace('/', '%2F')
		else:
			plugin_id = ''
		url = 'https://players.api.brightcove.com/v2/plugins/'+plugin_id
		return self.session.get(url, headers=headers)

	def GetAllEmbeds(self, player_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlayerManagement.base_url+'/players/{playerid}/embeds').format(account_id=account_id, playerid=player_id)
		return self.session.get(url, headers=headers)

	def GetEmbed(self, player_id, embed_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlayerManagement.base_url+'/players/{playerid}/embeds/{embedid}').format(account_id=account_id, playerid=player_id, embedid=embed_id)
		return self.session.get(url, headers=headers)

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
		if r.status_code == 200:
			access_token = r.json().get('access_token')
			self.__request_time = time.time()

		return access_token

	def get_access_token(self):
		if self.__access_token is None:
			self.__access_token = self.__get_access_token()
		elif (time.time()-self.__request_time) > self.__token_life:
			self.__access_token = self.__get_access_token()
		return self.__access_token

	def get_headers(self) -> dict:
		return { 'Authorization': f'Bearer {self.get_access_token()}', 'Content-Type': 'application/json' }

class JWT(Base):

	base_url = 'https://playback-auth.api.brightcove.com/v1/accounts/{account_id}'

	def __init__(self, oauth):
		self.__oauth = oauth

	def RegisterKey(self, key_data, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (JWT.base_url+'/keys').format(account_id=account_id)
		json_body = '{ "value":"'+key_data+'" }'
		return requests.post(url, headers=headers, data=self._json_to_string(json_body))

	def ListKeys(self, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (JWT.base_url+'/keys').format(account_id=account_id)
		return requests.get(url, headers=headers)

	def GetKey(self, key_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (JWT.base_url+'/keys/{keyid}').format(account_id=account_id,keyid=key_id)
		return requests.get(url, headers=headers)

	def DeleteKey(self, key_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (JWT.base_url+'/keys/{keyid}').format(account_id=account_id,keyid=key_id)
		return requests.delete(url, headers=headers)

class PlaybackRights(Base):

	base_url ='https://playback-rights.api.brightcove.com/v1/accounts/{account_id}'

	def __init__(self, oauth):
		self.__oauth = oauth

	def CreatePlaybackRight(self, json_body, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlaybackRights.base_url+'/playback_rights').format(account_id=account_id)
		return requests.post(url=url, headers=headers, data=self._json_to_string(json_body))

	def GetPlaybackRights(self, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlaybackRights.base_url+'/playback_rights').format(account_id=account_id)
		return requests.get(url=url, headers=headers)

	def GetPlaybackRight(self, epa_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlaybackRights.base_url+'/playback_rights/{epaid}').format(account_id=account_id, epaid=epa_id)
		return requests.get(url=url, headers=headers)

	def UpdatePlaybackRight(self, epa_id, json_body, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlaybackRights.base_url+'/playback_rights/{epaid}').format(account_id=account_id, epaid=epa_id)
		return requests.put(url=url, headers=headers, data=self._json_to_string(json_body))

	def DeletePlaybackRight(self, epa_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlaybackRights.base_url+'/playback_rights/{epaid}').format(account_id=account_id, epaid=epa_id)
		return requests.delete(url=url, headers=headers)

	def GetAllUserDevices(self, user_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlaybackRights.base_url+'/users/{userid}/devices').format(account_id=account_id, userid=user_id)
		return requests.get(url=url, headers=headers)

	def DeleteAllUserDevices(self, user_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlaybackRights.base_url+'/users/{userid}/devices').format(account_id=account_id, userid=user_id)
		return requests.delete(url=url, headers=headers)

	def DeleteUserDevice(self, user_id, device_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (PlaybackRights.base_url+'/users/{userid}/devices/{deviceid}').format(account_id=account_id, userid=user_id, deviceid=device_id)
		return requests.delete(url=url, headers=headers)

class DeliverySystem(Base):

	base_url = 'https://repos.api.brightcove.com/v1/accounts/{account_id}/repos'

	def __init__(self, oauth):
		self.__oauth = oauth

	def ListRepositories(self, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliverySystem.base_url).format(account_id=account_id)
		return requests.get(url=url, headers=headers)

	def GetRepositoryDetails(self, repo_name, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliverySystem.base_url+'/{reponame}').format(account_id=account_id,reponame=repo_name)
		return requests.get(url, headers=headers)

	def DeleteRepository(self, repo_name, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliverySystem.base_url+'/{reponame}').format(account_id=account_id,reponame=repo_name)
		return requests.delete(url, headers=headers)

	def CreateRepository(self, repo_name, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliverySystem.base_url+'/{reponame}').format(account_id=account_id,reponame=repo_name)
		return requests.put(url, headers=headers)

	def ListFilesInRepository(self, repo_name, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliverySystem.base_url+'/{reponame}/files').format(account_id=account_id,reponame=repo_name)
		return requests.get(url, headers=headers)

	def DeleteFileInRepository(self, repo_name, file_name, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (DeliverySystem.base_url+'/{reponame}/files/{filename}').format(account_id=account_id,reponame=repo_name,filename=file_name)
		return requests.delete(url, headers=headers)

	def AddFileToRepository(self, repo_name, file_name, account_id=None):
		account_id = account_id or self.__oauth.account_id
		url = (DeliverySystem.base_url+'/{reponame}/files/{filename}').format(account_id=account_id,reponame=repo_name,filename=basename(file_name))
		m = MultipartEncoder( fields={'contents': (None, open(file_name, 'rb'), 'text/plain')} )
		access_token = self.__oauth.get_access_token()
		headers = { 'Authorization': 'Bearer ' + access_token, 'Content-Type': m.content_type }
		return requests.put(url, headers=headers, data=m)

class CMS(Base):
	base_url = 'https://cms.api.brightcove.com/v1/accounts/{account_id}'

	def __init__(self, oauth:OAuth, query:str=None):
		super().__init__(query)
		self.__oauth = oauth

	#===========================================
	# get who created a video
	#===========================================
	@staticmethod
	def GetCreatedBy(video:dict) -> str:
		creator = 'Unknown'
		if video:
			created_by = video.get('created_by')
			if created_by:
				ctype = created_by.get('type')
				if ctype=='api_key':
					creator = 'API'
				elif ctype=='user':
					creator = created_by.get('email')
		return creator

	#===========================================
	# get number of videos in an account
	#===========================================
	def GetVideoCount(self, search_query=None, account_id=None):
		account_id = account_id or self.__oauth.account_id
		search_query = search_query or self.search_query
		headers = self.__oauth.get_headers()
		#url = (CMS.base_url+'/videos/count?q={query}').format(account_id=account_id,query=search_query)
		url = f'{CMS.base_url}/videos/count?q={search_query}'.format(account_id=account_id)
		r = self.session.get(url, headers=headers)
		if r.status_code == 200:
			return r.json().get('count')
		return -1

	#===========================================
	# create new video object in an account
	#===========================================
	def CreateVideo(self, video_title='Video Title', json_body=None, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/').format(account_id=account_id)
		json_body = json_body or '{"name": "'+video_title+'"}'
		return self.session.post(url=url, headers=headers, data=self._json_to_string(json_body))

	#===========================================
	# get a video
	#===========================================
	def GetVideo(self, video_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{video_id}').format(account_id=account_id,video_id=video_id)
		return self.session.get(url=url, headers=headers)

	#===========================================
	# get videos in an account
	#===========================================
	def GetVideos(self, page_size=20, page_offset=0, search_query=None, account_id=None):
		account_id = account_id or self.__oauth.account_id
		search_query = search_query or self.search_query
		headers = self.__oauth.get_headers()
		url = f'{CMS.base_url}/videos?limit={page_size}&offset={page_offset}&sort=created_at&q={search_query}'.format(account_id=account_id)
		return self.session.get(url, headers=headers)

	#===========================================
	# get light version of videos in an account
	#===========================================
	def GetLightVideos(self, page_size=20, page_offset=0, search_query=None, account_id=None):
		account_id = account_id or self.__oauth.account_id
		search_query = search_query or self.search_query
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/lightvideos?limit={page_size}&offset={offset}&sort=created_at{query}').format(account_id=account_id, page_size=page_size, offset=page_offset, query='&q=' + search_query)
		return self.session.get(url, headers=headers)

	#===========================================
	# get a video's sources
	#===========================================
	def GetVideoSources(self, video_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{video_id}/sources').format(account_id=account_id,video_id=video_id)
		return self.session.get(url=url, headers=headers)

	#===========================================
	# get a video's images
	#===========================================
	def GetVideoImages(self, video_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{video_id}/images').format(account_id=account_id,video_id=video_id)
		return self.session.get(url=url, headers=headers)

	#===========================================
	# get a video's audio tracks
	#===========================================
	def GetVideoAudioTracks(self, video_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{video_id}/audio_tracks').format(account_id=account_id,video_id=video_id)
		return self.session.get(url=url, headers=headers)

	#===========================================
	# get a specific audio track
	#===========================================
	def GetVideoAudioTrack(self, video_id, track_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{video_id}/audio_tracks/{trackid}').format(account_id=account_id,video_id=video_id,trackid=track_id)
		return self.session.get(url=url, headers=headers)

	#===========================================
	# delete a specific audio track
	#===========================================
	def DeleteVideoAudioTrack(self, video_id, track_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{video_id}/audio_tracks/{trackid}').format(account_id=account_id,video_id=video_id,trackid=track_id)
		return self.session.delete(url=url, headers=headers)

	#===========================================
	# update a specific audio track
	#===========================================
	def UpdateVideoAudioTrack(self, video_id, track_id, json_body, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{video_id}/audio_tracks/{trackid}').format(account_id=account_id,video_id=video_id,trackid=track_id)
		return self.session.patch(url=url, headers=headers, data=self._json_to_string(json_body))

	#===========================================
	# delete a video
	#===========================================
	def DeleteVideo(self, video_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{video_id}').format(account_id=account_id,video_id=video_id)
		return self.session.delete(url=url, headers=headers)

	#===========================================
	# get a digital master info
	#===========================================
	def GetDigitalMasterInfo(self, video_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{video_id}/digital_master').format(account_id=account_id,video_id=video_id)
		return self.session.get(url=url, headers=headers)

	#===========================================
	# delete a digital master
	#===========================================
	def DeleteMaster(self, video_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{video_id}/digital_master').format(account_id=account_id,video_id=video_id)
		return self.session.delete(url=url, headers=headers)

	#===========================================
	# update a video
	#===========================================
	def UpdateVideo(self, video_id, json_body, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{video_id}').format(account_id=account_id,video_id=video_id)
		return self.session.patch(url, headers=headers, data=self._json_to_string(json_body))

	#===========================================
	# get custom fields
	#===========================================
	def GetCustomFields(self, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/video_fields').format(account_id=account_id)
		return self.session.get(url=url, headers=headers)

	#===========================================
	# get ingest job status for a video
	#===========================================
	def GetStatusOfIngestJob(self, video_id, job_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{video_id}/ingest_jobs/{jobid}').format(account_id=account_id,video_id=video_id,jobid=job_id)
		return self.session.get(url=url, headers=headers)

	#===========================================
	# get all ingest jobs status for a video
	#===========================================
	def GetStatusOfIngestJobs(self, video_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{video_id}/ingest_jobs').format(account_id=account_id,video_id=video_id)
		return self.session.get(url=url, headers=headers)

	#===========================================
	# variants stuff
	#===========================================
	def GetAllVideoVariants(self, video_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{video_id}/variants').format(account_id=account_id,video_id=video_id)
		return self.session.get(url=url, headers=headers)

	def CreateVideoVariant(self, video_id, json_body, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{video_id}/variants').format(account_id=account_id,video_id=video_id)
		return self.session.post(url=url, headers=headers, data=self._json_to_string(json_body))

	def GetVideoVariant(self, video_id, language, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{video_id}/variants/{language}').format(account_id=account_id,video_id=video_id, language=language)
		return self.session.get(url=url, headers=headers)

	def UpdateVideoVariant(self, video_id, language, json_body, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{video_id}/variants/{language}').format(account_id=account_id,video_id=video_id, language=language)
		return self.session.patch(url=url, headers=headers, data=self._json_to_string(json_body))

	def DeleteVideoVariant(self, video_id, language, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{video_id}/variants/{language}').format(account_id=account_id,video_id=video_id, language=language)
		return self.session.delete(url=url, headers=headers)

	#===========================================
	# subscriptions bla bla
	#===========================================
	def GetSubscriptionsList(self, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/subscriptions').format(account_id=account_id)
		return self.session.get(url, headers=headers)

	def GetSubscription(self, sub_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/subscriptions/{subid}').format(account_id=account_id, subid=sub_id)
		return self.session.get(url, headers=headers)

	def CreateSubscription(self, callback_url, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/subscriptions').format(account_id=account_id)
		json_body = ('{ "endpoint":"' + callback_url + '", "events":["video-change"] }')
		return self.session.post(url, headers=headers, data=self._json_to_string(json_body))

	def DeleteSubscription(self, sub_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/subscriptions/{subid}').format(account_id=account_id,subid=sub_id)
		return self.session.delete(url, headers=headers)

	#===========================================
	# folders stuff
	#===========================================
	def GetFolders(self, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders').format(account_id=account_id)
		return self.session.get(url, headers=headers)

	def CreateFolder(self, folder_name, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders').format(account_id=account_id)
		json_body = ('{ "name":"' + folder_name + '" }')
		return self.session.post(url, headers=headers, data=self._json_to_string(json_body))

	def DeleteFolder(self, folder_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders/{folderid}').format(account_id=account_id, folderid=folder_id)
		return self.session.delete(url, headers=headers)

	def GetFolderInformation(self, folder_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders/{folderid}').format(account_id=account_id, folderid=folder_id)
		return self.session.get(url, headers=headers)

	def UpdateFolderName(self, folder_id, folder_name, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders/{folderid}').format(account_id=account_id, folderid=folder_id)
		json_body = ('{ "name":"' + folder_name + '" }')
		return self.session.patch(url, headers=headers, data=self._json_to_string(json_body))

	def AddVideoToFolder(self, folder_id, video_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders/{folderid}/videos/{video_id}').format(account_id=account_id, folderid=folder_id, video_id=video_id)
		return self.session.put(url, headers=headers)

	def RemoveVideoFromFolder(self, folder_id, video_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders/{folderid}/videos/{video_id}').format(account_id=account_id, folderid=folder_id, video_id=video_id)
		return self.session.delete(url, headers=headers)

	def GetVideosInFolder(self, folder_id, page_size=100, page_offset=0, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders/{folderid}/videos?limit={limit}&offset={offset}').format(account_id=account_id,folderid=folder_id,limit=page_size, offset=page_offset)
		return self.session.get(url, headers=headers)

	#===========================================
	# playlists stuff
	#===========================================
	def GetPlaylistsForVideo(self, video_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{video_id}/references').format(account_id=account_id, video_id=video_id)
		return self.session.get(url, headers=headers)

	def RemoveVideoFromAllPlaylists(self, video_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{video_id}/references').format(account_id=account_id, video_id=video_id)
		return self.session.delete(url, headers=headers)

	def GetVideosInPlaylist(self, playlist_id, include_details=True, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/playlists/{playlistid}/videos?include_details={details}').format(account_id=account_id, playlistid=playlist_id, details=('false','true')[include_details])
		return self.session.get(url, headers=headers)

	def GetVideoCountInPlaylist(self, playlist_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/counts/playlists/{playlistid}/videos').format(account_id=account_id, playlistid=playlist_id)
		return self.session.get(url, headers=headers)

	def DeletePlaylist(self, playlist_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/playlists/{playlistid}').format(account_id=account_id, playlistid=playlist_id)
		return self.session.delete(url, headers=headers)

	def UpdatePlaylist(self, playlist_id, json_body, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/playlists/{playlistid}').format(account_id=account_id, playlistid=playlist_id)
		return self.session.patch(url, headers=headers, data=self._json_to_string(json_body))

	def GetPlaylistByID(self, playlist_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/playlists/{playlistid}').format(account_id=account_id, playlistid=playlist_id)
		return self.session.get(url, headers=headers)

	def GetPlaylistCount(self, search_query=None, account_id=None):
		account_id = account_id or self.__oauth.account_id
		search_query = search_query or self.search_query
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/counts/playlists?q={query}').format(account_id=account_id, query=search_query)
		return self.session.get(url, headers=headers)

	def GetPlaylists(self, sort='-updated_at', search_query=None, page_size=100, page_offset=0, account_id=None):
		account_id = account_id or self.__oauth.account_id
		search_query = search_query or self.search_query
		headers = self.__oauth.get_headers()
		if sort not in ['name', 'reference_id', 'created_at', 'published_at', 'updated_at', 'schedule.starts_at', 'schedule.ends_at', 'state', 'plays_total', 'plays_trailing_week', '-name', '-reference_id', '-created_at', '-published_at', '-updated_at', '-schedule.starts_at', '-schedule.ends_at', '-state', '-plays_total', '-plays_trailing_week']:
			sort = '-updated_at'
		url = (CMS.base_url+'/playlists?limit={limit}&offset={offset}&sort={sort}&q={query}').format(account_id=account_id, limit=page_size, offset=page_offset, sort=sort, query=search_query)
		return self.session.get(url, headers=headers)

	def CreatePlaylist(self, json_body, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/playlists').format(account_id=account_id)
		return self.session.post(url, headers=headers, data=self._json_to_string(json_body))

	#===========================================
	# Assets stuff
	#===========================================
	def GetDynamicRenditions(self, video_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{video_id}/assets/dynamic_renditions').format(account_id=account_id, video_id=video_id)
		return self.session.get(url, headers=headers)

	def GetRenditionList(self, video_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{video_id}/assets/renditions').format(account_id=account_id, video_id=video_id)
		return self.session.get(url, headers=headers)

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

	base_url = 'https://data.brightcove.com/v1/xdr/accounts/{account_id}'

	def __init__(self, oAuth):
		self.__oauth = oAuth

	def GetViewerPlayheads(self, viewer_id, limit=1000, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		limit = 1000 if (limit>10000 or limit<1) else limit
		url = (XDR.base_url+'/playheads/{viewerid}?limit={limit}').format(account_id=account_id, viewerid=viewer_id, limit=limit)
		return requests.get(url=url, headers=headers)

	def GetViewerVideoPlayheads(self, viewer_id, video_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (XDR.base_url+'/playheads/{viewerid}/{video_id}').format(account_id=account_id, viewerid=viewer_id, video_id=video_id)
		return requests.get(url=url, headers=headers)

class IngestProfiles(Base):

	base_url = 'https://ingestion.api.brightcove.com/v1/accounts/{account_id}'

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

	def GetDefaultProfile(self, account_id=None):
		account_id = account_id or self.__oauth.account_id
		# if it's not the same as before then find it and cache it
		if account_id != self.__defaultProfileAccount:
			headers = self.__oauth.get_headers()
			url = (IngestProfiles.base_url+'/configuration').format(account_id=account_id)
			self.__defaultProfileResponse = self.session.get(url=url, headers=headers)
			self.__defaultProfileAccount = account_id
		# return cached response
		return self.__defaultProfileResponse

	def GetIngestProfile(self, profile_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		# if it's not the same as before then find it and cache it
		if self.__getProfileAccount != account_id or self.__getProfileID != profile_id:
			headers = self.__oauth.get_headers()
			url = (IngestProfiles.base_url+'/profiles/{profileid}').format(account_id=account_id, profileid=profile_id)
			self.__getProfileID = profile_id
			self.__getProfileAccount = account_id
			self.__getProfileResponse = self.session.get(url=url, headers=headers)
		# return cached response
		return self.__getProfileResponse

	def ProfileExists(self, profile_id, account_id=None):
		account_id = account_id or self.__oauth.account_id

		# check if it's a valid cached account/profile combo
		if self.__previousProfile == profile_id and self.__previousAccount == account_id:
			return True

		r = self.GetIngestProfile(account_id=account_id, profile_id=profile_id)
		if r.status_code in IngestProfiles.success_responses:
			self.__previousProfile = profile_id
			self.__previousAccount = account_id
			return True

		return False

	def UpdateDefaultProfile(self, json_body, account_id=None):
		account_id = account_id or self.__oauth.account_id
		self.__previousProfile = None
		self.__previousAccount = None
		headers = self.__oauth.get_headers()
		url = (IngestProfiles.base_url+'/configuration').format(account_id=account_id)
		return self.session.put(url=url, headers=headers, data=self._json_to_string(json_body))

	def SetDefaultProfile(self, json_body, account_id=None):
		account_id = account_id or self.__oauth.account_id
		self.__previousProfile = None
		self.__previousAccount = None
		headers = self.__oauth.get_headers()
		url = (IngestProfiles.base_url+'/configuration').format(account_id=account_id)
		return self.session.post(url=url, headers=headers, data=self._json_to_string(json_body))

	def DeleteIngestProfile(self, profile_id, account_id=None):
		account_id = account_id or self.__oauth.account_id
		self.__previousProfile = None
		self.__previousAccount = None
		headers = self.__oauth.get_headers()
		url = (IngestProfiles.base_url+'/profiles/{profileid}').format(account_id=account_id,profileid=profile_id)
		return self.session.delete(url=url, headers=headers)

	def UpdateIngestProfile(self, profile_id, json_body, account_id=None):
		account_id = account_id or self.__oauth.account_id
		self.__previousProfile = None
		self.__previousAccount = None
		headers = self.__oauth.get_headers()
		url = (IngestProfiles.base_url+'/profiles/{profileid}').format(account_id=account_id,profileid=profile_id)
		return self.session.put(url=url, headers=headers, data=self._json_to_string(json_body))

	def CreateIngestProfile(self, json_body, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (IngestProfiles.base_url+'/profiles').format(account_id=account_id)
		return self.session.post(url=url, headers=headers, data=self._json_to_string(json_body))

	def GetAllIngestProfiles(self, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (IngestProfiles.base_url+'/profiles').format(account_id=account_id)
		return self.session.get(url=url, headers=headers)

class DynamicIngest(Base):

	base_url = 'https://ingest.api.brightcove.com/v1/accounts/{account_id}'

	def __init__(self, oAuth, ingest_profile=None, priority_queue='normal'):
		super().__init__()
		self.__oauth = oAuth
		self.__previous_profile = None
		self.__previous_account = None
		self.__ip = IngestProfiles(oAuth)
		self.SetIngestProfile(ingest_profile)
		self.SetPriorityQueue(priority_queue)

	def SetIngestProfile(self, profile_id):
		if self.__ip.ProfileExists(account_id=self.__oauth.account_id, profile_id=profile_id):
			self.__ingest_profile = profile_id
		else:
			self.__ingest_profile = None
		return self.__ingest_profile

	def SetPriorityQueue(self, priority_queue):
		if priority_queue in ['low', 'normal', 'high']:
			self.__priority_queue = priority_queue
		else:
			self.__priority_queue = 'normal'
		return self.__priority_queue

	def RetranscodeVideo(self, video_id, profile_id=None, capture_images=True, priority_queue=None, account_id=None):
		account_id = account_id or self.__oauth.account_id

		profile = self.__ingest_profile
		if profile_id and self.__ip.ProfileExists(account_id=account_id, profile_id=profile_id):
			profile = profile_id
		elif self.__ingest_profile is None:
			r = self.__ip.GetDefaultProfile(account_id=account_id)
			if r.status_code in DynamicIngest.success_responses:
				profile = r.json().get('default_profile_id')

		priority = priority_queue or self.__priority_queue

		headers = self.__oauth.get_headers()
		url = (DynamicIngest.base_url+'/videos/{video_id}/ingest-requests').format(account_id=account_id, video_id=video_id)
		data =	'{ "profile":"'+profile+'", "master": { "use_archived_master": true }, "priority": "'+priority+'","capture-images": '+str(capture_images).lower()+' }'
		return self.session.post(url=url, headers=headers, data=data)

	def SubmitIngest(self, video_id, source_url, capture_images=True, priority_queue=None, callbacks=None, ingest_profile=None, account_id=None):
		account_id = account_id or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		profile = self.__ingest_profile

		if ingest_profile and self.__ip.ProfileExists(account_id=account_id, profile_id=ingest_profile):
			profile = ingest_profile
		elif self.__ingest_profile is None:
			r = self.__ip.GetDefaultProfile(account_id=account_id)
			if r.status_code in DynamicIngest.success_responses:
				profile = r.json().get('default_profile_id')

		priority = priority_queue or self.__priority_queue

		url = (DynamicIngest.base_url+'/videos/{video_id}/ingest-requests').format(account_id=account_id, video_id=video_id)
		data =	'{ "profile":"'+profile+'", "master": { "url": "'+source_url+'" }, "priority": "'+priority+'", "capture-images": '+str(capture_images).lower()+' }'
		return self.session.post(url=url, headers=headers, data=data)

	# get_upload_location_and_upload_file first performs an authenticated request to discover
	# a Brightcove-provided location to securely upload a source file
	def UploadFile(self, video_id, file_name, callback=None, account_id=None):
		account_id = account_id or self.__oauth.account_id
		# Perform an authorized request to obtain a file upload location
		url = (CMS.base_url+'/videos/{video_id}/upload-urls/{sourcefilename}').format(account_id=account_id, video_id=video_id, sourcefilename=file_name)
		r = self.session.get(url=url, headers=self.__oauth.get_headers())
		if r.status_code in DynamicIngest.success_responses:
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

			def empty_cb(muu):
				pass

			callback = callback or empty_cb

			s3.Object(upload_urls_response.get('bucket'), upload_urls_response.get('object_key')).upload_file(file_name, Callback=callback)
			return upload_urls_response
		except Exception as e:
			print (e)
			return None

#===========================================
# read account info from JSON file
#===========================================
def LoadAccountInfo(input_filename:Optional[str]=None) -> Tuple[str, str, str, dict]:
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
		with open(input_filename, 'r') as file:
			obj = json.loads( file.read() )
	except:
		raise Exception(f'Error: unable to open {input_filename}')

	# grab data, make it strings and strip it
	account = obj.get('account_id')
	account = str(account).strip() if account else None

	client = obj.get('client_id')
	client = str(client).strip() if client else None

	secret = obj.get('client_secret')
	secret = str(secret).strip() if secret else None

	# return the object just in case it's needed later
	return account, client, secret, obj

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

	if width == height:
		return 1,1

	if width > height:
		divisor = gcd(width, height)
	else:
		divisor = gcd(height, width)

	return int(width / divisor), int(height / divisor)

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
		return cls.from_milliseconds(int(seconds)*1000, fmt)

	@classmethod
	def from_minutes(cls, minutes:int, fmt:str=None) -> str:
		return cls.from_seconds(int(minutes)*60, fmt)

#===========================================
# returns a DI instance
#===========================================
@static_vars(di=None)
def GetDI(oauth:OAuth=None, profile:str=None, priority:str='normal') -> DynamicIngest:
	"""Returns an existing DynamicIngest instance. Creates one if information is provided.

	Args:
		oauth (OAuth, optional): OAuth instance to use. Defaults to None.
		profile (str, optional): Ingest profile ID. Defaults to None.
		priority (str, optional): Priority queue. Defaults to 'normal'.

	Returns:
		DynamicIngest: DynamicIngest instance. None if none was created yet.
	"""
	if not GetDI.di and oauth:
		GetDI.di = DynamicIngest(oAuth=oauth, ingest_profile=profile, priority_queue=priority)
		mac_logger.info('Obtained DI instance')

	return GetDI.di

@static_vars(cms=None)
def GetCMS(oauth:OAuth=None, query:str=None) -> CMS:
	"""Returns an existing CMS instance. Creates one if information is provided.

	Args:
		oauth (OAuth, optional): OAuth instance to use. Defaults to None.
		query (str, optional): Query string to use. Defaults to None.

	Returns:
		CMS: CMS instance. None if none was created yet.
	"""
	if not GetCMS.cms and oauth:
		GetCMS.cms = CMS(oauth=oauth, query=query)
		mac_logger.info('Obtained CMS instance')

	return GetCMS.cms

@static_vars(oauth=None)
def GetOAuth(account_id:str=None, client_id:str=None, client_secret:str=None) -> OAuth:
	if not GetOAuth.oauth:
		GetOAuth.oauth = OAuth(account_id, client_id, client_secret)
		mac_logger.info('Obtained OAuth instance')

	return GetOAuth.oauth

@static_vars(args=None)
def GetArgs(parser=None):
	if not GetArgs.args and parser:
		GetArgs.args = parser.parse_args()
		mac_logger.info('Obtained arguments')

	return GetArgs.args

@static_vars(session=None)
def GetSession():
	if not GetArgs.session:
		GetArgs.session = requests.Session()
		mac_logger.info('Obtained Requests Session')

	return GetArgs.session

#===========================================
# test if a value is a valid JSON string
#===========================================
@functools.lru_cache()
def is_json(myjson:str) -> bool:
	"""Function to check if a string is valid JSON

	Args:
		myjson (str): string to check

	Returns:
		bool: true if myjson is valid JSON, false otherwise
	"""
	try:
		_ = json.loads(myjson)
	except:
		return False
	return True

#===========================================
# converts asset ID to string
#===========================================
@functools.lru_cache()
def normalize_id(asset_id:Union[str, int, float]) -> Optional[str]:
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
def is_valid_id(asset_id:Union[str, int, float]) -> bool:
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
def wrangle_id(asset_id:Union[str, int, float]) -> Tuple[bool, Optional[str]]:
	"""Converts ID to string and checks if it's a valid ID

	Args:
		asset_id (any): asset ID (video or playlist)

	Returns:
		(bool, str): True and string representation of ID if valid, False and None otherwise
	"""
	is_valid = False
	work_id = None

	# is it an int?
	if isinstance(asset_id, int) and asset_id > 0:
		try:
			work_id = str(asset_id)
		except:
			is_valid = False
		else:
			is_valid = True

	# is it a string?
	elif isinstance(asset_id, str):
		if asset_id.lower().startswith('ref:') and len(asset_id)<=154:
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
	elif isinstance(asset_id, float):
		if asset_id.is_integer():
			work_id = str(int(asset_id))
			is_valid = True

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
	video_list = []
	try:
		if filename.lower().endswith('csv'):
			data = pandas.read_csv(filename)
		else:
			data = pandas.read_excel(filename)
	except Exception as e:
		eprint(f'Error while trying to read {filename}: {e}')
	else:
		try:
			if validate:
				video_list = [video_id for video_id in data[column_name] if is_valid_id(video_id)]
			else:
				video_list = list(data[column_name])
		except KeyError:
			eprint(f'Error while trying to read {filename} -> missing key: "{column_name}"')

	# make list unique
	if video_list and unique:
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
	print(f'{video.get("id")}, {video.get("name")}')

#===========================================
# function to fill queue with all videos
# from a Video Cloud account
#===========================================
def process_account(work_queue:Queue, account_id:str, cms_obj:CMS) -> None:
	"""Function to fill a Queue with a list of all video IDs in an account

	Args:
		work_queue (Queue): Queue to be filled with IDs
		cms_obj (CMS): CMS class instance
		account_id (str): Video Cloud account ID
	"""
	# ok, let's process all videos
	# get number of videos in account
	num_videos = cms_obj.GetVideoCount(account_id=account_id)

	if num_videos <= 0:
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
			response = cms_obj.GetVideos(account_id=account_id, page_size=page_size, page_offset=current_offset)
			status = response.status_code
		except:
			status = -1

		# good result
		if status in [200,202]:
			json_data = response.json()
			# make sure we actually got some data
			if len(json_data) > 0:
				# let's put all videos in a queue
				for video in json_data:
					work_queue.put_nowait(video)
				# reset retries count and increase page offset
				retries = 10
				current_offset += page_size
				num_videos = cms_obj.GetVideoCount(account_id=account_id)

			# looks like we got an empty response (it can happen)
			else:
				status = -1

		# we hit a retryable error
		if status == -1:
			code = response.status_code if response else 'unknown'
			if retries > 0:
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
def process_single_video_id(account_id:str, video_id:str, cms_obj:CMS, process_callback:Callable[[Dict[Any, Any]], None]) -> bool:
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
		response = cms_obj.GetVideo(account_id=account_id, video_id=video_id)
	except:
		response = None

	if response and response.status_code in CMS.success_responses:
		try:
			process_callback(response.json())
		except Exception as e:
			eprint(f'Error executing callback for video ID {video_id}: {e}')
			return False

	else:
		if response is None:
			code = 'exception'
		else:
			code = response.status_code
		eprint(f'Error getting information for video ID {video_id} ({code}).')
		return False

	return True

# worker class for multithreading
class Worker(Thread):

	@dataclass
	class WorkerData:
		queue: Queue
		account_id: str
		callback: callable
		cms_instance: CMS

	def __init__(self, q, cms_obj, account_id, process_callback, *args, **kwargs):
		self.queue = q
		self.cms_obj = cms_obj
		self.account_id = account_id
		self.process_callback = process_callback
		super().__init__(*args, **kwargs)

	def run(self):
		keep_working = True
		while keep_working:
			try:
				work = self.queue.get()
			except Empty:
				mac_logger.info('Queue empty -> exiting worker thread')
				return
			# is it the exit signal?
			if work == 'EXIT':
				mac_logger.info('EXIT found -> exiting worker thread')
				keep_working = False
			# do whatever work you have to do on work
			elif isinstance(work, dict):
				self.process_callback(work)
			else:
				process_single_video_id(account_id=self.account_id,
										video_id=work,
										cms_obj=self.cms_obj,
										process_callback=self.process_callback)

			self.queue.task_done()

#===========================================
# this is the main loop to process videos
#===========================================
def process_input(inputfile:str=None, process_callback:Callable[[Dict[Any, Any]], None]=list_videos, video_id:str=None) -> bool:
	# get the account info and credentials
	try:
		account_id, client_id, client_secret, opts = LoadAccountInfo(inputfile)
	except Exception as e:
		print(e)
		return False

	if None in [account_id, client_id, client_secret, opts]:
		return False

	# update account ID if passed in command line
	account_id = GetArgs().t or account_id

	GetOAuth(account_id, client_id, client_secret)
	GetCMS(oauth=GetOAuth(), query=GetArgs().q)
	GetDI(oauth=GetOAuth())

	# if async is enabled use more than one thread
	max_threads = GetArgs().a or 1
	mac_logger.info(f'Using {max_threads} thread(s) for processing')

	#=========================================================
	#=========================================================
	# check if we should process a specific video ID
	#=========================================================
	#=========================================================
	if video_id:
		print(f'Processing video ID {video_id} now.')
		return process_single_video_id(account_id, video_id, GetCMS(), process_callback)

	# create the work queue because everything below uses it
	work_queue:Queue = Queue(maxsize=0)

	#=========================================================
	#=========================================================
	# check if we should process a given list of videos
	#=========================================================
	#=========================================================
	if GetArgs().x:
		video_list = videos_from_file(GetArgs().x)
	else:
		video_list = opts.get('video_ids')

	if video_list and video_list[0] != 'all':
		num_videos = len(video_list)
		eprint(f'Found {num_videos} videos in options file. Processing them now.')
		# let's put all video IDs in a queue
		for video_id in video_list:
			work_queue.put_nowait(video_id)
		# starting worker threads on queue processing
		num_threads = min(max_threads, num_videos)
		for _ in range(num_threads):
			work_queue.put_nowait("EXIT")
			Worker(	q=work_queue,
					cms_obj=GetCMS(),
					account_id=account_id,
					process_callback=process_callback).start()
		# now we wait until the queue has been processed
		if not work_queue.empty():
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
	for _ in range(max_threads):
		Worker(q=work_queue, cms_obj=GetCMS(), account_id=account_id, process_callback=process_callback).start()

	# first wait for the queue filling thread to finish
	account_page_thread.join()

	# once the queue is filled with videos add exit signals
	for _ in range(max_threads):
		work_queue.put_nowait("EXIT")

	# now we wait until the queue has been processed
	if not work_queue.empty():
		work_queue.join()

	return True

#===========================================
# parse args and do the thing
#===========================================
def main(process_func:Callable[[Dict[Any, Any]], None]) -> None:
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

	if GetArgs().d:
		logging.basicConfig(level=logging.INFO, format='[%(levelname)s:%(lineno)d]: %(message)s')
		mac_logger.info('Logging at INFO level enabled')
	else:
		logging.basicConfig(level=logging.CRITICAL, format='[%(levelname)s:%(lineno)d]: %(message)s')

	# go through the library and do stuff
	process_input(inputfile=GetArgs().i, process_callback=process_func, video_id=GetArgs().v)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	print('video_id, title')
	main(list_videos)
