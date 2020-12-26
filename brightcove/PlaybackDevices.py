"""
Implements wrapper class and methods to work with Brightcove's Playback Devices API.

See: https://apis.support.brightcove.com/playback-rights/references/devices-api/reference.html#tag/Devices
"""

from typing import Union
from requests.models import Response
from .Base import Base
from .OAuth import OAuth

class PlaybackDevices(Base):
	"""
	Class to wrap the Brightcove Playback Devices API calls. Inherits from Base.

	Attributes:
	-----------
	base_url (str)
		Base URL for API calls.

	Methods:
	--------
	GetAllUserDevices(self, user_id: str, account_id: str='') -> Response
		Get all user devices.

	DeleteAllUserDevices(self, user_id: str, account_id: str='') -> Response
		Delete all user devices.

	UpdateUserDevice(self, user_id: str, device_id: str, json_body: Union[str, dict], account_id: str='') -> Response
		Lets you set a descriptive name for the device.

	DeleteUserDevice(self, user_id: str, device_id: str, account_id: str='') -> Response
		Delete a specific user device.
	"""

	# base URL for all API calls
	base_url ='https://playback-auth.api.brightcove.com/v1/accounts/{account_id}'

	def __init__(self, oauth: OAuth) -> None:
		"""
		Args:
			oauth (OAuth): OAuth instance to use for the API calls.
		"""
		super().__init__(oauth=oauth)

	def GetAllUserDevices(self, user_id: str, account_id: str='') -> Response:
		"""
		Get all user devices.

		Args:
			user_id (str): User unique ID.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/users/{user_id}/devices'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url=url, headers=self.oauth.headers)

	def DeleteAllUserDevices(self, user_id: str, account_id: str='') -> Response:
		"""
		Delete all user devices.

		Args:
			user_id (str): User unique ID.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/users/{user_id}/devices'.format(account_id=account_id or self.oauth.account_id)
		return self.session.delete(url=url, headers=self.oauth.headers)

	def UpdateUserDevice(self, user_id: str, device_id: str, json_body: Union[str, dict], account_id: str='') -> Response:
		"""
		Lets you set a descriptive name for the device.

		Args:
			user_id (str): User unique ID.
			device_id (str): End user device unique ID.
			json_body (Union[str, dict]): JSON data with new device name.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/users/{user_id}/devices/{device_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.patch(url=url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def DeleteUserDevice(self, user_id: str, device_id: str, account_id: str='') -> Response:
		"""
		Delete a specific user device.

		Args:
			user_id (str): User unique ID.
			device_id (str): End user device unique ID.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/users/{user_id}/devices/{device_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.delete(url=url, headers=self.oauth.headers)
