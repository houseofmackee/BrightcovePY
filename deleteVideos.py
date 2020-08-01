#!/usr/bin/env python3
import sys
import argparse
import math
from mackee import CMS
from mackee import OAuth
from mackee import GetAccountInfo
try:
	import pandas
except ImportError:
	pandas = None

# init the argument parsing
parser = argparse.ArgumentParser(prog=sys.argv[0])
parser.add_argument('--config', metavar='<config filename>', type=str, help='Name and path of account config information file')
parser.add_argument('--account', metavar='<Brightcove account ID>', type=str, help='Brightcove account ID to use (if different from ID in config)')
# if we have pandas add xls/column arguments
if(pandas):
	parser.add_argument('--xls', metavar='<XLS file>', type=str, help='Name of input XLS file')
	parser.add_argument('--column', metavar='<column name>', type=str, help='Name of video ID column in XLS file')

# parse the args
args = parser.parse_args()

# get account info from config file
account_id, client_id, client_secret, opts = GetAccountInfo(args.config)

# if account ID was provided override the one from config
if(args.account):
	account_id = args.account

# create a CMS API instance
cms = CMS( OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret) )

# if we have pandas and an xls and column then use that
if(pandas and args.xls and args.column):
	data = pandas.read_excel(args.xls) 
	for videoID in data[args.column]:
		# is it a float?
		if(type(videoID) is float):
			if(not math.isnan(videoID)):
				videoID = int(videoID)
			else:
				videoID = None
		# is it a string?
		elif (type(videoID) is str):
			try:
				videoID = int(videoID)
			except:
				videoID = None
		# is it an int?
		if(type(videoID) is int):
			print('Deleting video ID "'+str(videoID)+''": "+ str(cms.DeleteVideo(videoID=videoID).status_code))

# no pandas, so just use the options from the config file
else:
	# get list of videos from config file
	videoList = opts.get('video_ids')

	# either no list or "all" was found -> bail
	if(not videoList or videoList[0] == 'all'):
		print('Error: detected "all" option -> exiting because it is dangerous')
	# delete 'am all
	else:
		for videoID in videoList:
			print('Deleting video ID "'+str(videoID)+''": "+ str(cms.DeleteVideo(videoID=videoID).status_code))
