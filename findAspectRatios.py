#!/usr/bin/env python3
import mackee

#=============================================
# callback to find the aspect ratio of videos
#=============================================
def findAspectRatios(video):
	videoID = str(video['id'])
	deliveryType = video['delivery_type']
	sourceW, sourceH, response = None, None, None

	if(deliveryType == 'static_origin'):
		response = mackee.cms.GetRenditionList(videoID=videoID)
	elif(deliveryType == 'dynamic_origin'):
		response = mackee.cms.GetDynamicRenditions(videoID=videoID)
	else:
		print('No video dimensions found for video ID '+videoID+' (delivery type: '+deliveryType+').')
		return

	if(response.status_code in mackee.cms.success_responses):
		renditions = response.json()
		for rendition in renditions:
			if(rendition.get('media_type') == 'video' or rendition.get('audio_only') == False):
				sourceW = rendition['frame_width']
				sourceH = rendition['frame_height']
				break
		
		if(sourceH and sourceW):
			x,y = mackee.CalculateAspectRatio(sourceW, sourceH)
			print(videoID+': '+str(x)+'x'+str(y))
		else:
			print('No video renditions found for video ID '+videoID+'.')

	else:
		print('Could not get renditions for video ID '+videoID+'.')


#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(findAspectRatios)