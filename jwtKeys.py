#!/usr/bin/env python3
import sys
import argparse
from mackee import OAuth
from mackee import JWT
from mackee import LoadAccountInfo

# disable certificate warnings
import urllib3
urllib3.disable_warnings()

# init the argument parsing
parser = argparse.ArgumentParser(prog=sys.argv[0])
parser.add_argument('--list', action='store_true', default=False, help='List all keys in account')
parser.add_argument('--add', metavar='<key data>', type=str, help='Add a key to account')
parser.add_argument('--delete', metavar='<key ID|all>', type=str, help='Delete a key by ID or all')
parser.add_argument('--config', metavar='<config filename>', type=str, help='Name and path of account config information file')
parser.add_argument('--account', metavar='<Brightcove Account ID>', type=str, help='Brightcove Account ID to use (if different from ID in config)')

# parse the args
args = parser.parse_args()

# get account info from config file
account_id, client_id, client_secret, _ = LoadAccountInfo(args.config)

# if account ID was provided override the one from config
if(args.account):
	account_id = args.account

# create a JWT API instance
jwt = JWT( OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret) )

# delete one or all keys
if(args.delete):
	if(args.delete=='all'):
		keyList = jwt.ListKeys().json()
		for sub in keyList:
			print(jwt.DeleteKey(keyID=sub['id']).text)
	else:
		print(jwt.DeleteKey(keyID=args.delete).text)

# add a key
if(args.add):
	private_key = ''
	try:
		with open(args.add, 'r') as file:
			lines = file.readlines()

			for line in lines:
				if(not '-----' in line):
					private_key += line.strip()
	except:
		print('Error trying to access private keyfile "'+str(args.keyfile)+'".')
		sys.exit(2)

	print(jwt.RegisterKey(keyData=private_key).text)

# show all keys
if(args.list):
	print(jwt.ListKeys().text)
