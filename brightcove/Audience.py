"""
Implements wrapper class and methods to work with Brightcove's Audience API.

See: https://audience.support.brightcove.com/develop/overview-audience-api.html
"""

from dataclasses import dataclass
from requests.models import Response
from .Base import Base
from .OAuth import OAuth
from .utils import QueryStringDataclassBase

#region constants
LEADS_VALID_SORT_VALUES = ('video_id', 'video_name', 'player_id', 'created_at')
LEADS_VALID_FIELDS_VALUES = ('video_id', 'video_name', 'external_id', 'first_name', 'last_name', 'email_address', 'business_phone', 'country', 'company_name', 'industry', 'player_id', 'page_url', 'created_at')
LEADS_VALID_WHERE_VALUES = ('video_id', 'video_name', 'tracking_id', 'external_id', 'player_id', 'page_url', 'watched', 'time_watched', 'created_at', 'updated_at', 'is_synced')

VIEWS_VALID_SORT_VALUES = ('video_id', 'video_name', 'tracking_id', 'external_id', 'player_id', 'page_url', 'watched', 'time_watched', 'created_at', 'updated_at', 'is_synced', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content')
VIEWS_VALID_FIELDS_VALUES = VIEWS_VALID_SORT_VALUES
VIEWS_VALID_WHERE_VALUES = LEADS_VALID_WHERE_VALUES
#endregion

#region query string dataclasses
@dataclass
class AudienceLeadsQueryParameters(QueryStringDataclassBase):
    """
    Dataclass defining URL query parameters for Audience API leads calls.
    """
    limit: int = 25             # Number of items to return
    offset: int = 0             # Number of items to skip
    sort: str = 'created_at'    # Enum: 'video_id', 'video_name', 'player_id', 'created_at'
                                # Field to sort lead results by (prefix with - for descending order)
    fields: str =''             # Enum: 'video_id', 'video_name', 'external_id', 'first_name', 'last_name',
                                # 'email_address', 'business_phone', 'country', 'company_name', 'industry',
                                # 'player_id', 'page_url', 'created_at'
                                # Fields to return for leads
                                # Note: by default, all fields are returned. Use this parameter to return fewer fields.
    where: str =''              # One or more field==value pairs to filter the results
                                # Fields supported are video_id, video_name, tracking_id, external_id,
                                # player_id, page_url, watched, time_watched, created_at, updated_at, is_synced
    from_: str=''               # Start time for the period covered by the report — epoch time in milliseconds
                                # or a date in the format yyyy-mm-dd (such as 2013-09-26) or a relative date
                                # in d (days), h (hours), m (minutes), s (seconds) (such as -2d or -6h)
    to: str=''                  # End time for the period covered by the report — epoch time in milliseconds or
                                # a date in the format yyyy-mm-dd (such as 2013-09-26) or a relative date in
                                #  d (days), h (hours), m (minutes), s (seconds) (such as -2d or -6h)
    def __post_init__(self):
        """
        Add data validation information.
        """
        self.fix_data(
            {
                'from_': 'from',
            }
        )
        self.valid_data(
            {
                'sort': LEADS_VALID_SORT_VALUES,
                'fields': LEADS_VALID_FIELDS_VALUES,
                'where': LEADS_VALID_WHERE_VALUES,
            }
        )

@dataclass
class AudienceViewsQueryParameters(AudienceLeadsQueryParameters):
    """
    Dataclass defining URL query parameters for Audience API views events calls.
    """
    def __post_init__(self):
        """
        Add data validation information.
        """
        self.fix_data(
            {
                'from_': 'from',
            }
        )
        self.valid_data(
            {
                'sort': VIEWS_VALID_SORT_VALUES,
                'fields': VIEWS_VALID_FIELDS_VALUES,
                'where': VIEWS_VALID_WHERE_VALUES,
            }
        )
#endregion

class Audience(Base):
    """
    Class to wrap the Brightcove Audience API calls. Inherits from Base.

    Attributes:
    -----------
    base_url (str)
        Base URL for API calls.

    Methods:
    --------
    GetLeads(self, query_parameters: AudienceQueryParameters) -> Response
        Get leads for a Video Cloud account.
    GetViewEvents(self, query_parameters: AudienceViewsQueryParameters) -> Response
        Get view events for an account.
    SetContentType(self, video_id: str, content_type: str, account_id: str='') -> Response
        Sets the content type for a specific video ID.
    """

    # base URL for all API calls
    base_url = 'https://audience.api.brightcove.com/v1/accounts/{account_id}'

    def __init__(self, oauth: OAuth) -> None:
        """
        Args:
            oauth (OAuth): OAuth instance to use for the API calls.
        """
        super().__init__(oauth=oauth)

    #region Leads
    def GetLeads(self, query_parameters: AudienceLeadsQueryParameters) -> Response:
        """
        Get leads for a Video Cloud account.

        Args:
            query_parameters (AudienceLeadsQueryParameters): Query parameters as AudienceLeadsQueryParameters object.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/leads{query_parameters}'
        return self.session.get(url, headers=self.oauth.headers)
    #endregion

    #region View Events
    def GetViewEvents(self, query_parameters: AudienceViewsQueryParameters) -> Response:
        """
        Get view events for an account - note that only view events that have been
        processed will appear in the response

        Args:
            query_parameters (AudienceViewsQueryParameters): Query parameters as AudienceViewsQueryParameters object.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/view_events{query_parameters}'
        return self.session.get(url, headers=self.oauth.headers)
    #endregion

    #region Content Type
    def SetContentType(self, video_id: str, content_type: str, account_id: str='') -> Response:
        """
        Sets the content type for a specific video ID.

        Args:
            video_id (str): Video ID.
            content_type (str): Content type.
            account_id (str, optional): Account ID where to set the content type. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/content-type'.format(account_id=account_id or self.oauth.account_id)
        json_body = { 'videoId' : video_id, 'contentType' : content_type }
        return self.session.post(url, headers=self.oauth.headers, data=self._json_to_string(json_body))
    #endregion
