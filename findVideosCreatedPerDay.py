#!/usr/bin/env python3
import sys
import argparse
from calendar import monthrange
from brightcove.CMS import CMS
from brightcove.OAuth import OAuth
from brightcove.utils import load_account_info

# init the argument parsing
parser = argparse.ArgumentParser(prog=sys.argv[0])
parser.add_argument('--start', metavar='<YYYY-MM>', type=str, help='Start date')
parser.add_argument('--end', metavar='<YYYY-MM>', type=str, help='End date (inclusive)')

# parse the args
args = parser.parse_args()

# do we have some dates?
if not args.start or not args.end:
	print('ERROR: either start or end date is missing.')
	sys.exit(2)

# parse start year and month
start_year = int(args.start.split('-')[0])
start_month = int(args.start.split('-')[1])

# parse end year and month
end_year = int(args.end.split('-')[0])
end_month = int(args.end.split('-')[1])

# sanity checks
if start_year>end_year:
	print('ERROR: end year before start year.')
	sys.exit(2)

if start_year==end_year and start_month>end_month:
	print('ERROR: end month before start month.')
	sys.exit(2)

# get account info from config file
try:
	account_id, client_id, client_secret, _ = load_account_info()
except Exception as e:
	print(e)
	sys.exit(2)

# create a CMS API instance
cms = CMS(OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret))

# init variables for ze loop
current_year = start_year
current_month = start_month
stop_search = False

# loop through each month and find videos created that month
while not stop_search:
	print(f'Searching for videos created {current_year}/{current_month:02}:')

	# get number of days in a month
	days_in_week, days_in_month =  monthrange(current_year, current_month)

	# find how many videos were created each day in a month
	for currentDay in range(1,days_in_month+1):
		query = f'+created_at:{current_year}-{current_month:02}-{currentDay:02}T00:00:00.000Z..{current_year}-{current_month:02}-{currentDay:02}T23:59:59.000Z'
		print(f'{currentDay}. {cms.GetVideoCount(search_query=query)}')

	# neeeeeext month
	current_month += 1

	# have we reached the target year/month yet?
	if current_year==end_year and current_month>end_month:
		stop_search = True # could break here, but doing this way in case we add other exit cases

	# if we are past December move on to next year and reset to January
	elif current_month>12:
		current_year += 1
		current_month = 1
