"""
Implements wrapper class and methods to work with Brightcove's EPG API.

See: https://apis.support.brightcove.com/epg/getting-started/overview-epg-api.html
"""

from requests.models import Response
from .Base import Base
from .OAuth import OAuth

class EPG(Base):
	"""
	Class to wrap the Brightcove EPG API calls. Inherits from Base.

	Attributes:
	-----------
	base_url (str)
		Base URL for API calls.

	Methods:
	--------
	GetAllCPChannels(self, account_id: str='') -> Response
		Get a list of all Cloud Playout channels for an account.

	GetEPG(self, channel_id: str, query: str='', account_id: str='') -> Response
		Get EPG for a specific channel.
	"""

	# base URL for all API calls
	base_url ='https://cm.cloudplayout.brightcove.com/accounts/{account_id}'

	def __init__(self, oauth: OAuth, query: str='') -> None:
		"""
		Args:
			oauth (OAuth): OAuth instance to use for the API calls.
			query (str, optional): Default search query for this instance.
		"""
		super().__init__(oauth=oauth, query=query)

	def GetAllCPChannels(self, account_id: str='') -> Response:
		"""
		Get a list of all Cloud Playout channels for an account.

		Args:
			account_id (str, optional): Video Cloud account ID. Defaults to ''

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/cp_channels'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url=url, headers=self.oauth.headers)

	def GetEPG(self, channel_id: str, query: str='', account_id: str='') -> Response:
		"""
		Get EPG for a specific channel.

		Args:
			channel_id (str): Channel ID to get the EPG for.
			query (str, optional): Search query string. Defaults to ''.
			account_id (str, optional): Video Cloud account ID. Defaults to ''

		Returns:
			Response: API response as requests Response object.
		"""
		base = 'https://sm.cloudplayout.brightcove.com/accounts/{account_id}'
		query = query or self.search_query
		url = f'{base}/channels/{channel_id}/epg?{query}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url=url, headers=self.oauth.headers)
