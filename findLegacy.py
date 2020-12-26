#!/usr/bin/env python3
from mackee import main

#===========================================
# callback to find legacy delivery videos
#===========================================
def find_legacy(video: dict):
	"""
	Finds videos which are on Legacy Delivery.
	"""
	if video.get('delivery_type') == 'static_origin':
		print(f'{video.get("id")}, "{video.get("name")}"')

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(find_legacy)
