#!/usr/bin/env python3
import mackee
from threading import Lock
import csv

row_list = [ ['id', 'name', 'state', 'reference_id', 'created_at', 'tags'] ]

counter_lock = Lock()
data_lock = Lock()

videosProcessed = 0

def showProgress(progress):
	mackee.sys.stderr.write(f'\r{progress} processed...\r')
	mackee.sys.stderr.flush()

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
	mackee.main(createCSV)
	showProgress(videosProcessed)

	#write list to file
	try:
		with open('report.csv' if not mackee.args.o else mackee.args.o, 'w', newline='', encoding='utf-8') as file:
			try:
				writer = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter=',')
				writer.writerows(row_list)
			except Exception as e:
				mackee.eprint(f'\nError writing CSV data to file: {e}')
	except Exception as e:
		mackee.eprint(f'\nError creating outputfile: {e}')
