#!/usr/bin/env python3
from mackee import main, get_cms

#===========================================
# callback to enable Offline Playback
#===========================================
def enable_offline(video: dict):
	"""
	If video is not enabled for offline playback this will enable it.
	"""
	# does video have DRM?
	if video.get('offline_enabled') == False:
		# get the video ID
		video_id = video.get('id')
		# create the JSON body
		json_body = { 'offline_enabled': True }
		# make the PATCH call
		r = get_cms().UpdateVideo(video_id=video_id, json_body=json_body)
		# check if all went well
		if r.status_code in [200,202]:
			print(f'Enabled Offline Playback for video ID {video_id} with status {r.status_code}.')
		# otherwise report the error
		else:
			print(f'Error code {r.status_code} enabling Offline Playback for video ID {video_id}:')
			print(r.text)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(enable_offline)
