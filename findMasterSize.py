#!/usr/bin/env python3
from createReport import show_progress
import sys
import time
from threading import Lock
from requests.exceptions import RequestException
from mackee import main, eprint, GetCMS, GetArgs, TimeString, list_to_csv

data_lock = Lock()

row_list = [ ['video_id','delivery_type','master_size'] ]

class show_progress_gen():
	def __init__(self, steps:int=1) -> None:
		self.videos_processed = 0
		self.steps = steps
		self.lock = Lock()

	def __call__(self, force_display:bool=False):
		with self.lock:
			if not force_display:
				self.videos_processed += 1
			if force_display or self.videos_processed%self.steps==0:
				sys.stderr.write(f'\r{self.videos_processed} processed...\r')
				sys.stderr.flush()

show_progress = show_progress_gen(100)

#===========================================
# function to get size of master
#===========================================
def get_master_storage(video:dict) -> int:
	"""
	returns size of digital master if avaiable
	returns 0 if video has no master
	returns -1 in case of an error
	"""

	shared = video.get('sharing')
	if shared and shared.get('by_external_acct'):
		return 0

	if video.get('has_digital_master'):
		try:
			response = GetCMS().GetDigitalMasterInfo(video_id=video.get('id'))
		except RequestException:
			return -1
		else:
			if response.status_code == 200:
				return int(response.json().get('size'))
			return -1

	return 0

#===========================================
# callback getting storage sizes
#===========================================
def find_storage_size(video:dict) -> None:
	"""
	adds video ID, delivery type and master storage size to report list
	"""
	row = [ video.get('id'), video.get('delivery_type'), get_master_storage(video) ]

	# add a new row to the CSV data and increase counter
	with data_lock:
		row_list.append(row)
		show_progress()

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	s = time.perf_counter()
	main(find_storage_size)
	show_progress(True)

	#write list to file
	list_to_csv(row_list, GetArgs().o)

	elapsed = time.perf_counter() - s
	eprint(f"\n{__file__} executed in {TimeString.from_seconds(elapsed)}.")
