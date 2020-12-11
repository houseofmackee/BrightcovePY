"""
Implements wrapper class and methods to work with Brightcove's Dynamic Ingest API.

See: https://apis.support.brightcove.com/dynamic-ingest/references/reference.html
"""

from .Base import Base
from .OAuth import OAuth
from .IngestProfiles import IngestProfiles
from .CMS import CMS
import functools
import boto3
from typing import Callable, Optional

class DynamicIngest(Base):

	base_url = 'https://ingest.api.brightcove.com/v1/accounts/{account_id}'

	def __init__(self, oauth:OAuth, ingest_profile:str='', priority_queue:str='normal') -> None:
		super().__init__(oauth=oauth)
		self.__ip = IngestProfiles(oauth)
		self.SetIngestProfile(ingest_profile)
		self.SetPriorityQueue(priority_queue)

	@functools.lru_cache()
	def _verify_profile(self, account_id:str, profile_id:str) -> str:
		profile = self.__ingest_profile
		if profile_id and self.__ip.ProfileExists(account_id=account_id, profile_id=profile_id):
			profile = profile_id
		elif self.__ingest_profile=='':
			r = self.__ip.GetDefaultProfile(account_id=account_id)
			if r.status_code in DynamicIngest.success_responses:
				profile = r.json().get('default_profile_id')
		return profile

	def SetIngestProfile(self, profile_id:str) -> str:
		if profile_id and self.__ip.ProfileExists(account_id=self.oauth.account_id, profile_id=profile_id):
			self.__ingest_profile:str = profile_id
		else:
			self.__ingest_profile = ''
		return self.__ingest_profile

	def SetPriorityQueue(self, priority_queue:str) -> str:
		if priority_queue in ['low', 'normal', 'high']:
			self.__priority_queue:str = priority_queue
		else:
			self.__priority_queue = 'normal'
		return self.__priority_queue

	def RetranscodeVideo(self, video_id:str, profile_id:str='', capture_images:bool=True, priority_queue:str='', callbacks:Optional[list]=None, account_id:str=''):
		account_id = account_id or self.oauth.account_id

		profile = self._verify_profile(account_id=account_id, profile_id=profile_id)
		priority = priority_queue or self.__priority_queue

		url = f'{DynamicIngest.base_url}/videos/{video_id}/ingest-requests'.format(account_id=account_id)
		data = {
			"profile": profile,
			"master": {
				"use_archived_master": True
			},
			"priority": priority,
			"capture-images": capture_images,
			"callbacks": callbacks
		}
		if not callbacks:
			data.pop('callbacks', None)

		return self.session.post(url=url, headers=self.oauth.get_headers(), data=self._json_to_string(data))

	def SubmitIngest(self, video_id:str, source_url:str, capture_images:bool=True, priority_queue:str='', callbacks:Optional[list]=None, profile_id:str='', account_id:str=''):
		account_id = account_id or self.oauth.account_id
		profile = self._verify_profile(account_id=account_id, profile_id=profile_id)

		priority = priority_queue or self.__priority_queue
		url = f'{DynamicIngest.base_url}/videos/{video_id}/ingest-requests'.format(account_id=account_id)
		data = {
			"profile": profile,
			"master": {
				"url": source_url
			},
			"priority": priority,
			"capture-images": capture_images,
			"callbacks": callbacks
		}
		if not callbacks:
			data.pop('callbacks', None)

		return self.session.post(url=url, headers=self.oauth.get_headers(), data=self._json_to_string(data))

	# get_upload_location_and_upload_file first performs an authenticated request to discover
	# a Brightcove-provided location to securely upload a source file
	def UploadFile(self, video_id:str, file_name:str, callback:Optional[Callable]=None, account_id:str=''):
		account_id = account_id or self.oauth.account_id
		# Perform an authorized request to obtain a file upload location
		url = f'{CMS.base_url}/videos/{video_id}/upload-urls/{file_name}'.format(account_id=account_id)
		r = self.session.get(url=url, headers=self.oauth.get_headers())
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
