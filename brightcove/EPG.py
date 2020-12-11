from .Base import Base
from .OAuth import OAuth
from requests.models import Response

class EPG(Base):
	base_url ='https://cm.cloudplayout.brightcove.com/accounts/{account_id}'

	def __init__(self, oauth:OAuth, query:str='') -> None:
		super().__init__(oauth=oauth, query=query)

	def GetAllCPChannels(self, account_id:str='') -> Response:
		url = f'{EPG.base_url}/cp_channels'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url=url, headers=self.oauth.get_headers())

	def GetEPG(self, channel_id:str, query:str='', account_id:str='') -> Response:
		base = 'https://sm.cloudplayout.brightcove.com/accounts/{account_id}'
		query = query or self.search_query
		url = f'{base}/channels/{channel_id}/epg?{query}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url=url, headers=self.oauth.get_headers())
