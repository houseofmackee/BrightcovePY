#!/usr/bin/env python3
import mackee

#===========================================
# function to get size of master
#===========================================
def getMasterStorage(video):
	masterSize = 0

	if(video.get('has_digital_master')):
		shared = video.get('sharing')
		if(shared and shared.get('by_external_acct')):
			return 0
		response = mackee.cms.GetDigitalMasterInfo(videoID=video.get('id'))
		if(response.status_code == 200):
			masterSize = response.json().get('size')

	return masterSize

#===========================================
# callback to delete digital masters
#===========================================
def findStorageSize(video):
	print(str(video.get('id'))+', '+str(getMasterStorage(video)))

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(findStorageSize)
