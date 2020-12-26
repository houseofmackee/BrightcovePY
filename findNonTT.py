#!/usr/bin/env python3
from mackee import main

#===========================================
# callback to find videos with text tracks
#===========================================
def find_non_tt(video: dict):
	"""
	This prints video IDs which have no text tracks.
	"""
	if not video.get('text_tracks'):
		print( video.get('id') )

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(find_non_tt)
