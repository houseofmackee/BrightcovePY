#!/usr/bin/env python3
import sys
import argparse
import csv
import concurrent.futures
from typing import List
from mackee import eprint
from mackee import CMS
from mackee import OAuth
from mackee import wrangle_id
from mackee import videos_from_file
from mackee import LoadAccountInfo

# account/API credentials (can be None to use user defaults)
account_id = None
client_id = None
client_secret = None

cms = None
opts = None

def showProgress(progress:int) -> None:
	sys.stderr.write(f'\r{progress} processed...\r')
	sys.stderr.flush()

# function to check if a video ID is valid and then delete it
def deleteVideo(video_id:str) -> List:
	global cms
	_, work_id = wrangle_id(video_id)
	if(work_id):
		response = cms.DeleteVideo(videoID=work_id).status_code
		# if it failed try to remove it from playlists and try again
		if(response==409):
			cms.RemoveVideoFromAllPlaylists(videoID=work_id)
			response = cms.DeleteVideo(videoID=work_id).status_code
	
		return [video_id, response]
	
	return [video_id, 'invalid video ID']

# init the argument parsing
parser = argparse.ArgumentParser(prog=sys.argv[0])
parser.add_argument('--config', metavar='<filename>', type=str, help='Name and path of account config information file')
parser.add_argument('--account', metavar='<Brightcove account ID>', type=str, help='Brightcove account ID to use (if different from ID in config)')
parser.add_argument('--report', metavar='<filename>', type=str, help='Name for deletion report')
parser.add_argument('--xls', metavar='<XLS/CSV file>', type=str, help='Name of input XLS or CSV file')
parser.add_argument('--column', metavar='<column name>', type=str, help='Name of video ID column in XLS file')

# parse the args
args = parser.parse_args()

# get account info from config file if not hardcoded
if( account_id is None and client_id is None and client_secret is None):
	account_id, client_id, client_secret, opts = LoadAccountInfo(args.config)

# if account ID was provided override the one from config
if(args.account):
	account_id = args.account

# create a CMS API instance
cms = CMS( OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret) )

# list to contain all video IDs
videoList = None

# if we have an xls/csv
if(args.xls):
	videoList = videos_from_file(args.xls, column_name=args.column if args.column else 'video_id')

# otherwise just use the options from the config file
elif(opts):
	videoList = opts.get('video_ids')

# either no list or "all" was found -> bail
if(not videoList or videoList[0] == 'all'):
	eprint('Error: invalid or missing list of videos in config file.')

# delete 'em
else:
	videosProcessed = 0
	row_list = [['operation','video_id','result']]
	with concurrent.futures.ThreadPoolExecutor(max_workers = 5) as executor:
		future_to_videoid = {executor.submit(deleteVideo, videoID): videoID for videoID in videoList}
		for future in concurrent.futures.as_completed(future_to_videoid):
			video = future_to_videoid[future]
			try:
				data = future.result()
			except Exception as exc:
				eprint(f'{video} generated an exception: {exc}')
			else:
				# display counter every 100 videos
				videosProcessed += 1
				if(videosProcessed%100==0):
					showProgress(videosProcessed)
				if(data):
					row_list.append(['delete', data[0], data[1]])

	showProgress(videosProcessed)

	#write list to file
	try:
		with open('report.csv' if not args.report else args.report, 'w', newline='', encoding='utf-8') as file:
			try:
				writer = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter=',')
				writer.writerows(row_list)
			except Exception as e:
				eprint(f'\nError writing CSV data to file: {e}')
	except Exception as e:
		eprint(f'\nError creating outputfile: {e}')
