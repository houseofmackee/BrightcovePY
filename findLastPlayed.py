"""
script to find the most recent playback date for videos which had playback within the last 30 days
"""
import sys
import argparse
from json import dumps
from brightcove.Analytics import Analytics, AnalyticsQueryParameters
from brightcove.OAuth import OAuth
from brightcove.utils import load_account_info

# init the argument parsing
parser = argparse.ArgumentParser(prog=sys.argv[0])
parser.add_argument('-i', metavar='<config filename>', type=str, help='Name and path of account config information file')
parser.add_argument('-t', metavar='<Brightcove Account ID>', type=str, help='Brightcove Account ID to use (if different from ID in config)')
parser.add_argument('-j', action='store_true', default=False, help='Use JSON output instead of CSV')

# parse the args
args = parser.parse_args()

# get account info from config file
try:
	account_id, client_id, client_secret, _ = load_account_info(args.i)
except Exception as e:
	print(e)
	sys.exit(2)

# if account ID was provided override the one from config
account_id = args.t or account_id

# get OAuth and Analytics API instance
oauth = OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret)
aapi = Analytics(oauth)

# set Analytics report query parameters
qstr = AnalyticsQueryParameters(
    accounts = account_id,
    dimensions = 'video,date',
    limit = 'all',
    fields= 'video.name,video_view',
    reconciled = False,
    sort = 'date',
    from_ = '-30d')

# fields that shoul;d be reported in addition to the video ID
report_fields = ['date', 'video_view', 'video.name']

# make API call
response = aapi.GetAnalyticsReport(query_parameters=qstr).json().get('items', {})

# create a dictionary with unique video IDs and their most recent playback date and print it
if unique_videos := {item.get('video'):[item.get(field) for field in report_fields] for item in response if item.get('video')}:
    if args.j:
        print(dumps(unique_videos, indent=4, sort_keys=True))
    else:
        print('video_id', *report_fields, sep=', ')
        for video, info in unique_videos.items():
            print(video, *info, sep=', ')
