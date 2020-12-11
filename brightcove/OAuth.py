import time
#from .Base import Base
import requests

class OAuth():
	base_url = 'https://oauth.brightcove.com/v4/access_token'

	def __init__(self, account_id:str, client_id:str, client_secret:str) -> None:
		self.account_id = account_id
		self.client_id = client_id
		self.client_secret = client_secret
		self.__access_token = None
		self.__request_time = None
		self.__token_life = 240

	def __get_access_token(self):
		access_token = None
		r = requests.post(url=OAuth.base_url, params='grant_type=client_credentials', auth=(self.client_id, self.client_secret))
		if r.status_code == 200:
			access_token = r.json().get('access_token')
			self.__request_time = time.time()

		return access_token

	def get_access_token(self):
		if self.__access_token is None:
			self.__access_token = self.__get_access_token()
		elif (time.time()-self.__request_time) > self.__token_life:
			self.__access_token = self.__get_access_token()
		return self.__access_token

	def get_headers(self) -> dict:
		return { 'Authorization': f'Bearer {self.get_access_token()}', 'Content-Type': 'application/json' }
