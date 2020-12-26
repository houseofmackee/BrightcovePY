#!/usr/bin/env python3
import sys
import argparse
from json import JSONDecodeError
from brightcove.OAuth import OAuth
from brightcove.IngestProfiles import IngestProfiles
from brightcove.utils import load_account_info
from brightcove.utils import videos_from_file
from brightcove.utils import eprint

# init the argument parsing
parser = argparse.ArgumentParser(prog=sys.argv[0])
parser.add_argument('--config', metavar='<config filename>', type=str, help='Name and path of account config information file')
parser.add_argument('--account', metavar='<Brightcove Account ID>', type=str, help='Brightcove Account ID to use (if different from ID in config)')
parser.add_argument('--xls', metavar='<XLS/CSV file>', type=str, help='file with account IDs in account_id column')

# parse the args
args = parser.parse_args()

# get account info from config file
try:
	account_id, client_id, client_secret, opts = load_account_info(args.config)
except (OSError, JSONDecodeError) as e:
	print(e)
	sys.exit(2)

# if account ID was provided override the one from config
account_id = args.account or account_id

# create a Ingest Profiles API instance
ingest_profiles = IngestProfiles(OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret))

# list of account IDs to check
acc_ids:list = []

# if list is empty try to get it from xls or config JSON
if not acc_ids:
	# if we have an xls/csv
	if args.xls:
		try:
			acc_ids = videos_from_file(args.xls, column_name='account_id')
		except Exception as e:
			print(e)
			sys.exit(2)

	# otherwise just use the options from the config file
	elif opts:
		acc_ids = opts.get('target_account_ids', [])

if acc_ids:
	print('account_id, display_name, name')
	for acc_id in acc_ids:

		response = ingest_profiles.GetDefaultProfile(account_id=acc_id)
		if response.status_code == 200:
			dpid = response.json().get('default_profile_id')

			response = ingest_profiles.GetIngestProfile(account_id=acc_id, profile_id=dpid)
			if response.status_code == 200:
				display_name = response.json().get('display_name')
				name = response.json().get('name')
				print(f'{acc_id}, {display_name}, {name}')
else:
	eprint('No account IDs provided.')
