#!/usr/bin/env python3
import time
from csv import Error as CSVError
from threading import Lock
from collections import defaultdict
from mackee import main, get_cms, get_args
from brightcove.utils import list_to_csv, eprint
from brightcove.utils import SimpleProgressDisplay, TimeString

data_lock = Lock()
created_by_dict:defaultdict = defaultdict(int)
show_progress = SimpleProgressDisplay(steps=100, add_info='videos processed')

#===========================================
# callback to check who uploaded the video
#===========================================
def get_created_by_report(video: dict):
	"""
	Adds creator of the video to the dictionary.
	"""

	creator = get_cms().GetCreatedBy(video)

	with data_lock:
		created_by_dict[creator] += 1
		show_progress()

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	s = time.perf_counter()
	main(get_created_by_report)
	show_progress(force_display=True)

	row_list = [ ['user_id','number_videos'] ]
	for x,y in created_by_dict.items():
		row_list.append([x,y])

	#write list to file
	try:
		list_to_csv(row_list, get_args().o)
	except (OSError, CSVError) as e:
		eprint(f'\n{e}')

	elapsed = time.perf_counter() - s
	eprint(f"\n{__file__} executed in {TimeString.from_seconds(elapsed)}.")
