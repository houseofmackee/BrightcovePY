#!/usr/bin/env python3
from threading import Lock
from mackee import main
from brightcove.utils import TimeString as ts
from brightcove.utils import SimpleProgressDisplay

num_videos = 0
total_duration = 0
data_lock = Lock()
show_progress = SimpleProgressDisplay(steps=100, add_info='videos processed')

#===========================================
# callback to add up video durations
#===========================================
def find_average_duration(video: dict):
    """
    This will add the duration of the video to the total.
    """
    global num_videos
    global total_duration

    if duration := video.get('duration'):
        with data_lock:
            num_videos += 1
            total_duration += (duration/1000)
            show_progress()

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
    main(find_average_duration)
    show_progress(force_display=True)
    if num_videos>0:
        print(f'Average duration for {num_videos} videos with duration information is {ts.from_seconds(total_duration/num_videos)} (HH:MM:SS).')
