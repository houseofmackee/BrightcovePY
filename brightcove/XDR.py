"""
Implements wrapper class and methods to work with Brightcove's XDR API.

See: https://apis.support.brightcove.com/xdr/references/reference.html
"""

from requests.models import Response
from .Base import Base
from .OAuth import OAuth

class XDR(Base):
	"""
	Class to wrap the Brightcove XDR API calls. Inherits from Base.

	Methods:
	--------
	GetViewerPlayheads(self, viewer_id:str, limit:int=1000, account_id:Optional[str]=None) -> Response
		Get all playhead positions for a specific account and viewer.

	GetViewerVideoPlayheads(self, viewer_id:str, video_id:str, account_id:Optional[str]=None) -> Response
		Get the playhead(s) for all specified videos for a viewer.
	"""

	base_url = 'https://data.brightcove.com/v1/xdr/accounts/{account_id}'

	def __init__(self, oauth:OAuth) -> None:
		super().__init__(oauth=oauth)

	def GetViewerPlayheads(self, viewer_id:str, limit:int=1000, account_id:str='') -> Response:
		"""
		Get all playhead positions for a specific account and viewer.

		Args:
			viewer_id (str): ID of the viewer whose playheads are being retrieved.
			limit (int, optional): Number of results to return. Defaults to 1000.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API resonse as requests Response object.
		"""

		limit = 1000 if (limit>10000 or limit<1) else limit
		url = f'{XDR.base_url}/playheads/{viewer_id}?limit={limit}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url=url, headers=self.oauth.get_headers())

	def GetViewerVideoPlayheads(self, viewer_id:str, video_id:str, account_id:str='') -> Response:
		"""
		Get the playhead(s) for all specified videos for a viewer.

		Args:
			viewer_id (str): ID of the viewer whose playheads are being retrieved.
			video_id (str): ID(s) of the video(s) whose playheads are being retrieved. Comma-delimited for multiple video IDs. Up to 100 video IDs supported.
			account_id (str, optional): Video Cloud account ID. Defaults to ''

		Returns:
			Response: API resonse as requests Response object.
		"""

		url = f'{XDR.base_url}/playheads/{viewer_id}/{video_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url=url, headers=self.oauth.get_headers())
