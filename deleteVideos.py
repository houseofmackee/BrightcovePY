#!/usr/bin/env python3
import mackee
from sys import exit

#===========================================
# deletes a video
#===========================================
def deleteVideo(video):

	#safety net to prevent all videos from being deleted
	videoList = mackee.opts.get('video_ids')
	if(not videoList or videoList[0] == 'all'):
		print('Error: detected "all" option -> exiting because it is dangerous')
		exit(2)
	else:
		videoID = video['id']
		print('Deleting video ID "'+videoID+''": "+ str(mackee.cms.DeleteVideo(videoID).status_code))

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(deleteVideo)
