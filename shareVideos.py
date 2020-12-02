#!/usr/bin/env python3
import sys
import requests
import json
import argparse
import getopt

# disable certificate warnings
import urllib3
urllib3.disable_warnings()

# global variables
pub_id = None
client_id = None
client_secret = None

access_token_url = "https://oauth.brightcove.com/v4/access_token"
cms_base_url = "https://cms.api.brightcove.com/v1/accounts/{pubid}"

#===========================================
# get OAuth token for API calls
#===========================================
def get_access_token():
	access_token = None
	r = requests.post(access_token_url, params="grant_type=client_credentials", auth=(client_id, client_secret), verify=False)
	if r.status_code == 200:
		access_token = r.json().get('access_token')
	return access_token

#===========================================
# read account info from JSON file
#===========================================
def get_account_info(input_filename):
	global pub_id
	global client_id
	global client_secret

	# read file
	try:
		myfile = open(input_filename, 'r')
	except:
		print("Error: unable to open {filename}").format(filename=input_filename)
		sys.exit(2)
	else:
		data=myfile.read()

	# parse file
	obj = json.loads(data)

	# fetch the relevant info
	pub_id=str(obj["account_id"]).strip()
	client_id=str(obj["client_id"]).strip()
	client_secret=str(obj["client_secret"]).strip()

	# return the object just in case it's needed later
	return obj

#===========================================
# share list of videos to target account
#===========================================
def share_videos(inputfile):
	# get the account info and credentials
	obj = get_account_info(inputfile)

	# create the JSON body for the target accounts
	target_account_ids=obj.get("target_account_ids")
	json_body = json.dumps(target_account_ids)

	# get the access token and set request headers
	access_token = get_access_token()
	headers = { 'Authorization': 'Bearer ' + access_token, "Content-Type": "application/json" }

	# share each video to the list of accounts
	for video_id in obj.get("video_ids"):
		video_id=str(video_id).strip()
		api_call = (cms_base_url+r"/videos/{video_id}/shares").format(pubid=pub_id, video_id=video_id)
		r = requests.post(api_call, headers=headers, data=json_body)
		if r.status_code == 202:
			print(("Succesfully shared video ID {video_id}").format(video_id=video_id))
		elif r.status_code == 401:
			print(("Token expired, re-trying {video_id}").format(video_id=video_id))
			access_token = get_access_token()
			headers = { 'Authorization': 'Bearer ' + access_token, "Content-Type": "application/json" }
			r = requests.post(api_call, headers=headers, data=json_body)
		else:
			print(("Error ({error_code}) while sharing video ID {video_id}:").format(error_code=r.status_code, video_id=video_id))
			print(r.content)

#===========================================
# show how to use this script
#===========================================
def show_usage():
	print('Usage: sharevideos.py -i <inputfile>')

#===========================================
# parse args and call the sharing function
#===========================================
def main(argv):
	inputfile = None
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		show_usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			show_usage()
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg

	if(inputfile!=None):
		share_videos(inputfile)
	else:
		show_usage()

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == "__main__":
	main(sys.argv[1:])
