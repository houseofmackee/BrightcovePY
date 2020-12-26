"""
Abstract base class all API wrapper classes have to inherit from.
"""

from abc import ABC, abstractproperty
from typing import Union, Optional
import json
import requests
from .OAuth import OAuth

class Base(ABC):
	"""
	Abstract base class all API wrapper classes have to inherit from.

	Attributes:
	-----------
	base_url (str)
		Base URL for API calls.
	"""

	@abstractproperty
	def base_url(self):
		"""
		every derived class must have a base URL
		"""

	API_VERSION = ''

	# generally accepted success responses
	success_responses = [200,201,202,203,204]

	def __init__(self, oauth: OAuth, query: str='') -> None:
		"""
		Args:
			oauth (OAuth): OAuth instance to use for the API calls.
			query (str, optional): Query string to be used for API calls. Defaults to ''.
		"""
		self.search_query = query
		self.__session = self._get_session()
		self.__oauth = oauth

	@staticmethod
	def _get_session() -> requests.Session:
		"""
		Returns a requests Session with a connection pool of 100.
		"""
		sess = requests.Session()
		adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
		sess.mount('https://', adapter)
		return sess

	@staticmethod
	def _json_to_string(json_object:Union[str, dict]) -> Optional[str]:
		"""
		If json_object is a dict convert to str.
		If json_object is a str validate it.
		Returns str if it's valid JSON, None otherwise.
		"""
		if isinstance(json_object, dict):
			return json.dumps(json_object)
		if isinstance(json_object, str):
			try:
				_ = json.loads(json_object)
				return json_object
			except ValueError:
				pass
		return None

	@property
	def search_query(self) -> str:
		"""
		Return the query string.
		"""
		return self.__search_query

	@search_query.setter
	def search_query(self, query: str) -> None:
		"""
		Setter for query string.
		"""
		self.__search_query = '' if not query else requests.utils.quote(query) # type: ignore

	@property
	def session(self) -> requests.Session:
		"""
		Get the instances requests session.
		"""
		return self.__session

	@property
	def oauth(self) -> OAuth:
		"""
		Get the instances oauth instance.
		"""
		return self.__oauth
