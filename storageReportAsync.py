#!/usr/bin/env python3
import csv
import time
from threading import Lock
from requests.exceptions import RequestException
from mackee import main, get_cms, get_args
from brightcove.utils import list_to_csv, eprint, is_shared_by
from brightcove.utils import TimeString
from brightcove.utils import SimpleProgressDisplay

data_lock = Lock()
row_list = [('account_id','video_id','delivery_type','master_size','hls_renditions_size','mp4_renditions_size','audio_renditions_size', 'flv_renditions_size')]
show_progress = SimpleProgressDisplay(steps=100, add_info='videos processed')

#===========================================
# function to get size of master
#===========================================
def get_master_storage(video: dict) -> int:
    """
    Function to get the size of the digital master for a video.

    Returns size of digital master if available, 0 if video has no master or -1 in case of an error.
    """
    if is_shared_by(video):
        return 0

    if video.get('has_digital_master'):
        try:
            response = get_cms().GetDigitalMasterInfo(video_id=video.get('id'))
        except RequestException:
            return -1
        else:
            if response.status_code == 200:
                return int(response.json().get('size', 0))
            return -1
    return 0

#===========================================
# function to get size of all renditions
#===========================================
def get_rendition_sizes(video: dict) -> dict:
    """
    Function to get the sizes of all rendtions for a video.

    Returns a dict with the relevant sizes if available, 0 for sizes if video has no renditions or -1 in case of an error.
    """
    sizes = {
        'hls_renditions_size': 0,
        'mp4_renditions_size': 0,
        'audio_renditions_size': 0,
        'flv_renditions_size': 0,
    }

    if is_shared_by(video):
        return sizes

    rendition_types = {
        'MP4': 'mp4_renditions_size',
        'M2TS': 'hls_renditions_size',
        'FLV': 'flv_renditions_size',
        'audio': 'audio_renditions_size',
        'video': 'hls_renditions_size',
    }

    response = None
    delivery_type = video.get('delivery_type')
    video_id = video.get('id')

    try:
        if delivery_type == 'static_origin':
            response = get_cms().GetRenditionList(video_id=video_id)
        elif delivery_type == 'dynamic_origin':
            response = get_cms().GetDynamicRenditions(video_id=video_id)
        else:
            return sizes
    except RequestException:
        return { key:-1 for key in sizes }

    if response and response.ok:
        renditions = response.json()
        for rendition in renditions:
            size = rendition.get('size', 0)
            video_container = rendition.get('video_container')
            media_type = rendition.get('media_type')
            try:
                # legacy rendition types
                if video_container:
                    sizes[rendition_types[video_container]] += size
                # dyd rendition types
                elif media_type:
                    sizes[rendition_types[media_type]] += size
            # something I haven't seen before?
            except KeyError:
                eprint(f'WARNING: unexpected container/media type for video ID {video_id}: "{video_container}"/"{media_type}"')
                eprint('Please report the above message to MacKenzie Glanzer.')

        # if it's Dynamic Delivery we need to get MP4 sizes from the sources endpoint
        if delivery_type == 'dynamic_origin' and sizes['mp4_renditions_size'] == 0:
            try:
                response = get_cms().GetVideoSources(video_id=video_id)
            except RequestException:
                sizes['mp4_renditions_size'] = -1
            else:
                if response.status_code in get_cms().success_responses:
                    sizes['mp4_renditions_size'] += sum(set(rendition.get('size', 0) for rendition in response.json() if rendition.get('container') == 'MP4'))
    return sizes

#===========================================
# callback getting storage sizes
#===========================================
def find_storage_size(video: dict) -> None:
    """
    Function to add a list with all storage info for a video to the global report list.
    """
    row_dict = {
        'account_id': video.get('account_id'),
        'video_id': video.get('id'),
        'delivery_type': video.get('delivery_type') if not is_shared_by(video) else 'shared_into_account',
        'master_size': get_master_storage(video)
    }
    row_dict.update(get_rendition_sizes(video))

    # add a new row to the CSV data
    with data_lock:
        row_list.append((row_dict.values()))
        show_progress()

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
    s = time.perf_counter()
    main(find_storage_size)
    show_progress(force_display=True)

    #write list to file
    try:
        list_to_csv(row_list, get_args().o)
    except (OSError, csv.Error) as e:
        eprint(f'\n{e}')

    elapsed = time.perf_counter() - s
    eprint(f'\n{__file__} executed in {TimeString.from_seconds(int(elapsed))}.')
