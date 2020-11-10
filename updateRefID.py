#!/usr/bin/env python3
import sys
import argparse
import math
import pandas
import time
from mackee import CMS
from mackee import OAuth
from mackee import LoadAccountInfo

cms = None

# account/API credentials (can be None to use user defaults)
account_id = None
client_id = None
client_secret = None

# names of the columns in the xls file
video_id_col = "video_id"
ref_id_col =  "reference_id"

# function to check if a video ID is valid and then update it
def updateVideo(videoID, updateData):
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
		response = cms.UpdateVideo(videoID=videoID, jsonBody=updateData).status_code
		print('Updating video ID "'+str(videoID)+'": '+ str(response))

		if(response==429):
			for remaining in range(3, 0, -1):
				sys.stderr.write('\rRetrying in {:2d} seconds.'.format(remaining))
				sys.stderr.flush()
				time.sleep(1)
			# let's call ourself again, shall we?
			updateVideo(videoID=videoID, updateData=updateData)

# init the argument parsing
parser = argparse.ArgumentParser(prog=sys.argv[0])
parser.add_argument('--config', metavar='<config filename>', type=str, help='Name and path of account config information file')
parser.add_argument('--account', metavar='<Brightcove account ID>', type=str, help='Brightcove account ID to use (if different from ID in config)')
parser.add_argument('--xls', metavar='<XLS file>', type=str, help='Name of input XLS file')
parser.add_argument('--validate', action='store_true', default=False, help='Validate the reference IDs, do not process')

# parse the args
args = parser.parse_args()

# get account info from config file if not hardcoded
if( account_id is None and client_id is None and client_secret is None):
	account_id, client_id, client_secret, _ = LoadAccountInfo(args.config)

# if account ID was provided override the one from config
if(args.account):
	account_id = args.account

# create a CMS API instance
cms = CMS( OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret) )

# if we have an xls let's get going
if(args.xls):
	data = pandas.read_excel(args.xls)

	# check if all ref IDs are unique
	numRows = len(data)

	# get the columns
	ref_data = data[ref_id_col]
	video_data = data[video_id_col]

	# check if all ref IDs are unique
	# can't use if( data[ref_id_col].nunique() != numRows ):
	isUnique = True
	for countA in range(numRows-1):
		valueA = ref_data[countA]
		for countB in range(countA+1, numRows):
			valueB = ref_data[countB]
			if(valueA==valueB):
				print(f'Error: ref IDs are not unique -> {countA+2}, {countB+2}, {valueA}')
				isUnique = False

	if(video_data.nunique() != numRows):
		print('Error: video IDs are not unique')
		isUnique = False

	if(not isUnique):
		sys.exit(2)

	if(args.validate):
		print('Reference IDs and video IDs are unique.')
		sys.exit(2)

	for row in range(0, len(data) ):
		videoID = int(video_data[row])
		refID = str(ref_data[row])

		jsonBody = ('{ "reference_id":"' + refID + '" }')

		updateVideo(videoID=videoID, updateData=jsonBody)

# no pandas, so just use the options from the config file
else:
	print('Error: no XLS file specified.')
