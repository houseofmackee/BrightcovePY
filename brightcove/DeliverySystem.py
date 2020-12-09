from .Base import Base
from .OAuth import OAuth
from os.path import basename
from requests_toolbelt import MultipartEncoder # type: ignore # pip3 install requests_toolbelt

class DeliverySystem(Base):

	base_url = 'https://repos.api.brightcove.com/v1/accounts/{account_id}/repos'

	def __init__(self, oauth:OAuth):
		super().__init__(oauth=oauth)

	def ListRepositories(self, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (DeliverySystem.base_url).format(account_id=account_id)
		return self.session.get(url=url, headers=headers)

	def GetRepositoryDetails(self, repo_name, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (DeliverySystem.base_url+'/{reponame}').format(account_id=account_id,reponame=repo_name)
		return self.session.get(url, headers=headers)

	def DeleteRepository(self, repo_name, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (DeliverySystem.base_url+'/{reponame}').format(account_id=account_id,reponame=repo_name)
		return self.session.delete(url, headers=headers)

	def CreateRepository(self, repo_name, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (DeliverySystem.base_url+'/{reponame}').format(account_id=account_id,reponame=repo_name)
		return self.session.put(url, headers=headers)

	def ListFilesInRepository(self, repo_name, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (DeliverySystem.base_url+'/{reponame}/files').format(account_id=account_id,reponame=repo_name)
		return self.session.get(url, headers=headers)

	def DeleteFileInRepository(self, repo_name, file_name, account_id=None):
		account_id = account_id or self.oauth.account_id
		headers = self.oauth.get_headers()
		url = (DeliverySystem.base_url+'/{reponame}/files/{filename}').format(account_id=account_id,reponame=repo_name,filename=file_name)
		return self.session.delete(url, headers=headers)

	def AddFileToRepository(self, repo_name, file_name, account_id=None):
		account_id = account_id or self.oauth.account_id
		url = (DeliverySystem.base_url+'/{reponame}/files/{filename}').format(account_id=account_id,reponame=repo_name,filename=basename(file_name))
		m = MultipartEncoder( fields={'contents': (None, open(file_name, 'rb'), 'text/plain')} )
		access_token = self.oauth.get_access_token()
		headers = { 'Authorization': 'Bearer ' + access_token, 'Content-Type': m.content_type }
		return self.session.put(url, headers=headers, data=m)
