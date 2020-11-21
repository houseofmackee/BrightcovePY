#!/usr/bin/env python3
from mackee import main, eprint, GetCMS, GetArgs
from threading import Lock
import csv
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
	try:
		with open('report.csv' if not GetArgs().o else GetArgs().o, 'w', newline='', encoding='utf-8') as file:
			try:
				writer = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter=',')
				writer.writerows(row_list)
			except Exception as e:
				eprint(f'\nError writing CSV data to file: {e}')
	except Exception as e:
		eprint(f'\nError creating outputfile: {e}')
