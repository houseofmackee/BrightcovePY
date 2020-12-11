"""
Implements wrapper class and methods to work with Brightcove's Playback Authentication API.

See: https://general.support.brightcove.com/developer/create-jwt.html
"""

from requests.models import Response
from .Base import Base
from .OAuth import OAuth

class JWT(Base):
	"""
	Class to wrap the Brightcove JWT API calls. Inherits from Base.

	Methods:
	--------
	RegisterKey(self, key_data:str, account_id:str='') -> Response
		Put the a public key on the account. You can find the key in the public_key.txt file.

	ListKeys(self, account_id:str='') -> Response
		Get a list of public keys in account.

	GetKey(self, key_id:str, account_id:str='') -> Response
		Get the details for a public key in account.

	DeleteKey(self, key_id:str, account_id:str='') -> Response
		Delete a public key in account.
	"""

	base_url = 'https://playback-auth.api.brightcove.com/v1/accounts/{account_id}'

	def __init__(self, oauth:OAuth) -> None:
		super().__init__(oauth=oauth)

	def RegisterKey(self, key_data:str, account_id:str='') -> Response:
		"""
		Put the a public key on the account. You can find the key in the public_key.txt file.

		Args:
			key_data (str): Public key as str.
			account_id (str, optional): Account ID to get key from. Defaults to ''.

		Returns:
			Response: API resonse as requests Response object.
		"""

		url = f'{JWT.base_url}/keys'.format(account_id=account_id or self.oauth.account_id)
		json_body = { "value": key_data }
		return self.session.post(url, headers=self.oauth.get_headers(), data=self._json_to_string(json_body))

	def ListKeys(self, account_id:str='') -> Response:
		"""
		Get a list of public keys in account.

		Args:
			account_id (str, optional): Account ID to get key from. Defaults to ''.

		Returns:
			Response: API resonse as requests Response object.
		"""

		url = f'{JWT.base_url}/keys'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.get_headers())

	def GetKey(self, key_id:str, account_id:str='') -> Response:
		"""
		Get the details for a public key in account.

		Args:
			key_id (str): public key ID.
			account_id (str, optional): Account ID to get key from. Defaults to ''.

		Returns:
			Response: API resonse as requests Response object.
		"""

		url = f'{JWT.base_url}/keys/{key_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.get_headers())

	def DeleteKey(self, key_id:str, account_id:str='') -> Response:
		"""
		Delete a public key in account.

		Args:
			key_id (str): public key ID.
			account_id (str, optional): Account ID to get key from. Defaults to ''.

		Returns:
			Response: API resonse as requests Response object.
		"""

		url = f'{JWT.base_url}/keys/{key_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.delete(url, headers=self.oauth.get_headers())
