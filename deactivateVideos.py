#!/usr/bin/env python3
from mackee import main, get_cms

#===========================================
# callback to deactivate a video
#===========================================
def deactivate_video(video: dict):
	"""
	If a vide is active this will deactiavte it.
	"""
	if video.get('state')=='ACTIVE':
		video_id = video.get('id')
		json = { 'state': 'INACTIVE' }
		print(f'Deactivating video ID {video_id}: {get_cms().UpdateVideo(video_id=video_id, json_body=json).status_code}')

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(deactivate_video)
