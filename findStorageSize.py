#!/usr/bin/env python3
import mackee

#===========================================
# function to get size of master
#===========================================
def getMasterStorage(video):
	if(video.get('has_digital_master')):
		shared = video.get('sharing')
		if(shared and shared.get('by_external_acct')):
			return 0
		response = mackee.cms.GetDigitalMasterInfo(videoID=video.get('id'))
		if(response.status_code in mackee.cms.success_responses):
			return response.json().get('size')
	else:
		return 0

#===========================================
# function to get size of all renditions
#===========================================
def getRenditionSizes(video):
	renSize = 0

	response = mackee.cms.GetDynamicRenditions(videoID=video.get('id'))
	if(response.status_code in mackee.cms.success_responses):
		renditions = response.json()
		for rendition in renditions:
			renSize += rendition.get('size')

	return renSize

#===========================================
# callback to delete digital masters
#===========================================
def findStorageSize(video):
	totalSize = getMasterStorage(video) + getRenditionSizes(video)
	print(str(video.get('id'))+', '+str(totalSize))

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(findStorageSize)
