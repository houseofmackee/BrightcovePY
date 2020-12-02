#!/usr/bin/env python3
from mackee import main, eprint, GetCMS, GetArgs, list_to_csv
import sys
import time
from threading import Lock
from collections import defaultdict

videos_processed = 0
counter_lock = Lock()
data_lock = Lock()

created_by_dict = defaultdict(int)

def show_progress(progress):
	sys.stderr.write(f'\r{progress} processed...\r')
	sys.stderr.flush()

#===========================================
# callback to check who uploaded the video
#===========================================
def get_created_by_report(video):
	global created_by_dict
	global videos_processed

	creator = GetCMS().GetCreatedBy(video)

	with data_lock:
		created_by_dict[creator] += 1

	with counter_lock:
		videos_processed += 1

	if videos_processed%100==0:
		show_progress(videos_processed)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	s = time.perf_counter()
	main(get_created_by_report)
	show_progress(videos_processed)
	elapsed = time.perf_counter() - s
	eprint(f"\n{__file__} executed in {elapsed:0.2f} seconds.\n")

	row_list = [ ['user_id','number_videos'] ]
	for x,y in created_by_dict.items():
		row_list.append([x,y])

	#write list to file
	list_to_csv(row_list, GetArgs().o)
