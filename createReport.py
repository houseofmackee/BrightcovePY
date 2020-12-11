#!/usr/bin/env python3
from mackee import main, get_args
from brightcove.utils import list_to_csv, eprint
from threading import Lock
import sys

row_list = [ ['id', 'name', 'state', 'reference_id', 'created_at', 'tags'] ]

counter_lock = Lock()
data_lock = Lock()

videos_processed = 0

def show_progress(progress):
	sys.stderr.write(f'\r{progress} processed...\r')
	sys.stderr.flush()

def create_csv(video):
	global row_list
	global videos_processed

	row = [ video.get(field) for field in row_list[0] ]

	with data_lock:
		row_list.append(row)

	with counter_lock:
		videos_processed += 1

	if videos_processed%100==0:
		show_progress(videos_processed)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	#generate the CSV list
	main(create_csv)
	show_progress(videos_processed)

	#write list to file
	try:
		list_to_csv(row_list, get_args().o)
	except Exception as e:
		eprint(f'\n{e}')
