"""
Implements wrapper class and methods to work with Brightcove's Dynamic Ingest API.

See: https://apis.support.brightcove.com/dynamic-ingest/references/reference.html
"""

from typing import Callable, Optional
import functools
from requests.models import Response
import boto3
from .Base import Base
from .OAuth import OAuth
from .IngestProfiles import IngestProfiles
from .CMS import CMS
from .utils import empty_function

class DynamicIngest(Base):
    """
    Class to wrap the Brightcove Dynamic Ingest API calls. Inherits from Base.

    Attributes:
    -----------
    base_url (str)
        Base URL for API calls.

    Methods:
    --------
    _verify_profile(self, account_id: str, profile_id: str) -> str
        Checks and verifies that a profile ID exists in an account.

    SetIngestProfile(self, profile_id: str) -> str
        Sets the ingest profile which should be used as default for this DI instance.

    SetPriorityQueue(self, priority_queue: str) -> str
        Sets the priority queue which should be used as default for this DI instance.

    RetranscodeVideo(self, video_id: str, profile_id: str='', capture_images: bool=True, priority_queue: str='', callbacks: Optional[list]=None, account_id: str='') -> Response
        Trigger retranscode for a video using the digital master.

    SubmitIngest(self, video_id: str, source_url: str, capture_images: bool=True, priority_queue: str='', callbacks: Optional[list]=None, profile_id: str='', account_id: str='') -> Response
        Submits an ingest request to the Dynamic Ingest API.

    UploadFile(self, video_id: str, file_name: str, callback: Optional[Callable]=None, account_id: str='') -> dict
        Upload the contents of a local file to a temporary S3 bucket provided by Brightcove using
        the boto3 library to perform a multipart upload.
    """

    # base URL for all API calls
    base_url = 'https://ingest.api.brightcove.com/v1/accounts/{account_id}'

    def __init__(self, oauth: OAuth, ingest_profile: str='', priority_queue: str='normal') -> None:
        """
        Args:
            oauth (OAuth): OAuth instance to use for the API calls.
            ingest_profile (str, optional): Default ingest profile to use for ingests. Defaults to ''.
            priority_queue (str, optional): Default priority queue to use for ingests. Defaults to 'normal'.
        """
        super().__init__(oauth=oauth)
        self.__ip = IngestProfiles(oauth)
        self.__ingest_profile = self.SetIngestProfile(ingest_profile)
        self.__priority_queue = self.SetPriorityQueue(priority_queue)

    @functools.lru_cache()
    def _verify_profile(self, account_id: str, profile_id: str) -> str:
        """
        Checks and verifies that a profile ID exists in an account.

        Args:
            account_id (str): Account ID to check.
            profile_id (str): Profile ID to verify.

        Returns:
            str: Profile ID if valid, '' otherwise.
        """
        profile = self.__ingest_profile
        if profile_id and self.__ip.ProfileExists(account_id=account_id, profile_id=profile_id):
            profile = profile_id
        elif self.__ingest_profile=='':
            response = self.__ip.GetDefaultProfile(account_id=account_id)
            if response.status_code in DynamicIngest.success_responses:
                profile = response.json().get('default_profile_id')
        return profile

    def SetIngestProfile(self, profile_id: str) -> str:
        """
        Sets the ingest profile which should be used as default for this DI instance.

        Args:
            profile_id (str): Ingest profile ID or name.

        Returns:
            str: ID or name of profile which was actually set as default.
        """
        if profile_id and self.__ip.ProfileExists(account_id=self.oauth.account_id, profile_id=profile_id):
            self.__ingest_profile:str = profile_id
        else:
            self.__ingest_profile = ''
        return self.__ingest_profile

    def SetPriorityQueue(self, priority_queue: str) -> str:
        """
        Sets the priority queue which should be used as default for this DI instance.

        Args:
            priority_queue (str): Name of the priortity queue to use as default.

        Returns:
            str: Name of the priority queue which was actually set as default.
        """
        if priority_queue in ['low', 'normal', 'high']:
            self.__priority_queue:str = priority_queue
        else:
            self.__priority_queue = 'normal'
        return self.__priority_queue

    def RetranscodeVideo(self, video_id: str, profile_id: str='', capture_images: bool=True, priority_queue: str='', callbacks: Optional[list]=None, account_id: str='') -> Response:
        """
        Trigger retranscode for a video using the digital master.

        Args:
            video_id (str): Video ID to retranscode.
            profile_id (str, optional): Ingest profile to use for retranscode. Defaults to ''.
            capture_images (bool, optional): Flag to see if new images should be captured. Defaults to True.
            priority_queue (str, optional): Priority queue to use for retranscode. Defaults to ''.
            callbacks (Optional[list], optional): List of URLs to use for notification callbacks. Defaults to None.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        account_id = account_id or self.oauth.account_id
        url = f'{DynamicIngest.base_url}/videos/{video_id}/ingest-requests'.format(account_id=account_id)
        data = {
            'profile': self._verify_profile(account_id=account_id, profile_id=profile_id),
            'master': {
                'use_archived_master': True
            },
            'priority': priority_queue or self.__priority_queue,
            'capture-images': capture_images,
        }
        if callbacks:
            data['callbacks'] = callbacks

        return self.session.post(url=url, headers=self.oauth.headers, data=self._json_to_string(data))

    def SubmitIngest(self, video_id: str, source_url: str, capture_images: bool=True, priority_queue: str='', callbacks: Optional[list]=None, profile_id: str='', account_id: str='') -> Response:
        """
        Submits an ingest request to the Dynamic Ingest API.

        Args:
            video_id (str): Video ID to ingest video to.
            source_url (str): URL of the source video asset to ingest.
            capture_images (bool, optional): [description]. Defaults to True.
            capture_images (bool, optional): Flag to see if images should be captured. Defaults to True.
            priority_queue (str, optional): Priority queue to use for ingest. Defaults to ''.
            callbacks (Optional[list], optional): List of URLs to use for notification callbacks. Defaults to None.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        account_id = account_id or self.oauth.account_id
        url = f'{DynamicIngest.base_url}/videos/{video_id}/ingest-requests'.format(account_id=account_id)
        data = {
            'profile': self._verify_profile(account_id=account_id, profile_id=profile_id),
            'master': {
                'url': source_url
            },
            'priority': priority_queue or self.__priority_queue,
            'capture-images': capture_images,
        }
        if callbacks:
            data['callbacks'] = callbacks

        return self.session.post(url=url, headers=self.oauth.headers, data=self._json_to_string(data))

    def UploadFile(self, video_id: str, file_name: str, callback: Optional[Callable]=None, account_id: str='') -> dict:
        """
        Upload the contents of a local file to a temporary S3 bucket provided by Brightcove using
        the boto3 library to perform a multipart upload.

        Args:
            video_id (str): Video ID to use for upload.
            file_name (str): Path and name of file to upload.
            callback (Optional[Callable], optional): Callback function for progress reporting. Defaults to None.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            dict: Dictionary with the relevant URLs returned by the CMS API. Empty in case of an error.
        """
        url = f'{CMS.base_url}/videos/{video_id}/upload-urls/{file_name}'.format(account_id=account_id or self.oauth.account_id)
        response = self.session.get(url=url, headers=self.oauth.headers)
        if response.status_code in DynamicIngest.success_responses:
            upload_urls_response = response.json()
            try:
                s3 = boto3.resource('s3',
                    aws_access_key_id=upload_urls_response.get('access_key_id'),
                    aws_secret_access_key=upload_urls_response.get('secret_access_key'),
                    aws_session_token=upload_urls_response.get('session_token'))

                callback = callback or empty_function

                s3.Object(upload_urls_response.get('bucket'), upload_urls_response.get('object_key')).upload_file(file_name, Callback=callback)
                return upload_urls_response
            except Exception as e:
                print (e)
        return {}
