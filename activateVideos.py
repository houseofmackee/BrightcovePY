#!/usr/bin/env python3
from mackee import main, get_cms

#===========================================
# callback to activate a video
#===========================================
def activate_video(video: dict):
	"""
	If video is inactive this will activate it.
	"""
	if video.get('state')=='INACTIVE':
		video_id = video.get('id')
		json = { 'state': 'ACTIVE' }
		print(f'Activating video ID {video_id}: {get_cms().UpdateVideo(video_id=video_id, json_body=json).status_code}')

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(activate_video)
