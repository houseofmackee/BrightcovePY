#!/usr/bin/env python3
from mackee import main, get_cms
from brightcove.utils import aspect_ratio, eprint
#=============================================
# callback to find the aspect ratio of videos
#=============================================
def find_aspect_ratios(video: dict) -> None:
    """
    This will print out the aspectratio of a video.
    """
    video_id = video.get('id')
    delivery_type = video.get('delivery_type')
    source_w, source_h, response = None, None, None

    if delivery_type == 'static_origin':
        response = get_cms().GetRenditionList(video_id=video_id)
    elif delivery_type == 'dynamic_origin':
        response = get_cms().GetDynamicRenditions(video_id=video_id)
    else:
        eprint(f'No video dimensions found for video ID {video_id} (delivery type: {delivery_type}).')
        return

    if response.status_code in get_cms().success_responses:
        renditions = response.json()
        for rendition in renditions:
            if rendition.get('media_type') == 'video' or rendition.get('audio_only') == False:
                source_w = rendition.get('frame_width')
                source_h = rendition.get('frame_height')
                break

        if source_h and source_w:
            x, y = aspect_ratio(source_w, source_h)
            print(video_id, x, y, sep=', ')
        else:
            eprint(f'No video renditions found for video ID {video_id}.')

    else:
        eprint(f'Could not get renditions for video ID {video_id}.')

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
    main(find_aspect_ratios)
