#!/usr/bin/env python3
from mackee import main

#===========================================
# example callback function
#===========================================
def example_function(video):
	print(video.get('id'), video.get('name'))

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(example_function)
