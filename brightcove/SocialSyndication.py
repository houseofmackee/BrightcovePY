from .Base import Base
from .OAuth import OAuth

class SocialSyndication(Base):

	base_url = 'https://social.api.brightcove.com/v1/accounts/{account_id}/mrss/syndications'

	def __init__(self, oauth:OAuth):
		super().__init__(oauth=oauth)

	def GetAllSyndications(self, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (SocialSyndication.base_url).format(account_id=account_id)
		return self.session.get(url, headers=headers)

	def GetSyndication(self, syndication_id, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (SocialSyndication.base_url+'/{syndicationid}').format(account_id=account_id, syndicationid=syndication_id)
		return self.session.get(url, headers=headers)

	def CreateSyndication(self, json_body, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (SocialSyndication.base_url).format(account_id=account_id)
		return self.session.post(url, headers=headers, data=self._json_to_string(json_body))

	def DeleteSyndication(self, syndication_id, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (SocialSyndication.base_url+'/{syndicationid}').format(account_id=account_id, syndicationid=syndication_id)
		return self.session.delete(url, headers=headers)

	def UpdateSyndication(self, syndication_id, json_body, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (SocialSyndication.base_url+'/{syndicationid}').format(account_id=account_id, syndicationid=syndication_id)
		return self.session.patch(url, headers=headers, data=self._json_to_string(json_body))

	def GetTemplate(self, syndication_id, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (SocialSyndication.base_url+'/{syndicationid}/template').format(account_id=account_id, syndicationid=syndication_id)
		return self.session.get(url, headers=headers)

	def UploadTemplate(self, syndication_id, json_body, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (SocialSyndication.base_url+'/{syndicationid}/template').format(account_id=account_id, syndicationid=syndication_id)
		return self.session.put(url, headers=headers, data=self._json_to_string(json_body))
