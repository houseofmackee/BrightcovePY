#!/usr/bin/env python3
import sys
import argparse
from mackee import CMS
from mackee import OAuth
from mackee import GetAccountInfo

# init the argument parsing
parser = argparse.ArgumentParser(prog=sys.argv[0])
parser.add_argument('--start', metavar='<YYYY-MM>', type=str, help='Start date')
parser.add_argument('--end', metavar='<YYYY-MM>', type=str, help='End date (inclusive)')

# parse the args
args = parser.parse_args()

# do we have some dates?
if(not args.start or not args.end):
	print('ERROR: either start or end date is missing.')
	sys.exit(2)

# parse start year and month
startYear = int(args.start.split('-')[0])
startMonth = int(args.start.split('-')[1])

# parse end year and month
endYear = int(args.end.split('-')[0])
endMonth = int(args.end.split('-')[1])

# sanity checks
if(startYear>endYear):
	print('ERROR: end year before start year.')
	sys.exit(2)

if(startYear==endYear and startMonth>endMonth):
	print('ERROR: end month before start month.')
	sys.exit(2)

# get account info from config file
account_id, client_id, client_secret, _ = GetAccountInfo()

# create a CMS API instance
cms = CMS( OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret) )

# init variables for ze loop
currentYear = startYear
currentMonth = startMonth
stopSearch = False

# loop through each month and find videos created that month
while True:
	print(f'Searching for videos created {currentYear}/{currentMonth:02}:')

	for currentDay in range(1,32):
		query = f'+created_at:{currentYear}-{currentMonth:02}-{currentDay:02}T00:00:00.000Z..{currentYear}-{currentMonth:02}-{currentDay:02}T23:59:59.000Z'
		print(str(currentDay)+'. '+str(cms.GetVideoCount(searchQuery=query)) )

	currentMonth += 1

	if(currentYear==endYear and currentMonth>endMonth):
		stopSearch = True # could break here, but doing this way in case we add other exit cases
	elif(currentMonth>12):
		currentYear += 1
		currentMonth = 1

	if(stopSearch):
		break
