from typing import Callable, Tuple, Union, Optional, Dict, Any
from requests.models import Response
from .Base import Base
from .OAuth import OAuth

class CMS(Base):
	base_url = 'https://cms.api.brightcove.com/v1/accounts/{account_id}'

	def __init__(self, oauth:OAuth, query:str=''):
		super().__init__(oauth=oauth, query=query)

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
	def GetVideoCount(self, search_query:str='', account_id:str='') -> int:
		search_query = search_query or self.search_query
		url = f'{CMS.base_url}/videos/count?q={search_query}'.format(account_id=account_id or self.oauth.account_id)
		response = self.session.get(url, headers=self.oauth.get_headers())
		if response.status_code == 200:
			return int(response.json().get('count'))
		return -1

	#===========================================
	# create new video object in an account
	#===========================================
	def CreateVideo(self, video_title:str='Video Title', json_body:Optional[Union[dict,str]]=None, account_id:str='') -> Response:
		url = f'{CMS.base_url}/videos/'.format(account_id=account_id or self.oauth.account_id)
		json_body = json_body or { "name": video_title }
		return self.session.post(url=url, headers=self.oauth.get_headers(), data=self._json_to_string(json_body))

	#===========================================
	# get a video
	#===========================================
	def GetVideo(self, video_id:str, account_id:str='') -> Response:
		url = f'{CMS.base_url}/videos/{video_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url=url, headers=self.oauth.get_headers())

	#===========================================
	# get videos in an account
	#===========================================
	def GetVideos(self, page_size:int=20, page_offset:int=0, search_query:str='', account_id:str='') -> Response:
		search_query = search_query or self.search_query
		url = f'{CMS.base_url}/videos?limit={page_size}&offset={page_offset}&sort=created_at&q={search_query}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.get_headers())

	#===========================================
	# get light version of videos in an account
	#===========================================
	def GetLightVideos(self, page_size=20, page_offset=0, search_query:str='', account_id:str='') -> Response:
		search_query = search_query or self.search_query
		url = (CMS.base_url+'/lightvideos?limit={page_size}&offset={offset}&sort=created_at{query}').format(account_id=account_id or self.oauth.account_id, page_size=page_size, offset=page_offset, query='&q=' + search_query)
		return self.session.get(url, headers=self.oauth.get_headers())

	#===========================================
	# get a video's sources
	#===========================================
	def GetVideoSources(self, video_id:str, account_id:str='') -> Response:
		url = (CMS.base_url+'/videos/{video_id}/sources').format(account_id=account_id or self.oauth.account_id,video_id=video_id)
		return self.session.get(url=url, headers=self.oauth.get_headers())

	#===========================================
	# get a video's images
	#===========================================
	def GetVideoImages(self, video_id:str, account_id:str='') -> Response:
		url = (CMS.base_url+'/videos/{video_id}/images').format(account_id=account_id or self.oauth.account_id,video_id=video_id)
		return self.session.get(url=url, headers=self.oauth.get_headers())

	#===========================================
	# get a video's audio tracks
	#===========================================
	def GetVideoAudioTracks(self, video_id:str, account_id:str='') -> Response:
		url = (CMS.base_url+'/videos/{video_id}/audio_tracks').format(account_id=account_id or self.oauth.account_id,video_id=video_id)
		return self.session.get(url=url, headers=self.oauth.get_headers())

	#===========================================
	# get a specific audio track
	#===========================================
	def GetVideoAudioTrack(self, video_id:str, track_id, account_id:str='') -> Response:
		url = (CMS.base_url+'/videos/{video_id}/audio_tracks/{trackid}').format(account_id=account_id or self.oauth.account_id,video_id=video_id,trackid=track_id)
		return self.session.get(url=url, headers=self.oauth.get_headers())

	#===========================================
	# delete a specific audio track
	#===========================================
	def DeleteVideoAudioTrack(self, video_id:str, track_id, account_id:str='') -> Response:
		url = (CMS.base_url+'/videos/{video_id}/audio_tracks/{trackid}').format(account_id=account_id or self.oauth.account_id,video_id=video_id,trackid=track_id)
		return self.session.delete(url=url, headers=self.oauth.get_headers())

	#===========================================
	# update a specific audio track
	#===========================================
	def UpdateVideoAudioTrack(self, video_id:str, track_id, json_body, account_id:str='') -> Response:
		url = (CMS.base_url+'/videos/{video_id}/audio_tracks/{trackid}').format(account_id=account_id or self.oauth.account_id,video_id=video_id,trackid=track_id)
		return self.session.patch(url=url, headers=self.oauth.get_headers(), data=self._json_to_string(json_body))

	#===========================================
	# delete a video
	#===========================================
	def DeleteVideo(self, video_id:str, account_id:str='') -> Response:
		url = (CMS.base_url+'/videos/{video_id}').format(account_id=account_id or self.oauth.account_id,video_id=video_id)
		return self.session.delete(url=url, headers=self.oauth.get_headers())

	#===========================================
	# get a digital master info
	#===========================================
	def GetDigitalMasterInfo(self, video_id:str, account_id:str='') -> Response:
		url = (CMS.base_url+'/videos/{video_id}/digital_master').format(account_id=account_id or self.oauth.account_id,video_id=video_id)
		return self.session.get(url=url, headers=self.oauth.get_headers())

	#===========================================
	# delete a digital master
	#===========================================
	def DeleteMaster(self, video_id:str, account_id:str='') -> Response:
		url = (CMS.base_url+'/videos/{video_id}/digital_master').format(account_id=account_id or self.oauth.account_id,video_id=video_id)
		return self.session.delete(url=url, headers=self.oauth.get_headers())

	#===========================================
	# update a video
	#===========================================
	def UpdateVideo(self, video_id:str, json_body:Union[str, dict], account_id:str='') -> Response:
		url = (CMS.base_url+'/videos/{video_id}').format(account_id=account_id or self.oauth.account_id,video_id=video_id)
		return self.session.patch(url, headers=self.oauth.get_headers(), data=self._json_to_string(json_body))

	#===========================================
	# get custom fields
	#===========================================
	def GetCustomFields(self, account_id:str='') -> Response:
		url = (CMS.base_url+'/videos/video_fields').format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url=url, headers=self.oauth.get_headers())

	#===========================================
	# get ingest job status for a video
	#===========================================
	def GetStatusOfIngestJob(self, video_id:str, job_id:str, account_id:str='') -> Response:
		url = (CMS.base_url+'/videos/{video_id}/ingest_jobs/{jobid}').format(account_id=account_id or self.oauth.account_id,video_id=video_id,jobid=job_id)
		return self.session.get(url=url, headers=self.oauth.get_headers())

	#===========================================
	# get all ingest jobs status for a video
	#===========================================
	def GetStatusOfIngestJobs(self, video_id:str, account_id:str='') -> Response:
		url = (CMS.base_url+'/videos/{video_id}/ingest_jobs').format(account_id=account_id or self.oauth.account_id,video_id=video_id)
		return self.session.get(url=url, headers=self.oauth.get_headers())

	#===========================================
	# variants stuff
	#===========================================
	def GetAllVideoVariants(self, video_id:str, account_id:str='') -> Response:
		url = (CMS.base_url+'/videos/{video_id}/variants').format(account_id=account_id or self.oauth.account_id,video_id=video_id)
		return self.session.get(url=url, headers=self.oauth.get_headers())

	def CreateVideoVariant(self, video_id:str, json_body:Union[str, dict], account_id:str='') -> Response:
		url = (CMS.base_url+'/videos/{video_id}/variants').format(account_id=account_id or self.oauth.account_id,video_id=video_id)
		return self.session.post(url=url, headers=self.oauth.get_headers(), data=self._json_to_string(json_body))

	def GetVideoVariant(self, video_id:str, language:str, account_id:str='') -> Response:
		url = (CMS.base_url+'/videos/{video_id}/variants/{language}').format(account_id=account_id or self.oauth.account_id,video_id=video_id, language=language)
		return self.session.get(url=url, headers=self.oauth.get_headers())

	def UpdateVideoVariant(self, video_id:str, language:str, json_body:Union[str, dict], account_id:str='') -> Response:
		url = (CMS.base_url+'/videos/{video_id}/variants/{language}').format(account_id=account_id or self.oauth.account_id,video_id=video_id, language=language)
		return self.session.patch(url=url, headers=self.oauth.get_headers(), data=self._json_to_string(json_body))

	def DeleteVideoVariant(self, video_id:str, language:str, account_id:str='') -> Response:
		url = (CMS.base_url+'/videos/{video_id}/variants/{language}').format(account_id=account_id or self.oauth.account_id,video_id=video_id, language=language)
		return self.session.delete(url=url, headers=self.oauth.get_headers())

	#===========================================
	# subscriptions bla bla
	#===========================================
	def GetSubscriptionsList(self, account_id:str='') -> Response:
		url = (CMS.base_url+'/subscriptions').format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.get_headers())

	def GetSubscription(self, sub_id, account_id:str='') -> Response:
		url = (CMS.base_url+'/subscriptions/{subid}').format(account_id=account_id or self.oauth.account_id, subid=sub_id)
		return self.session.get(url, headers=self.oauth.get_headers())

	def CreateSubscription(self, callback_url, account_id:str='') -> Response:
		url = (CMS.base_url+'/subscriptions').format(account_id=account_id or self.oauth.account_id)
		json_body = ('{ "endpoint":"' + callback_url + '", "events":["video-change"] }')
		return self.session.post(url, headers=self.oauth.get_headers(), data=self._json_to_string(json_body))

	def DeleteSubscription(self, sub_id, account_id:str='') -> Response:
		url = (CMS.base_url+'/subscriptions/{subid}').format(account_id=account_id or self.oauth.account_id,subid=sub_id)
		return self.session.delete(url, headers=self.oauth.get_headers())

	#===========================================
	# folders stuff
	#===========================================
	def GetFolders(self, account_id:str='') -> Response:
		url = (CMS.base_url+'/folders').format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.get_headers())

	def CreateFolder(self, folder_name, account_id:str='') -> Response:
		url = (CMS.base_url+'/folders').format(account_id=account_id or self.oauth.account_id)
		json_body = ('{ "name":"' + folder_name + '" }')
		return self.session.post(url, headers=self.oauth.get_headers(), data=self._json_to_string(json_body))

	def DeleteFolder(self, folder_id, account_id:str='') -> Response:
		url = (CMS.base_url+'/folders/{folderid}').format(account_id=account_id or self.oauth.account_id, folderid=folder_id)
		return self.session.delete(url, headers=self.oauth.get_headers())

	def GetFolderInformation(self, folder_id, account_id:str='') -> Response:
		url = (CMS.base_url+'/folders/{folderid}').format(account_id=account_id or self.oauth.account_id, folderid=folder_id)
		return self.session.get(url, headers=self.oauth.get_headers())

	def UpdateFolderName(self, folder_id, folder_name, account_id:str='') -> Response:
		url = (CMS.base_url+'/folders/{folderid}').format(account_id=account_id or self.oauth.account_id, folderid=folder_id)
		json_body = ('{ "name":"' + folder_name + '" }')
		return self.session.patch(url, headers=self.oauth.get_headers(), data=self._json_to_string(json_body))

	def AddVideoToFolder(self, folder_id, video_id, account_id:str='') -> Response:
		url = (CMS.base_url+'/folders/{folderid}/videos/{video_id}').format(account_id=account_id or self.oauth.account_id, folderid=folder_id, video_id=video_id)
		return self.session.put(url, headers=self.oauth.get_headers())

	def RemoveVideoFromFolder(self, folder_id, video_id, account_id:str='') -> Response:
		url = (CMS.base_url+'/folders/{folderid}/videos/{video_id}').format(account_id=account_id or self.oauth.account_id, folderid=folder_id, video_id=video_id)
		return self.session.delete(url, headers=self.oauth.get_headers())

	def GetVideosInFolder(self, folder_id, page_size=100, page_offset=0, account_id:str='') -> Response:
		url = (CMS.base_url+'/folders/{folderid}/videos?limit={limit}&offset={offset}').format(account_id=account_id or self.oauth.account_id,folderid=folder_id,limit=page_size, offset=page_offset)
		return self.session.get(url, headers=self.oauth.get_headers())

	#===========================================
	# playlists stuff
	#===========================================
	def GetPlaylistsForVideo(self, video_id:str, account_id:str='') -> Response:
		url = (CMS.base_url+'/videos/{video_id}/references').format(account_id=account_id or self.oauth.account_id, video_id=video_id)
		return self.session.get(url, headers=self.oauth.get_headers())

	def RemoveVideoFromAllPlaylists(self, video_id:str, account_id:str='') -> Response:
		url = (CMS.base_url+'/videos/{video_id}/references').format(account_id=account_id or self.oauth.account_id, video_id=video_id)
		return self.session.delete(url, headers=self.oauth.get_headers())

	def GetVideosInPlaylist(self, playlist_id, include_details=True, account_id:str='') -> Response:
		url = (CMS.base_url+'/playlists/{playlistid}/videos?include_details={details}').format(account_id=account_id or self.oauth.account_id, playlistid=playlist_id, details=('false','true')[include_details])
		return self.session.get(url, headers=self.oauth.get_headers())

	def GetVideoCountInPlaylist(self, playlist_id, account_id:str='') -> Response:
		url = (CMS.base_url+'/counts/playlists/{playlistid}/videos').format(account_id=account_id or self.oauth.account_id, playlistid=playlist_id)
		return self.session.get(url, headers=self.oauth.get_headers())

	def DeletePlaylist(self, playlist_id, account_id:str='') -> Response:
		url = (CMS.base_url+'/playlists/{playlistid}').format(account_id=account_id or self.oauth.account_id, playlistid=playlist_id)
		return self.session.delete(url, headers=self.oauth.get_headers())

	def UpdatePlaylist(self, playlist_id, json_body, account_id:str='') -> Response:
		url = (CMS.base_url+'/playlists/{playlistid}').format(account_id=account_id or self.oauth.account_id, playlistid=playlist_id)
		return self.session.patch(url, headers=self.oauth.get_headers(), data=self._json_to_string(json_body))

	def GetPlaylistByID(self, playlist_id, account_id:str='') -> Response:
		url = (CMS.base_url+'/playlists/{playlistid}').format(account_id=account_id or self.oauth.account_id, playlistid=playlist_id)
		return self.session.get(url, headers=self.oauth.get_headers())

	def GetPlaylistCount(self, search_query:str='', account_id:str='') -> Response:
		search_query = search_query or self.search_query
		url = (CMS.base_url+'/counts/playlists?q={query}').format(account_id=account_id or self.oauth.account_id, query=search_query)
		return self.session.get(url, headers=self.oauth.get_headers())

	def GetPlaylists(self, sort='-updated_at', search_query:str='', page_size=100, page_offset=0, account_id:str='') -> Response:
		search_query = search_query or self.search_query
		if sort not in ['name', 'reference_id', 'created_at', 'published_at', 'updated_at', 'schedule.starts_at', 'schedule.ends_at', 'state', 'plays_total', 'plays_trailing_week', '-name', '-reference_id', '-created_at', '-published_at', '-updated_at', '-schedule.starts_at', '-schedule.ends_at', '-state', '-plays_total', '-plays_trailing_week']:
			sort = '-updated_at'
		url = (CMS.base_url+'/playlists?limit={limit}&offset={offset}&sort={sort}&q={query}').format(account_id=account_id or self.oauth.account_id, limit=page_size, offset=page_offset, sort=sort, query=search_query)
		return self.session.get(url, headers=self.oauth.get_headers())

	def CreatePlaylist(self, json_body, account_id:str='') -> Response:
		url = (CMS.base_url+'/playlists').format(account_id=account_id or self.oauth.account_id)
		return self.session.post(url, headers=self.oauth.get_headers(), data=self._json_to_string(json_body))

	#===========================================
	# Assets stuff
	#===========================================
	def GetDynamicRenditions(self, video_id:str, account_id:str='') -> Response:
		url = f'{CMS.base_url}/videos/{video_id}/assets/dynamic_renditions'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.get_headers())

	def GetRenditionList(self, video_id:str, account_id:str='') -> Response:
		url = f'{CMS.base_url}/videos/{video_id}/assets/renditions'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.get_headers())
