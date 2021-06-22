#!/usr/bin/env python3
from mackee import main, get_cms

#===========================================
# callback to disable DRM
#===========================================
def disable_drm(video: dict):
	"""
	If video has DRM enabled this will disable DRM.
	"""
	# does video have DRM?
	is_drm_disabled = video.get('drm_disabled')
	if is_drm_disabled == False:
		# get the video ID
		video_id = video.get('id')
		# create the JSON body
		json_body = { 'drm_disabled': True }
		# make the PATCH call
		r = get_cms().UpdateVideo(video_id=video_id, json_body=json_body)
		# check if all went well
		if r.status_code in [200,202]:
			print(f'Disabled DRM for video ID {video_id} with status {r.status_code}.')
		# otherwise report the error
		else:
			print(f'Error code {r.status_code} disabling DRM for video ID {video_id}:')
			print(r.text)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(disable_drm)
