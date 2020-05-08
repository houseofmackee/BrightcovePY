#!/usr/bin/env python3
import sys
import argparse
from mackee import SocialSyndication
from mackee import OAuth
from mackee import GetAccountInfo

# init the argument parsing
parser = argparse.ArgumentParser(prog=sys.argv[0])
parser.add_argument('--list', action='store_true', default=False, help='List all syndications for an')
parser.add_argument('--get', metavar='<syndication ID>', type=str, help='List all syndications for an')
parser.add_argument('--delete', metavar='<all|syndication ID>', help='Delete one or all syndications in account')
parser.add_argument('--add', metavar='<JSON body>', help='Add a syndication to account')
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
mrss = SocialSyndication( OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret) )

# add syndication to account
if(args.add):
	print( mrss.CreateSyndication(accountID=account_id,jsonBody=args.add).text )

# delete one or all syndication
if(args.delete):
	# delete all?
	if(args.delete=='all'):
		synList = mrss.GetAllSyndications(accountID=account_id).json()
		for syn in synList:
			sID= syn['id']
			print( 'Deleting syndication ID '+sID+': '+str(mrss.DeleteSyndication(accountID=account_id, syndicationID=syn['id']).status_code) )
	# just delete one
	else:
		print( 'Deleting syndication ID '+args.delete+': '+str(mrss.DeleteSyndication(accountID=account_id, syndicationID=args.delete).status_code) )

# list all syndications in an account
if(args.list):
	print( mrss.GetAllSyndications(accountID=account_id).text )

# get a specific syndication
if(args.get):
	print( mrss.GetSyndication(accountID=account_id, syndicationID=args.get).text )
