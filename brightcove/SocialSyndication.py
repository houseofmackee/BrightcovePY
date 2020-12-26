"""
Implements wrapper class and methods to work with Brightcove's Social Syndication API.

See: https://apis.support.brightcove.com/social-syndication/getting-started/public-syndication-api-overview.html
"""

from typing import Union
from requests.models import Response
from .Base import Base
from .OAuth import OAuth

class SocialSyndication(Base):
	"""
	Class to wrap the Brightcove Social Syndication API calls. Inherits from Base.

	Attributes:
	-----------
	base_url (str)
		Base URL for API calls.

	Methods:
	--------
	GetAllSyndications(self, account_id: str='') -> Response
		Gets a list of all syndications currently configured for the account.

	GetSyndication(self, syndication_id: str, account_id: str='') -> Response
		Gets the configuration data for a syndication.

	CreateSyndication(self, json_body: Union[str, dict], account_id: str='') -> Response
		Creates a new syndication.

	DeleteSyndication(self, syndication_id: str, account_id: str='') -> Response
		Deletes a syndication.

	UpdateSyndication(self, syndication_id: str, json_body: Union[str, dict], account_id: str='') -> Response
		Updates the configuration data for a syndication.

	GetTemplate(self, syndication_id: str, account_id: str='') -> Response
		Gets a universal syndication's custom feed template.

	UploadTemplate(self, syndication_id: str, json_body: Union[str, dict], account_id: str='') -> Response
		Uploads a custom feed template to a universal syndication.
	"""

	# base URL for all API calls
	base_url = 'https://social.api.brightcove.com/v1/accounts/{account_id}/mrss/syndications'

	def __init__(self, oauth: OAuth) -> None:
		"""
		Args:
			oauth (OAuth): OAuth instance to use for the API calls.
		"""
		super().__init__(oauth=oauth)

	def GetAllSyndications(self, account_id: str='') -> Response:
		"""
		Gets a list of all syndications currently configured for the account.

		Args:
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = (self.base_url).format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def GetSyndication(self, syndication_id: str, account_id: str='') -> Response:
		"""
		Gets the configuration data for a syndication.

		Args:
			syndication_id (str): Syndication ID to get config for.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/{syndication_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def CreateSyndication(self, json_body: Union[str, dict], account_id: str='') -> Response:
		"""
		Creates a new syndication.

		Args:
			json_body (Union[str, dict]): JSON body for the call.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = (self.base_url).format(account_id=account_id or self.oauth.account_id)
		return self.session.post(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def DeleteSyndication(self, syndication_id: str, account_id: str='') -> Response:
		"""
		Deletes a syndication.

		Args:
			syndication_id (str): Syndication ID to delete.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/{syndication_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.delete(url, headers=self.oauth.headers)

	def UpdateSyndication(self, syndication_id: str, json_body: Union[str, dict], account_id: str='') -> Response:
		"""
		Updates the configuration data for a syndication. A Syndication object specifying non-null values for
		writable fields to be updated should be passed as the request body. Note that the type property cannot
		be changed from the value specified when the syndication was created.

		Args:
			syndication_id (str): Syndication ID to update.
			json_body (Union[str, dict]): JSON body for the call.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/{syndication_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.patch(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def GetTemplate(self, syndication_id: str, account_id: str='') -> Response:
		"""
		Gets a universal syndication's custom feed template.

		Args:
			syndication_id (str): Syndication ID to get the tempate for.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/{syndication_id}/template'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def UploadTemplate(self, syndication_id: str, json_body: Union[str, dict], account_id: str='') -> Response:
		"""
		Uploads a custom feed template to a universal syndication.

		Args:
			syndication_id (str): Syndication ID to upload the template to.
			json_body (Union[str, dict]): JSON body for the call.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/{syndication_id}/template'.format(account_id=account_id or self.oauth.account_id)
		return self.session.put(url, headers=self.oauth.headers, data=self._json_to_string(json_body))
