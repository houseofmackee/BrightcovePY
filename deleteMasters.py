#!/usr/bin/env python3
import mackee

#===========================================
# callback to delete digital masters
#===========================================
def deleteMasters(video):
	if(video['has_digital_master']):
		shared = video.get('sharing')
		if(shared and shared['by_external_acct']):
			return
		videoID = video['id']
		print('Deleting master for video ID '+videoID+': '+ str(mackee.cms.DeleteMaster(videoID=videoID).status_code))

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(deleteMasters)
