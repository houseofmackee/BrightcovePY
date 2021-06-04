#!/usr/bin/env python3
from threading import Lock
from mackee import main, get_cms
from brightcove.utils import SimpleProgressDisplay

data_lock = Lock()
show_progress = SimpleProgressDisplay(steps=100, add_info='videos processed')

#===========================================
# callback to delete digital masters
#===========================================
def delete_masters(video: dict):
    """
    If video has a master this will delete the master.
    """
    if video.get('has_digital_master'):
        shared: dict = video.get('sharing')
        if shared and shared.get('by_external_acct'):
            return
        video_id = video.get('id')
        print(f'Deleting master for video ID {video_id}: {get_cms().DeleteDigitalMaster(video_id=video_id).status_code}')

    with data_lock:
        show_progress()

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
    main(delete_masters)
    show_progress(force_display=True)
