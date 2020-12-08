#!/usr/bin/env python3
import sys
import argparse
import pandas
import time
from mackee import CMS
from mackee import OAuth
from mackee import LoadAccountInfo
from mackee import normalize_id

cms = None

# account/API credentials (can be None to use user defaults)
account_id = None
client_id = None
client_secret = None

# names of the columns in the xls file
video_id_col = "video_id"
ref_id_col =  "reference_id"

# function to check if a video ID is valid and then update it
def update_video(video_id, update_data):
	global cms
	video_id = normalize_id(video_id)
	if video_id:
		response = cms.UpdateVideo(video_id=video_id, json_body=update_data).status_code
		print(f'Updating video ID "{video_id}": {response}')

		if response==429:
			for remaining in range(3, 0, -1):
				sys.stderr.write(f'\rRetrying in {remaining:2d} seconds.')
				sys.stderr.flush()
				time.sleep(1)
			# let's call ourself again, shall we?
			update_video(video_id=video_id, update_data=update_data)

# init the argument parsing
parser = argparse.ArgumentParser(prog=sys.argv[0])
parser.add_argument('--config', metavar='<config filename>', type=str, help='Name and path of account config information file')
parser.add_argument('--account', metavar='<Brightcove account ID>', type=str, help='Brightcove account ID to use (if different from ID in config)')
parser.add_argument('--xls', metavar='<XLS file>', type=str, help='Name of input XLS file')
parser.add_argument('--validate', action='store_true', default=False, help='Validate the reference IDs, do not process')

# parse the args
args = parser.parse_args()

# get account info from config file if not hardcoded
if None in [account_id, client_id, client_secret]:
	try:
		account_id, client_id, client_secret, _ = LoadAccountInfo(args.config)
	except Exception as e:
		print(e)
		sys.exit(2)

# if account ID was provided override the one from config
account_id = args.account or account_id

# create a CMS API instance
cms = CMS( OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret) )

# if we have an xls let's get going
if args.xls:
	data = pandas.read_excel(args.xls)

	# check if all ref IDs are unique
	num_rows = len(data)

	# get the columns
	ref_data = data[ref_id_col]
	video_data = data[video_id_col]

	# check if all ref IDs are unique
	# can't use if( data[ref_id_col].nunique() != numRows ):
	is_unique = True
	for count_a in range(num_rows-1):
		value_a = ref_data[count_a]
		for count_b in range(count_a+1, num_rows):
			value_b = ref_data[count_b]
			if value_a==value_b:
				print(f'Error: ref IDs are not unique -> {count_a+2}, {count_b+2}, {value_a}')
				is_unique = False

	if video_data.nunique() != num_rows:
		print('Error: video IDs are not unique')
		is_unique = False

	if not is_unique:
		sys.exit(2)

	if args.validate:
		print('Reference IDs and video IDs are unique.')
		sys.exit(2)

	for row in range(0, len(data) ):
		video_id = int(video_data[row])
		ref_id = str(ref_data[row])

		json_body = ('{ "reference_id":"' + ref_id + '" }')

		update_video(video_id=video_id, update_data=json_body)

# no pandas, so just use the options from the config file
else:
	print('Error: no XLS file specified.')
