#!/usr/bin/env python3
from mackee import main, get_cms
#=============================================
# callback to find the aspect ratio of videos
#=============================================
def report_renditions(video: dict) -> None:
    """
    This will print out the aspectratio of a video.
    """
    video_id = str(video.get('id'))
    delivery_type = video.get('delivery_type')
    source_w, source_h, response = None, None, None

    if delivery_type == 'static_origin':
        response = get_cms().GetRenditionList(video_id=video_id)
    elif delivery_type == 'dynamic_origin':
        response = get_cms().GetDynamicRenditions(video_id=video_id)
    else:
        return

    if response.status_code not in get_cms().success_responses:
        return

    results = {}
    rendition: dict
    for rendition in response.json():
        if rendition.get('media_type') == 'video' or rendition.get('audio_only') is False:
            source_w = rendition.get('frame_width')
            source_h = rendition.get('frame_height')
            if source_h and source_w:
                results[rendition.get('size')] = [source_w, source_h, rendition.get('size'), 'MP4' if rendition.get('video_container') == 'MP4' else 'HLS/DASH' ]

    if delivery_type == 'dynamic_origin':
        response = get_cms().GetVideoSources(video_id=video_id)
        if response.status_code in get_cms().success_responses:
            for rendition in response.json():
                if rendition.get('container') == 'MP4':
                    source_w = rendition.get('width')
                    source_h = rendition.get('height')
                    if source_h and source_w:
                        results[rendition.get('size')] = [source_w, source_h, rendition.get('size'), 'MP4']

    for _, values in results.items():
        print(video_id, *values, sep=', ')

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
    main(report_renditions)
