from .Base import Base
from .OAuth import OAuth
from .IngestProfiles import IngestProfiles
from .CMS import CMS

import boto3

class DynamicIngest(Base):

	base_url = 'https://ingest.api.brightcove.com/v1/accounts/{account_id}'

	def __init__(self, oauth, ingest_profile=None, priority_queue='normal'):
		super().__init__(oauth=oauth)
		self.__previous_profile = None
		self.__previous_account = None
		self.__ip = IngestProfiles(oauth)
		self.SetIngestProfile(ingest_profile)
		self.SetPriorityQueue(priority_queue)

	def SetIngestProfile(self, profile_id):
		if self.__ip.ProfileExists(account_id=self.oauth.account_id, profile_id=profile_id):
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
		account_id = account_id or self.oauth.account_id

		profile = self.__ingest_profile
		if profile_id and self.__ip.ProfileExists(account_id=account_id, profile_id=profile_id):
			profile = profile_id
		elif self.__ingest_profile is None:
			r = self.__ip.GetDefaultProfile(account_id=account_id)
			if r.status_code in DynamicIngest.success_responses:
				profile = r.json().get('default_profile_id')

		priority = priority_queue or self.__priority_queue

		headers = self.oauth.get_headers()
		url = (DynamicIngest.base_url+'/videos/{video_id}/ingest-requests').format(account_id=account_id, video_id=video_id)
		data =	'{ "profile":"'+profile+'", "master": { "use_archived_master": true }, "priority": "'+priority+'","capture-images": '+str(capture_images).lower()+' }'
		return self.session.post(url=url, headers=headers, data=data)

	def SubmitIngest(self, video_id, source_url, capture_images=True, priority_queue=None, callbacks=None, ingest_profile=None, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
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
		account_id = account_id or self.oauth.account_id
		# Perform an authorized request to obtain a file upload location
		url = (CMS.base_url+'/videos/{video_id}/upload-urls/{sourcefilename}').format(account_id=account_id, video_id=video_id, sourcefilename=file_name)
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
