#!/usr/bin/env python3
import mackee
import json
import csv

row_list = [ ['id', 'name', 'status', 'reference_id', 'created_at', 'tags'] ]

videosProcessed = 0

def showProgress(progress):
	mackee.sys.stderr.write(f'\r{progress} processed...')
	mackee.sys.stderr.flush()

def createCSV(video):
	global row_list
	global videosProcessed

	row = []
	for field in row_list[0]:
		value = video.get(field)
		row.append(str('' if not value else value))

	row_list.append(row)

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
	with open('report.csv' if not mackee.args.o else mackee.args.o, 'w', newline='', encoding='utf-8') as file:
		writer = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter=',')
		writer.writerows(row_list)
