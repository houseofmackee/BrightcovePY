#!/usr/bin/env python3
import mackee

#===========================================
# callback to disable Offline Playback
#===========================================
def disableOffline(video):
	# does video have DRM?
	if(video.get('offline_enabled')):
		# get the video ID
		videoID = str(video.get('id'))
		# create the JSON body
		jsonBody = ('{ "offline_enabled": false }')
		# make the PATCH call
		r = mackee.cms.UpdateVideo(videoID=videoID, jsonBody=jsonBody)
		# check if all went well
		if(r.status_code in [200,202]):
			print(('Disabled Offline Playback for video ID {videoid} with status {status}.').format(videoid=videoID, status=r.status_code))
		# otherwise report the error
		else:
			print(('Error code {error} disabling Offline Playback for video ID {videoid}:').format(error=r.status_code, videoid=videoID))
			print(r.text)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(disableOffline)
