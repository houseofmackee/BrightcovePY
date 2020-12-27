"""
Implements wrapper class and methods to work with Brightcove's CMS API.

See: https://apis.support.brightcove.com/cms/getting-started/overview-cms-api.html
"""

from typing import Union, Optional
from requests.models import Response
from .Base import Base
from .OAuth import OAuth

class CMS(Base):
	"""
	Class to wrap the Brightcove CMS API calls. Inherits from Base.

	Attributes:
	-----------
	base_url (str)
		Base URL for API calls.

	Methods:
	--------
	"""

	# base URL for API calls
	base_url = 'https://cms.api.brightcove.com/v1/accounts/{account_id}'

	def __init__(self, oauth: OAuth, query: str=''):
		"""
		Args:
			oauth (OAuth): OAuth instance to use for the API calls.
			query (str, optional): Query string to be used by API calls. Defaults to ''.
		"""
		super().__init__(oauth=oauth, query=query)

	#===========================================
	# get who created a video
	#===========================================
	@staticmethod
	def GetCreatedBy(video: dict) -> str:
		"""
		Gets creator of a video.

		Args:
			video (dict): Video object.

		Returns:
			str: name of the creator.
		"""
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
	def GetVideoCount(self, search_query: str='', account_id: str='') -> int:
		search_query = search_query or self.search_query
		url = f'{self.base_url}/videos/count?q={search_query}'.format(account_id=account_id or self.oauth.account_id)
		response = self.session.get(url, headers=self.oauth.headers)
		if response.status_code == 200:
			return int(response.json().get('count'))
		return -1

	#===========================================
	# create new video object in an account
	#===========================================
	def CreateVideo(self, video_title:str='Video Title', json_body:Optional[Union[dict,str]]=None, account_id:str='') -> Response:
		url = f'{self.base_url}/videos/'.format(account_id=account_id or self.oauth.account_id)
		json_body = json_body or { "name": video_title }
		return self.session.post(url=url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	#===========================================
	# get a video
	#===========================================
	def GetVideo(self, video_id:str, account_id:str='') -> Response:
		url = f'{self.base_url}/videos/{video_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url=url, headers=self.oauth.headers)

	#===========================================
	# get videos in an account
	#===========================================
	def GetVideos(self, page_size:int=20, page_offset:int=0, search_query:str='', account_id:str='') -> Response:
		search_query = search_query or self.search_query
		url = f'{self.base_url}/videos?limit={page_size}&offset={page_offset}&sort=created_at&q={search_query}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	#===========================================
	# get light version of videos in an account
	#===========================================
	def GetLightVideos(self, page_size=20, page_offset=0, search_query:str='', account_id:str='') -> Response:
		search_query = search_query or self.search_query
		url = (self.base_url+'/lightvideos?limit={page_size}&offset={offset}&sort=created_at{query}').format(account_id=account_id or self.oauth.account_id, page_size=page_size, offset=page_offset, query='&q=' + search_query)
		return self.session.get(url, headers=self.oauth.headers)

	#===========================================
	# get a video's sources
	#===========================================
	def GetVideoSources(self, video_id:str, account_id:str='') -> Response:
		url = (self.base_url+'/videos/{video_id}/sources').format(account_id=account_id or self.oauth.account_id,video_id=video_id)
		return self.session.get(url=url, headers=self.oauth.headers)

	#===========================================
	# get a video's images
	#===========================================
	def GetVideoImages(self, video_id:str, account_id:str='') -> Response:
		url = (self.base_url+'/videos/{video_id}/images').format(account_id=account_id or self.oauth.account_id,video_id=video_id)
		return self.session.get(url=url, headers=self.oauth.headers)

	#===========================================
	# get a video's audio tracks
	#===========================================
	def GetVideoAudioTracks(self, video_id:str, account_id:str='') -> Response:
		url = (self.base_url+'/videos/{video_id}/audio_tracks').format(account_id=account_id or self.oauth.account_id,video_id=video_id)
		return self.session.get(url=url, headers=self.oauth.headers)

	#===========================================
	# get a specific audio track
	#===========================================
	def GetVideoAudioTrack(self, video_id:str, track_id, account_id:str='') -> Response:
		url = (self.base_url+'/videos/{video_id}/audio_tracks/{trackid}').format(account_id=account_id or self.oauth.account_id,video_id=video_id,trackid=track_id)
		return self.session.get(url=url, headers=self.oauth.headers)

	#===========================================
	# delete a specific audio track
	#===========================================
	def DeleteVideoAudioTrack(self, video_id:str, track_id, account_id:str='') -> Response:
		url = (self.base_url+'/videos/{video_id}/audio_tracks/{trackid}').format(account_id=account_id or self.oauth.account_id,video_id=video_id,trackid=track_id)
		return self.session.delete(url=url, headers=self.oauth.headers)

	#===========================================
	# update a specific audio track
	#===========================================
	def UpdateVideoAudioTrack(self, video_id:str, track_id, json_body, account_id:str='') -> Response:
		url = (self.base_url+'/videos/{video_id}/audio_tracks/{trackid}').format(account_id=account_id or self.oauth.account_id,video_id=video_id,trackid=track_id)
		return self.session.patch(url=url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	#===========================================
	# delete a video
	#===========================================
	def DeleteVideo(self, video_id:str, account_id:str='') -> Response:
		url = (self.base_url+'/videos/{video_id}').format(account_id=account_id or self.oauth.account_id,video_id=video_id)
		return self.session.delete(url=url, headers=self.oauth.headers)

	#===========================================
	# get a digital master info
	#===========================================
	def GetDigitalMasterInfo(self, video_id:str, account_id:str='') -> Response:
		url = (self.base_url+'/videos/{video_id}/digital_master').format(account_id=account_id or self.oauth.account_id,video_id=video_id)
		return self.session.get(url=url, headers=self.oauth.headers)

	#===========================================
	# delete a digital master
	#===========================================
	def DeleteMaster(self, video_id:str, account_id:str='') -> Response:
		url = (self.base_url+'/videos/{video_id}/digital_master').format(account_id=account_id or self.oauth.account_id,video_id=video_id)
		return self.session.delete(url=url, headers=self.oauth.headers)

	#===========================================
	# update a video
	#===========================================
	def UpdateVideo(self, video_id:str, json_body:Union[str, dict], account_id:str='') -> Response:
		url = (self.base_url+'/videos/{video_id}').format(account_id=account_id or self.oauth.account_id,video_id=video_id)
		return self.session.patch(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	#===========================================
	# get custom fields
	#===========================================
	def GetCustomFields(self, account_id:str='') -> Response:
		url = (self.base_url+'/videos/video_fields').format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url=url, headers=self.oauth.headers)

	#===========================================
	# get ingest job status for a video
	#===========================================
	def GetStatusOfIngestJob(self, video_id:str, job_id:str, account_id:str='') -> Response:
		url = (self.base_url+'/videos/{video_id}/ingest_jobs/{jobid}').format(account_id=account_id or self.oauth.account_id,video_id=video_id,jobid=job_id)
		return self.session.get(url=url, headers=self.oauth.headers)

	#===========================================
	# get all ingest jobs status for a video
	#===========================================
	def GetStatusOfIngestJobs(self, video_id:str, account_id:str='') -> Response:
		url = (self.base_url+'/videos/{video_id}/ingest_jobs').format(account_id=account_id or self.oauth.account_id,video_id=video_id)
		return self.session.get(url=url, headers=self.oauth.headers)

	#===========================================
	# variants stuff
	#===========================================
	def GetAllVideoVariants(self, video_id:str, account_id:str='') -> Response:
		url = (self.base_url+'/videos/{video_id}/variants').format(account_id=account_id or self.oauth.account_id,video_id=video_id)
		return self.session.get(url=url, headers=self.oauth.headers)

	def CreateVideoVariant(self, video_id:str, json_body:Union[str, dict], account_id:str='') -> Response:
		url = (self.base_url+'/videos/{video_id}/variants').format(account_id=account_id or self.oauth.account_id,video_id=video_id)
		return self.session.post(url=url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def GetVideoVariant(self, video_id:str, language:str, account_id:str='') -> Response:
		url = (self.base_url+'/videos/{video_id}/variants/{language}').format(account_id=account_id or self.oauth.account_id,video_id=video_id, language=language)
		return self.session.get(url=url, headers=self.oauth.headers)

	def UpdateVideoVariant(self, video_id:str, language:str, json_body:Union[str, dict], account_id:str='') -> Response:
		url = (self.base_url+'/videos/{video_id}/variants/{language}').format(account_id=account_id or self.oauth.account_id,video_id=video_id, language=language)
		return self.session.patch(url=url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def DeleteVideoVariant(self, video_id:str, language:str, account_id:str='') -> Response:
		url = (self.base_url+'/videos/{video_id}/variants/{language}').format(account_id=account_id or self.oauth.account_id,video_id=video_id, language=language)
		return self.session.delete(url=url, headers=self.oauth.headers)

	#===========================================
	# subscriptions bla bla
	#===========================================
	#region subscriptions
	def GetSubscriptionsList(self, account_id: str='') -> Response:
		"""
		Get a list of all notification subscriptions for the account.

		Args:
			account_id (str, optional): Brightcove Account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/subscriptions'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def GetSubscription(self, sub_id: str, account_id: str='') -> Response:
		"""
		Get a notification subscription for the account.

		Args:
			sub_id (str): Subscription ID.
			account_id (str, optional): Brightcove Account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/subscriptions/{sub_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def CreateSubscription(self, callback_url: str, account_id: str='') -> Response:
		"""
		Establishes up to 10 endpoints that video changes should be sent to. Any change in video
		metadata will trigger a video change event and a notification - changes to assets used by
		the video will not trigger change events.

		Args:
			callback_url (str): The notifications endpoint URL.
			account_id (str, optional): Brightcove Account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/subscriptions'.format(account_id=account_id or self.oauth.account_id)
		json_body = { "endpoint": callback_url, "events": ["video-change"] }
		return self.session.post(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def DeleteSubscription(self, sub_id: str, account_id: str='') -> Response:
		"""
		Delete a notification subscription for the account.

		Args:
			sub_id (str): Subscription ID.
			account_id (str, optional): Brightcove Account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/subscriptions/{sub_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.delete(url, headers=self.oauth.headers)
	#endregion

	#===========================================
	# folders stuff
	#===========================================
	#region folders
	def GetFolders(self, account_id: str='') -> Response:
		"""
		Gets list of folders for the account.

		Args:
			account_id (str, optional): Brightcove Account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/folders'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def CreateFolder(self, folder_name: str, account_id: str='') -> Response:
		"""
		Create a new folder for the account.

		Args:
			folder_name (str): Name for the folder.
			account_id (str, optional): Brightcove Account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/folders'.format(account_id=account_id or self.oauth.account_id)
		json_body = { "name": folder_name }
		return self.session.post(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def GetFolderInformation(self, folder_id: str, account_id: str='') -> Response:
		"""
		Gets information about a folder.

		Args:
			folder_id (str): Folder ID.
			account_id (str, optional): Brightcove Account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/folders/{folder_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def UpdateFolderName(self, folder_id: str, folder_name: str, account_id: str='') -> Response:
		"""
		Update the folder name.

		Args:
			folder_id (str): Folder ID.
			folder_name (str): Name for the folder.
			account_id (str, optional): Brightcove Account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/folders/{folder_id}'.format(account_id=account_id or self.oauth.account_id)
		json_body = { "name": folder_name }
		return self.session.patch(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def DeleteFolder(self, folder_id: str, account_id: str='') -> Response:
		"""
		Delete a folder.

		Args:
			folder_id (str): Folder ID.
			account_id (str, optional): Brightcove Account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/folders/{folder_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.delete(url, headers=self.oauth.headers)

	def GetVideosInFolder(self, folder_id: str, page_size: int=20, page_offset: int=0, account_id: str='') -> Response:
		"""
		Gets list of video objects in a folder. This method uses pagination.

		Args:
			folder_id (str): Folder ID.
			page_size (int, optional): Number of items to return. Defaults to 20.
			page_offset (int, optional): Number of items to skip. Defaults to 0.
			account_id (str, optional): Brightcove Account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/folders/{folder_id}/videos?limit={page_size}&offset={page_offset}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def AddVideoToFolder(self, folder_id: str, video_id: str, account_id: str='') -> Response:
		"""
		Add a video to a folder.

		Args:
			folder_id (str): Folder ID.
			video_id (str): Video ID.
			account_id (str, optional): Brightcove Account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/folders/{folder_id}/videos/{video_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.put(url, headers=self.oauth.headers)

	def RemoveVideoFromFolder(self, folder_id: str, video_id: str, account_id: str='') -> Response:
		"""
		Remove a video from a folder.

		Args:
			folder_id (str): Folder ID.
			video_id (str): Video ID.
			account_id (str, optional): Brightcove Account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/folders/{folder_id}/videos/{video_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.delete(url, headers=self.oauth.headers)
	#endregion

	#===========================================
	# labels stuff
	#===========================================
	#region labels
	def CreateLabel(self, json_body: Union[str, dict], account_id: str='') -> Response:
		"""
		Create a new label for the account.

		Args:
			json_body (Union[str, dict]): JSON data with label info.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/labels'.format(account_id=account_id or self.oauth.account_id)
		return self.session.post(url=url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def GetLabels(self, account_id: str='') -> Response:
		"""
		Gets list of labels for the account.

		Args:
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/labels'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url=url, headers=self.oauth.headers)

	def UpdateLabel(self, label_path: str, json_body: Union[str, dict], account_id: str='') -> Response:
		"""
		Update a label for the account.

		Args:
			label_path (str): The path for a label to update or delete. Note that the operation performed
				is on the last item in the path, so for example, if you specify the path /nature/birds/seabirds,
				only the seabirds label will be updated/deleted, but if you specify the path as /nature/birds,
				birds and any sub-labels of birds will be updated/deleted.
			json_body (Union[str, dict]): JSON data with label info.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/labels/by_path/{label_path}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.patch(url=url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def DeleteLabel(self, label_path: str, account_id: str='') -> Response:
		"""
		Delete a label.

		Args:
			label_path (str): The path for a label to update or delete. Note that the operation performed
				is on the last item in the path, so for example, if you specify the path /nature/birds/seabirds,
				only the seabirds label will be updated/deleted, but if you specify the path as /nature/birds,
				birds and any sub-labels of birds will be updated/deleted.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/labels/by_path/{label_path}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.delete(url=url, headers=self.oauth.headers)
	#endregion

	#===========================================
	# playlists stuff
	#===========================================
	def GetPlaylistsForVideo(self, video_id:str, account_id:str='') -> Response:
		url = (self.base_url+'/videos/{video_id}/references').format(account_id=account_id or self.oauth.account_id, video_id=video_id)
		return self.session.get(url, headers=self.oauth.headers)

	def RemoveVideoFromAllPlaylists(self, video_id:str, account_id:str='') -> Response:
		url = (self.base_url+'/videos/{video_id}/references').format(account_id=account_id or self.oauth.account_id, video_id=video_id)
		return self.session.delete(url, headers=self.oauth.headers)

	def GetVideosInPlaylist(self, playlist_id, include_details=True, account_id:str='') -> Response:
		url = (self.base_url+'/playlists/{playlistid}/videos?include_details={details}').format(account_id=account_id or self.oauth.account_id, playlistid=playlist_id, details=('false','true')[include_details])
		return self.session.get(url, headers=self.oauth.headers)

	def GetVideoCountInPlaylist(self, playlist_id, account_id:str='') -> Response:
		url = (self.base_url+'/counts/playlists/{playlistid}/videos').format(account_id=account_id or self.oauth.account_id, playlistid=playlist_id)
		return self.session.get(url, headers=self.oauth.headers)

	def DeletePlaylist(self, playlist_id, account_id:str='') -> Response:
		url = (self.base_url+'/playlists/{playlistid}').format(account_id=account_id or self.oauth.account_id, playlistid=playlist_id)
		return self.session.delete(url, headers=self.oauth.headers)

	def UpdatePlaylist(self, playlist_id, json_body, account_id:str='') -> Response:
		url = (self.base_url+'/playlists/{playlistid}').format(account_id=account_id or self.oauth.account_id, playlistid=playlist_id)
		return self.session.patch(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def GetPlaylistByID(self, playlist_id, account_id:str='') -> Response:
		url = (self.base_url+'/playlists/{playlistid}').format(account_id=account_id or self.oauth.account_id, playlistid=playlist_id)
		return self.session.get(url, headers=self.oauth.headers)

	def GetPlaylistCount(self, search_query:str='', account_id:str='') -> Response:
		search_query = search_query or self.search_query
		url = (self.base_url+'/counts/playlists?q={query}').format(account_id=account_id or self.oauth.account_id, query=search_query)
		return self.session.get(url, headers=self.oauth.headers)

	def GetPlaylists(self, sort='-updated_at', search_query:str='', page_size=100, page_offset=0, account_id:str='') -> Response:
		search_query = search_query or self.search_query
		if sort not in ['name', 'reference_id', 'created_at', 'published_at', 'updated_at', 'schedule.starts_at', 'schedule.ends_at', 'state', 'plays_total', 'plays_trailing_week', '-name', '-reference_id', '-created_at', '-published_at', '-updated_at', '-schedule.starts_at', '-schedule.ends_at', '-state', '-plays_total', '-plays_trailing_week']:
			sort = '-updated_at'
		url = (self.base_url+'/playlists?limit={limit}&offset={offset}&sort={sort}&q={query}').format(account_id=account_id or self.oauth.account_id, limit=page_size, offset=page_offset, sort=sort, query=search_query)
		return self.session.get(url, headers=self.oauth.headers)

	def CreatePlaylist(self, json_body, account_id:str='') -> Response:
		url = (self.base_url+'/playlists').format(account_id=account_id or self.oauth.account_id)
		return self.session.post(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	#===========================================
	# Assets stuff
	#===========================================
	def GetDynamicRenditions(self, video_id:str, account_id:str='') -> Response:
		url = f'{self.base_url}/videos/{video_id}/assets/dynamic_renditions'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def GetRenditionList(self, video_id:str, account_id:str='') -> Response:
		url = f'{self.base_url}/videos/{video_id}/assets/renditions'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)
