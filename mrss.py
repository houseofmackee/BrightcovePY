#!/usr/bin/env python3
import sys
import argparse
from pprint import pprint
from brightcove.SocialSyndication import SocialSyndication
from brightcove.OAuth import OAuth
from brightcove.utils import load_account_info

# init the argument parsing
parser = argparse.ArgumentParser(prog=sys.argv[0])
parser.add_argument('--list', action='store_true', default=False, help='List all syndications for account')
parser.add_argument('--get', metavar='<syndication ID>', type=str, help='Get a specific syndication for account')
parser.add_argument('--delete', metavar='<all|syndication ID>', type=str, help='Delete one or all syndications for account')
parser.add_argument('--add', metavar='<JSON body>', type=str, help='Add a syndication to account')
parser.add_argument('--config', metavar='<config filename>', type=str, help='Name and path of account config information file')
parser.add_argument('--account', metavar='<Brightcove Account ID>', type=str, help='Brightcove Account ID to use (if different from ID in config)')

# parse the args
args = parser.parse_args()

# get account info from config file
try:
	account_id, client_id, client_secret, _ = load_account_info(args.config)
except Exception as e:
	print(e)
	sys.exit(2)

# if account ID was provided override the one from config
account_id = args.account or account_id

# create a CMS API instance
mrss = SocialSyndication(OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret))

# add syndication to account
if args.add:
	print(mrss.CreateSyndication(account_id=account_id,json_body=args.add).text)

# delete one or all syndication
if args.delete:
	# the actual delete function
	def delete_sid(s_id):
		"""
		Delete a single syndication ID
		"""
		print(f'Deleting syndication ID {s_id}: {mrss.DeleteSyndication(account_id=account_id, syndication_id=s_id).status_code}')

	# delete all?
	if args.delete=='all':
		syn_list = mrss.GetAllSyndications(account_id=account_id).json()
		for syn in syn_list:
			delete_sid(syn['id'])
	# just delete one
	else:
		delete_sid(args.delete)

# list all syndications in an account
if args.list:
	pprint(mrss.GetAllSyndications(account_id=account_id).json())

# get a specific syndication
if args.get:
	pprint(mrss.GetSyndication(account_id=account_id, syndication_id=args.get).json())
