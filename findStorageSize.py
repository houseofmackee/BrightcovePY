#!/usr/bin/env python3
import mackee

#===========================================
# function to get size of master
#===========================================
def getMasterStorage(video):
	if(video['has_digital_master']):
		shared = video.get('sharing')
		if(shared and shared['by_external_acct']):
			return 0
		videoID = video['id']
		response = mackee.cms.GetDigitalMasterInfo(videoID=videoID)
		if(response.status_code in mackee.cms.success_responses):
			return response.json().get('size')
	else:
		return 0

#===========================================
# function to get size of all renditions
#===========================================
def getRenditionSizes(video):
	videoID = video['id']
	renSize = 0
	response = mackee.cms.GetDynamicRenditions(videoID=videoID)
	if(response.status_code in mackee.cms.success_responses):
		renditions = response.json()
		for rendition in renditions:
			renSize += rendition.get('size')

	return renSize

#===========================================
# callback to delete digital masters
#===========================================
def findStorageSize(video):
	totalSize = 0
	videoID = video['id']

	totalSize += getMasterStorage(video)
	totalSize += getRenditionSizes(video)

	print(str(videoID+', '+str(totalSize)))

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(findStorageSize)
