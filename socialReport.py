#!/usr/bin/env python3
import sys
from mackee import Social
from mackee import OAuth
from mackee import load_account_info
from mackee import list_to_csv

videos_processed = 0
hits_to_process = 0
def show_progress(progress, total):
	sys.stderr.write(f'\r{progress}/{total} processed...\r')
	sys.stderr.flush()

cms = None

# account/API credentials (can be None to use user defaults)
account_id = None
client_id = None
client_secret = None

report_name = 'social_report.csv'

# get account info from config file if not hardcoded
if None in [account_id, client_id, client_secret]:
	try:
		account_id, client_id, client_secret, _ = load_account_info()
	except Exception as e:
		print(e)
		sys.exit(2)

# create a Social API instance
social = Social( OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret) )

page_key = None
keep_running = True

row_list = [ ['id','account_id','destination_id','remote_id','remote_url','status','timestamp','published_at','distribution_method','autosync_id','error','warning','action','result'] ]

while(keep_running):
	search_query = '' if not page_key else ('page_key='+page_key)
	response = social.ListStatusForVideos(search_query=search_query)

	if response.status_code == 200:
		body = response.json()
		hits_to_process = body.get('total_hits')
		page_key = body.get('page_key')
		if page_key == None:
			keep_running = False
		videos = body.get('videos')
		if videos:
			for video in videos:
				row = [ video.get(field) for field in row_list[0] ]
				row_list.append(row)

				videos_processed += 1
				if videos_processed%100==0:
					show_progress(videos_processed,hits_to_process)
	else:
		keep_running = False

show_progress(videos_processed,hits_to_process)

#write list to file
list_to_csv(row_list, report_name)
