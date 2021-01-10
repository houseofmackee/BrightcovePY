#!/usr/bin/env python3
from mackee import main

#===========================================
# callback to report images for the video
#===========================================
def find_images(video: dict):
	"""
	Find URLs for poster and thumbnail images.
	"""
	if images := video.get('images'):
		poster = images.get('poster')
		thumb  = images.get('thumbnail')

		line = str(video.get('id'))+','
		line += (str(poster.get('src'))+',') if poster else ','
		line += (str(thumb.get('src'))) if thumb else ''

		print(line)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(find_images)
