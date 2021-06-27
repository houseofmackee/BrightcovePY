"""
Implements wrapper class and methods to work with Brightcove's Analytics API.

See: https://apis.support.brightcove.com/analytics/index.html
"""

from dataclasses import dataclass
from requests.models import Response
from .Base import Base
from .OAuth import OAuth
from .utils import QueryStringDataclassBase

VALID_DIMENSIONS = ('account', 'city', 'country', 'region', 'date', 'date-time', 'device_os', 'device_type',
                    'player', 'referrer_domain', 'destination_domain', 'search_terms', 'social_platform',
                    'source_type', 'video', 'viewer')

@dataclass
class AnalyticsQueryParameters(QueryStringDataclassBase):
    """
    Dataclass defining URL query parameters for Analytics calls.
    """
    accounts: str = ''                      # One or more account ids, separated by commas
    dimensions: str = ''                    # Enum: "account" "city" "country" "region" "date" "date-time"
                                            # "device_os" "device_type" "player" "referrer_domain" "destination_domain"
                                            # "search_terms" "social_platform" "source_type" "video"
                                            # One or more dimensions to report on; see Multiple Dimensions or
                                            # which combined dimensions are supported.
    limit: int = 10                         # Number of items to return.
    offset: int = 0                         # Number of items to skip.
    sort: str = 'video_view'                # Field to sort results by (prefix with - for descending order).
    fields: str = ''                        # Default: "`video_view` + others (varies by dimension)"
                                            # Fields to return - available fields varies according to the dimensions -
                                            # see the Overview: Analytics API for more details.
    where: str = ''                         # Enum: "account" "city" "country" "region" "date" "date-time" "device_os"
                                            # "device_type" "player" "referrer_domain" "destination_domain" "search_terms"
                                            # "social_platform" "source_type" "video"
                                            # One or more 'dimension==value' pairs to filter the results; see Where Filters
                                            # for details; note that you can also limit the video set returned by filtering
                                            # on video properties.
    from_: str = ''                         # Start time for the period covered by the report — epoch time in milliseconds
                                            # (1535654206775) or a date in the format yyyy-mm-dd (such as 2013-09-26)
    to: str = 'now'                         # End time for the period covered by the report — now or epoch time in milliseconds
                                            # (1535654206775) or a date in the format yyyy-mm-dd (such as 2013-09-26)
    format: str = ''                        # Enum: "csv" "json" "xlxs"
                                            # Format to return the results in.
    reconciled: bool = True                 # If True, only reconciled data is returned; if False, only realtime data is
                                            # returned; if not present, both reconciled and realtime data are returned.

    def __post_init__(self):
        """
        Add data validation information.
        """
        self.fix_data(
            {
                'from_': 'from'
            }
        )

        self.valid_data(
            {
                'dimensions': VALID_DIMENSIONS,
                'where': VALID_DIMENSIONS,
                'format': ('csv', 'json', 'xlxs')
            }
        )

@dataclass
class AnalyticsLiveQueryParameters(QueryStringDataclassBase):
    """
    Dataclass defining URL query parameters for Live Analytics calls.
    """
    dimensions_for_live_analytics: str = ''     # Enum: "account" "city" "country" "region" "date"
                                                # "date-time" "device_os" "device_type" "player"
                                                # "referrer_domain" "destination_domain" "search_terms"
                                                # "social_platform" "source_type" "video"
                                                # Example: dimensions for live analytics=account
                                                # One or more dimensions to report on for Live Analytics requests Dimensions.
    bucket_limit: int = 0                       # Max number of points to be returned for a time-series
    bucket_duration: str = ''                   # Intervals duration in the form of an integer plus m (minutes), h (hours), or d (days)
    metrics: str = ''                           # Enum: "video_impression" "video_view" "video_seconds_viewed"
                                                # "alive_ss_ad_start" "fingerprint_count" "ccu"
                                                # Data metrics to return for live analytics requests.
    where: str = ''                             # Enum: "account" "city" "country" "region" "date" "date-time"
                                                # "device_os" "device_type" "player" "referrer_domain" "destination_domain"
                                                # "search_terms" "social_platform" "source_type" "video"
                                                # One or more 'dimension==value' pairs to filter the results;
                                                # see Where Filters for details; note that you can also limit the video
                                                # set returned by filtering on video properties
    from_: str = ''                             # Start time for the period covered by the report — epoch time in milliseconds
                                                # (1535654206775) or a date in the format yyyy-mm-dd (such as 2013-09-26)
    to: str = 'now'                             # End time for the period covered by the report — now or epoch time in milliseconds
                                                # (1535654206775) or a date in the format yyyy-mm-dd (such as 2013-09-26)

    def __post_init__(self):
        self.fix_data(
            {
                'from_': 'from',
                'dimensions_for_live_analytics': 'dimensions%20for%20live%20analytics'
            }
        )

        self.valid_data(
            {
                'dimensions%20for%20live%20analytics': VALID_DIMENSIONS,
                'where': VALID_DIMENSIONS,
                'metrics':
                    ('video_impression', 'video_view', 'video_seconds_viewed', 'alive_ss_ad_start',
                    'fingerprint_count', 'ccu'),
            }
        )

