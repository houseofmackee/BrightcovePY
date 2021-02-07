#!/usr/bin/env python3
from threading import Lock
from csv import Error as CSVError
from time import perf_counter
from mackee import main, get_args
from brightcove.utils import list_to_csv, eprint
from brightcove.utils import SimpleProgressDisplay, TimeString

tag_list = ['unique_tags_in_account']

# some globals
data_lock = Lock()
show_progress = SimpleProgressDisplay(steps=100, add_info='videos processed')

def create_report(video: dict) -> None:
    """
    Function to add a row of information about a video object to the report.

    Args:
        video (dict): video object obtained from the CMS API.
    """
    with data_lock:
        tag_list.extend(item for item in video.get('tags',[]) if item not in tag_list)
        show_progress()

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
    # generate the report
    s = perf_counter()
    main(create_report)
    show_progress(force_display=True)

    # write report to CSV file
    try:
        list_to_csv(tag_list, get_args().o)
    except (OSError, CSVError) as e:
        eprint(f'\n{e}')

    elapsed = perf_counter() - s
    eprint(f"\n{__file__} executed in {TimeString.from_seconds(elapsed)}.")
