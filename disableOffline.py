#!/usr/bin/env python3
from mackee import main, get_cms

#===========================================
# callback to disable Offline Playback
#===========================================
def disable_offline(video: dict):
	"""
	If video is enabled for offline payback this will disable it.
	"""
	# is video offline enabled?
	if video.get('offline_enabled'):
		# get the video ID
		video_id = video.get('id')
		# create the JSON body
		json_body = { 'offline_enabled': False }
		# make the PATCH call
		r = get_cms().UpdateVideo(video_id=video_id, json_body=json_body)
		# check if all went well
		if r.status_code in [200,202]:
			print(f'Disabled Offline Playback for video ID {video_id} with status {r.status_code}.')
		# otherwise report the error
		else:
			print(f'Error code {r.status_code} disabling Offline Playback for video ID {video_id}:')
			print(r.text)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(disable_offline)
