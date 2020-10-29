#!/usr/bin/env python3
import sys
import argparse
import math
import concurrent.futures
from mackee import eprint
from mackee import CMS
from mackee import OAuth
from mackee import GetAccountInfo
try:
	import pandas
except ImportError:
	pandas = None

# account/API credentials (can be None to use user defaults)
account_id = None
client_id = None
client_secret = None

column_name = 'video_id'

cms = None
opts = None

# function to check if a video ID is valid and then delete it
def deleteVideo(videoID):
	global cms
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
		response = cms.DeleteVideo(videoID=videoID).status_code
		# if it failed try to remove it from playlists and try again
		if(response==409):
			cms.RemoveVideoFromAllPlaylists(videoID=videoID)
			response = cms.DeleteVideo(videoID=videoID).status_code

		return [videoID, response]

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

# get account info from config file if not hardcoded
if( account_id is None and client_id is None and client_secret is None):
	account_id, client_id, client_secret, opts = GetAccountInfo(args.config)

# if account ID was provided override the one from config
if(args.account):
	account_id = args.account

# if a column name was passed then use that
if(args.column):
	column_name = args.column

# create a CMS API instance
cms = CMS( OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret) )

# list to contain all video IDs
videoList = None

# if we have pandas and an xls and column then use that
if(pandas and args.xls):
	data = pandas.read_excel(args.xls) 
	videoList = [videoID for videoID in data[column_name]]

# no pandas, so just use the options from the config file
elif(opts):
	# get list of videos from config file
	videoList = opts.get('video_ids')

# either no list or "all" was found -> bail
if(not videoList or videoList[0] == 'all'):
	eprint('Error: invalid or missing list of videos in config file.')

# delete 'em
else:
	with concurrent.futures.ThreadPoolExecutor(max_workers = 5) as executor:
		future_to_videoid = {executor.submit(deleteVideo, videoID): videoID for videoID in videoList}
		for future in concurrent.futures.as_completed(future_to_videoid):
			video = future_to_videoid[future]
			try:
				data = future.result()
			except Exception as exc:
				eprint(f'{video} generated an exception: {exc}')
			else:
				print(f'delete, {data[0]}, {data[1]}')
