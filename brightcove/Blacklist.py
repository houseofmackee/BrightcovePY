"""
Implements wrapper class and methods to work with Brightcove's Blacklist API.

See: https://apis.support.brightcove.com/playback-rights/references/blacklist-api/reference.html
"""

from requests.models import Response
from .Base import Base
from .OAuth import OAuth

class Blacklist(Base):
	"""
	Class to wrap the Brightcove Blacklist API calls. Inherits from Base.

	Attributes:
	-----------
	base_url (str)
		Base URL for API calls.

	Methods:
	--------
	GetCurrentBlacklist(self, account_id: str='') -> Response
		Get the JSON Web Tokens that are on the blacklist.

	CheckBlacklist(self, token: str, account_id: str='') -> Response
		Check if a JSON Web Token is on the blacklist.

	AddTokenToBlacklist(self, token: str, account_id: str='') -> Response
		Add a token to the blacklist to invalidate for license requests when using
		Brightcove's Playback Authorization Service.

	RemoveTokenFromBlacklist(self, token: str, account_id: str='') -> Response
		Remove a JSON Web Token from the blacklist.
	"""

	# base URL for all API calls
	base_url = 'https://playback-auth.api.brightcove.com/v1/accounts/{account_id}/blacklist'

	def __init__(self, oauth: OAuth) -> None:
		"""
		Args:
			oauth (OAuth): OAuth instance to use for the API calls.
		"""
		super().__init__(oauth=oauth)

	def GetCurrentBlacklist(self, account_id: str='') -> Response:
		"""
		Get the JSON Web Tokens that are on the blacklist.

		Args:
			account_id (str, optional): Brightcove Account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def CheckBlacklist(self, token: str, account_id: str='') -> Response:
		"""
		Check if a JSON Web Token is on the blacklist.

		Args:
			token (str): The entire encoded JSON Web Token string.
			account_id (str, optional): Brightcove Account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/tokens/{token}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def AddTokenToBlacklist(self, token: str, account_id: str='') -> Response:
		"""
		Add a token to the blacklist to invalidate for license requests when using
		Brightcove's Playback Authorization Service.

		Args:
			token (str): The entire encoded JSON Web Token string.
			account_id (str, optional): Brightcove Account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/tokens/{token}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.put(url, headers=self.oauth.headers)

	def RemoveTokenFromBlacklist(self, token: str, account_id: str='') -> Response:
		"""
		Remove a JSON Web Token from the blacklist.

		Args:
			token (str): The entire encoded JSON Web Token string.
			account_id (str, optional): Brightcove Account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/tokens/{token}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.delete(url, headers=self.oauth.headers)
