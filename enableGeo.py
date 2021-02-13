#!/usr/bin/env python3
from threading import Lock
from mackee import main, get_cms
from brightcove.utils import eprint
from brightcove.utils import SimpleProgressDisplay

counter_lock = Lock()
show_progress = SimpleProgressDisplay(steps=100, add_info='videos processed')

#===========================================
# callback to enable Geo restrictions
#===========================================
def enable_geo(video: dict):
    """
    If no geo restrictions are enabled this will add some.
    """
    if not video.get('geo'):
        # get the video ID
        video_id = str(video.get('id'))
        # create the JSON body
        json_body = { 'geo' : { 'restricted' : True, 'exclude_countries' : False, 'countries' : ['ca'] } }
        # make the PATCH call
        r = get_cms().UpdateVideo(video_id=video_id, json_body=json_body)
        # check if all went well
        if r.status_code not in [200,202]:
            eprint(f'Error code {r.status_code} disabling Geo for video ID {video_id}:')
            eprint(r.text)
    with counter_lock:
        show_progress()

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
    main(enable_geo)
    show_progress(force_display=True)
