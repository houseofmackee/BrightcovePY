#!/usr/bin/env python3
from mackee import main, GetCMS

#===========================================
# callback to delete digital masters
#===========================================
def delete_masters(video):
	if video.get('has_digital_master'):
		shared = video.get('sharing')
		if shared and shared.get('by_external_acct'):
			return
		video_id = video.get('id')
		print(f'Deleting master for video ID {video_id}: {GetCMS().DeleteMaster(video_id=video_id).status_code}')

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(delete_masters)
