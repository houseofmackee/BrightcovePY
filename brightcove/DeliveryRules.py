from .Base import Base
from .OAuth import OAuth

class DeliveryRules(Base):
	base_url = 'https://delivery-rules.api.brightcove.com/accounts/{account_id}'

	def __init__(self, oauth:OAuth):
		super().__init__(oauth=oauth)

	def DeliveryRulesEnabled(self, account_id=None):
		return self.GetDeliveryRules(account_id=account_id).status_code == 200

	def GetDeliveryRules(self, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (DeliveryRules.base_url).format(account_id=account_id)
		return self.session.get(url, headers=headers)

	def GetConditions(self, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (DeliveryRules.base_url+'/conditions').format(account_id=account_id)
		return self.session.get(url, headers=headers)

	def UpdateConditions(self, json_body, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (DeliveryRules.base_url+'/conditions').format(account_id=account_id)
		return self.session.put(url, headers=headers, data=self._json_to_string(json_body))

	def GetActions(self, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (DeliveryRules.base_url+'/actions').format(account_id=account_id)
		return self.session.get(url, headers=headers)

	def GetSpecificAction(self, action_id, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (DeliveryRules.base_url+'/actions/{action_id}').format(account_id=account_id, action_id=action_id)
		return self.session.get(url, headers=headers)

	def CreateAction(self, json_body, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (DeliveryRules.base_url+'/actions').format(account_id=account_id)
		return self.session.post(url, headers=headers, data=self._json_to_string(json_body))

	def UpdateAction(self, action_id, json_body, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (DeliveryRules.base_url+'/actions/{action_id}').format(account_id=account_id, action_id=action_id)
		return self.session.put(url, headers=headers, data=self._json_to_string(json_body))

	def DeleteAction(self, action_id, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (DeliveryRules.base_url+'/actions/{action_id}').format(account_id=account_id, action_id=action_id)
		return self.session.delete(url, headers=headers)

