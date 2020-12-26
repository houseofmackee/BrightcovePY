#!/usr/bin/env python3
from mackee import main

#===========================================
# callback to find 360 videos
#===========================================
def find_360(video: dict):
	"""
	Finds videos which are 360/VR enabled.
	"""
	if video.get('projection') == 'equirectangular':
		print(f'{video.get("id")}, "{video.get("name")}"')

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(find_360)
