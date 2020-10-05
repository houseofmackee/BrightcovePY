#!/usr/bin/env python3
import mackee_async as mackee
from threading import Thread

videosProcessed = 0

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

	response = mackee.cms.GetDynamicRenditions(videoID=video.get('id'))
	if(response.status_code in mackee.cms.success_responses):
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

	masterSize = results[0]
	renditionSize = results[1]
	videoId = video.get('id') 

	print(f'{videoId}, {masterSize}, {renditionSize}')

	videosProcessed += 1
	if(videosProcessed%100==0):
		showProgress(videosProcessed)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	import time
	print('video_id, master_size, renditions_size')
	s = time.perf_counter()
	mackee.main(findStorageSize)
	showProgress(videosProcessed)
	elapsed = time.perf_counter() - s
	mackee.eprint(f"\n{__file__} executed in {elapsed:0.2f} seconds.")	

