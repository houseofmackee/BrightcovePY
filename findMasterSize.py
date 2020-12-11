#!/usr/bin/env python3
import sys
import time
from threading import Lock
from mackee import main, eprint, GetCMS, GetArgs, TimeString, list_to_csv

videosProcessed = 0
counter_lock = Lock()
data_lock = Lock()

row_list = [ ['video_id','delivery_type','master_size'] ]

def showProgress(progress: int) -> None:
	sys.stderr.write(f'\r{progress} processed...\r')
	sys.stderr.flush()

#===========================================
# function to get size of master
#===========================================
def getMasterStorage(video: dict) -> int:
	masterSize = 0
	response = None

	shared = video.get('sharing')
	if shared and shared.get('by_external_acct'):
		return 0

	if video.get('has_digital_master'):
		try:
			response = GetCMS().GetDigitalMasterInfo(video_id=video.get('id'))
		except Exception as e:
			response = None
			masterSize = -1

		if response and response.status_code == 200:
			masterSize = response.json().get('size')

	return masterSize

#===========================================
# callback getting storage sizes
#===========================================
def findStorageSize(video: dict) -> None:
	global videosProcessed
	row = [ video.get('id'), video.get('delivery_type'), getMasterStorage(video) ]

	# add a new row to the CSV data
	with data_lock:
		row_list.append(row)

	# increase processed videos counter
	with counter_lock:
		videosProcessed += 1

	# display counter every 100 videos
	if videosProcessed%100==0:
		showProgress(videosProcessed)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	s = time.perf_counter()
	main(findStorageSize)
	showProgress(videosProcessed)

	#write list to file
	list_to_csv(row_list, GetArgs().o)

	elapsed = time.perf_counter() - s
	eprint(f"\n{__file__} executed in {TimeString.from_seconds(elapsed)}.")
