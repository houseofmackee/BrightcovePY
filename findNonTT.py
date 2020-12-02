#!/usr/bin/env python3
import mackee

#===========================================
# callback to find videos with text tracks
#===========================================
def find_non_tt(video):
	if not video.get('text_tracks'):
		print( video.get('id') )

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(find_non_tt)
