from .Base import Base
from .OAuth import OAuth

class PlaybackRights(Base):

	base_url ='https://playback-rights.api.brightcove.com/v1/accounts/{account_id}'

	def __init__(self, oauth:OAuth) -> None:
		super().__init__(oauth=oauth)

	def CreatePlaybackRight(self, json_body, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (PlaybackRights.base_url+'/playback_rights').format(account_id=account_id)
		return self.session.post(url=url, headers=headers, data=self._json_to_string(json_body))

	def GetPlaybackRights(self, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (PlaybackRights.base_url+'/playback_rights').format(account_id=account_id)
		return self.session.get(url=url, headers=headers)

	def GetPlaybackRight(self, epa_id, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (PlaybackRights.base_url+'/playback_rights/{epaid}').format(account_id=account_id, epaid=epa_id)
		return self.session.get(url=url, headers=headers)

	def UpdatePlaybackRight(self, epa_id, json_body, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (PlaybackRights.base_url+'/playback_rights/{epaid}').format(account_id=account_id, epaid=epa_id)
		return self.session.put(url=url, headers=headers, data=self._json_to_string(json_body))

	def DeletePlaybackRight(self, epa_id, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (PlaybackRights.base_url+'/playback_rights/{epaid}').format(account_id=account_id, epaid=epa_id)
		return self.session.delete(url=url, headers=headers)

	def GetAllUserDevices(self, user_id, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (PlaybackRights.base_url+'/users/{userid}/devices').format(account_id=account_id, userid=user_id)
		return self.session.get(url=url, headers=headers)

	def DeleteAllUserDevices(self, user_id, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (PlaybackRights.base_url+'/users/{userid}/devices').format(account_id=account_id, userid=user_id)
		return self.session.delete(url=url, headers=headers)

	def DeleteUserDevice(self, user_id, device_id, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (PlaybackRights.base_url+'/users/{userid}/devices/{deviceid}').format(account_id=account_id, userid=user_id, deviceid=device_id)
		return self.session.delete(url=url, headers=headers)
