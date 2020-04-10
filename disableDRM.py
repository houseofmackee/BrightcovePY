#!/usr/bin/env python3
import mackee

#===========================================
# callback to disable DRM
#===========================================
def disableDRM(video):
	# does video have DRM?
	isDRMDisabled = video.get('drm_disabled')
	if(isDRMDisabled is not None and isDRMDisabled==False):
		# get the video ID
		videoID = video['id']
		# create the JSON body
		jsonBody = ('{ "drm_disabled": true }')
		# make the PATCH call
		r = mackee.cms.UpdateVideo(videoID=videoID, jsonBody=jsonBody)
		# check if all went well
		if(r.status_code in [200,202]):
			print(('Disabled DRM for video ID {videoid} with status {status}.').format(videoid=videoID, status=r.status_code))
		# otherwise report the error
		else:
			print(('Error code {error} disabling DRM for video ID {videoid}:').format(error=r.status_code, videoid=videoID))
			print(r.text)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(disableDRM)
