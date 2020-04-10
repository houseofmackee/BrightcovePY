#!/usr/bin/env python3
import mackee
import json

#===========================================
# callback to disable all default tracks
#===========================================
def disableTT(video):
	# flag to signal we found and changed a default track
	gotHit = False
	# try to get all text tracks
	tts = video['text_tracks']
	# check if we found some
	if(len(tts)>0):
		# go through all tracks
		for track in tts:
			#check if it's a default track
			if(track['default']==True):
				# change the setting
				track['default'] = False
				# set the flag so we know we found one
				gotHit = True

		# check if we found and changed one
		if(gotHit):
			# get the video ID
			videoID = video['id']
			# create the JSON body
			jsonBody = ('{ "text_tracks":'+json.dumps(tts)+'}')
			# make the PATCH call
			r = mackee.cms.UpdateVideo(videoID=videoID, jsonBody=jsonBody)
			# check if all went well
			if(r.status_code in [200,202]):
				print(('Disabled default track(s) for video ID {videoid} with status {status}.').format(videoid=videoID, status=r.status_code))
			# otherwise report the error
			else:
				print(('Error code {error} disabling default track(s) for video ID {videoid}:').format(error=r.status_code, videoid=videoID))
				print(r.text)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(disableTT)
