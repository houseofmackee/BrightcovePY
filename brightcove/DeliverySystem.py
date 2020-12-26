"""
Implements wrapper class and methods to work with Brightcove's Delivery System API.

See: https://apis.support.brightcove.com/delivery-system/overview-delivery-system-api.html
"""

from os.path import basename
from requests_toolbelt import MultipartEncoder # type: ignore
from requests.models import Response
from .Base import Base
from .OAuth import OAuth

class DeliverySystem(Base):
	"""
	Class to wrap the Brightcove Delivery System API calls. Inherits from Base.

	Attributes:
	-----------
	base_url (str)
		Base URL for API calls.

	Methods:
	--------
	ListRepositories(self, account_id: str='') -> Response
		This will get the the details for all repositories in an account.

	GetRepositoryDetails(self, repo_name: str, account_id: str='') -> Response
		This will retrieve the details for a repository.

	DeleteRepository(self, repo_name: str, account_id: str='') -> Response
		Delete a repository.

	CreateRepository(self, repo_name: str, account_id: str='') -> Response
		Create a repository.

	ListFilesInRepository(self, repo_name: str, account_id: str='') -> Response
		Lists all the files in a repository.

	DeleteFileInRepository(self, repo_name: str, file_name: str, account_id: str='') -> Response
		Delete a file in a repository.

	AddFileToRepository(self, repo_name: str, file_name: str, account_id: str='') -> Response
		Upload a file to a repository.
	"""

	# base URL for all API calls
	base_url = 'https://repos.api.brightcove.com/v1/accounts/{account_id}/repos'

	def __init__(self, oauth:OAuth):
		"""
		Args:
			oauth (OAuth): OAuth instance to use for the API calls
		"""
		super().__init__(oauth=oauth)

	def ListRepositories(self, account_id: str='') -> Response:
		"""
		This will get the the details for all repositories in an account.

		Args:
			account_id (str, optional): Brightcove Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = (self.base_url).format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url=url, headers=self.oauth.headers)

	def GetRepositoryDetails(self, repo_name: str, account_id: str='') -> Response:
		"""
		This will retrieve the details for a repository.

		Args:
			repo_name (str): name of the repository.
			account_id (str, optional): Brightcove Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/{repo_name}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def DeleteRepository(self, repo_name: str, account_id: str='') -> Response:
		"""
		Delete a repository.

		Args:
			repo_name (str): name of the repository.
			account_id (str, optional): Brightcove Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/{repo_name}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.delete(url, headers=self.oauth.headers)

	def CreateRepository(self, repo_name: str, account_id: str='') -> Response:
		"""
		Create a repository.

		Args:
			repo_name (str): name of the repository.
			account_id (str, optional): Brightcove Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/{repo_name}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.put(url, headers=self.oauth.headers)

	def ListFilesInRepository(self, repo_name: str, account_id: str='') -> Response:
		"""
		Lists all the files in a repository.

		Args:
			repo_name (str): name of the repository.
			account_id (str, optional): Brightcove Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/{repo_name}/files'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def DeleteFileInRepository(self, repo_name: str, file_name: str, account_id: str='') -> Response:
		"""
		Delete a file in a repository.

		Args:
			repo_name (str): name of the repository.
			file_name (str): name of the file to delete.
			account_id (str, optional): Brightcove Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/{repo_name}/files/{file_name}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.delete(url, headers=self.oauth.headers)

	def AddFileToRepository(self, repo_name: str, file_name: str, account_id: str='') -> Response:
		"""
		Upload a file to a repository.

		Args:
			repo_name (str): name of the repository.
			file_name (str): name of the file to upload.
			account_id (str, optional): Brightcove Video Cloud account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/{repo_name}/files/{basename(file_name)}'.format(account_id=account_id or self.oauth.account_id)
		upload_data = MultipartEncoder( fields={'contents': (None, open(file_name, 'rb'), 'text/plain')} )
		access_token = self.oauth.access_token
		headers = { 'Authorization': f'Bearer {access_token}', 'Content-Type': upload_data.content_type }
		return self.session.put(url, headers=headers, data=upload_data)
