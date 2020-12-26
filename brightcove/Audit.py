"""
Implements wrapper class and methods to work with Brightcove's Audit API.

See: https://apis.support.brightcove.com/playback-rights/references/blacklist-api/reference.html
"""

from requests.models import Response
from .Base import Base
from .OAuth import OAuth

class Blacklist(Base):
	"""
	Class to wrap the Brightcove Audit API calls. Inherits from Base.

	Attributes:
	-----------
	base_url (str)
		Base URL for API calls.

	Methods:
	--------
	RequestDailyUsageReport(self, date: str, account_id: str='') -> Response
		Request a daily usage report for Brightcove's Playback Authorization Service.

	CheckUsageReportStatus(self, execution_id: str, account_id: str='') -> Response
		Check the status of your usage report request.

	FetchUsageReport(self, execution_id: str, account_id: str='') -> Response
		Fetch your daily usage report.
	"""

	# base URL for all API calls
	base_url = 'https://playback-auth.api.brightcove.com/v1/audit/accounts/{account_id}'

	def __init__(self, oauth: OAuth) -> None:
		"""
		Args:
			oauth (OAuth): OAuth instance to use for the API calls.
		"""
		super().__init__(oauth=oauth)

	def RequestDailyUsageReport(self, date: str, account_id: str='') -> Response:
		"""
		Request a daily usage report for Brightcove's Playback Authorization Service.

		Args:
			date (str): Date for requested usage report Validations. Format YYYY-MM-DD
				Date cannot be today (UTC time), date cannot be < 30 days in the past
				Brightcove does not hold on to the authorization service usage reports
				after 30 days to follow GDPR compliance
			account_id (str, optional): Brightcove Account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/query/{date}'.format(account_id=account_id or self.oauth.account_id)
		return self.session.post(url, headers=self.oauth.headers)

	def CheckUsageReportStatus(self, execution_id: str, account_id: str='') -> Response:
		"""
		Check the status of your usage report request.

		Args:
			execution_id (str): A unique ID associated with a usage report for a specified account ID and date.
			account_id (str, optional): Brightcove Account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/execution/{execution_id}/status'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)

	def FetchUsageReport(self, execution_id: str, account_id: str='') -> Response:
		"""
		Fetch your daily usage report.

		Args:
			execution_id (str): A unique ID associated with a usage report for a specified account ID and date.
			account_id (str, optional): Brightcove Account ID. Defaults to ''.

		Returns:
			Response: API response as requests Response object.
		"""
		url = f'{self.base_url}/execution/{execution_id}/report'.format(account_id=account_id or self.oauth.account_id)
		return self.session.get(url, headers=self.oauth.headers)
