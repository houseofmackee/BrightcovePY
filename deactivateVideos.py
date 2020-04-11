#!/usr/bin/env python3
import mackee

#===========================================
# callback to deactivate a video
#===========================================
def deactivateVideo(video):
	if(video['state']=='ACTIVE'):
		videoID = video['id']
		json = '{ "state": "INACTIVE" }'
		print('Deactivating video ID '+videoID+': '+ str(mackee.cms.UpdateVideo(videoID=videoID, jsonBody=json).status_code))

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(deactivateVideo)