class Analytics(Base):
    """
    Class to wrap the Brightcove Analytics API calls. Inherits from Base.

    Attributes:
    -----------
    base_url (str)
        Base URL for API calls.

    Methods:
    --------
    GetAccountEngagement(self, account_id: str='') -> Response
        Get a summary report of engagement for the account.

    GetPlayerEngagement(self, player_id: str, account_id: str='') -> Response
        Get a summary report of engagement for a player.

    GetVideoEngagement(self, video_id: str, account_id: str='') -> Response
        Get a summary report of engagement for a video.

    GetAnalyticsReport(self, query_parameters: AnalyticsQueryParameters) -> Response
        Get an analytics report on one or more dimensions.

    GetAvailableDateRange(self, query_parameters: AnalyticsQueryParameters) -> Response
        Get the date range for which reconciled data is available for any Analytics API report.

    GetAlltimeVideoViews(self, video_id: str, account_id: str='') -> Response
        Returns the total alltime video views for a video.

    GetLiveAnalyticsTimeSeries(self, query_parameters: AnalyticsLiveQueryParameters, account_id: str='') -> Response
        Returns a list of timestamp-value pairs representing samples of a variable (metric).

    GetLiveAnalyticsEvent(self, query_parameters: AnalyticsLiveQueryParameters, account_id: str='') -> Response
        Provides a summary of analytics data collected for a live stream.
    """

    # base URL for all API calls
    base_url = 'https://analytics.api.brightcove.com/v1'

    def __init__(self, oauth: OAuth) -> None:
        """
        Args:
            oauth (OAuth): OAuth instance to use for the API calls.
        """
        super().__init__(oauth=oauth)

    #region Engagement Report
    def GetAccountEngagement(self, account_id: str='') -> Response:
        """
        Get a summary report of engagement for the account. Note: Engagement reports are only available
        for periods within the past 32 days. Requests outside that range will return an error The only
        parameters supported for Engagement reports are from and to Engagement reports are available
        for single accounts only - reports on multiple accounts will not work.

        Args:
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        account_id = account_id or self.oauth.account_id
        url = f'{self.base_url}/engagement/accounts/{account_id}'
        return self.session.get(url, headers=self.oauth.headers)

    def GetPlayerEngagement(self, player_id: str, account_id: str='') -> Response:
        """
        Get a summary report of engagement for a player. Note: Engagement reports are only available
        for periods within the past 32 days. Requests outside that range will return an error The
        only parameters supported for Engagement reports are from and to Engagement reports are
        available for single accounts only - reports on multiple accounts will not work.

        Args:
            player_id (str): Video Cloud player ID.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        account_id = account_id or self.oauth.account_id
        url = f'{self.base_url}/engagement/accounts/{account_id}/players/{player_id}'
        return self.session.get(url, headers=self.oauth.headers)

    def GetVideoEngagement(self, video_id: str, account_id: str='') -> Response:
        """
        Get a summary report of engagement for a video. Note: Engagement reports are only available
        for periods within the past 32 days. Requests outside that range will return an error The only
        parameters supported for Engagement reports are from and to Engagement reports are available
        for single accounts only - reports on multiple accounts will not work.

        Args:
            video_id (str): Video Cloud video ID.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        account_id = account_id or self.oauth.account_id
        url = f'{self.base_url}/engagement/accounts/{account_id}/videos/{video_id}'
        return self.session.get(url, headers=self.oauth.headers)
    #endregion

    #region Analytics Report
    def GetAnalyticsReport(self, query_parameters: AnalyticsQueryParameters) -> Response:
        """
        Get an analytics report on one or more dimensions. Note that the fields returned in the response
        will vary according to the dimension(s) requested and the fields specified in the fields parameter.
        See the API Overview and the dimension guides for details.

        Args:
            query_parameters (AnalyticsQueryParameters): Query parameters as AnalyticsQueryParameters object.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/data{query_parameters}'
        return self.session.get(url, headers=self.oauth.headers)

    def GetAvailableDateRange(self, query_parameters: AnalyticsQueryParameters) -> Response:
        """
        Get the date range for which reconciled data is available for any Analytics API report. All parameters
        are allowed, but only account, dimensions, and where affect the result - all others are ignored. Note
        that date range for this request must fall within the available date range for the dimensions requested.

        Args:
            query_parameters (AnalyticsQueryParameters): Query parameters as AnalyticsQueryParameters object.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/data/status{query_parameters}'
        return self.session.get(url, headers=self.oauth.headers)
    #endregion

    #region Video Data
    def GetAlltimeVideoViews(self, video_id: str, account_id: str='') -> Response:
        """
        Returns the total alltime video views for a video. This is a low-latency endpoint appropriate
        for use by client-side apps such as the Brightcove Player.

        Args:
            video_id (str): Video Cloud video ID.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        account_id = account_id or self.oauth.account_id
        url = f'{self.base_url}/alltime/accounts/{account_id}/videos/{video_id}'
        return self.session.get(url, headers=self.oauth.headers)
    #endregion

    #region Live Analytics
    def GetLiveAnalyticsTimeSeries(self, query_parameters: AnalyticsLiveQueryParameters, account_id: str='') -> Response:
        """
        A time-series is defined as a an list of timestamp-value pairs representing samples of a
        variable (metric). The time-series API intends to allow the user to return a time-series
        for the set of metrics requested in the query.

        Args:
            query_parameters (AnalyticsLiveQueryParameters): Query parameters as AnalyticsLiveQueryParameters object.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        account_id = account_id or self.oauth.account_id
        url = f'{self.base_url}/timeseries/accounts/{account_id}{query_parameters}'
        return self.session.get(url, headers=self.oauth.headers)

    def GetLiveAnalyticsEvent(self, query_parameters: AnalyticsLiveQueryParameters, account_id: str='') -> Response:
        """
        Provides a summary of analytics data collected for a live stream.

        Args:
            query_parameters (AnalyticsLiveQueryParameters): Query parameters as AnalyticsLiveQueryParameters object.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        account_id = account_id or self.oauth.account_id
        url = f'{self.base_url}/events/accounts/{account_id}{query_parameters}'
        return self.session.get(url, headers=self.oauth.headers)
    #endregion
