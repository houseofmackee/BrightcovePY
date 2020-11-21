#!/usr/bin/env python3
from mackee import main, GetCMS

#===========================================
# callback to activate a video
#===========================================
def activateVideo(video):
	if(video.get('state')=='INACTIVE'):
		videoID = str(video.get('id'))
		json = '{ "state": "ACTIVE" }'
		print('Activating video ID '+videoID+': '+ str(GetCMS().UpdateVideo(videoID=videoID, jsonBody=json).status_code))

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(activateVideo)
