"""
Implements wrapper class and methods to work with Brightcove's Social API.

See: https://social.support.brightcove.com/develop/overview-social-api.html
"""

from requests.models import Response
from .Base import Base
from .OAuth import OAuth

class Social(Base):
	"""
	Class to wrap the Brightcove Social API calls. Inherits from Base.

	Attributes:
	-----------
	base_url (str)
		Base URL for API calls.

	Methods:
	--------
	ListStatusForVideos(self, search_query: str='', account_id: str='') -> Response
		Gets the current status of every video Social has ever attempted to distribute to
		a social platform. Note that this endpoint has pagination.

	ListStatusForVideo(self, video_id: str, search_query: str='', account_id: str='') -> Response
		Gets the current status of the requested video for every Social Destination is has ever
		been distributed to. Note that this endpoint has pagination

	ListHistoryForVideos(self, search_query: str='', account_id: str='') -> Response
		Gets the lifetime history of every video Social has ever attempted to distribute to a social
		platform. Note that this endpoint has pagination.

	ListHistoryForVideo(self, video_id: str, search_query: str='', account_id: str='') -> Response
		Gets the lifetime history of the requested video for every Social Destination is has ever
		been distributed to. Note that this endpoint has pagination.
	"""

	# base URL for all API calls
	base_url = 'https://edge.social.api.brightcove.com/v1/accounts/{account_id}'

	def __init__(self, oauth: OAuth, query: str='') -> None:
		"""
		Args:
			oauth (OAuth): OAuth instance to use for the API calls.
			query (str, optional): Query string to be used by API calls. Defaults to ''.
		"""
		super().__init__(oauth=oauth, query=query)

	def ListStatusForVideos(self, search_query: str='', account_id: str='') -> Response:
		"""
		Gets the current status of every video Social has ever attempted to distribute to
		a social platform. Note that this endpoint has pagination.

		Args:
			search_query (str, optional): Search query and URL parameters for API call. Defaults to ''.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		search_query = search_query or self.search_query
		url = f'{self.base_url}/videos/status?{search_query}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def ListStatusForVideo(self, video_id: str, search_query: str='', account_id: str='') -> Response:
		"""
		Gets the current status of the requested video for every Social Destination is has ever
		been distributed to. Note that this endpoint has pagination

		Args:
			video_id (str): Video ID to get status for.
			search_query (str, optional): Search query and URL parameters for API call. Defaults to ''.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		search_query = search_query or self.search_query
		url = f'{self.base_url}/videos/{video_id}/status?{search_query}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def ListHistoryForVideos(self, search_query: str='', account_id: str='') -> Response:
		"""
		Gets the lifetime history of every video Social has ever attempted to distribute to a social
		platform. Note that this endpoint has pagination.

		Args:
			search_query (str, optional): Search query and URL parameters for API call. Defaults to ''.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		search_query = search_query or self.search_query
		url = f'{self.base_url}/videos/history?{search_query}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def ListHistoryForVideo(self, video_id: str, search_query: str='', account_id: str='') -> Response:
		"""
		Gets the lifetime history of the requested video for every Social Destination is has ever
		been distributed to. Note that this endpoint has pagination.

		Args:
			video_id (str): Video ID to get history for.
			search_query (str, optional): Search query and URL parameters for API call. Defaults to ''.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		search_query = search_query or self.search_query
		url = f'{self.base_url}/videos/{video_id}/history?{search_query}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)
