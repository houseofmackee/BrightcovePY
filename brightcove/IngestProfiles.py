from .Base import Base
from .OAuth import OAuth

class IngestProfiles(Base):

	base_url = 'https://ingestion.api.brightcove.com/v1/accounts/{account_id}'

	def __init__(self, oauth:OAuth) -> None:
		super().__init__(oauth=oauth)
		# cache for ProfileExists
		self.__previousProfile = None
		self.__previousAccount = None
		# cache for GetDefaultProfile
		self.__defaultProfileResponse = None
		self.__defaultProfileAccount = None
		# cache for GetProfile
		self.__getProfileAccount = None
		self.__getProfileID = None
		self.__getProfileResponse = None

	def GetDefaultProfile(self, account_id=None):
		account_id = account_id or self.oauth.account_id
		# if it's not the same as before then find it and cache it
		if account_id != self.__defaultProfileAccount:
			headers = self.oauth.get_headers()
			url = (IngestProfiles.base_url+'/configuration').format(account_id=account_id)
			self.__defaultProfileResponse = self.session.get(url=url, headers=headers)
			self.__defaultProfileAccount = account_id
		# return cached response
		return self.__defaultProfileResponse

	def GetIngestProfile(self, profile_id, account_id=None):
		account_id = account_id or self.oauth.account_id
		# if it's not the same as before then find it and cache it
		if self.__getProfileAccount != account_id or self.__getProfileID != profile_id:
			headers = self.oauth.get_headers()
			url = (IngestProfiles.base_url+'/profiles/{profileid}').format(account_id=account_id, profileid=profile_id)
			self.__getProfileID = profile_id
			self.__getProfileAccount = account_id
			self.__getProfileResponse = self.session.get(url=url, headers=headers)
		# return cached response
		return self.__getProfileResponse

	def ProfileExists(self, profile_id, account_id=None):
		account_id = account_id or self.oauth.account_id

		# check if it's a valid cached account/profile combo
		if self.__previousProfile == profile_id and self.__previousAccount == account_id:
			return True

		r = self.GetIngestProfile(account_id=account_id, profile_id=profile_id)
		if r.status_code in IngestProfiles.success_responses:
			self.__previousProfile = profile_id
			self.__previousAccount = account_id
			return True

		return False

	def UpdateDefaultProfile(self, json_body, account_id=None):
		account_id = account_id or self.oauth.account_id
		self.__previousProfile = None
		self.__previousAccount = None
		headers = self.oauth.get_headers()
		url = (IngestProfiles.base_url+'/configuration').format(account_id=account_id)
		return self.session.put(url=url, headers=headers, data=self._json_to_string(json_body))

	def SetDefaultProfile(self, json_body, account_id=None):
		account_id = account_id or self.oauth.account_id
		self.__previousProfile = None
		self.__previousAccount = None
		headers = self.oauth.get_headers()
		url = (IngestProfiles.base_url+'/configuration').format(account_id=account_id)
		return self.session.post(url=url, headers=headers, data=self._json_to_string(json_body))

	def DeleteIngestProfile(self, profile_id, account_id=None):
		account_id = account_id or self.oauth.account_id
		self.__previousProfile = None
		self.__previousAccount = None
		headers = self.oauth.get_headers()
		url = (IngestProfiles.base_url+'/profiles/{profileid}').format(account_id=account_id,profileid=profile_id)
		return self.session.delete(url=url, headers=headers)

	def UpdateIngestProfile(self, profile_id, json_body, account_id=None):
		account_id = account_id or self.oauth.account_id
		self.__previousProfile = None
		self.__previousAccount = None
		headers = self.oauth.get_headers()
		url = (IngestProfiles.base_url+'/profiles/{profileid}').format(account_id=account_id,profileid=profile_id)
		return self.session.put(url=url, headers=headers, data=self._json_to_string(json_body))

	def CreateIngestProfile(self, json_body, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (IngestProfiles.base_url+'/profiles').format(account_id=account_id)
		return self.session.post(url=url, headers=headers, data=self._json_to_string(json_body))

	def GetAllIngestProfiles(self, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (IngestProfiles.base_url+'/profiles').format(account_id=account_id)
		return self.session.get(url=url, headers=headers)
