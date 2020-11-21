#!/usr/bin/env python3
from mackee import main, GetCMS

#===========================================
# function to get size of master
#===========================================
def getMasterStorage(video):
	masterSize = 0
	if(video.get('has_digital_master')):
		shared = video.get('sharing')
		if(shared and shared.get('by_external_acct')):
			return 0
		response = GetCMS().GetDigitalMasterInfo(videoID=video.get('id'))
		if(response.status_code == 200):
			masterSize = response.json().get('size')

	return masterSize

#===========================================
# function to get size of all renditions
#===========================================
def getRenditionSizes(video):
	renSize = 0

	response = GetCMS().GetDynamicRenditions(videoID=video.get('id'))
	if(response.status_code in GetCMS().success_responses):
		renditions = response.json()
		for rendition in renditions:
			renSize += rendition.get('size')

	return renSize

#===========================================
# callback getting storage sizes
#===========================================
def findStorageSize(video):
	totalSize = getMasterStorage(video) + getRenditionSizes(video)
	print(str(video.get('id'))+', '+str(totalSize))

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(findStorageSize)
