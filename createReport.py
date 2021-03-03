#!/usr/bin/env python3
from threading import Lock
from csv import Error as CSVError
from mackee import main, get_args
from brightcove.utils import list_to_csv, eprint
from brightcove.utils import SimpleProgressDisplay, SimpleTimer
from brightcove.utils import get_value, default_split

# list of information to be added to the report (edit as needed)
# use . to to get sub fields (like specific custom fields (e.g. 'custom_fields.my_field'))
# use : to specify a default value in case the response is empty (e.g 'name:NoName')
# use [] to specify a specific index
row_list = [ ('account_id','id', 'name', 'state', 'reference_id', 'created_at', 'tags', 'created_by.type') ]

# some globals
data_lock = Lock()
show_progress = SimpleProgressDisplay(steps=100, add_info='videos processed')

def create_report(video: dict) -> None:
	"""
	Function to add a row of information about a video object to the report.

	Args:
		video (dict): video object obtained from the CMS API.
	"""
	row = (get_value(video, *default_split(field, separator=':', maxsplits=1)) for field in row_list[0])
	with data_lock:
		row_list.append(row)
		show_progress()

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
    with SimpleTimer():
        # generate the report
        main(create_report)
        show_progress(force_display=True)
        # write report to CSV file
        try:
            list_to_csv(row_list, get_args().o)
        except (OSError, CSVError) as e:
            eprint(f'\n{e}')
