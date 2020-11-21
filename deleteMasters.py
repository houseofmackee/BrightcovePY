#!/usr/bin/env python3
from mackee import main, GetCMS

#===========================================
# callback to delete digital masters
#===========================================
def deleteMasters(video):
	if(video.get('has_digital_master')):
		shared = video.get('sharing')
		if(shared and shared.get('by_external_acct')):
			return
		videoID = str(video.get('id'))
		print('Deleting master for video ID '+videoID+': '+ str(GetCMS().DeleteMaster(videoID=videoID).status_code))

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(deleteMasters)
