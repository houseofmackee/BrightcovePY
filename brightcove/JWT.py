from .Base import Base
from .OAuth import OAuth

class JWT(Base):

	base_url = 'https://playback-auth.api.brightcove.com/v1/accounts/{account_id}'

	def __init__(self, oauth:OAuth) -> None:
		super().__init__(oauth=oauth)

	def RegisterKey(self, key_data, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (JWT.base_url+'/keys').format(account_id=account_id)
		json_body = '{ "value":"'+key_data+'" }'
		return self.session.post(url, headers=headers, data=self._json_to_string(json_body))

	def ListKeys(self, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (JWT.base_url+'/keys').format(account_id=account_id)
		return self.session.get(url, headers=headers)

	def GetKey(self, key_id, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (JWT.base_url+'/keys/{keyid}').format(account_id=account_id,keyid=key_id)
		return self.session.get(url, headers=headers)

	def DeleteKey(self, key_id, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (JWT.base_url+'/keys/{keyid}').format(account_id=account_id,keyid=key_id)
		return self.session.delete(url, headers=headers)
