#!/usr/bin/env python3
import sys
import argparse
from brightcove.CMS import CMS
from brightcove.OAuth import OAuth
from brightcove.utils import load_account_info
from brightcove.utils import list_to_csv, eprint

# init the argument parsing
parser = argparse.ArgumentParser(prog=sys.argv[0])
parser.add_argument('--config', metavar='<config filename>', type=str, help='Name and path of account config information file')
parser.add_argument('--account', metavar='<Brightcove account ID>', type=str, help='Brightcove account ID to use (if different from ID in config)')
parser.add_argument('--out', metavar='<output filename>', type=str, help='Name and path for report output file')

# parse the args
args = parser.parse_args()

# account/API credentials (can be None to use user defaults)
account_id = ''
client_id = ''
client_secret = ''

# get account info from config file if not hardcoded
if None in [account_id, client_id, client_secret]:
	try:
		account_id, client_id, client_secret, _ = load_account_info(args.config)
	except Exception as e:
		print(e)
		sys.exit(2)

# if account ID was provided override the one from config
account_id = args.account or account_id

# create a CMS API instance
cms = CMS(oauth=OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret))

row_list = [ ['id', 'account_id', 'name', 'created_at', 'updated_at', 'video_count'] ]

response = cms.GetFolders()

if response.status_code == 200:
	folders = response.json()
	for folder in folders:
		row = [ folder.get(field) for field in row_list[0] ]
		row_list.append(row)

#write list to file
try:
	list_to_csv(row_list, args.out)
except Exception as e:
	eprint(f'{e}')
