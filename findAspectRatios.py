#!/usr/bin/env python3
import mackee

def calculate_aspect(width: int, height: int):
	def gcd(a, b):
		return a if b == 0 else gcd(b, a % b)

	temp = 0
	if width == height:
		return '1x1'

	if width < height:
		temp = width
		width = height
		height = temp

	divisor = gcd(width, height)

	x = int(width / divisor) if not temp else int(height / divisor)
	y = int(height / divisor) if not temp else int(width / divisor)

	return (str(x)+'x'+str(y))

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
			print(videoID+': '+calculate_aspect(sourceW, sourceH))
		else:
			print('No video renditions found for video ID '+videoID+'.')

	else:
		print('Could not get renditions for video ID '+videoID+'.')


#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(findAspectRatios)