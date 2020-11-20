#!/usr/bin/env python3
import sys
from mackee import main, TimeString as ts
from threading import Lock

num_videos = 0
total_duration = 0
data_lock = Lock()

def showProgress(progress: int) -> None:
	sys.stderr.write(f'\r{progress} processed...\r')
	sys.stderr.flush()

#===========================================
# callback to add up video durations
#===========================================
def findAverageDuration(video):
	global num_videos
	global total_duration

	duration = video.get('duration')
	if(duration):
		with data_lock:
			num_videos += 1
			total_duration += (duration/1000)

		# display counter every 100 videos
		if(num_videos%100==0):
			showProgress(num_videos)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(findAverageDuration)
	showProgress(num_videos)
	if(num_videos>0):
		print(f'Average duration for {num_videos} videos with duration information is {ts.from_seconds(total_duration/num_videos)} (HH:MM:SS).')
