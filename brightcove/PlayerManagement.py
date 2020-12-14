"""
Implements wrapper class and methods to work with Brightcove's Player Management API.

See: https://apis.support.brightcove.com/player-management/
"""

from typing import Union
from requests.models import Response
from .Base import Base
from .OAuth import OAuth

class PlayerManagement(Base):

	base_url = 'https://players.api.brightcove.com/v2/accounts/{account_id}'

	def __init__(self, oauth:OAuth) -> None:
		super().__init__(oauth=oauth)

	def GetListOfPlayers(self, account_id:str='') -> Response:
		url = (PlayerManagement.base_url+'/players').format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.get_headers())

	def GetSinglePlayer(self, player_id:str, account_id:str='') -> Response:
		url = (PlayerManagement.base_url+'/players/{playerid}').format(account_id=account_id or self.oauth.account_id, playerid=player_id)
		return self.session.get(url, headers=self.oauth.get_headers())

	def CreatePlayer(self, json_body:Union[str, dict], account_id:str='') -> Response:
		url = (PlayerManagement.base_url+'/players').format(account_id=account_id or self.oauth.account_id)
		return self.session.post(url, headers=self.oauth.get_headers(), data=self._json_to_string(json_body))

	def DeletePlayer(self, player_id:str, account_id:str='') -> Response:
		url = (PlayerManagement.base_url+'/players/{playerid}').format(account_id=account_id or self.oauth.account_id, playerid=player_id)
		return self.session.delete(url, headers=self.oauth.get_headers())

	def PublishPlayer(self, player_id:str, account_id:str='') -> Response:
		url = (PlayerManagement.base_url+'/players/{playerid}/publish').format(account_id=account_id or self.oauth.account_id, playerid=player_id)
		return self.session.post(url, headers=self.oauth.get_headers())

	def UpdatePlayer(self, player_id:str, json_body:Union[str, dict], account_id:str='') -> Response:
		url = (PlayerManagement.base_url+'/players/{playerid}').format(account_id=account_id or self.oauth.account_id, playerid=player_id)
		return self.session.patch(url, headers=self.oauth.get_headers(), data=self._json_to_string(json_body))

	def GetPlayerConfiguration(self, player_id:str, branch:str, account_id:str='') -> Response:
		url = (PlayerManagement.base_url+'/players/{playerid}/configuration/{branch}').format(account_id=account_id or self.oauth.account_id, playerid=player_id, branch=branch)
		return self.session.get(url, headers=self.oauth.get_headers())

	def UpdatePlayerConfiguration(self, player_id:str, json_body:Union[str, dict], account_id:str='') -> Response:
		url = (PlayerManagement.base_url+'/players/{playerid}/configuration').format(account_id=account_id or self.oauth.account_id, playerid=player_id)
		return self.session.patch(url, headers=self.oauth.get_headers(), data=self._json_to_string(json_body))

	def GetAllPlugins(self, template_version:str='') -> Response:
		if template_version:
			template_version = f'?template_version={template_version}'
		url = f'https://players.api.brightcove.com/v2/plugins{template_version}'
		return self.session.get(url, headers=self.oauth.get_headers())

	def GetSinglePlugin(self, plugin_id:str) -> Response:
		if plugin_id:
			plugin_id = plugin_id.replace('@', '%40')
			plugin_id = plugin_id.replace('/', '%2F')
		url = f'https://players.api.brightcove.com/v2/plugins/{plugin_id}'
		return self.session.get(url, headers=self.oauth.get_headers())

	def GetAllEmbeds(self, player_id:str, account_id:str='') -> Response:
		url = (PlayerManagement.base_url+'/players/{playerid}/embeds').format(account_id=account_id or self.oauth.account_id, playerid=player_id)
		return self.session.get(url, headers=self.oauth.get_headers())

	def GetEmbed(self, player_id:str, embed_id:str, account_id:str='') -> Response:
		url = (PlayerManagement.base_url+'/players/{playerid}/embeds/{embedid}').format(account_id=account_id or self.oauth.account_id, playerid=player_id, embedid=embed_id)
		return self.session.get(url, headers=self.oauth.get_headers())
