"""
Implements wrapper class and methods to work with Brightcove's OAuth Token API.

See: https://apis.support.brightcove.com/player-management/
"""

import time
import requests

class OAuth():
	"""
	Implements wrapper class and methods to work with Brightcove's OAuth Token API.

	Attributes:
	-----------
	base_url (str)
		Base URL for API calls.

	Properties:
	-----------
	access_token(self) -> str:
		Gets stored access token for API calls. Refreshes it if it has expired.

	headers(self) -> dict:
		Gets authorization headers for http requests.
	"""

	# base URL for all API calls
	base_url = 'https://oauth.brightcove.com/v4/access_token'

	def __init__(self, account_id: str, client_id: str, client_secret: str) -> None:
		"""
		Args:
			account_id (str): Brightcove Account ID.
			client_id (str): Client ID.
			client_secret (str): Client Secret.
		"""
		self.account_id = account_id
		self.client_id = client_id
		self.client_secret = client_secret
		self.__access_token = ''
		self.__request_time = 0.0
		self.__token_life = 240.0

	def __get_access_token(self) -> str:
		"""
		Gets access token from API call and stores it along with the request time.
		"""
		access_token = ''
		response = requests.post(url=self.base_url, params='grant_type=client_credentials', auth=(self.client_id, self.client_secret))
		if response.status_code == 200:
			access_token = response.json().get('access_token','')
			self.__request_time = time.time()
		return access_token

	@property
	def access_token(self) -> str:
		"""
		Gets stored access token for API calls. Refreshes it if it has expired.
		"""
		if not self.__access_token:
			self.__access_token = self.__get_access_token()
		elif time.time()-self.__request_time > self.__token_life:
			self.__access_token = self.__get_access_token()
		return self.__access_token

	@property
	def headers(self) -> dict:
		"""
		Gets authorization headers for http requests.
		"""
		return { 'Authorization': f'Bearer {self.access_token}', 'Content-Type': 'application/json' }
