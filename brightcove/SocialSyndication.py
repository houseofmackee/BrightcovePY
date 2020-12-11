from requests.models import Response
from typing import Optional, Union
from .Base import Base
from .OAuth import OAuth

class SocialSyndication(Base):

	base_url = 'https://social.api.brightcove.com/v1/accounts/{account_id}/mrss/syndications'

	def __init__(self, oauth:OAuth) -> None:
		super().__init__(oauth=oauth)

	def GetAllSyndications(self, account_id:str='') -> Response:
		url = (SocialSyndication.base_url).format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.get_headers())

	def GetSyndication(self, syndication_id:str, account_id:str='') -> Response:
		url = f'{SocialSyndication.base_url}/{syndication_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.get_headers())

	def CreateSyndication(self, json_body:Union[str, dict], account_id:str='') -> Response:
		url = (SocialSyndication.base_url).format(account_id=account_id or self.oauth.account_id)
		return self.session.post(url, headers=self.oauth.get_headers(), data=self._json_to_string(json_body))

	def DeleteSyndication(self, syndication_id:str, account_id:str='') -> Response:
		url = f'{SocialSyndication.base_url}/{syndication_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.delete(url, headers=self.oauth.get_headers())

	def UpdateSyndication(self, syndication_id:str, json_body:Union[str, dict], account_id:str='') -> Response:
		url = f'{SocialSyndication.base_url}/{syndication_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.patch(url, headers=self.oauth.get_headers(), data=self._json_to_string(json_body))

	def GetTemplate(self, syndication_id:str, account_id:str='') -> Response:
		url = f'{SocialSyndication.base_url}/{syndication_id}/template'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.get_headers())

	def UploadTemplate(self, syndication_id:str, json_body:Union[str, dict], account_id:str='') -> Response:
		url = f'{SocialSyndication.base_url}/{syndication_id}/template'.format(account_id=account_id or self.oauth.account_id)
		return self.session.put(url, headers=self.oauth.get_headers(), data=self._json_to_string(json_body))
