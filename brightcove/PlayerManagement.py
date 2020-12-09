from .Base import Base
from .OAuth import OAuth

class PlayerManagement(Base):

	base_url = 'https://players.api.brightcove.com/v2/accounts/{account_id}'

	def __init__(self, oauth:OAuth) -> None:
		super().__init__(oauth=oauth)

	def GetListOfPlayers(self, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (PlayerManagement.base_url+'/players').format(account_id=account_id)
		return self.session.get(url, headers=headers)

	def GetSinglePlayer(self, account_id=None, player_id=None):
		account_id = account_id or self.oauth.account_id
		player_id = player_id or 'default'
		headers = self.oauth.get_headers()
		url = (PlayerManagement.base_url+'/players/{playerid}').format(account_id=account_id, playerid=player_id)
		return self.session.get(url, headers=headers)

	def CreatePlayer(self, json_body, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (PlayerManagement.base_url+'/players').format(account_id=account_id)
		return self.session.post(url, headers=headers, data=self._json_to_string(json_body))

	def DeletePlayer(self, player_id, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (PlayerManagement.base_url+'/players/{playerid}').format(account_id=account_id, playerid=player_id)
		return self.session.delete(url, headers=headers)

	def PublishPlayer(self, player_id=None, account_id=None):
		account_id = account_id or self.oauth.account_id
		player_id = player_id or 'default'
		headers = self.oauth.get_headers()
		url = (PlayerManagement.base_url+'/players/{playerid}/publish').format(account_id=account_id, playerid=player_id)
		return self.session.post(url, headers=headers)

	def UpdatePlayer(self, player_id, json_body, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (PlayerManagement.base_url+'/players/{playerid}').format(account_id=account_id, playerid=player_id)
		return self.session.patch(url, headers=headers, data=self._json_to_string(json_body))

	def GetPlayerConfiguration(self, player_id, branch, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (PlayerManagement.base_url+'/players/{playerid}/configuration/{branch}').format(account_id=account_id, playerid=player_id, branch=branch)
		return self.session.get(url, headers=headers)

	def UpdatePlayerConfiguration(self, player_id, json_body, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (PlayerManagement.base_url+'/players/{playerid}/configuration').format(account_id=account_id, playerid=player_id)
		return self.session.patch(url, headers=headers, data=self._json_to_string(json_body))

	def GetAllPlugins(self, template_version=None):
		headers = self.oauth.get_headers()
		if template_version:
			query = '?template_version='+template_version
		else:
			query = ''
		url = 'https://players.api.brightcove.com/v2/plugins'+query
		return self.session.get(url, headers=headers)

	def GetSinglePlugin(self, plugin_id):
		headers = self.oauth.get_headers()
		if plugin_id:
			plugin_id = plugin_id.replace('@', '%40')
			plugin_id = plugin_id.replace('/', '%2F')
		else:
			plugin_id = ''
		url = 'https://players.api.brightcove.com/v2/plugins/'+plugin_id
		return self.session.get(url, headers=headers)

	def GetAllEmbeds(self, player_id, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (PlayerManagement.base_url+'/players/{playerid}/embeds').format(account_id=account_id, playerid=player_id)
		return self.session.get(url, headers=headers)

	def GetEmbed(self, player_id, embed_id, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (PlayerManagement.base_url+'/players/{playerid}/embeds/{embedid}').format(account_id=account_id, playerid=player_id, embedid=embed_id)
		return self.session.get(url, headers=headers)
