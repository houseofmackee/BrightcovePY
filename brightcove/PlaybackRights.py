"""
Implements wrapper class and methods to work with Brightcove's Playback Rights API.

See: https://apis.support.brightcove.com/playback-rights/references/reference.html
"""

from typing import Union
from requests.models import Response
from .Base import Base
from .OAuth import OAuth

class PlaybackRights(Base):
	"""
	Class to wrap the Brightcove Playback Rights API calls. Inherits from Base.

	Attributes:
	-----------
	base_url (str)
		Base URL for API calls.

	Methods:
	--------
	GetPlaybackRights(self, account_id: str='') -> Response
		Get all Playback Rights for an account.

	CreatePlaybackRight(self, json_body: Union[str, dict], account_id: str='') -> Response
		Create a new Playback Right.

	GetPlaybackRight(self, playback_rights_id: str, account_id: str='') -> Response
		Get a specific Playback Right for an account.

	UpdatePlaybackRight(self, playback_rights_id: str, json_body: Union[str, dict], account_id: str='') -> Response
		Update a specific Playback Right for an account.

	DeletePlaybackRight(self, playback_rights_id: str, account_id: str='') -> Response
		Delete a specific Playback Right.
	"""

	# base URL for all API calls
	base_url ='https://playback-rights.api.brightcove.com/v1/accounts/{account_id}'

	def __init__(self, oauth: OAuth) -> None:
		"""
		Args:
			oauth (OAuth): OAuth instance to use for the API calls.
		"""
		super().__init__(oauth=oauth)

	def GetPlaybackRights(self, account_id: str='') -> Response:
		"""
		Get all Playback Rights for an account.

		Args:
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/playback_rights'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url=url, headers=self.oauth.headers)

	def CreatePlaybackRight(self, json_body: Union[str, dict], account_id: str='') -> Response:
		"""
		Create a new Playback Right.

		Args:
			json_body (Union[str, dict]): JSON data with Playback Right metadata.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/playback_rights'.format(account_id=account_id or self.oauth.account_id)
		return self.session.post(url=url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def GetPlaybackRight(self, playback_rights_id: str, account_id: str='') -> Response:
		"""
		Get a specific Playback Right for an account.

		Args:
			playback_rights_id (str): The Playback Right ID to retrieve.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/playback_rights/{playback_rights_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url=url, headers=self.oauth.headers)

	def UpdatePlaybackRight(self, playback_rights_id: str, json_body: Union[str, dict], account_id: str='') -> Response:
		"""
		Update a specific Playback Right for an account.

		Args:
			playback_rights_id (str): The Playback Right ID to update.
			json_body (Union[str, dict]): JSON data with Playback Right metadata.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/playback_rights/{playback_rights_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.put(url=url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def DeletePlaybackRight(self, playback_rights_id: str, account_id: str='') -> Response:
		"""
		Delete a specific Playback Right.

		Args:
			playback_rights_id (str): The Playback Right ID to delete.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/playback_rights/{playback_rights_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.delete(url=url, headers=self.oauth.headers)
