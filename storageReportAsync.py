#!/usr/bin/env python3
import mackee
import csv
import time
from threading import Thread
from threading import Lock

videosProcessed = 0
counter_lock = Lock()
data_lock = Lock()

row_list = [ ['video_id','master_size','renditions_size'] ]

def showProgress(progress):
	mackee.sys.stderr.write(f'\r{progress} processed...\r')
	mackee.sys.stderr.flush()

#===========================================
# function to get size of master
#===========================================
def getMasterStorage(video, result, index):
	masterSize = 0
	if(video.get('has_digital_master')):
		shared = video.get('sharing')
		if(shared and shared.get('by_external_acct')):
			result[index] = 0
			return
		response = mackee.cms.GetDigitalMasterInfo(videoID=video.get('id'))
		if(response.status_code == 200):
			masterSize = response.json().get('size')

	result[index] = masterSize

#===========================================
# function to get size of all renditions
#===========================================
def getRenditionSizes(video, result, index):
	renSize = 0
	response = None
	delivery_type = video.get('delivery_type')

	if(delivery_type == 'static_origin'):
		response = mackee.cms.GetRenditionList(videoID=video.get('id'))
	elif(delivery_type == 'dynamic_origin'):
		response = mackee.cms.GetDynamicRenditions(videoID=video.get('id'))

	if(response and response.status_code in mackee.cms.success_responses):
		renditions = response.json()
		for rendition in renditions:
			renSize += rendition.get('size')

	result[index] = renSize

#===========================================
# callback getting storage sizes
#===========================================
def findStorageSize(video):
	global videosProcessed

	threads = []
	functions = [getMasterStorage, getRenditionSizes]
	results = [0 for x in functions]

	# In this case 'functions' is a list of functions to be executed per video ID
	for i in range(len(functions)):
		# We start one thread per function present
		thread = Thread(target=functions[i], args=[video, results, i])
		thread.start()
		threads.append(thread)

	# We now pause execution on the main thread by 'joining' all of our started threads.
	# This ensures that each has finished processing the functions
	for thread in threads:
		thread.join()

	# add a new row to the CSV data
	row = [ video.get('id'), results[0], results[1] ]
	with data_lock:
		row_list.append(row)

	# increase processed videos counter
	with counter_lock:
		videosProcessed += 1

	# display counter every 100 videos
	if(videosProcessed%100==0):
		showProgress(videosProcessed)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	s = time.perf_counter()
	mackee.main(findStorageSize)
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

	elapsed = time.perf_counter() - s
	mackee.eprint(f"\n{__file__} executed in {elapsed:0.2f} seconds.")	

