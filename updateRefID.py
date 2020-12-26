#!/usr/bin/env python3
from typing import Union
import time
import sys
import argparse
import pandas
from brightcove.CMS import CMS
from brightcove.OAuth import OAuth
from brightcove.utils import load_account_info, normalize_id

# names of the columns in the xls file
video_id_col = 'video_id'
ref_id_col =  'reference_id'

# function to check if a video ID is valid and then update it
def update_video(cms_api: CMS, vid_id: str, update_data: Union[str, dict]) -> None:
	"""
	Updates a video using the data in the JSON.

	Args:
		cms_api (CMS): CMS API instance to use.
		video_id (str): Video ID to update.
		update_data (Union[str, dict]): Update data in JSON format.
	"""
	vid_id = normalize_id(vid_id)
	if vid_id:
		response = cms_api.UpdateVideo(video_id=vid_id, json_body=update_data).status_code
		print(f'Updating video ID "{vid_id}": {response}')

		if response==429:
			for remaining in range(3, 0, -1):
				sys.stderr.write(f'\rRetrying in {remaining:2d} seconds.')
				sys.stderr.flush()
				time.sleep(1)
			# let's call ourself again, shall we?
			update_video(cms_api=cms_api, vid_id=vid_id, update_data=update_data)

# init the argument parsing
parser = argparse.ArgumentParser(prog=sys.argv[0])
parser.add_argument('--config', metavar='<config filename>', type=str, help='Name and path of account config information file')
parser.add_argument('--account', metavar='<Brightcove account ID>', type=str, help='Brightcove account ID to use (if different from ID in config)')
parser.add_argument('--xls', metavar='<XLS file>', type=str, help='Name of input XLS file')
parser.add_argument('--validate', action='store_true', default=False, help='Validate the reference IDs, do not process')

# parse the args
args = parser.parse_args()

# account/API credentials (can be None to use user defaults)
account_id = ''
client_id = ''
client_secret = ''

# get account info from config file if not hardcoded
if '' in [account_id, client_id, client_secret]:
	try:
		account_id, client_id, client_secret, _ = load_account_info(args.config)
	except Exception as e:
		print(e)
		sys.exit(2)

# if account ID was provided override the one from config
account_id = args.account or account_id

# create a CMS API instance
cms = CMS( oauth=OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret) )

# if we have an xls let's get going
if args.xls:
	data = pandas.read_excel(args.xls) # type: ignore

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
		video_id = str(video_data[row])
		ref_id = str(ref_data[row])
		json_body = { "reference_id": ref_id }
		update_video(cms_api=cms, vid_id=video_id, update_data=json_body)

# no pandas, so just use the options from the config file
else:
	print('Error: no XLS file specified.')
