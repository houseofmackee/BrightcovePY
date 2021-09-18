"""
Implements wrapper class and methods to work with Brightcove's CMS API.

See: https://apis.support.brightcove.com/cms/getting-started/overview-cms-api.html
"""

from typing import Union, Optional
from requests.models import Response
from .Base import Base
from .OAuth import OAuth

class CMS(Base):
    """
    Class to wrap the Brightcove CMS API calls. Inherits from Base.

    Attributes:
    -----------
    base_url (str)
        Base URL for API calls.

    Methods:
    --------
    GetCreatedBy(video: dict) -> str
        Gets creator of a video.

    GetVideoCount(self, search_query: str='', account_id: str='') -> int
        Gets count of videos for the account or a search.

    GetVideos(self, page_size: int=20, page_offset: int=0, search_query: str='', account_id: str='') -> Response
        Gets a page of video objects.

    GetLightVideos(self, page_size: int=20, page_offset: int=0, search_query: str='', account_id: str='') -> Response
        Gets a page of video objects with fewer information.

    CreateVideo(self, video_title: str='Video Title', json_body: Optional[Union[dict,str]]=None, account_id: str='') -> Response
        Create a new video object in the account.

    GetVideo(self, video_id: str, account_id: str='') -> Response
        Gets a video object.

    DeleteVideo(self, video_id: str, account_id: str='') -> Response
        Deletes one or more videos.

    UpdateVideo(self, video_id: str, json_body: Union[str, dict], account_id: str='') -> Response
        Update video metadata.

    GetVideoSources(self, video_id: str, account_id: str='') -> Response
        Gets an array of sources (renditions) for a video.

    GetVideoImages(self, video_id: str, account_id: str='') -> Response
        Gets the images for a video.

    GetVideoAudioTracks(self, video_id: str, account_id: str='') -> Response
        Gets the audio tracks for a video Dynamic Delivery only.

    GetVideoAudioTrack(self, video_id: str, track_id: str, account_id: str='') -> Response
        Gets one audio track for a video by its ID Dynamic Delivery only.

    DeleteVideoAudioTrack(self, video_id: str, track_id: str, account_id: str='') -> Response
        Deletes one audio track for a video by its ID Dynamic Delivery only.

    UpdateVideoAudioTrack(self, video_id: str, track_id: str, json_body: Union[str, dict], account_id: str='') -> Response
        Updates audio track metadata for a video Dynamic Delivery only.

    GetDigitalMasterInfo(self, video_id: str, account_id: str='') -> Response
        Gets the stored digital master for a video, if any.

    DeleteDigitalMaster(self, video_id: str, account_id: str='') -> Response
        Deletes the archived digital master for a video.

    GetVideoFields(self, account_id: str='') -> Response
        Gets a list of custom fields for the account.

    GetCustomFields(self, account_id: str='') -> Response
        Gets a list of custom fields from account.

    GetCustomField(self, custom_field_id: str, account_id: str='') -> Response
        Gets a specific custom field from the account.

    CreateCustomField(self, json_body: Union[str, dict], account_id: str='') -> Response
        Create a custom field in account.

    UpdateCustomField(self, custom_field_id: str, json_body: Union[str, dict], account_id: str='') -> Response
        Update a custom field.

    DeleteCustomField(self, custom_field_id: str, account_id: str='') -> Response
        Delete a specific custom field.

    GetStatusOfIngestJob(self, video_id: str, job_id: str, account_id: str='') -> Response
        Get the status of an ingest job associated with a video.

    GetStatusOfIngestJobs(self, video_id: str, account_id: str='') -> Response
        Get the status of all ingest jobs associated with a video.

    GetAllVideoVariants(self, video_id: str, account_id: str='') -> Response
        Gets the language variants for the video metadata.

    CreateVideoVariant(self, video_id: str, json_body: Union[str, dict], account_id: str='') -> Response
        Creates a language variant for a video metadata.

    GetVideoVariant(self, video_id: str, language: str, account_id: str='') -> Response
        Gets the variant for the video metadata for the specified language.

    UpdateVideoVariant(self, video_id: str, language: str, json_body: Union[str, dict], account_id: str='') -> Response
        Updates a language variant for a video metadata.

    DeleteVideoVariant(self, video_id: str, language: str, account_id: str='') -> Response
        Deletes a language variant for a video metadata.

    GetSubscriptionsList(self, account_id: str='') -> Response
        Get a list of all notification subscriptions for the account.

    GetSubscription(self, sub_id: str, account_id: str='') -> Response
        Get a notification subscription for the account.

    CreateSubscription(self, callback_url: str, account_id: str='') -> Response
        Establishes up to 10 endpoints that video changes should be sent to.

    DeleteSubscription(self, sub_id: str, account_id: str='') -> Response
        Delete a notification subscription for the account.

    GetFolders(self, account_id: str='') -> Response
        Gets list of folders for the account.

    CreateFolder(self, folder_name: str, account_id: str='') -> Response
        Create a new folder for the account.

    GetFolderInformation(self, folder_id: str, account_id: str='') -> Response
        Gets information about a folder.

    UpdateFolderName(self, folder_id: str, folder_name: str, account_id: str='') -> Response
        Update the folder name.

    DeleteFolder(self, folder_id: str, account_id: str='') -> Response
        Delete a folder.

    GetVideosInFolder(self, folder_id: str, page_size: int=20, page_offset: int=0, account_id: str='') -> Response
        Gets list of video objects in a folder.

    AddVideoToFolder(self, folder_id: str, video_id: str, account_id: str='') -> Response
        Add a video to a folder.

    RemoveVideoFromFolder(self, folder_id: str, video_id: str, account_id: str='') -> Response
        Remove a video from a folder.

    CreateLabel(self, json_body: Union[str, dict], account_id: str='') -> Response
        Create a new label for the account.

    GetLabels(self, account_id: str='') -> Response
        Gets list of labels for the account.

    UpdateLabel(self, label_path: str, json_body: Union[str, dict], account_id: str='') -> Response
        Update a label for the account.

    DeleteLabel(self, label_path: str, account_id: str='') -> Response
        Delete a label.

    GetPlaylistsForVideo(self, video_id: str, account_id: str='') -> Response
        Gets an array of Manual (EXPLICIT) playlists that contain a video object for the account.

    RemoveVideoFromAllPlaylists(self, video_id: str, account_id: str='') -> Response
        Removes the video from all EXPLICIT playlists for the account.

    GetVideosInPlaylist(self, playlist_id: str, include_details: bool=True, account_id: str='') -> Response
        Gets the video objects for videos in a playlist for the account.

    GetVideoCountInPlaylist(self, playlist_id: str, account_id: str='') -> Response
        Gets a count of the videos in a playlist for the account.

    DeletePlaylist(self, playlist_id: str, account_id: str='') -> Response
        Deletes a playlist.

    UpdatePlaylist(self, playlist_id: str, json_body: Union[str, dict], account_id: str='') -> Response
        Updates a playlist for the account.

    GetPlaylistByID(self, playlist_id: str, account_id: str='') -> Response
        Gets one or more playlist objects for the account.

    GetPlaylistCount(self, search_query: str='', account_id: str='') -> Response
        Gets a count of playlists in the account for the account.

    GetPlaylists(self, sort: str='-updated_at', search_query: str='', page_size: int=20, page_offset: int=0, account_id: str='') -> Response
        Gets a page of playlist objects for the account.

    CreatePlaylist(self, json_body: Union[str, dict], account_id: str='') -> Response
        Creates a new playlist.

    GetAssets(self, video_id: str, account_id: str='') -> Response
        Gets assets for a given video.

    GetDynamicRenditions(self, video_id: str, account_id: str='') -> Response
        Gets a list of dynamic renditions for a Dynamic Delivery video.

    GetRenditionList(self, video_id: str, account_id: str='') -> Response
        Gets a list of renditions for a given video.

    GetRendition(self, video_id: str, asset_id: str, account_id: str='') -> Response
        Gets a specified rendition for a video.

    DeleteRendition(self, video_id: str, asset_id: str, account_id: str='') -> Response
        Deletes a remote rendition for the given video.

    UpdateRendition(self, video_id: str, asset_id: str, json_body: Union[str, dict], account_id: str='') -> Response
        Update the location for a remote rendition.

    AddRendition(self, video_id: str, json_body: Union[str, dict], account_id: str='') -> Response
        Add a remote rendition to the given video.

    ResolveManifestType(manifest_type: str) -> str
        Translates a manifest type to the proper API endpoint.

    GetManifestList(self, video_id: str, manifest_type: str, account_id: str='') -> Response
        Gets a list of manifests of manifest_type for a given video.

    AddManifest(self, video_id: str, manifest_type: str, json_body: Union[str, dict], account_id: str='') -> Response
        Adds the location of an manifest_type file for a remote asset.

    GetManifest(self, video_id: str, asset_id: str, manifest_type: str, account_id: str='') -> Response
        Gets a specified manifest_type manifest for a video.

    DeleteManifest(self, video_id: str, asset_id: str, manifest_type: str, account_id: str='') -> Response
        Deletes an manifest_type manifest file for a remote asset.

    UpdateManifest(self, video_id: str, asset_id: str, manifest_type: str, json_body: Union[str, dict], account_id: str='') -> Response
        Updates the location of a remote manifest_type manifest file for a remote asset.

    ListChannels(self, account_id: str='') -> Response
        Gets a list of channels.

    GetChannelDetails(self, channel_name: str='default', account_id: str='') -> Response
        Gets settings for a sharing channel.

    UpdateChannel(self, json_body: Union[str, dict], channel_name: str='default', account_id: str='') -> Response
        Updates settings for a sharing channel.

    ListChannelAffiliates(self, channel_name: str='default', account_id: str='') -> Response
        Gets a list of affiliates for a channel.

    AddAffiliate(self, affiliate_account_id: str, json_body: Union[str, dict], channel_name: str='default', account_id: str='') -> Response
        Adds an affiliate to a channel.

    RemoveAffiliate(self, affiliate_account_id: str, channel_name: str='default', account_id: str='') -> Response
        Removes an affiliate from a channel.

    ListContracts(self, account_id: str='') -> Response
        Gets a list of available contracts.

    GetContract(self, master_account_id: str, account_id: str='') -> Response
        Gets contract for specific account.

    ApproveContract(self, master_account_id: str, json_body: Union[str, dict], account_id: str='') -> Response
        Approve a contract.

    ListShares(self, video_id: str, account_id: str='') -> Response
        Lists the existing shares for an account.

    ShareVideo(self, video_id: str, json_body: Union[str, dict], account_id: str='') -> Response
        Shares a video to one or more affiliates.

    GetShare(self, video_id: str, affiliate_account_id: str, account_id: str='') -> Response
        Lists the existing shares for an account.

    UnshareVideo(self, video_id: str, affiliate_account_id: str, account_id: str='') -> Response
        Un-shares a video with a specific affiliate.
    """

    # base URL for API calls
    base_url = 'https://cms.api.brightcove.com/v1/accounts/{account_id}'

    def __init__(self, oauth: OAuth, query: str=''):
        """
        Args:
            oauth (OAuth): OAuth instance to use for the API calls.
            query (str, optional): Query string to be used by API calls. Defaults to ''.
        """
        super().__init__(oauth=oauth, query=query)

    #===========================================
    # get who created a video
    #===========================================
    @staticmethod
    def GetCreatedBy(video: dict) -> str:
        """
        Gets creator of a video.

        Args:
            video (dict): Video object.

        Returns:
            str: name of the creator.
        """
        creator = 'Unknown'
        if video:
            created_by = video.get('created_by')
            if created_by:
                ctype = created_by.get('type')
                if ctype=='api_key':
                    creator = 'API'
                elif ctype=='user':
                    creator = created_by.get('email')
        return creator

    #===========================================
    # account based video information
    #===========================================
    #region account based video information
    def GetVideoCount(self, search_query: str='', account_id: str='') -> int:
        """
        Gets count of videos for the account or a search.

        Args:
            search_query (str, optional): Search query. Defaults to ''.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            int: Number of videos in account, -1 if error occured.
        """
        search_query = search_query or self.search_query
        url = f'{self.base_url}/videos/count?q={search_query}'.format(account_id=account_id or self.oauth.account_id)
        response = self.session.get(url, headers=self.oauth.headers)
        if response.status_code == 200:
            return int(response.json().get('count'))
        return -1

    def GetVideos(self, page_size: int=20, page_offset: int=0, search_query: str='', account_id: str='') -> Response:
        """
        Gets a page of video objects.

        Args:
            page_size (int, optional): Number of items to return. Defaults to 20.
            page_offset (int, optional): Number of items to skip. Defaults to 0.
            search_query (str, optional): Search query. Defaults to ''.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        search_query = search_query or self.search_query
        url = f'{self.base_url}/videos?limit={page_size}&offset={page_offset}&sort=created_at&q={search_query}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def GetLightVideos(self, page_size: int=20, page_offset: int=0, search_query: str='', account_id: str='') -> Response:
        """
        Gets a page of video objects with fewer information.

        Args:
            page_size (int, optional): Number of items to return. Defaults to 20.
            page_offset (int, optional): Number of items to skip. Defaults to 0.
            search_query (str, optional): Search query. Defaults to ''.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        search_query = search_query or self.search_query
        url = f'{self.base_url}/lightvideos?limit={page_size}&offset={page_offset}&sort=created_at&q={search_query}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)
    #endregion

    #===========================================
    # single video operations
    #===========================================
    #region video management
    def CreateVideo(self, video_title: str='Video Title', json_body: Optional[Union[dict,str]]=None, account_id: str='') -> Response:
        """
        Create a new video object in the account.
        Note: this does not ingest a video file - use the Dynamic Ingest API for ingestion

        Args:
            video_title (str, optional): Name/title of the video. Defaults to 'Video Title'.
            json_body (Optional[Union[dict,str]], optional): JSON data with metadata. Defaults to None.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/'.format(account_id=account_id or self.oauth.account_id)
        json_body = json_body or { "name": video_title }
        return self.session.post(url=url, headers=self.oauth.headers, data=self._json_to_string(json_body))

    def GetVideo(self, video_id: str, account_id: str='') -> Response:
        """
        Gets a video object - you can include up to 10 video IDs separated by commas.

        Args:
            video_id (str): Video ID(s).
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url=url, headers=self.oauth.headers)

    def DeleteVideo(self, video_id: str, account_id: str='') -> Response:
        """
        Deletes one or more videos.
        Note that for this operation you can specify a comma-delimited list of video ids to delete

        Args:
            video_id (str): Video ID(s).
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.delete(url=url, headers=self.oauth.headers)

    def UpdateVideo(self, video_id: str, json_body: Union[str, dict], account_id: str='') -> Response:
        """
        Update video metadata - note that this API does not ingest any media files - use the
        Dynamic Ingest API for ingestion. Also note that replacing WebVTT text tracks is a
        two-step operation - see Add WebVTT Captions for details.

        Args:
            video_id (str): Video ID.
            json_body (Union[str, dict]): JSON data with video metadata.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.patch(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

    def GetVideoSources(self, video_id: str, account_id: str='') -> Response:
        """
        Gets an array of sources (renditions) for a video.

        Args:
            video_id (str): Video ID(s).
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/sources'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url=url, headers=self.oauth.headers)

    def GetVideoImages(self, video_id: str, account_id: str='') -> Response:
        """
        Gets the images for a video.

        Args:
            video_id (str): Video ID(s).
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/images'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url=url, headers=self.oauth.headers)
    #endregion

    #===========================================
    # audio tracks
    #===========================================
    #region audio tracks
    def GetVideoAudioTracks(self, video_id: str, account_id: str='') -> Response:
        """
        Gets the audio tracks for a video Dynamic Delivery only.

        Args:
            video_id (str): Video ID.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/audio_tracks'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url=url, headers=self.oauth.headers)

    def GetVideoAudioTrack(self, video_id: str, track_id: str, account_id: str='') -> Response:
        """
        Gets one audio track for a video by its ID Dynamic Delivery only.

        Args:
            video_id (str): Video ID.
            track_id (str): Audio track ID.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/audio_tracks/{track_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url=url, headers=self.oauth.headers)

    def DeleteVideoAudioTrack(self, video_id: str, track_id: str, account_id: str='') -> Response:
        """
        Deletes one audio track for a video by its ID Dynamic Delivery only.

        Args:
            video_id (str): Video ID.
            track_id (str): Audio track ID.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/audio_tracks/{track_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.delete(url=url, headers=self.oauth.headers)

    def UpdateVideoAudioTrack(self, video_id: str, track_id: str, json_body: Union[str, dict], account_id: str='') -> Response:
        """
        Updates audio track metadata for a video Dynamic Delivery only.

        Args:
            video_id (str): Video ID.
            track_id (str): Audio track ID.
            json_body (Union[str, dict]): JSON data with the audio track information.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/audio_tracks/{track_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.patch(url=url, headers=self.oauth.headers, data=self._json_to_string(json_body))
    #endregion

    #===========================================
    # digital master
    #===========================================
    #region digital master
    def GetDigitalMasterInfo(self, video_id: str, account_id: str='') -> Response:
        """
        Gets the stored digital master for a video, if any.

        Args:
            video_id (str): Video ID.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/digital_master'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url=url, headers=self.oauth.headers)

    def DeleteDigitalMaster(self, video_id: str, account_id: str='') -> Response:
        """
        Deletes the archived digital master for a video. Be sure to read Digital Master Delete API
        before using this operation to understand the implications.

        Args:
            video_id (str): Video ID.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/digital_master'.format(account_id=account_id or self.oauth.account_id)
        return self.session.delete(url=url, headers=self.oauth.headers)
    #endregion

    #===========================================
    # custom fields
    #===========================================
    #region custom fields
    def GetVideoFields(self, account_id: str='') -> Response:
        """
        Gets a list of video fields from account.

        Args:
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/video_fields'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url=url, headers=self.oauth.headers)

    def GetCustomFields(self, account_id: str='') -> Response:
        """
        Gets a list of custom fields from account.

        Args:
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/video_fields/custom_fields'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url=url, headers=self.oauth.headers)

    def GetCustomField(self, custom_field_id: str, account_id: str='') -> Response:
        """
        Gets a specific custom field from the account.

        Args:
            custom_field_id (str): ID of custom field to retrieve.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.
        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/video_fields/custom_fields/{custom_field_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url=url, headers=self.oauth.headers)

    def CreateCustomField(self, json_body: Union[str, dict], account_id: str='') -> Response:
        """
        Create a custom field in account.

        Args:
            json_body (Union[str, dict]): JSON data with info for the custom field.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/video_fields/custom_fields'.format(account_id=account_id or self.oauth.account_id)
        return self.session.post(url=url, headers=self.oauth.headers, data=self._json_to_string(json_body))

    def UpdateCustomField(self, custom_field_id: str, json_body: Union[str, dict], account_id: str='') -> Response:
        """
        Update a custom field.

        Args:
            custom_field_id (str): ID of custom field to update.
            json_body (Union[str, dict]): JSON data with info for the custom field.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/video_fields/custom_fields/{custom_field_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.patch(url=url, headers=self.oauth.headers, data=self._json_to_string(json_body))

    def DeleteCustomField(self, custom_field_id: str, account_id: str='') -> Response:
        """
        Delete a specific custom field.

        Args:
            custom_field_id (str): ID of custom field to retrieve.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.
        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/video_fields/custom_fields/{custom_field_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.delete(url=url, headers=self.oauth.headers)
    #endregion

    #===========================================
    # ingest jobs
    #===========================================
    #region ingest jobs
    def GetStatusOfIngestJob(self, video_id: str, job_id: str, account_id: str='') -> Response:
        """
        Get the status of an ingest job associated with a video (including the original ingestion,
        replacing and retranscoding the video). NOTE: this operation only works for videos that were
        ingested using Dynamic Delivery profiles.

        Args:
            video_id (str): Video ID.
            job_id (str): Ingest job ID.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/ingest_jobs/{job_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url=url, headers=self.oauth.headers)

    def GetStatusOfIngestJobs(self, video_id: str, account_id: str='') -> Response:
        """
        Get the status of all ingest jobs associated with a video (including the original ingestion,
        replacing and retranscoding the video). NOTE: this operation only works for videos that were
        ingested using Dynamic Delivery profiles.

        Args:
            video_id (str): Video ID.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/ingest_jobs'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url=url, headers=self.oauth.headers)
    #endregion

    #===========================================
    # variants
    #===========================================
    #region variants
    def GetAllVideoVariants(self, video_id: str, account_id: str='') -> Response:
        """
        Gets the language variants for the video metadata.

        Args:
            video_id (str): Video ID.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/variants'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url=url, headers=self.oauth.headers)

    def CreateVideoVariant(self, video_id: str, json_body: Union[str, dict], account_id: str='') -> Response:
        """
        Creates a language variant for a video metadata.

        Args:
            video_id (str): Video ID.
            json_body (Union[str, dict]): JSON data with info for the variant.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/variants'.format(account_id=account_id or self.oauth.account_id)
        return self.session.post(url=url, headers=self.oauth.headers, data=self._json_to_string(json_body))

    def GetVideoVariant(self, video_id: str, language: str, account_id: str='') -> Response:
        """
        Gets the variant for the video metadata for the specified language

        Args:
            video_id (str): Video ID.
            language (str): The language for the variant in the language-country code format (example: en-US).
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/variants/{language}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url=url, headers=self.oauth.headers)

    def UpdateVideoVariant(self, video_id: str, language: str, json_body: Union[str, dict], account_id: str='') -> Response:
        """
        Updates a language variant for a video metadata.

        Args:
            video_id (str): Video ID.
            language (str): The language for the variant in the language-country code format (example: en-US).
            json_body (Union[str, dict]): JSON data with info for the variant.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/variants/{language}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.patch(url=url, headers=self.oauth.headers, data=self._json_to_string(json_body))

    def DeleteVideoVariant(self, video_id: str, language: str, account_id: str='') -> Response:
        """
        Deletes a language variant for a video metadata.

        Args:
            video_id (str): Video ID.
            language (str): The language for the variant in the language-country code format (example: en-US).
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/variants/{language}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.delete(url=url, headers=self.oauth.headers)
    #endregion

    #===========================================
    # notificatons/subscriptions
    #===========================================
    #region subscriptions
    def GetSubscriptionsList(self, account_id: str='') -> Response:
        """
        Get a list of all notification subscriptions for the account.

        Args:
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/subscriptions'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def GetSubscription(self, sub_id: str, account_id: str='') -> Response:
        """
        Get a notification subscription for the account.

        Args:
            sub_id (str): Subscription ID.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/subscriptions/{sub_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def CreateSubscription(self, callback_url: str, account_id: str='') -> Response:
        """
        Establishes up to 10 endpoints that video changes should be sent to. Any change in video
        metadata will trigger a video change event and a notification - changes to assets used by
        the video will not trigger change events.

        Args:
            callback_url (str): The notifications endpoint URL.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/subscriptions'.format(account_id=account_id or self.oauth.account_id)
        json_body = { "endpoint": callback_url, "events": ["video-change"] }
        return self.session.post(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

    def DeleteSubscription(self, sub_id: str, account_id: str='') -> Response:
        """
        Delete a notification subscription for the account.

        Args:
            sub_id (str): Subscription ID.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/subscriptions/{sub_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.delete(url, headers=self.oauth.headers)
    #endregion

    #===========================================
    # folders
    #===========================================
    #region folders
    def GetFolders(self, account_id: str='') -> Response:
        """
        Gets list of folders for the account.

        Args:
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/folders'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def CreateFolder(self, folder_name: str, account_id: str='') -> Response:
        """
        Create a new folder for the account.

        Args:
            folder_name (str): Name for the folder.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/folders'.format(account_id=account_id or self.oauth.account_id)
        json_body = { "name": folder_name }
        return self.session.post(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

    def GetFolderInformation(self, folder_id: str, account_id: str='') -> Response:
        """
        Gets information about a folder.

        Args:
            folder_id (str): Folder ID.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/folders/{folder_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def UpdateFolderName(self, folder_id: str, folder_name: str, account_id: str='') -> Response:
        """
        Update the folder name.

        Args:
            folder_id (str): Folder ID.
            folder_name (str): Name for the folder.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/folders/{folder_id}'.format(account_id=account_id or self.oauth.account_id)
        json_body = { "name": folder_name }
        return self.session.patch(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

    def DeleteFolder(self, folder_id: str, account_id: str='') -> Response:
        """
        Delete a folder.

        Args:
            folder_id (str): Folder ID.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/folders/{folder_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.delete(url, headers=self.oauth.headers)

    def GetVideosInFolder(self, folder_id: str, page_size: int=20, page_offset: int=0, account_id: str='') -> Response:
        """
        Gets list of video objects in a folder. This method uses pagination.

        Args:
            folder_id (str): Folder ID.
            page_size (int, optional): Number of items to return. Defaults to 20.
            page_offset (int, optional): Number of items to skip. Defaults to 0.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/folders/{folder_id}/videos?limit={page_size}&offset={page_offset}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def AddVideoToFolder(self, folder_id: str, video_id: str, account_id: str='') -> Response:
        """
        Add a video to a folder.

        Args:
            folder_id (str): Folder ID.
            video_id (str): Video ID.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/folders/{folder_id}/videos/{video_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.put(url, headers=self.oauth.headers)

    def RemoveVideoFromFolder(self, folder_id: str, video_id: str, account_id: str='') -> Response:
        """
        Remove a video from a folder.

        Args:
            folder_id (str): Folder ID.
            video_id (str): Video ID.
            account_id (str, optional): Brightcove Account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/folders/{folder_id}/videos/{video_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.delete(url, headers=self.oauth.headers)
    #endregion

    #===========================================
    # labels
    #===========================================
    #region labels
    def CreateLabel(self, json_body: Union[str, dict], account_id: str='') -> Response:
        """
        Create a new label for the account.

        Args:
            json_body (Union[str, dict]): JSON data with label info.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/labels'.format(account_id=account_id or self.oauth.account_id)
        return self.session.post(url=url, headers=self.oauth.headers, data=self._json_to_string(json_body))

    def GetLabels(self, account_id: str='') -> Response:
        """
        Gets list of labels for the account.

        Args:
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/labels'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url=url, headers=self.oauth.headers)

    def UpdateLabel(self, label_path: str, json_body: Union[str, dict], account_id: str='') -> Response:
        """
        Update a label for the account.

        Args:
            label_path (str): The path for a label to update or delete. Note that the operation performed
                is on the last item in the path, so for example, if you specify the path /nature/birds/seabirds,
                only the seabirds label will be updated/deleted, but if you specify the path as /nature/birds,
                birds and any sub-labels of birds will be updated/deleted.
            json_body (Union[str, dict]): JSON data with label info.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/labels/by_path/{label_path}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.patch(url=url, headers=self.oauth.headers, data=self._json_to_string(json_body))

    def DeleteLabel(self, label_path: str, account_id: str='') -> Response:
        """
        Delete a label.

        Args:
            label_path (str): The path for a label to update or delete. Note that the operation performed
                is on the last item in the path, so for example, if you specify the path /nature/birds/seabirds,
                only the seabirds label will be updated/deleted, but if you specify the path as /nature/birds,
                birds and any sub-labels of birds will be updated/deleted.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/labels/by_path/{label_path}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.delete(url=url, headers=self.oauth.headers)
    #endregion

    #===========================================
    # playlists
    #===========================================
    #region playlists
    def GetPlaylistsForVideo(self, video_id: str, account_id: str='') -> Response:
        """
        Gets an array of Manual (EXPLICIT) playlists that contain a video object for the account

        Args:
            video_id (str): Video ID or reference ID.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/references'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def RemoveVideoFromAllPlaylists(self, video_id: str, account_id: str='') -> Response:
        """
        Removes the video from all EXPLICIT playlists for the account.

        Args:
            video_id (str): Video ID or reference ID.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/references'.format(account_id=account_id or self.oauth.account_id)
        return self.session.delete(url, headers=self.oauth.headers)

    def GetVideosInPlaylist(self, playlist_id: str, include_details: bool=True, limit: int=100, offset: int=0, account_id: str='') -> Response:
        """
        Gets the video objects for videos in a playlist for the account.

        Args:
            playlist_id (str): Playlist ID.
            include_details (bool, optional): When it's False, API call response won't include caption
                info in [text_tracks] at all and it makes the response returns quicker. Defaults to True.
            limit (int, optional): Number of videos to return. Defaults to 100.
            offset (int, optional): Number of videos to skip. Defaults to 0.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/playlists/{playlist_id}/videos?include_details={("false","true")[include_details]}&limit={limit}&offset={offset}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def GetVideoCountInPlaylist(self, playlist_id: str, account_id: str='') -> Response:
        """
        Gets a count of the videos in a playlist for the account.

        Args:
            playlist_id (str): Playlist ID.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/counts/playlists/{playlist_id}/videos'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def DeletePlaylist(self, playlist_id: str, account_id: str='') -> Response:
        """
        Deletes a playlist.

        Args:
            playlist_id (str): Playlist ID.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/playlists/{playlist_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.delete(url, headers=self.oauth.headers)

    def UpdatePlaylist(self, playlist_id: str, json_body: Union[str, dict], account_id: str='') -> Response:
        """
        Updates a playlist for the account.

        Args:
            playlist_id (str): Playlist ID.
            json_body (Union[str, dict]): JSON data with the data.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/playlists/{playlist_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.patch(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

    def GetPlaylistByID(self, playlist_id: str, account_id: str='') -> Response:
        """
        Gets one or more playlist objects for the account.

        Args:
            playlist_id (str): Video Cloud playlist ID, or multiple playlist IDs separated by commas.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/playlists/{playlist_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def GetPlaylistCount(self, search_query: str='', account_id: str='') -> Response:
        """
        Gets a count of playlists in the account for the account.

        Args:
            search_query (str, optional): Search string. See search guide for details. Defaults to ''.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/counts/playlists?q={search_query or self.search_query}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def GetPlaylists(self, sort: str='-updated_at', search_query: str='', page_size: int=20, page_offset: int=0, account_id: str='') -> Response:
        """
        Gets a page of playlist objects for the account.

        Args:
            sort (str, optional): Field to sort results by. Defaults to '-updated_at'.
            search_query (str, optional): Search query. Defaults to ''.
            page_size (int, optional): Number of items to return. Defaults to 200.
            page_offset (int, optional): Number of items to skip. Defaults to 0.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        search_query = search_query or self.search_query
        if sort not in ['name', 'reference_id', 'created_at', 'published_at', 'updated_at', 'schedule.starts_at', 'schedule.ends_at', 'state', 'plays_total', 'plays_trailing_week', '-name', '-reference_id', '-created_at', '-published_at', '-updated_at', '-schedule.starts_at', '-schedule.ends_at', '-state', '-plays_total', '-plays_trailing_week']:
            sort = '-updated_at'
        url = f'{self.base_url}/playlists?limit={page_size}&offset={page_offset}&sort={sort}&q={search_query}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def CreatePlaylist(self, json_body: Union[str, dict], account_id: str='') -> Response:
        """
        Creates a new playlist.
        A maximum of 100 videos can be added to a playlist (both Manual and Smart). There is no limit
        to the number of playlists that can be created. The videos that are initially loaded into a
        playlist in the player is determined by the type of playlist.

        Args:
            json_body (Union[str, dict]): JSON data with the needed information.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/playlists'.format(account_id=account_id or self.oauth.account_id)
        return self.session.post(url, headers=self.oauth.headers, data=self._json_to_string(json_body))
    #endregion

    #===========================================
    # Clear-Sources
    #===========================================
    #region clear-sources
    def GetVideoWithClearSources(self, video_id: str, account_id: str='') -> Response:
        """
        Get video data with unencrypted sources.
        - Once the unprotected URL is made available, Brightcove and the client have no control over who
        has access to the content or how it is used.
        - There will be egress bandwidth charges made to the customer when the sources are accessed.

        Args:
            video_id (str): Video ID.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/clear_videos/{video_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def GetVideoClearSources(self, video_id: str, account_id: str='') -> Response:
        """
        Get unencrypted sources for a video.
        - Once the unprotected URL is made available, Brightcove and the client have no control over who
        has access to the content or how it is used.
        - There will be egress bandwidth charges made to the customer when the sources are accessed.

        Args:
            video_id (str): Video ID.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/clear_sources'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)
    #endregion

    #===========================================
    # assets
    #===========================================
    #region assets
    def GetAssets(self, video_id: str, account_id: str='') -> Response:
        """
        Gets assets for a given video.

        Args:
            video_id (str): Video ID.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/assets'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def GetDynamicRenditions(self, video_id: str, account_id: str='') -> Response:
        """
        Gets a list of dynamic renditions for a Dynamic Delivery video.

        Args:
            video_id (str): Video ID.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/assets/dynamic_renditions'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def GetRenditionList(self, video_id: str, account_id: str='') -> Response:
        """
        Gets a list of renditions for a given video.
        Note: this endpoint is for renditions created using the legacy ingest profiles.

        Args:
            video_id (str): Video ID.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/assets/renditions'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def GetRendition(self, video_id: str, asset_id: str, account_id: str='') -> Response:
        """
        Gets a specified rendition for a video.

        Args:
            video_id (str): Video ID.
            asset_id (str): Asset ID.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/assets/renditions/{asset_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def DeleteRendition(self, video_id: str, asset_id: str, account_id: str='') -> Response:
        """
        Deletes a remote rendition for the given video. Note: this operation is only for remote renditions
        for remote asset videos do not use it for renditions created by Video Cloud for ingested videos.

        Args:
            video_id (str): Video ID.
            asset_id (str): Asset ID.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/assets/renditions/{asset_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.delete(url, headers=self.oauth.headers)

    def UpdateRendition(self, video_id: str, asset_id: str, json_body: Union[str, dict], account_id: str='') -> Response:
        """
        Update the location for a remote rendition.

        Args:
            video_id (str): Video ID.
            asset_id (str): Asset ID.
            json_body (Union[str, dict]): JSON data with the needed information.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/assets/renditions/{asset_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.patch(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

    def AddRendition(self, video_id: str, json_body: Union[str, dict], account_id: str='') -> Response:
        """
        Add a remote rendition to the given video.

        Args:
            video_id (str): Video ID.
            json_body (Union[str, dict]): JSON data with the needed information.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/assets/renditions'.format(account_id=account_id or self.oauth.account_id)
        return self.session.post(url, headers=self.oauth.headers, data=self._json_to_string(json_body))
    #endregion

    #===========================================
    # manifests
    #===========================================
    #region manifests
    @staticmethod
    def ResolveManifestType(manifest_type: str) -> str:
        """
        Translates a manifest type to the proper API endpoint.
        """
        manifest_types = {
            "hls" : "hls_manifest",
            "dash" : "dash_manifests",
            "hds" : "hds_manifest",
            "ism" : "ism_manifest",
            "ismc" : "ismc_manifest"
        }
        return manifest_types.get(manifest_type.lower().strip(), '')

    def GetManifestList(self, video_id: str, manifest_type: str, account_id: str='') -> Response:
        """
        Gets a list of manifests of manifest_type for a given video.
        Note: this method only returns remote asset manifest(s), not for ingested videos.

        Args:
            video_id (str): Video ID.
            manifest_type (str): Manifest format type.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        manifest_type = self.ResolveManifestType(manifest_type)
        url = f'{self.base_url}/videos/{video_id}/assets/{manifest_type}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def AddManifest(self, video_id: str, manifest_type: str, json_body: Union[str, dict], account_id: str='') -> Response:
        """
        Adds the location of an manifest_type file for a remote asset.

        Args:
            video_id (str): Video ID.
            manifest_type (str): Manifest format type.
            json_body (Union[str, dict]): JSON data with the needed information.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        manifest_type = self.ResolveManifestType(manifest_type)
        url = f'{self.base_url}/videos/{video_id}/assets/{manifest_type}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.post(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

    def GetManifest(self, video_id: str, asset_id: str, manifest_type: str, account_id: str='') -> Response:
        """
        Gets a specified manifest_type manifest for a video.

        Args:
            video_id (str): Video ID.
            asset_id (str): Asset ID.
            manifest_type (str): Manifest format type.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        manifest_type = self.ResolveManifestType(manifest_type)
        url = f'{self.base_url}/videos/{video_id}/assets/{manifest_type}/{asset_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def DeleteManifest(self, video_id: str, asset_id: str, manifest_type: str, account_id: str='') -> Response:
        """
        Deletes an manifest_type manifest file for a remote asset.

        Args:
            video_id (str): Video ID.
            asset_id (str): Asset ID.
            manifest_type (str): Manifest format type.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        manifest_type = self.ResolveManifestType(manifest_type)
        url = f'{self.base_url}/videos/{video_id}/assets/{manifest_type}/{asset_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.delete(url, headers=self.oauth.headers)

    def UpdateManifest(self, video_id: str, asset_id: str, manifest_type: str, json_body: Union[str, dict], account_id: str='') -> Response:
        """
        Updates the location of a remote manifest_type manifest file for a remote asset.

        Args:
            video_id (str): Video ID.
            asset_id (str): Asset ID.
            manifest_type (str): Manifest format type.
            json_body (Union[str, dict]): JSON data with the needed information.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        manifest_type = self.ResolveManifestType(manifest_type)
        url = f'{self.base_url}/videos/{video_id}/assets/{manifest_type}/{asset_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.patch(url, headers=self.oauth.headers, data=self._json_to_string(json_body))
    #endregion

    #===========================================
    # media sharing
    #===========================================
    #region media sharing
    def ListChannels(self, account_id: str='') -> Response:
        """
        Gets a list of channels (currently there is only one default channel).
        This is a Master account operation.

        Args:
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/channels'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def GetChannelDetails(self, channel_name: str='default', account_id: str='') -> Response:
        """
        Gets settings for a sharing channel (currently there is only one default channel).
        This is a Master account operation.

        Args:
            channel_name (str, optional): The name of the channel. Defaults to 'default'.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/channels/{channel_name}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def UpdateChannel(self, json_body: Union[str, dict], channel_name: str='default', account_id: str='') -> Response:
        """
        Updates settings for a sharing channel (currently there is only one default channel).
        This is a Master account operation

        Args:
            channel_name (str, optional): The name of the channel. Defaults to 'default'.
            json_body (Union[str, dict]): JSON data with the needed information.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/channels/{channel_name}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.patch(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

    def ListChannelAffiliates(self, channel_name: str='default', account_id: str='') -> Response:
        """
        Gets a list of affiliates for a channel. This is a Master account operation.

        Args:
            channel_name (str, optional): The name of the channel. Defaults to 'default'.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/channels/{channel_name}/members'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def AddAffiliate(self, affiliate_account_id: str, json_body: Union[str, dict], channel_name: str='default', account_id: str='') -> Response:
        """
        Adds an affiliate to a channel - this is a Master account operation.

        Args:
            affiliate_account_id (str): Video Cloud affiliate account ID for media sharing relationships.
            channel_name (str, optional): The name of the channel. Defaults to 'default'.
            json_body (Union[str, dict]): JSON data with the needed information.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/channels/{channel_name}/members/{affiliate_account_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.put(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

    def RemoveAffiliate(self, affiliate_account_id: str, channel_name: str='default', account_id: str='') -> Response:
        """
        Removes an affiliate from a channel - this is a Master account operation.

        Args:
            affiliate_account_id (str): Video Cloud affiliate account ID for media sharing relationships.
            channel_name (str, optional): The name of the channel. Defaults to 'default'.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/channels/{channel_name}/members/{affiliate_account_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.delete(url, headers=self.oauth.headers)

    def ListContracts(self, account_id: str='') -> Response:
        """
        Gets a list of available contracts.

        Args:
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/contracts'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def GetContract(self, master_account_id: str, account_id: str='') -> Response:
        """
        Gets contract for specific account.

        Args:
            master_account_id (str): Video Cloud master account ID for media sharing relationships.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/contracts/{master_account_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def ApproveContract(self, master_account_id: str, json_body: Union[str, dict], account_id: str='') -> Response:
        """
        Approve a contract - this is an Affiliate account operation.

        Args:
            master_account_id (str): Video Cloud master account ID for media sharing relationships.
            json_body (Union[str, dict]): JSON data with the needed information.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/contracts/{master_account_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.patch(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

    def ListShares(self, video_id: str, account_id: str='') -> Response:
        """
        Lists the existing shares for an account - this is a Master account operation - do this
        before sharing to insure that you are not re-sharing to an affiliate, which would
        overwrite any affiliate metadata changes.

        Args:
            video_id (str): Video ID.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/shares'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def ShareVideo(self, video_id: str, json_body: Union[str, dict], account_id: str='') -> Response:
        """
        Shares a video to one or more affiliates - this is an Master account operation - if the
        video has already been shared to an affiliate, this operation will re-share it and
        overwrite any affiliate metadata changes.

        Args:
            video_id (str): Video ID.
            json_body (Union[str, dict]): JSON data with the needed information.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/shares'.format(account_id=account_id or self.oauth.account_id)
        return self.session.post(url, headers=self.oauth.headers, data=self._json_to_string(json_body))

    def GetShare(self, video_id: str, affiliate_account_id: str, account_id: str='') -> Response:
        """
        Lists the existing shares for an account - this is a Master account operation - do this before
        sharing to insure that you are not re-sharing to an affiliate, which would overwrite any
        affiliate metadata changes.

        Args:
            video_id (str): Video ID.
            affiliate_account_id (str): Video Cloud affiliate account ID for media sharing relationships.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/shares/{affiliate_account_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.get(url, headers=self.oauth.headers)

    def UnshareVideo(self, video_id: str, affiliate_account_id: str, account_id: str='') -> Response:
        """
        Un-shares a video with a specific affiliate - this is an Master account operation - do this before
        sharing to insure that you are not re-sharing to an affiliate, which would overwrite any affiliate
        metadata changes.

        Args:
            video_id (str): Video ID.
            affiliate_account_id (str): Video Cloud affiliate account ID for media sharing relationships.
            account_id (str, optional): Video Cloud account ID. Defaults to ''.

        Returns:
            Response: API response as requests Response object.
        """
        url = f'{self.base_url}/videos/{video_id}/shares/{affiliate_account_id}'.format(account_id=account_id or self.oauth.account_id)
        return self.session.delete(url, headers=self.oauth.headers)
    #endregion
