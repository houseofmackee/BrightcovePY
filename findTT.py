#!/usr/bin/env python3
from mackee import main

#===========================================
# callback to find videos with text tracks
#===========================================
def find_tt(video: dict):
	"""
	This will find and list videos which have text tracks.
	"""
	if tts := video.get('text_tracks'):
		print(f'{video.get("id")}, "{video.get("name")}"')
		for track in tts:
			print(track.get('srclang'))

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(find_tt)
