#!/usr/bin/env python3
from mackee import main, GetCMS

#===========================================
# callback to activate a video
#===========================================
def activate_video(video):
	if video.get('state')=='INACTIVE':
		video_id = video.get('id')
		json = '{ "state": "ACTIVE" }'
		print(f'Activating video ID {video_id}: {GetCMS().UpdateVideo(video_id=video_id, json_body=json).status_code}')

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(activate_video)
