"""
Implements wrapper class and methods to work with Brightcove's Player Management API.

See: https://apis.support.brightcove.com/player-management/
"""

from typing import Union
from requests.models import Response
from .Base import Base
from .OAuth import OAuth

class PlayerManagement(Base):
	"""
	Class to wrap the Brightcove Player Management API calls. Inherits from Base.

	Attributes:
	-----------
	base_url (str)
		Base URL for API calls.

	Methods:
	--------
	GetListOfPlayers(self, account_id: str='') -> Response
		Get a list of players in an account.

	GetSinglePlayer(self, player_id: str, account_id: str='') -> Response
		Get a player by ID from an account.

	CreatePlayer(self, json_body: Union[str, dict], account_id: str='') -> Response
		Create a player.

	DeletePlayer(self, player_id: str, account_id: str='') -> Response
		Delete a player and all embeds associated with it.

	PublishPlayer(self, player_id: str, account_id: str='') -> Response
		Publish a player for optimization and production use.

	UpdatePlayer(self, player_id: str, json_body: Union[str, dict], account_id: str='') -> Response
		Update a single player.

	GetPlayerConfiguration(self, player_id: str, branch: str, account_id: str='') -> Response
		Get a preview or published player configuration.

	UpdatePlayerConfiguration(self, player_id: str, json_body: Union[str, dict], account_id: str='') -> Response
		Update a player configuration.

	GetAllPlugins(self, template_version: str='') -> Response
		Get all plugins from plugin registry.

	GetSinglePlugin(self, plugin_id: str) -> Response
		Get a single plugin from plugin registry.

	GetAllEmbeds(self, player_id: str, account_id: str='') -> Response
		Get all the embeds (child players) for a player.

	GetEmbed(self, player_id: str, embed_id: str, account_id: str='') -> Response
		Get a specific embed (child player) for a player.

	CreateEmbed(self, player_id: str, json_body: Union[str, dict], account_id: str='') -> Response
		Create an embed (child player) for a player.

	DeleteEmbed(self, player_id: str, embed_id: str, account_id: str='') -> Response
		Delete a particular embed (child player) for a player.

	GetPlayerEmbedConfiguration(self, player_id: str, embed_id: str, branch: str, account_id: str='') -> Response
		Get the configuration for an embed. You must specify the branch, either "master" or "preview".

	UpdateEmbedConfiguration(self, player_id: str, embed_id: str, json_body: Union[str, dict], account_id: str='', use_put: bool=False) -> Response
		Update the configuration for an embed.

	GetConfigurationCombinations(self, player_id: str, embed_id: str, query: str, account_id: str='') -> Response
		Retrieve the configuration for a parent/child combination of master and preview branches.
	"""

	# base URL for all API calls
	base_url = 'https://players.api.brightcove.com/v2/accounts/{account_id}'

	def __init__(self, oauth: OAuth) -> None:
		"""
		Args:
			oauth (OAuth): OAuth instance to use for the API calls.
		"""
		super().__init__(oauth=oauth)

	def GetListOfPlayers(self, account_id: str='') -> Response:
		"""
		Get a list of players in an account.

		Args:
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/players'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def GetSinglePlayer(self, player_id: str, account_id: str='') -> Response:
		"""
		Get a player by ID from an account.

		Args:
			player_id (str): Player ID to retrieve.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/players/{player_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def CreatePlayer(self, json_body: Union[str, dict], account_id: str='') -> Response:
		"""
		Create a player. The POST method creates a player by submitting a player configuration. The properties
		of Brightcove Player you can manipulate with player management are detailed in the API documentation.
		To create a player, a publisher must decide what properties the final player will have. If no properties
		are given at creation, a blank player will be created with only the base player skin applied to the
		player. A user may then use an HTTP PATCH method to update properties after the player has been created.

		Args:
			json_body (Union[str, dict]): JSON data with the player configuration.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/players'.format(account_id=account_id or self.oauth.account_id)
		return self.session.post(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def DeletePlayer(self, player_id: str, account_id: str='') -> Response:
		"""
		Delete a player and all embeds associated with it.

		Args:
			player_id (str): Player ID to delete.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/players/{player_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.delete(url, headers=self.oauth.headers)

	def PublishPlayer(self, player_id: str, account_id: str='') -> Response:
		"""
		Publish a player for optimization and production use.

		Args:
			player_id (str): Player ID to publish.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/players/{player_id}/publish'.format(account_id=account_id or self.oauth.account_id)
		return self.session.post(url, headers=self.oauth.headers)

	def UpdatePlayer(self, player_id: str, json_body: Union[str, dict], account_id: str='') -> Response:
		"""
		Update a single player. The PATCH method can be used on a single player to do a VERY limited update.
		The only fields you can update in this manner are the name and description properties. All other
		player configuration must be done via the PLAYER CONFIGURATIONS APIs, detailed in the API docs.

		Args:
			player_id (str): Player ID to update.
			json_body (Union[str, dict]): JSON data with the updated player configuration.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/players/{player_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.patch(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def GetPlayerConfiguration(self, player_id: str, branch: str, account_id: str='') -> Response:
		"""
		Get a preview or published player configuration.

		Args:
			player_id (str): Player ID to get configuration from.
			branch (str): ID of branch to get. Can be "master" or "preview".
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/players/{player_id}/configuration/{branch}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def UpdatePlayerConfiguration(self, player_id: str, json_body: Union[str, dict], account_id: str='') -> Response:
		"""
		Update a player configuration.

		Args:
			player_id (str): Player ID to update.
			json_body (Union[str, dict]): JSON data with the updated player configuration.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/players/{player_id}/configuration'.format(account_id=account_id or self.oauth.account_id)
		return self.session.patch(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def GetAllPlugins(self, template_version: str='') -> Response:
		"""
		Get all plugins from plugin registry.

		Args:
			template_version (str, optional): Limit results to plugins compatible with a
				specific player template version. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		if template_version:
			template_version = f'?template_version={template_version}'
		url = f'https://players.api.brightcove.com/v2/plugins{template_version}'
		return self.session.get(url, headers=self.oauth.headers)

	def GetSinglePlugin(self, plugin_id: str) -> Response:
		"""
		Get a single plugin from plugin registry.

		Args:
			plugin_id (str): The plugin ID in the plugin registry.

		Returns:
			Response: API response as requests Response object.
		"""
		if plugin_id:
			plugin_id = plugin_id.replace('@', '%40')
			plugin_id = plugin_id.replace('/', '%2F')
		url = f'https://players.api.brightcove.com/v2/plugins/{plugin_id}'
		return self.session.get(url, headers=self.oauth.headers)

	def GetAllEmbeds(self, player_id: str, account_id: str='') -> Response:
		"""
		Get all the embeds (child players) for a player.

		Args:
			player_id (str): Player ID to get the embeds from.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/players/{player_id}/embeds'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def GetEmbed(self, player_id: str, embed_id: str, account_id: str='') -> Response:
		"""
		Get a specific embed (child player) for a player.

		Args:
			player_id (str): Player ID to get the embed from.
			embed_id (str): Embed ID to get.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/players/{player_id}/embeds/{embed_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def CreateEmbed(self, player_id: str, json_body: Union[str, dict], account_id: str='') -> Response:
		"""
		Create an embed (child player) for a player.

		Args:
			player_id (str): Player ID to create the embed for.
			json_body (Union[str, dict]): JSON data with the embed configuration.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/players/{player_id}/embeds'.format(account_id=account_id or self.oauth.account_id)
		return self.session.post(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def DeleteEmbed(self, player_id: str, embed_id: str, account_id: str='') -> Response:
		"""
		Delete a particular embed (child player) for a player.

		Args:
			player_id (str): Player ID to delete the embed from.
			embed_id (str): Embed ID to delete.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/players/{player_id}/embeds/{embed_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.delete(url, headers=self.oauth.headers)

	def GetPlayerEmbedConfiguration(self, player_id: str, embed_id: str, branch: str, account_id: str='') -> Response:
		"""
		Get the configuration for an embed. You must specify the branch, either "master" or "preview".

		Args:
			player_id (str): Player ID to get the embed's config from.
			embed_id (str): Embed ID to get configuration for.
			branch (str): ID of branch to get embed config for. Can be "master" or "preview".
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/players/{player_id}/embeds/{embed_id}/configuration/{branch}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def UpdateEmbedConfiguration(self, player_id: str, embed_id: str, json_body: Union[str, dict], account_id: str='', use_put: bool=False) -> Response:
		"""
		Update the configuration for an embed.
		Note that you will need to publish the altered embed for optimization and production use.

		Args:
			player_id (str): Player ID to update the embed's config in.
			embed_id (str): Embed ID to update.
			json_body (Union[str, dict]): JSON data with the embed configuration.
			account_id (str, optional): Video Cloud account ID. Defaults to ''.
			use_put (bool, optional): Use PUT instead of PATCH for API call. See docs for more info.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/players/{player_id}/embeds/{embed_id}/configuration/'.format(account_id=account_id or self.oauth.account_id)
		if use_put:
			return self.session.put(url, headers=self.oauth.headers, data=self._json_to_string(json_body))
		return self.session.patch(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def GetConfigurationCombinations(self, player_id: str, embed_id: str, query: str, account_id: str='') -> Response:
		"""
		Retrieve the configuration for a parent/child combination of master and preview branches.
		Using this endpoint provides a way to view what the resulting configuration would be when combining
		different combinations of parent and child (also called embed) versions of players.
		Using this endpoint does not change any configurations, it is only useful for seeing results of
		merging changes to configurations.

		Args:
			player_id (str): Player ID to get configuration combinations from.
			embed_id (str): Embed ID to get configuration combinations from.
			query (str): Query parameters: "playerBranch" and "embedBranch", set to "master" or "preview".
			account_id (str, optional): Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/players/{player_id}/embeds/{embed_id}/configuration/merged?{query}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)
