#!/usr/bin/env python3
from mackee import main
from brightcove.utils import SimpleProgressDisplay, SimpleTimer

show_progress = SimpleProgressDisplay(steps=100, add_info='videos processed')

num_drm_videos = 0

#===========================================
# function to check if a video has DRM
#===========================================
def count_drm(video: dict):
    global num_drm_videos
    if video.get('drm_disabled') == False:
        num_drm_videos += 1
    show_progress()

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
    with SimpleTimer():
        main(count_drm)
        show_progress(force_display=True)
        print(f'\nDRM enabled videos: {num_drm_videos}')
