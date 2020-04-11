#!/usr/bin/env python3
import mackee

#===========================================
# callback to activate a video
#===========================================
def activateVideo(video):
	if(video['state']=='INACTIVE'):
		videoID = video['id']
		json = '{ "state": "ACTIVE" }'
		print('Activating video ID '+videoID+': '+ str(mackee.cms.UpdateVideo(videoID=videoID, jsonBody=json).status_code))

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(activateVideo)
