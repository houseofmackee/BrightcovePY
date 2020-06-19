#!/usr/bin/env python3
import mackee

numberVideos = 0
totalDuration = 0

def convertMillis(millis):
	millis = int(millis)
	seconds = int((millis/1000)%60)
	minutes = int((millis/(1000*60))%60)
	hours = int((millis/(1000*60*60))%24)
	return f'{hours:02}:{minutes:02}:{seconds:02}'

#===========================================
# callback add up video durations
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
		print(f'Average duration for {numberVideos} videos is {convertMillis(totalDuration/numberVideos)}')
