"""
Implements wrapper class and methods to work with Brightcove's Live API.

See: https://live.support.brightcove.com/live-api/index.html
"""

from dataclasses import dataclass
from typing import Union
from requests.models import Response
from .Base import Base
from .utils import QueryStringDataclassBase

@dataclass
class LiveQueryParameters(QueryStringDataclassBase):
    """
    Dataclass defining URL query parameters for Live API calls.
    """
    start_token: str = ''       # Next token from previous page; do not specify when fetching first page
    page_size: int = 10         # Max number of items to return in one request (1-1000, default is 10)
    sort: str = 'created_at'    # Attribute to sort jobs by (created_at | modified_at, default is created_at)
    sort_dir: str = 'asc'       # Sort direction (default is asc):asc - ascending; desc - descending
    user_id: str = ''           # Filter results by one or more user IDs
    account_id: str = ''        # Filter results by particular account, or specify ‘*’ to search all accounts.
                                # Default value is account API key belongs to
    created_at: int = 0         # Filter results by Unix time of job creation (in milliseconds)
    modified_at: int = 0        # Filter results by Unix time of job last modified (in milliseconds)
    ad_insertion: bool = False  # Filter results by is SSAI enabled
    static: bool = False        # Filter results by has static endpoint
    state: str = ''             # Filter results by one or more job states
                                # Enum: "error" "standby" "waiting" "processing" "disconnected" "cancelling"
                                #       "finishing" "cancelled" "finished" "failed"
    ssai_state: str = ''        # Filter results by one or more SSAI states
                                # Enum: "none" "ready" "waiting_input" "start_transcoding" "transcoding" "error"
    region: str = ''            # Filter results by one or more regions
                                # Enum: "us-west-2" "us-east-1" "ap-southeast-2" "ap-northeast-1"
                                #       "ap-southeast-1" "eu-central-1" "eu-west-1" "sa-east-1"

    def __post_init__(self):
        """
        Add data validation information.
        """
        self.valid_data(
            {
                'sort':
                    ('created_at', 'modified_at'),
                'sort_dir':
                    ('asc', 'desc'),
                'region':
                    ('us-west-2', 'us-east-1', 'ap-southeast-2', 'ap-northeast-1', 'ap-southeast-1', 'eu-central-1', 'eu-west-1', 'sa-east-1'),
                'ssai_state':
                    ('none', 'ready', 'waiting_input', 'start_transcoding', 'transcoding', 'error'),
                'state':
                    ('error', 'standby', 'waiting', 'processing', 'disconnected', 'cancelling', 'finishing', 'cancelled', 'finished', 'failed'),
            }
        )

@dataclass
class LiveClipsQueryParameters(LiveQueryParameters):
    """
    Dataclass defining URL query parameters for Live Clips/VOD specific API calls.
    """
    jvod_state: str = ''        # Filter results by one or more VOD job states
                                # Enum: "error" "waiting" "waiting_finish_live" "processing" "cancelling"
                                #       "cancelled" "finished" "failed" "creating_asset"
    jvod_type: str = ''         # Filter results by one or more VOD job types
                                # Enum: "s3" "ftp" "instant" "error"
    label: str = ''             # Filter results by one or more VOD job labels
                                # Enum: "none" "ready" "waiting_input" "start_transcoding" "transcoding" "error"

    def __post_init__(self):
        """
        Add data validation information.
        """
        super().__post_init__()
        self.valid_data(
            {
                'jvod_state':
                    ('error', 'waiting', 'waiting_finish_live', 'processing', 'cancelling', 'cancelled', 'finished', 'failed', 'creating_asset'),
                'jvod_type':
                    ('s3', 'ftp', 'instant', 'error'),
                'label':
                    ('none', 'ready', 'waiting_input', 'start_transcoding', 'transcoding', 'error')
            }
        )

