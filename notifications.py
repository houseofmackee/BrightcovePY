#!/usr/bin/env python3
import sys
import argparse
from mackee import CMS
from mackee import OAuth
from mackee import GetAccountInfo

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
account_id, client_id, client_secret, _ = GetAccountInfo(args.config)

# if account ID was provided override the one from config
if(args.account):
	account_id = args.account

# create a CMS API instance
cms = CMS( OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret) )

# delete one or all subscriptions
if(args.delete):
	if(args.delete=='all'):
		subList = cms.GetSubscriptionsList().json()
		for sub in subList:
			print(cms.DeleteSubscription(subID=sub['id']).text)
	else:
		print(cms.DeleteSubscription(subID=args.delete).text)

# add a subscription
if(args.add):
	print(cms.CreateSubscription(callbackURL=args.add).text)

# show all subscriptions
if(args.list):
	print(cms.GetSubscriptionsList().text)
