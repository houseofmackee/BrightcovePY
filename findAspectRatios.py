#!/usr/bin/env python3
import mackee

def calculate_aspect(width: int, height: int):
	def gcd(a, b):
		return a if b == 0 else gcd(b, a % b)

	r = gcd(width, height)
	x = int(width / r)
	y = int(height / r)

	return (str(x)+'x'+str(y))

#===========================================
# callback to find 360 videos 
#===========================================
def findAspectRatios(video):
	videoID = str(video['id'])
	sourceW, sourceH = None, None

	response = mackee.cms.GetDynamicRenditions(videoID=videoID)
	if(response.status_code in mackee.cms.success_responses):
		renditions = response.json()
		for rendition in renditions:
			if(rendition['media_type'] == 'video'):
				sourceW = rendition['frame_width']
				sourceH = rendition['frame_height']
				break
		
		if(sourceH and sourceW):
			print(videoID+": "+calculate_aspect(sourceW, sourceH))


#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(findAspectRatios)