#!/usr/bin/env python3
import sys
import argparse
import csv
from mackee import eprint
from mackee import CMS
from mackee import OAuth
from mackee import LoadAccountInfo

# account/API credentials (can be None to use user defaults)
account_id = None
client_id = None
client_secret = None

cms = None

# init the argument parsing
parser = argparse.ArgumentParser(prog=sys.argv[0])
parser.add_argument('--config', metavar='<config filename>', type=str, help='Name and path of account config information file')
parser.add_argument('--account', metavar='<Brightcove account ID>', type=str, help='Brightcove account ID to use (if different from ID in config)')
parser.add_argument('--out', metavar='<output filename>', type=str, help='Name and path for report output file')

# parse the args
args = parser.parse_args()

# get account info from config file if not hardcoded
if( account_id is None and client_id is None and client_secret is None):
	account_id, client_id, client_secret, _ = LoadAccountInfo(args.config)

# if account ID was provided override the one from config
if(args.account):
	account_id = args.account

# create a CMS API instance
cms = CMS( OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret) )

row_list = [ ['id', 'account_id', 'name', 'created_at', 'updated_at', 'video_count'] ]

response = cms.GetFolders()

if(response.status_code == 200):
	folders = response.json()
	for folder in folders:
		row = [ folder.get(field) for field in row_list[0] ]
		row_list.append(row)

#write list to file
try:
	with open('report.csv' if not args.out else args.out, 'w', newline='', encoding='utf-8') as file:
		try:
			writer = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter=',')
			writer.writerows(row_list)
		except Exception as e:
			eprint(f'\nError writing CSV data to file: {e}')
except Exception as e:
	eprint(f'\nError creating outputfile: {e}')
