#!/usr/bin/env python3
import mackee

numberVideos = 0
totalDuration = 0

#===========================================
# callback to add up video durations
#===========================================
def findAverageDuration(video):
	global numberVideos
	global totalDuration

	duration = video.get('duration')
	if(duration):
		numberVideos += 1
		totalDuration += duration

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(findAverageDuration)
	if(numberVideos>0):
		print(f'Average duration for {numberVideos} videos is {mackee.ConvertMilliseconds(totalDuration/numberVideos)}')
