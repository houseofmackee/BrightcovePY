#!/usr/bin/env python3
from mackee import main

#===========================================
# example callback function
#===========================================
def example_function(video: dict):
	"""
	This will print out the video ID and the name of the video.
	"""
	print(video.get('id'), video.get('name'))

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(example_function)
