#!/usr/bin/env python3
from mackee import main, eprint, GetCMS, GetArgs
import sys
import time
import csv
from threading import Lock
from collections import defaultdict

videosProcessed = 0
counter_lock = Lock()
data_lock = Lock()

createdByDict = defaultdict(int)

def showProgress(progress):
	sys.stderr.write(f'\r{progress} processed...\r')
	sys.stderr.flush()

#===========================================
# callback to check who uploaded the video
#===========================================
def getCreatedByReport(video):
	global createdByDict
	global videosProcessed

	creator = GetCMS().GetCreatedBy(video)

	with data_lock:
		createdByDict[creator] += 1

	with counter_lock:
		videosProcessed += 1
	if(videosProcessed%100==0):
		showProgress(videosProcessed)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	s = time.perf_counter()
	main(getCreatedByReport)
	showProgress(videosProcessed)
	elapsed = time.perf_counter() - s
	eprint(f"\n{__file__} executed in {elapsed:0.2f} seconds.\n")	

	row_list = [ ['user_id','number_videos'] ]
	for x,y in createdByDict.items():
		row_list.append([x,y])

	#write list to file
	try:
		with open('report.csv' if not GetArgs().o else GetArgs().o, 'w', newline='', encoding='utf-8') as file:
			try:
				writer = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter=',')
				writer.writerows(row_list)
			except Exception as e:
				eprint(f'\nError writing CSV data to file: {e}')
	except Exception as e:
		eprint(f'\nError creating outputfile: {e}')
