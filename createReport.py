#!/usr/bin/env python3
from mackee import main, GetArgs, list_to_csv
from threading import Lock
import sys

row_list = [ ['id', 'name', 'state', 'reference_id', 'created_at', 'tags'] ]

counter_lock = Lock()
data_lock = Lock()

videosProcessed = 0

def showProgress(progress):
	sys.stderr.write(f'\r{progress} processed...\r')
	sys.stderr.flush()

def createCSV(video):
	global row_list
	global videosProcessed

	row = [ video.get(field) for field in row_list[0] ]

	with data_lock:
		row_list.append(row)

	with counter_lock:
		videosProcessed += 1

	if(videosProcessed%100==0):
		showProgress(videosProcessed)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	#generate the CSV list
	main(createCSV)
	showProgress(videosProcessed)

	#write list to file
	list_to_csv(row_list, GetArgs().o)

