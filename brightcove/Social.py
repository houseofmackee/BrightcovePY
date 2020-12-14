from typing import Optional
from requests.models import Response
from .Base import Base
from .OAuth import OAuth

class Social(Base):

	base_url = 'https://edge.social.api.brightcove.com/v1/accounts/{account_id}'

	def __init__(self, oauth:OAuth, query:Optional[str]=None) -> None:
		super().__init__(oauth=oauth, query=query)

	def ListStatusForVideos(self, search_query:Optional[str]=None, account_id:str='') -> Response:
		search_query = search_query or self.search_query
		url = f'{Social.base_url}/videos/status?{search_query}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.get_headers())

	def ListStatusForVideo(self, video_id:str, search_query:Optional[str]=None, account_id:str='') -> Response:
		search_query = search_query or self.search_query
		url = f'{Social.base_url}/videos/{video_id}/status?{search_query}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.get_headers())

	def ListHistoryForVideos(self, search_query:Optional[str]=None, account_id:str='') -> Response:
		search_query = search_query or self.search_query
		url = f'{Social.base_url}/videos/history?{search_query}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.get_headers())

	def ListHistoryForVideo(self, video_id:str, search_query:Optional[str]=None, account_id:str='') -> Response:
		search_query = search_query or self.search_query
		url = f'{Social.base_url}/videos/{video_id}/history?{search_query}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.get_headers())
