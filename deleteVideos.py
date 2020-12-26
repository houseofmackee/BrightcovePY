#!/usr/bin/env python3
import sys
import argparse
import concurrent.futures
from typing import List
from brightcove.CMS import CMS
from brightcove.OAuth import OAuth
from brightcove.utils import load_account_info, eprint, wrangle_id, videos_from_file, list_to_csv

def show_progress(progress: int) -> None:
	"""
	Simple progess counter.
	"""
	sys.stderr.write(f'\r{progress} processed...\r')
	sys.stderr.flush()

# function to check if a video ID is valid and then delete it
def delete_video(video_id: str) -> List:
	"""
	Delete video ID in default account.
	Returns list [video ID, response]
	"""
	global cms
	_, work_id = wrangle_id(video_id)
	if work_id:
		response = cms.DeleteVideo(video_id=work_id).status_code
		# if it failed try to remove it from playlists and try again
		if response==409:
			cms.RemoveVideoFromAllPlaylists(video_id=work_id)
			response = cms.DeleteVideo(video_id=work_id).status_code

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

# account/API credentials (can be None to use user defaults)
account_id = ''
client_id = ''
client_secret = ''
opts:dict = {}

# get account info from config file if not hardcoded
if '' in [account_id, client_id, client_secret]:
	try:
		account_id, client_id, client_secret, opts = load_account_info(args.config)
	except Exception as e:
		print(e)
		sys.exit(2)

# if account ID was provided override the one from config
account_id = args.account or account_id

# create a CMS API instance
cms = CMS( OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret) )

# list to contain all video IDs
video_list = []

# if we have an xls/csv
if args.xls:
	try:
		video_list = videos_from_file(args.xls, column_name=args.column if args.column else 'video_id')
	except Exception as e:
		print(e)

# otherwise just use the options from the config file
elif opts:
	video_list = opts.get('video_ids')

# either no list or "all" was found -> bail
if not video_list or video_list[0] == 'all':
	eprint('Error: invalid or missing list of videos in config file.')

# delete 'em
else:
	videos_processed = 0
	row_list = [['operation','video_id','result']]
	with concurrent.futures.ThreadPoolExecutor(max_workers = 5) as executor:
		future_to_video_id = {executor.submit(delete_video, video_id): video_id for video_id in video_list}
		for future in concurrent.futures.as_completed(future_to_video_id):
			video = future_to_video_id[future]
			try:
				data = future.result()
			except Exception as exc:
				eprint(f'{video} generated an exception: {exc}')
			else:
				# display counter every 100 videos
				videos_processed += 1
				if videos_processed%100==0:
					show_progress(videos_processed)
				if data:
					row_list.append(['delete', data[0], data[1]])

	show_progress(videos_processed)

	#write list to file
	try:
		list_to_csv(row_list=row_list, filename=args.report)
	except Exception as e:
		eprint(f'\n{e}')
