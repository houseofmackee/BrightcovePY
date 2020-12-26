"""
Implements wrapper class and methods to work with Brightcove's Ingest Profiles API.

See: https://apis.support.brightcove.com/ingest-profiles/index.html
"""

from typing import Union, cast
from requests.models import Response
from .Base import Base
from .OAuth import OAuth

class IngestProfiles(Base):
	"""
	Class to wrap the Brightcove Ingest Profiles API calls. Inherits from Base.

	Attributes:
	-----------
	base_url (str)
		Base URL for API calls.

	Methods:
	--------
	GetDefaultProfile(self, account_id: str='') -> Response
		Gets the list of default profiles from an account.

	GetIngestProfile(self, profile_id: str, account_id: str='') -> Response
		Gets a specific ingest profile from an account.

	ProfileExists(self, profile_id: str, account_id: str='') -> bool
		Checks if a give ingest profile ID exists in an account.

	UpdateDefaultProfile(self, json_body: Union[str, dict], account_id: str='') -> Response
		Updates existing default profiles in an account.

	SetDefaultProfile(self, json_body: Union[str, dict], account_id: str='') -> Response
		Sets the default profiles in an account.

	DeleteIngestProfile(self, profile_id: str, account_id: str='') -> Response
		Deletes an ingest profile from an account.

	UpdateIngestProfile(self, profile_id: str, json_body: Union[str, dict], account_id: str='') -> Response
		Updates an existing ingest profile in an account.

	CreateIngestProfile(self, json_body: Union[str, dict], account_id: str='') -> Response
		Creates a new ingest profile in an account.

	GetAllIngestProfiles(self, account_id: str='') -> Response
		Get a list of all ingest profiles for an account.
	"""

	# base URL for all API calls
	base_url = 'https://ingestion.api.brightcove.com/v1/accounts/{account_id}'

	def __init__(self, oauth: OAuth) -> None:
		"""
		Args:
			oauth (OAuth): OAuth instance to use for the API calls.
		"""
		super().__init__(oauth=oauth)
		# cache for ProfileExists
		self.__previousProfile = ''
		self.__previousAccount = ''
		# cache for GetDefaultProfile
		self.__defaultProfileResponse = cast(Response, None)
		self.__defaultProfileAccount = ''
		# cache for GetProfile
		self.__getProfileAccount = ''
		self.__getProfileID = ''
		self.__getProfileResponse = cast(Response, None)

	def GetDefaultProfile(self, account_id: str='') -> Response:
		"""
		Gets the list of default profiles from an account.

		Args:
			account_id (str, optional): Account ID to get the ingest profiles from. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		# if it's not the same as before then find it and cache it
		account_id = account_id or self.oauth.account_id
		if account_id != self.__defaultProfileAccount:
			url = f'{self.base_url}/configuration'.format(account_id=account_id)
			self.__defaultProfileResponse = self.session.get(url=url, headers=self.oauth.headers)
			self.__defaultProfileAccount = account_id
		# return cached response
		return self.__defaultProfileResponse

	def GetIngestProfile(self, profile_id: str, account_id: str='') -> Response:
		"""
		Gets a specific ingest profile from an account.

		Args:
			profile_id (str): ID of ingest profile to retrieve.
			account_id (str, optional): Account ID to get the ingest profile from. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		# if it's not the same as before then find it and cache it
		account_id = account_id or self.oauth.account_id
		if self.__getProfileAccount != account_id or self.__getProfileID != profile_id:
			url = f'{self.base_url}/profiles/{profile_id}'.format(account_id=account_id)
			self.__getProfileID = profile_id
			self.__getProfileAccount = account_id
			self.__getProfileResponse = self.session.get(url=url, headers=self.oauth.headers)
		# return cached response
		return self.__getProfileResponse

	def ProfileExists(self, profile_id: str, account_id: str='') -> bool:
		"""
		Checks if a give ingest profile ID exists in an account.

		Args:
			profile_id (str): ID of ingest profile to check if it exists.
			account_id (str, optional): Account ID to check if profile exists. Defaults to ''.

		Returns:
			bool: True if ingest profile exists, False otherwise.
		"""
		# check if it's a valid cached account/profile combo
		account_id = account_id or self.oauth.account_id
		if self.__previousProfile == profile_id and self.__previousAccount == account_id:
			return True

		r = self.GetIngestProfile(account_id=account_id, profile_id=profile_id)
		if r.status_code in IngestProfiles.success_responses:
			self.__previousProfile = profile_id
			self.__previousAccount = account_id
			return True

		return False

	def UpdateDefaultProfile(self, json_body: Union[str, dict], account_id: str='') -> Response:
		"""
		Updates existing default profiles in an account.

		Args:
			json_body (Union[str, dict]): JSON data with all the info for the profiles.
			account_id (str, optional): Account ID to update the default profiles in. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		self.__previousProfile = self.__previousAccount = ''
		url = f'{self.base_url}/configuration'.format(account_id=account_id or self.oauth.account_id)
		return self.session.put(url=url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def SetDefaultProfile(self, json_body: Union[str, dict], account_id: str='') -> Response:
		"""
		Sets the default profiles in an account.

		Args:
			json_body (Union[str, dict]): JSON data with all the info for the profiles.
			account_id (str, optional): Account ID to set the default profiles in. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		self.__previousProfile = self.__previousAccount = ''
		url = f'{self.base_url}/configuration'.format(account_id=account_id or self.oauth.account_id)
		return self.session.post(url=url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def DeleteIngestProfile(self, profile_id: str, account_id: str='') -> Response:
		"""
		Deletes an ingest profile from an account.

		Args:
			profile_id (str): Ingest profile ID to delete.
			account_id (str, optional): Account ID to delete the ingest profile from. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		self.__previousProfile = self.__previousAccount = ''
		url = f'{self.base_url}/profiles/{profile_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.delete(url=url, headers=self.oauth.headers)

	def UpdateIngestProfile(self, profile_id: str, json_body: Union[str, dict], account_id: str='') -> Response:
		"""
		Updates an existing ingest profile in an account.

		Args:
			profile_id (str): Ingest profile ID to update.
			json_body (Union[str, dict]): JSON data with all the info for the profile.
			account_id (str, optional): Account ID to update the ingest profile in. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		self.__previousProfile = self.__previousAccount = ''
		url = f'{self.base_url}/profiles/{profile_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.put(url=url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def CreateIngestProfile(self, json_body: Union[str, dict], account_id: str='') -> Response:
		"""
		Creates a new ingest profile in an account.

		Args:
			json_body (Union[str, dict]): JSON data with all the info for the profile.
			account_id (str, optional): Account ID to create the ingest profile in. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/profiles'.format(account_id=account_id or self.oauth.account_id)
		return self.session.post(url=url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def GetAllIngestProfiles(self, account_id: str='') -> Response:
		"""
		Get a list of all ingest profiles for an account.

		Args:
			account_id (str, optional): Account ID to get the ingest profiles from. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/profiles'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url=url, headers=self.oauth.headers)
