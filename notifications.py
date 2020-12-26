#!/usr/bin/env python3
import sys
import argparse
from pprint import pprint
from brightcove.CMS import CMS
from brightcove.OAuth import OAuth
from brightcove.utils import load_account_info

# init the argument parsing
parser = argparse.ArgumentParser(prog=sys.argv[0])
parser.add_argument('--list', action='store_true', default=False, help='List all subscription callbacks')
parser.add_argument('--add', metavar='<callback URL>', type=str, help='Add a subscription callback')
parser.add_argument('--delete', metavar='<subscription ID|all>', type=str, help='Delete a subscription callback ID or all')
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
cms = CMS(OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret))

# delete one or all subscriptions
if args.delete:
	if args.delete=='all':
		sub_list = cms.GetSubscriptionsList().json()
		for sub in sub_list:
			print(cms.DeleteSubscription(sub_id=sub['id']).text)
	else:
		print(cms.DeleteSubscription(sub_id=args.delete).text)

# add a subscription
if args.add:
	print(cms.CreateSubscription(callback_url=args.add).text)

# show all subscriptions
if args.list:
	pprint(cms.GetSubscriptionsList().json())
