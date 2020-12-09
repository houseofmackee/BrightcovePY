from .Base import Base
from .OAuth import OAuth

class EPG(Base):
	base_url ='https://cm.cloudplayout.brightcove.com/accounts/{account_id}'

	def __init__(self, oauth:OAuth, query=None) -> None:
		super().__init__(oauth=oauth, query=query)

	def GetAllCPChannels(self, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (EPG.base_url+'/cp_channels').format(account_id=account_id)
		return self.session.get(url=url, headers=headers)

	def GetEPG(self, channel_id, query=None, account_id=None):
		# https://sm.cloudplayout.brightcove.com/accounts/{account_id}/channels/{channel_id}/epg
		query = query or self.search_query
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (EPG.base_url+'/channels/{channel_id}/epg?{query}').format(account_id=account_id, channel_id=channel_id, query=query)
		return self.session.get(url=url, headers=headers)
