from .Base import Base
from .OAuth import OAuth
from typing import Callable, Tuple, Union, Optional, Dict, Any

class Social(Base):

	base_url = 'https://edge.social.api.brightcove.com/v1/accounts/{account_id}'

	def __init__(self, oauth:OAuth, query:Optional[str]=None):
		super().__init__(oauth=oauth, query=query)

	def ListStatusForVideos(self, search_query=None, account_id=None):
		account_id = account_id or self.oauth.account_id
		search_query = search_query or self.search_query
		headers = self.oauth.get_headers()
		url = (Social.base_url+'/videos/status?{query_string}').format(account_id=account_id, query_string=search_query)
		return self.session.get(url, headers=headers)

	def ListStatusForVideo(self, video_id, search_query=None, account_id=None):
		account_id = account_id or self.oauth.account_id
		search_query = search_query or self.search_query
		headers = self.oauth.get_headers()
		url = (Social.base_url+'/videos/{video_id}/status?{query_string}').format(account_id=account_id, video_id=video_id, query_string=search_query)
		return self.session.get(url, headers=headers)

	def ListHistoryForVideos(self, search_query=None, account_id=None):
		account_id = account_id or self.oauth.account_id
		search_query = search_query or self.search_query
		headers = self.oauth.get_headers()
		url = (Social.base_url+'/videos/history?{query_string}').format(account_id=account_id, query_string=search_query)
		return self.session.get(url, headers=headers)

	def ListHistoryForVideo(self, video_id, search_query=None, account_id=None):
		account_id = account_id or self.oauth.account_id
		search_query = search_query or self.search_query
		headers = self.oauth.get_headers()
		url = (Social.base_url+'/videos/{video_id}/history?{query_string}').format(account_id=account_id, video_id=video_id, query_string=search_query)
		return self.session.get(url, headers=headers)
