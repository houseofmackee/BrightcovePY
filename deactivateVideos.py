#!/usr/bin/env python3
from mackee import main, GetCMS

#===========================================
# callback to deactivate a video
#===========================================
def deactivateVideo(video):
	if(video.get('state')=='ACTIVE'):
		videoID = str(video.get('id'))
		json = '{ "state": "INACTIVE" }'
		print('Deactivating video ID '+videoID+': '+ str(GetCMS().UpdateVideo(videoID=videoID, jsonBody=json).status_code))

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(deactivateVideo)
