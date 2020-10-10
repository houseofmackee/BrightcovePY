#!/usr/bin/env python3
import sys
import csv
from mackee import Social
from mackee import OAuth
from mackee import GetAccountInfo

videos_processed = 0
hits_to_process = 0
def showProgress(progress, total):
	sys.stderr.write(f'\r{progress}/{total} processed...\r')
	sys.stderr.flush()

cms = None

# account/API credentials (can be None to use user defaults)
account_id = None
client_id = None
client_secret = None

report_name = 'social_report.csv'

# get account info from config file if not hardcoded
if( account_id is None and client_id is None and client_secret is None):
	account_id, client_id, client_secret, _ = GetAccountInfo()

# create a Social API instance
social = Social( OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret) )

page_key = None
keep_running = True

row_list = [ ['id','account_id','destination_id','remote_id','remote_url','status','timestamp','published_at','distribution_method','autosync_id','error','warning','action','result'] ]

while(keep_running):
	search_query = '' if not page_key else ('page_key='+page_key)
	response = social.ListStatusForVideos(searchQuery=search_query)

	if(response.status_code == 200):
		body = response.json()
		hits_to_process = body.get('total_hits')
		page_key = body.get('page_key')
		if(page_key == None):
			keep_running = False
		videos = body.get('videos')
		if(videos):
			for video in videos:

				row = []
				for field in row_list[0]:
					value = video.get(field)
					row.append(str('' if not value else value))

				row_list.append(row)

				videos_processed += 1
				if(videos_processed%100==0):
					showProgress(videos_processed,hits_to_process)
	else:
		keep_running = False

showProgress(videos_processed,hits_to_process)

#write list to file
try:
	with open(report_name, 'w', newline='', encoding='utf-8') as file:
		try:
			writer = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter=',')
			writer.writerows(row_list)
		except Exception as e:
			print(f'\nError writing CSV data to file: {e}')
except Exception as e:
	print(f'\nError creating outputfile: {e}')