"""
script to create a live API report for an API key
"""
import sys
from os import getenv
from argparse import ArgumentParser
from brightcove.Live import Live, LiveQueryParameters
from brightcove.utils import get_value, default_split

# init the argument parsing
parser = ArgumentParser(prog=sys.argv[0])
parser.add_argument('--xkey', metavar='<API key>', type=str, help='Live API Key')
args = parser.parse_args()

# get API key from command line or the env variable
if api_key := args.xkey or getenv('X_API_KEY', ''):
    # get all jobs associated with that API key
    if jobs := Live(api_key=api_key).ListLiveJobs(LiveQueryParameters(page_size='1000')).json().get('jobs'):
        # define the info we want (edit as needed)
        # use . to to get sub fields (like specific custom fields (e.g. 'videocloud.video.name'))
        # use : to specify a default value in case the response is empty (e.g 'name:NoName')
        # use [] to specify a specific index
        info_list = ['id', 'state', 'channel_type', 'protocol', 'static', 'sep_state', 'videocloud.video.name']

        # print header for CSV
        print(*info_list, sep=', ')

        # get all info from all returned jobs and print it
        for job in jobs:
            print(*[get_value(job, *default_split(data=field, separator=':', maxsplits=1)) for field in info_list], sep=', ')
    else:
        print(f'Error while getting jobs for API key "{api_key}"')
else:
    print('No API key provided or found in env.')