class Live(Base):
    """
    Class to wrap the Brightcove Live API calls. Inherits from Base.

    Attributes:
    -----------
    base_url (str)
        Base URL for API calls.

    Methods:
    --------
    CreateLiveJob(self, json_body: Union[str, dict]) -> Response
        Create a live streaming job.

    ListLiveJobs(self, query_parameters: LiveQueryParameters) -> Response
        List live jobs. Uses pagination.

    GetLiveJobDetails(self, job_id: str) -> Response
        Get Live Job details.

    CreatePlaybackToken(self, job_id: str, json_body: Union[str, dict]) -> Response
        The request returns a generated ad_config_id.

    ActivateSEPStream(self, job_id: str) -> Response
        Activate SEP (static entry point) stream.

    DeactivateSEPStream(self, job_id: str) -> Response
        Deactivate SEP (static entry point) stream.

    ManualCuePointInsertion(self, job_id: str, json_body: Union[str, dict]) -> Response
        Inserts a manual Cue-Out with a duration to the Live ingest point.

    AddAdMetadata(self, job_id: str, json_body: Union[str, dict]) -> Response
        Allows content metadata to be pushed and constantly updated out-of-band from a live stream.

    UpdateAdMetadata(self, job_id: str, json_body: Union[str, dict]) -> Response
        Allows content metadata to be pushed and constantly updated out-of-band from a live stream.

    DeleteAdMetadata(self, job_id: str) -> Response
        Deletes ad metadata from a live stream.

    InsertID3TimedMetadata(self, job_id: str, json_body: Union[str, dict]) -> Response
        Inserts an ID3 timed metadata tag for an ongoing job.

    CancelLiveJob(self, job_id: str) -> Response
        Cancel a live stream.

    StopLiveJob(self, job_id: str) -> Response
        Stop a live job.

    CreateRedundantGroup(self, json_body: Union[str, dict]) -> Response
        Creates a redundant group of live jobs to provide failover in case one stream fails.

    GetRedundantGroups(self, state: str, page_size: int=10) -> Response
        Get redundant groups for the account.

    AddJobsToRedundantGroup(self, redundant_group_id: str, json_body: Union[str, dict]) -> Response
        Add Jobs to Redundant Group.

    RemoveJobFromRedundantGroup(self, redundant_group_id: str, job_id: str, force: str='') -> Response
        Remove the specified Jobs from a Redundant Group.

    GetRedundantGroupStatus(self, redundant_group_id: str) -> Response
        Get the current status of a redundant group.

    DeleteRedundantGroup(self, redundant_group_id: str, force: str='') -> Response
        Deletes a redundant group and ends the redundant stream.

    ForceRedundantStreamFailover(self, redundant_group_id: str, json_body: Union[str, dict], force: str='') -> Response
        Force failover from the on_air stream to a specified secondary stream.

    InsertCuepointForRedundantGroup(self, redundant_group_id: str, json_body: Union[str, dict]) -> Response
        Manually inserts a cuepoint for a redundant Live job.

    ListRTMPOutputs(self, job_id: str) -> Response
        Get a list of RTMP outputs.

    CreateRTMPOutput(self, job_id: str, json_body: Union[str, dict]) -> Response
        Create an RTMP output.

    StopRTMPOutput(self, job_id: str, rtmp_out_id: str) -> Response
        Stop an RTMP output.

    CreateVODClip(self, json_body: Union[str, dict], job_id: str='') -> Response
        Create VOD clips from a Live Stream.

    GetVODClipJob(self, jvod_id: str) -> Response
        Get a VOD clip job by ID.

    CancelVODClipJob(self, jvod_id: str) -> Response
        Cancel a VOD clip job by ID.

    ListVODClipJobs(self, job_id: str, query_parameters: LiveClipsQueryParameters) -> Response
        List VOD clips for a Live Stream.

    CreateAdConfiguration(self, json_body: Union[str, dict]) -> Response
        Create a configuration for server-side ad application.

    GetAdConfigurations(self) -> Response
        Get ad applications for the current user.

    GetAccountAdConfigurations(self, live_account_id: str) -> Response
        Get ad applications for an account.

    GetAdConfiguration(self, application_id: str) -> Response
        Get an ad application.

    UpdateAdConfiguration(self, application_id: str, json_body: Union[str, dict]) -> Response
        Update a configuration for server-side ad application.

    DeleteAdConfiguration(self, application_id: str) -> Response
        Get an ad application.

    CreateBeaconSet(self, json_body: Union[str, dict]) -> Response
        Creates a beacon set.

    GetBeaconSetForUser(self) -> Response
        Get all beacon sets for the requesting user..

    UpdateBeaconSet(self, beacon_set_id: str, json_body: Union[str, dict]) -> Response
        Updates a beacon set.

    DeleteBeaconSet(self, beacon_set_id: str) -> Response
        Delete an ad application.

    GetBeaconSets(self, live_account_id: str) -> Response
        Get all beacon sets for an account.

    IngestSlateMediaSourceAsset(self, json_body: Union[str, dict]) -> Response
        Ingest Slate Media Source Asset.

    GetUserSlateMediaSourceAssets(self) -> Response
        Get Slate Media Source Assets for the current user.

    DeleteSlateMediaSourceAsset(self, slate_msa_id: str) -> Response
        Delete Slate Media Source Asset.

    GetSlatesForAccount(self, live_account_id: str) -> Response
        Get all slates for an account.

    ListCredentials(self) -> Response
        This endpoint can be used to get user credentials for a given user provided one has an API key.

    CreateCredential(self, json_body: Union[str, dict]) -> Response
        Create a new credential.

    UpdateCredential(self, credential_id: str, json_body: Union[str, dict]) -> Response
        Update a credential.

    DeleteCredential(self, credential_id: str) -> Response
        Delete a credential.
    """

    base_url = 'https://api.bcovlive.io/v1'

    def __init__(self, api_key: str):
        """
        Args:
        -----
            api_key (str): The Live API key to be used in API calls.
        """
        super().__init__(None)
        self.__api_key = api_key

    #region properties
    @property
    def api_key(self) -> str:
        """
        Returns the API key.
        """
        return self.__api_key

    @property
    def headers(self) -> dict:
        """
        Gets authorization headers for http requests.
        """
        return { 'X-API-KEY': self.api_key, 'Content-Type': 'application/json' }
    #endregion

    #region Live Jobs
    def CreateLiveJob(self, json_body: Union[str, dict]) -> Response:
        """
        Create a live streaming job.

        Args:
            json_body (Union[str, dict]): JSON data with the configuration.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/jobs'
        return self.session.post(url, headers=self.headers, data=self._json_to_string(json_body))

    def ListLiveJobs(self, query_parameters: LiveQueryParameters) -> Response:
        """
        List live jobs. Uses pagination.

        Args:
            query_parameters (LiveQueryParameters): Query parameters as LiveQueryParameters object.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/jobs{query_parameters}'
        return self.session.get(url, headers=self.headers)

    def GetLiveJobDetails(self, job_id: str) -> Response:
        """
        Get Live Job details.

        Args:
            job_id (str): Live job ID.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/jobs/{job_id}'
        return self.session.get(url, headers=self.headers)

    def CreatePlaybackToken(self, job_id: str, json_body: Union[str, dict]) -> Response:
        """
        The request returns a generated ad_config_id. This behavior is handled automatically when
        you publish a live video from the Live module publishing screen, but may be useful if you
        have a custom workflow.

        Args:
            job_id (str): Live job ID.
            json_body (Union[str, dict]): JSON data with the configuration.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/jobs/{job_id}/playback-token'
        return self.session.post(url, headers=self.headers, data=self._json_to_string(json_body))

    def ActivateSEPStream(self, job_id: str) -> Response:
        """
        Activate SEP (static entry point) stream.

        Args:
            job_id (str): Live job ID.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/jobs/{job_id}/activate'
        return self.session.put(url, headers=self.headers)

    def DeactivateSEPStream(self, job_id: str) -> Response:
        """
        Deactivate SEP (static entry point) stream.

        Args:
            job_id (str): Live job ID.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/jobs/{job_id}/deactivate'
        return self.session.put(url, headers=self.headers)

    def ManualCuePointInsertion(self, job_id: str, json_body: Union[str, dict]) -> Response:
        """
        Inserts a manual Cue-Out with a duration to the Live ingest point.

        Args:
            job_id (str): Live job ID.
            json_body (Union[str, dict]): JSON data with the configuration.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/jobs/{job_id}/cuepoint'
        return self.session.post(url, headers=self.headers, data=self._json_to_string(json_body))

    def AddAdMetadata(self, job_id: str, json_body: Union[str, dict]) -> Response:
        """
        Allows content metadata to be pushed and constantly updated out-of-band from a live stream.

        Args:
            job_id (str): Live job ID.
            json_body (Union[str, dict]): JSON data with the configuration.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/jobs/{job_id}/cuepointdata'
        return self.session.post(url, headers=self.headers, data=self._json_to_string(json_body))

    def UpdateAdMetadata(self, job_id: str, json_body: Union[str, dict]) -> Response:
        """
        Allows content metadata to be pushed and constantly updated out-of-band from a live stream.

        Args:
            job_id (str): Live job ID.
            json_body (Union[str, dict]): JSON data with the configuration.

        Returns:
            Response: API response as requests Response object.
        """
        return self.AddAdMetadata(job_id=job_id, json_body=json_body)

    def DeleteAdMetadata(self, job_id: str) -> Response:
        """
        Deletes ad metadata from a live stream.

        Args:
            job_id (str): Live job ID.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/jobs/{job_id}/cuepointdata'
        return self.session.delete(url, headers=self.headers)

    def InsertID3TimedMetadata(self, job_id: str, json_body: Union[str, dict]) -> Response:
        """
        Inserts an ID3 timed metadata tag for an ongoing job. Note that: 1) If using timecode
        property, the job only stores the most recent request for insertion; 2) If using timecode
        property, the encoder must be sending SMPTE-formatted (HH:MM:SS:FF) timecode stored in
        the tc property via OnFI.

        Args:
            job_id (str): Live job ID.
            json_body (Union[str, dict]): JSON data with the configuration.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/jobs/{job_id}/id3tag'
        return self.session.post(url, headers=self.headers, data=self._json_to_string(json_body))

    def CancelLiveJob(self, job_id: str) -> Response:
        """
        Cancel a live stream. When a live job is cancelled, it is ended, and any unprocessed VOD
        jobs associated with the live job will not be processed.

        Args:
            job_id (str): Live job ID.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/jobs/{job_id}/cancel'
        return self.session.put(url, headers=self.headers)

    def StopLiveJob(self, job_id: str) -> Response:
        """
        Stop a live job. When a live job is stopped (as opposed to cancelled), the live stream
        will stop, but any VOD jobs associated with the live job will continue to process.

        Args:
            job_id (str): Live job ID.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/jobs/{job_id}/stop'
        return self.session.put(url, headers=self.headers)
    #endregion

    #region Redundant Groups
    def CreateRedundantGroup(self, json_body: Union[str, dict]) -> Response:
        """
        Creates a redundant group of live jobs to provide failover in case one stream fails.

        Args:
            json_body (Union[str, dict]): JSON data with the configuration.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/redundantgroups'
        return self.session.post(url, headers=self.headers, data=self._json_to_string(json_body))

    def GetRedundantGroups(self, state: str, page_size: int=10) -> Response:
        """
        Get redundant groups for the account.

        Args:
            state (str): Filter redundant grous by state.
            page_size (int): Max number of items to return in one request (1-1000, default is 10).

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/redundantgroups?state={state}&page_size={page_size}'
        return self.session.get(url, headers=self.headers)

    def AddJobsToRedundantGroup(self, redundant_group_id: str, json_body: Union[str, dict]) -> Response:
        """
        Add Jobs to Redundant Group.

        Args:
            redundant_group_id (str): Redundant group ID.
            json_body (Union[str, dict]): JSON data with the configuration.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/redundantgroups/{redundant_group_id}/jobs'
        return self.session.post(url, headers=self.headers, data=self._json_to_string(json_body))

    def RemoveJobFromRedundantGroup(self, redundant_group_id: str, job_id: str, force: str='') -> Response:
        """
        Remove the specified Jobs from a Redundant Group; normally the operation will not remove the job
        that is currently on_air, but adding the force=true query parameter will remove it.

        Args:
            redundant_group_id (str): Redundant group ID.
            job_id (str): Live job ID.
            force (str, optional): Flag to force removal. Any non empty value counts as true. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        force = force or '?force=true'
        url = f'{self.base_url}/redundantgroups/{redundant_group_id}/jobs/{job_id}{force}'
        return self.session.delete(url, headers=self.headers)

    def GetRedundantGroupStatus(self, redundant_group_id: str) -> Response:
        """
        Get the current status of a redundant group.

        Args:
            redundant_group_id (str): Redundant group ID.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/redundantgroups/{redundant_group_id}'
        return self.session.get(url, headers=self.headers)

    def DeleteRedundantGroup(self, redundant_group_id: str, force: str='') -> Response:
        """
        Deletes a redundant group and ends the redundant stream. Note that alternatively you can put
        the stream in standby mode by removing all jobs from it.

        Args:
            redundant_group_id (str): Redundant group ID.
            force (str, optional): Flag to force deletion. Any non empty value counts as true. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        force = force or '?force=true'
        url = f'{self.base_url}/redundantgroups/{redundant_group_id}{force}'
        return self.session.delete(url, headers=self.headers)

    def ForceRedundantStreamFailover(self, redundant_group_id: str, json_body: Union[str, dict], force: str='') -> Response:
        """
        Force failover from the on_air stream to a specified secondary stream; note that you can also
        accomplish this by stopping the encoder for the on_air stream.

        Args:
            redundant_group_id (str): Redundant group ID.
            json_body (Union[str, dict]): JSON data with the configuration.
            force (str, optional): Flag to force deletion. Any non empty value counts as true. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        force = force or '?force=true'
        url = f'{self.base_url}/redundantgroups/{redundant_group_id}/switch{force}'
        return self.session.put(url, headers=self.headers, data=self._json_to_string(json_body))

    def InsertCuepointForRedundantGroup(self, redundant_group_id: str, json_body: Union[str, dict]) -> Response:
        """
        Manually inserts a cuepoint for a redundant Live job.

        Args:
            redundant_group_id (str): Redundant group ID.
            json_body (Union[str, dict]): JSON data with the configuration.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/redundantgroups/{redundant_group_id}/cuepoint'
        return self.session.post(url, headers=self.headers, data=self._json_to_string(json_body))
    #endregion

    #region RTMP Outputs
    def ListRTMPOutputs(self, job_id: str) -> Response:
        """
        Get a list of RTMP outputs.

        Args:
            job_id (str): Live job ID.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/jobs/{job_id}/rtmpouts'
        return self.session.get(url, headers=self.headers)

    def CreateRTMPOutput(self, job_id: str, json_body: Union[str, dict]) -> Response:
        """
        Create an RTMP output.

        Args:
            job_id (str): Live job ID.
            json_body (Union[str, dict]): JSON data with the configuration.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/jobs/{job_id}/rtmpouts'
        return self.session.post(url, headers=self.headers, data=self._json_to_string(json_body))

    def StopRTMPOutput(self, job_id: str, rtmp_out_id: str) -> Response:
        """
        Stop an RTMP output.

        Args:
            job_id (str): Live job ID.
            rtmp_out_id (str): RTMP output ID.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/jobs/{job_id}/rtmpouts/{rtmp_out_id}/stop'
        return self.session.put(url, headers=self.headers)
    #endregion

    #region Clips
    def CreateVODClip(self, json_body: Union[str, dict], job_id: str='') -> Response:
        """
        Create VOD clips from a Live Stream.

        Args:
            json_body (Union[str, dict]): JSON data with the configuration.
            job_id (str, optional): Live job ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        if job_id:
            url = f'{self.base_url}/{job_id}/vods'
        else:
            url = f'{self.base_url}/vods'
        return self.session.post(url, headers=self.headers, data=self._json_to_string(json_body))

    def GetVODClipJob(self, jvod_id: str) -> Response:
        """
        Get a VOD clip job by ID.

        Args:
            jvod_id (str): VOD job ID.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/vods/{jvod_id}'
        return self.session.get(url, headers=self.headers)

    def CancelVODClipJob(self, jvod_id: str) -> Response:
        """
        Cancel a VOD clip job by ID.

        Args:
            jvod_id (str): VOD job ID.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/vods/{jvod_id}/cancel'
        return self.session.put(url, headers=self.headers)


    def ListVODClipJobs(self, job_id: str, query_parameters: LiveClipsQueryParameters) -> Response:
        """
        List VOD clips for a Live Stream - for additional useful information on the search filters,
        see Getting a List of Live or VOD Jobs documentation.

        Args:
            job_id (str): Live job ID.
            query_parameters (LiveClipsQueryParameters): Query parameters as LiveClipsQueryParameters object.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/jobs/{job_id}/vods{query_parameters}'
        return self.session.get(url, headers=self.headers)
    #endregion

    #region SSAI
    def CreateAdConfiguration(self, json_body: Union[str, dict]) -> Response:
        """
        Create a configuration for server-side ad application.
        Note: SSAI is supported for the following regions:
        us-west-2, us-east-1, ap-southeast-2, ap-northeast-1, ap-southeast-1, eu-central-1.

        Args:
            json_body (Union[str, dict]): JSON data with the configuration.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/ssai/applications'
        return self.session.post(url, headers=self.headers, data=self._json_to_string(json_body))

    def GetAdConfigurations(self) -> Response:
        """
        Get ad applications for the current user.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/ssai/applications'
        return self.session.get(url, headers=self.headers)

    def GetAccountAdConfigurations(self, live_account_id: str) -> Response:
        """
        Get ad applications for an account.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/ssai/applications/account/{live_account_id}'
        return self.session.get(url, headers=self.headers)

    def GetAdConfiguration(self, application_id: str) -> Response:
        """
        Get an ad application.

        Args:
            application_id (str): The ad application ID.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/ssai/applications/application/{application_id}'
        return self.session.get(url, headers=self.headers)

    def UpdateAdConfiguration(self, application_id: str, json_body: Union[str, dict]) -> Response:
        """
        Update a configuration for server-side ad application.

        Args:
            application_id (str): The ad application ID.
            json_body (Union[str, dict]): JSON data with the configuration.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/ssai/applications/application/{application_id}'
        return self.session.put(url, headers=self.headers, data=self._json_to_string(json_body))

    def DeleteAdConfiguration(self, application_id: str) -> Response:
        """
        Get an ad application.

        Args:
            application_id (str): The ad application ID.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/ssai/applications/application/{application_id}'
        return self.session.delete(url, headers=self.headers)

    def CreateBeaconSet(self, json_body: Union[str, dict]) -> Response:
        """
        Beacons are data points on playback sent to ad servers to track whether and how much of
        ads were played. Creates a beacon set.

        Args:
            json_body (Union[str, dict]): JSON data with the configuration.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/ssai/beaconsets'
        return self.session.post(url, headers=self.headers, data=self._json_to_string(json_body))

    def GetBeaconSetForUser(self) -> Response:
        """
        Get all beacon sets for the requesting user..

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/ssai/beaconsets'
        return self.session.get(url, headers=self.headers)

    def UpdateBeaconSet(self, beacon_set_id: str, json_body: Union[str, dict]) -> Response:
        """
        Updates a beacon set.

        Args:
            beacon_set_id (str): The beacon set ID.
            json_body (Union[str, dict]): JSON data with the configuration.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/v1/ssai/beaconsets/beaconset/{beacon_set_id}'
        return self.session.put(url, headers=self.headers, data=self._json_to_string(json_body))

    def DeleteBeaconSet(self, beacon_set_id: str) -> Response:
        """
        Delete an ad application.

        Args:
            beacon_set_id (str): The beacon set ID.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/ssai/beaconsets/beaconset/{beacon_set_id}'
        return self.session.delete(url, headers=self.headers)

    def GetBeaconSets(self, live_account_id: str) -> Response:
        """
        Get all beacon sets for an account.

        Args:
            live_account_id (str): Live account ID.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/ssai/beaconsets/account/{live_account_id}'
        return self.session.get(url, headers=self.headers)

    def IngestSlateMediaSourceAsset(self, json_body: Union[str, dict]) -> Response:
        """
        Ingest Slate Media Source Asset.

        Args:
            json_body (Union[str, dict]): JSON data with the configuration.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/ssai/slates'
        return self.session.post(url, headers=self.headers, data=self._json_to_string(json_body))

    def GetUserSlateMediaSourceAssets(self) -> Response:
        """
        Get Slate Media Source Assets for the current user.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/ssai/slates'
        return self.session.get(url, headers=self.headers)

    def DeleteSlateMediaSourceAsset(self, slate_msa_id: str) -> Response:
        """
        Delete Slate Media Source Asset.

        Args:
            slate_msa_id (str): The slate media source ID.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/ssai/slates/slate:{slate_msa_id}'
        return self.session.delete(url, headers=self.headers)

    def GetSlatesForAccount(self, live_account_id: str) -> Response:
        """
        Get all slates for an account.

        Args:
            live_account_id (str): Live account ID.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/ssai/slates/account/{live_account_id}'
        return self.session.get(url, headers=self.headers)
    #endregion

    #region Credentials
    def ListCredentials(self) -> Response:
        """
        This endpoint can be used to get user credentials for a given user provided one has an API key.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/credentials'
        return self.session.get(url, headers=self.headers)

    def CreateCredential(self, json_body: Union[str, dict]) -> Response:
        """
        Create a new credential.

        Args:
            json_body (Union[str, dict]): JSON data with the configuration.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/credentials'
        return self.session.post(url, headers=self.headers, data=self._json_to_string(json_body))

    def UpdateCredential(self, credential_id: str, json_body: Union[str, dict]) -> Response:
        """
        Update a credential.

        Args:
            credential_id (str): A credential ID.
            json_body (Union[str, dict]): JSON data with the configuration.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/credentials/{credential_id}'
        return self.session.put(url, headers=self.headers, data=self._json_to_string(json_body))

    def DeleteCredential(self, credential_id: str) -> Response:
        """
        Delete a credential.

        Args:
            credential_id (str): A credential ID.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/credentials/{credential_id}'
        return self.session.delete(url, headers=self.headers)
    #endregion
