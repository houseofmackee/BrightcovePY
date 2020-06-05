#!/usr/bin/env python3
import mackee

#===================================================
# retranscode video and use MP4 if it has no master
#===================================================
def retranscode(video):
	# get some basic info about the video
	videoID = str(video.get('id'))
	deliveryType = video.get('delivery_type')
	hasMaster = video.get('has_digital_master')
	isShared = video.get('sharing')

	# if it's not legacy or dynamic delivery we bail
	if(deliveryType != 'static_origin' and deliveryType != 'dynamic_origin'):
		print(videoID+': can not be retranscoded (delivery type: '+deliveryType+')')
		return
	
	# if it's a shared video we also bail
	if(isShared and isShared.get('by_external_acct')):
		print(videoID+': can not be retranscoded (shared into account)')
		return

	# retranscode specific settings
	ingestProfile = 'multi-platform-extended-static-with-mp4'
	priority = 'low'
	captureImages = 'false'

	# if it has a master then use that for retranscode
	if(hasMaster):
		print(videoID+': retranscoding using digital master -> '+str(mackee.di.RetranscodeVideo(videoID=videoID, profileID=ingestProfile,captureImages=captureImages, priorityQueue=priority).status_code))

	
	# otherwise try to find a high resolution MP4 rendition and use that
	else:
		# get sources for the video and try to find the biggest MP4 video
		sourceURL, sourceW, sourceH = None, 0, 0
		sourceList = mackee.cms.GetVideoSources(videoID=videoID).json()
		for source in sourceList:
			sourceType = source.get('container')
			if(sourceType and sourceType=='MP4'):
				w, h = source.get('width'), source.get('height')
				if(h and w and w>sourceW): # checking w/h to avoid error by audio only renditions
					sourceW, sourceH, sourceURL = w, h, source.get('src')

		# if a source was found download it, using the video ID as filename
		if(sourceURL):
			print(videoID+': retranscoding using highest resolution MP4 ('+str(sourceW)+'x'+str(sourceH)+') -> '+str(mackee.di.SubmitIngest(videoID=videoID, sourceURL=sourceURL, ingestProfile=ingestProfile,captureImages=captureImages, priorityQueue=priority).status_code))

		else:
			print(videoID+': can not be retranscoded (no master or MP4 video rendition)')

#===================================================
# only run code if it's not imported
#===================================================
if __name__ == '__main__':
	mackee.main(retranscode)