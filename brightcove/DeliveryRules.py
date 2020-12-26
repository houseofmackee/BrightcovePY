"""
Implements wrapper class and methods to work with Brightcove's Delivery Rules API.

See: https://apis.support.brightcove.com/delivery-rules/index.html
"""

from typing import Union
from requests.models import Response
from .Base import Base
from .OAuth import OAuth

class DeliveryRules(Base):
	"""
	Class to wrap the Brightcove Delivery Rules API calls. Inherits from Base.

	Attributes:
	-----------
	base_url (str)
		Base URL for API calls.

	Methods:
	--------
	DeliveryRulesEnabled(self, account_id: str='') -> bool
		Returns Tue if an account is enabled for Delivery Rules. False otherwise.

	GetDeliveryRules(self, account_id: str='') -> Response
		Get the Delivery Rules defined for an account.

	GetConditions(self, account_id: str='') -> Response
		Get the Conditions for an account.

	UpdateConditions(self, json_body: Union[str, dict], account_id: str='') -> Response
		Update Conditions for an account.

	GetActions(self, account_id: str='') -> Response
		Get the Actions for an account.

	GetSpecificAction(self, action_id: str, account_id: str='') -> Response
		Get a specific Action based on its ID.

	CreateAction(self, json_body: Union[str, dict], account_id: str='') -> Response
		Create an Action for a specific account.

	UpdateAction(self, action_id: str, json_body: Union[str, dict], account_id: str='') -> Response
		Update an Action for a specific account.

	DeleteAction(self, action_id: str, account_id: str='') -> Response
		Delete an Action for an account.
	"""

	# base URL for all API calls
	base_url = 'https://delivery-rules.api.brightcove.com/accounts/{account_id}'

	def __init__(self, oauth: OAuth) -> None:
		"""
		Args:
			oauth (OAuth): OAuth instance to use for the API calls.
		"""
		super().__init__(oauth=oauth)

	def DeliveryRulesEnabled(self, account_id: str='') -> bool:
		"""
		Check if an account has Delivery Rules enabled.

		Args:
			account_id (str, optional): Account ID to check. Defaults to ''.

		Returns:
			bool: True if account is enabled for Delivery Rules. False otherwise
		"""
		return self.GetDeliveryRules(account_id=account_id).status_code == 200

	def GetDeliveryRules(self, account_id: str='') -> Response:
		"""
		Get the Delivery Rules defined for an account.

		Args:
			account_id (str, optional): Account ID to get the Delivery Rules from. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = (self.base_url).format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def GetConditions(self, account_id: str='') -> Response:
		"""
		Get the Conditions defined for an account.

		Args:
			account_id (str, optional): Account ID to get the Conditions from. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/conditions'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def UpdateConditions(self, json_body: Union[str, dict], account_id: str='') -> Response:
		"""
		Update Conditions for an account.

		Args:
			json_body (Union[str, dict]): JSON data for the Conditions.
			account_id (str, optional): Account ID where to update the Conditions. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/conditions'.format(account_id=account_id or self.oauth.account_id)
		return self.session.put(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def GetActions(self, account_id: str='') -> Response:
		"""
		Get the Actions for an account.

		Args:
			account_id (str, optional): Account ID from where to get the Actions from. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/actions'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def GetSpecificAction(self, action_id: str, account_id: str='') -> Response:
		"""
		Get a specific Action based on its ID.

		Args:
			action_id (str): ID of the Action to get.
			account_id (str, optional): Account ID from where to get the Action from. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/actions/{action_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def CreateAction(self, json_body: Union[str, dict], account_id: str='') -> Response:
		"""
		Create an Action for a specific account.

		Args:
			json_body (Union[str, dict]): JSON data for the Action.
			account_id (str, optional): Account ID where to create the Action. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/actions'.format(account_id=account_id or self.oauth.account_id)
		return self.session.post(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def UpdateAction(self, action_id: str, json_body: Union[str, dict], account_id: str='') -> Response:
		"""
		Update an Action for a specific account.

		Args:
			action_id (str): ID of the Action to update.
			json_body (Union[str, dict]): JSON data for the Action.
			account_id (str, optional): Account ID where to update the Action. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/actions/{action_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.put(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

	def DeleteAction(self, action_id: str, account_id: str='') -> Response:
		"""
		Delete an Action for an account.

		Args:
			action_id (str): ID of the Action to delete.
			account_id (str, optional): Account ID where to delete the Action. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/actions/{action_id}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.delete(url, headers=self.oauth.headers)
