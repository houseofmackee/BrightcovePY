from abc import ABC, abstractproperty
from typing import Callable, Tuple, Union, Optional, Dict, Any
import json
import requests
from .OAuth import OAuth

class Base(ABC):

	# every derived class must have a base URL
	@abstractproperty
	def base_url(self):
		pass

	API_VERSION = None
	# generally accepted success responses
	success_responses = [200,201,202,203,204]

	def __init__(self, oauth:OAuth, query:str='') -> None:
		self.search_query:str = query
		self.__session = self._get_session()
		self.__oauth = oauth

	@staticmethod
	def _get_session() -> requests.Session:
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
		elif isinstance(json_object, str):
			try:
				_ = json.loads(json_object)
				return json_object
			except:
				pass
		return None

	@property
	def search_query(self) -> str:
		return self.__search_query

	@search_query.setter
	def search_query(self, query:str) -> None:
		self.__search_query = '' if not query else requests.utils.quote(query) # type: ignore

	@property
	def session(self) -> requests.Session:
		return self.__session

	@property
	def oauth(self) -> OAuth:
		return self.__oauth
