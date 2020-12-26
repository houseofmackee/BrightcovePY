#!/usr/bin/env python3
import sys
import argparse
from pprint import pprint
from brightcove.OAuth import OAuth
from brightcove.Key import Key
from brightcove.utils import load_account_info

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
try:
	account_id, client_id, client_secret, _ = load_account_info(args.config)
except Exception as e:
	print(e)
	sys.exit(2)

# if account ID was provided override the one from config
account_id = args.account or account_id

# create a JWT API instance
jwt = Key( OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret) )

# delete one or all keys
if args.delete:
	if args.delete=='all':
		keyList = jwt.ListPublicKeys().json()
		for sub in keyList:
			print(jwt.DeletePublicKey(key_id=sub['id']).text)
	else:
		print(jwt.DeletePublicKey(key_id=args.delete).text)

# add a key
if args.add:
	private_key = ''
	try:
		with open(args.add, 'r') as file:
			lines = file.readlines()

			for line in lines:
				if not '-----' in line:
					private_key += line.strip()
	except:
		print(f'Error trying to access private keyfile "{args.keyfile}".')
		sys.exit(2)

	print(jwt.RegisterPublicKey(key_data=private_key).text)

# show all keys
if args.list:
	pprint(jwt.ListPublicKeys().json())
