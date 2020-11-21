#!/usr/bin/env python3
import mackee
from threading import Lock

counter_lock = Lock()
videosProcessed = 0

def showProgress(progress):
	mackee.sys.stderr.write(f'\r{progress} processed...\r')
	mackee.sys.stderr.flush()

#===========================================
# callback to disable Geo restrictions
#===========================================
def disableGeo(video):
	global videosProcessed
	# does video have Geo restrictions?
	if(video.get('geo')):
		# get the video ID
		videoID = str(video.get('id'))
		# create the JSON body
		jsonBody = ('{ "geo": null }')
		# make the PATCH call
		r = mackee.cms.UpdateVideo(videoID=videoID, jsonBody=jsonBody)
		# check if all went well
		if(r.status_code not in [200,202]):
			mackee.eprint(('Error code {error} disabling Geo for video ID {videoid}:').format(error=r.status_code, videoid=videoID))
			mackee.eprint(r.text)

	with counter_lock:
		videosProcessed += 1

	if(videosProcessed%100==0):
		showProgress(videosProcessed)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(disableGeo)
	showProgress(videosProcessed)
