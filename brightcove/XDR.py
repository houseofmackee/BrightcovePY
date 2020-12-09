from .Base import Base
from .OAuth import OAuth

class XDR(Base):

	base_url = 'https://data.brightcove.com/v1/xdr/accounts/{account_id}'

	def __init__(self, oauth:OAuth) -> None:
		super().__init__(oauth=oauth)

	def GetViewerPlayheads(self, viewer_id, limit:int=1000, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		limit = 1000 if (limit>10000 or limit<1) else limit
		url = (XDR.base_url+'/playheads/{viewerid}?limit={limit}').format(account_id=account_id, viewerid=viewer_id, limit=limit)
		return self.session.get(url=url, headers=headers)

	def GetViewerVideoPlayheads(self, viewer_id, video_id, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (XDR.base_url+'/playheads/{viewerid}/{video_id}').format(account_id=account_id, viewerid=viewer_id, video_id=video_id)
		return self.session.get(url=url, headers=headers)
