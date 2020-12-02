#!/usr/bin/env python3
from mackee import main, GetCMS

#===========================================
# callback to enable DRM
#===========================================
def enable_drm(video):
	# does video have DRM?
	if video.get('drm_disabled') == True:
		# get the video ID
		video_id = video.get('id')
		# create the JSON body
		json_body = ('{ "drm_disabled": false }')
		# make the PATCH call
		r = GetCMS().UpdateVideo(video_id=video_id, json_body=json_body)
		# check if all went well
		if r.status_code in [200,202]:
			print(f'Enabled DRM for video ID {video_id} with status {r.status_code}.')
		# otherwise report the error
		else:
			print(f'Error code {r.status_code} enabling DRM for video ID {video_id}:')
			print(r.text)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(enable_drm)
