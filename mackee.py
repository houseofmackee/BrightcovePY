#!/usr/bin/env python3
import sys
import json
import argparse
import time
import requests # pip3 install requests
import boto3 # pip3 install boto3
from os.path import expanduser

class OAuth:
	access_token_url = 'https://oauth.brightcove.com/v4/access_token'

	def __init__(self, account_id, client_id, client_secret):
		self.account_id = account_id
		self.client_id = client_id
		self.client_secret = client_secret
		self.__access_token = None
		self.__request_time = None
		self.__token_life = 240

	def __get_access_token(self):
		access_token = None
		r = requests.post(url=OAuth.access_token_url, params='grant_type=client_credentials', auth=(self.client_id, self.client_secret), verify=False)
		if(r.status_code == 200):
			access_token = r.json().get('access_token')
			self.__request_time = time.time()

		return access_token

	def get_access_token(self):
		if(self.__access_token == None):
			self.__access_token = self.__get_access_token()
		elif( (time.time()-self.__request_time) > self.__token_life ):
			self.__access_token = self.__get_access_token()
		return self.__access_token

	def get_headers(self):
		access_token = self.get_access_token()
		headers = { 'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json' }
		return headers

class Base:
	API_VERSION = None
	BaseURL = ''

	def __init__(self):
		pass

class CMS:

	# allowed success response codes
	success_responses = [200,201,202,203,204]
	base_url = 'https://cms.api.brightcove.com/v1/accounts/{pubid}'

	def __init__(self, oauth):
		self.__oauth = oauth

	#===========================================
	# get number of videos in an account
	#===========================================
	def GetVideoCount(self, accountID=None, searchQuery=''):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/count?q={query}').format(pubid=accountID,query=searchQuery)
		r = requests.get(url, headers=headers)
		if(r.status_code == 200):
			return r.json().get('count')
		return -1

	#===========================================
	# create new video object in an account
	#===========================================
	def CreateVideo(self, accountID=None, videoTitle='Video Title', jsonBody=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/').format(pubid=accountID)
		if(not jsonBody):
			jsonBody = '{"name": "' + videoTitle + '"}'
		return requests.post(url=url, headers=headers, data=jsonBody)

	#===========================================
	# get a video
	#===========================================
	def GetVideo(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}').format(pubid=accountID,videoid=videoID)
		return requests.get(url=url, headers=headers)

	#===========================================
	# get videos in an account
	#===========================================
	def GetVideos(self, accountID=None, pageSize=20, pageOffset=0, searchQuery=''):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		apiRequest = (CMS.base_url+'/videos?limit={pageSize}&offset={offset}&sort=created_at{query}').format(pubid=accountID, pageSize=pageSize, offset=pageOffset, query='&q=' + searchQuery)
		return requests.get(apiRequest, headers=headers)

	#===========================================
	# get a video's sources
	#===========================================
	def GetVideoSources(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/sources').format(pubid=accountID,videoid=videoID)
		return requests.get(url=url, headers=headers)

	#===========================================
	# delete a video
	#===========================================
	def DeleteVideo(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}').format(pubid=accountID,videoid=videoID)
		return requests.delete(url=url, headers=headers)

	#===========================================
	# get a digital master info
	#===========================================
	def GetDigitalMasterInfo(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/sources').format(pubid=accountID,videoid=videoID)
		return requests.get(url=url, headers=headers)

	#===========================================
	# delete a digital master
	#===========================================
	def DeleteMaster(self, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}/digital_master').format(pubid=accountID,videoid=videoID)
		return requests.delete(url=url, headers=headers)

	#===========================================
	# update a video
	#===========================================
	def UpdateVideo(self, videoID, jsonBody, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/videos/{videoid}').format(pubid=accountID,videoid=videoID)
		return requests.patch(url, headers=headers, data=jsonBody)

	#===========================================
	# subscriptions bla bla
	#===========================================
	def GetSubscriptionsList(self, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/subscriptions').format(pubid=accountID)
		return (requests.get(url, headers=headers))

	def GetSubscription(self, subID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/subscriptions/{subid}').format(pubid=accountID, subid=subID)
		return (requests.get(url, headers=headers))

	def CreateSubscription(self, callbackURL, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/subscriptions').format(pubid=accountID)
		jsonBody = ('{ "endpoint":"' + callbackURL + '", "events":["video-change"] }')
		return (requests.post(url, headers=headers, data=jsonBody))

	def DeleteSubscription(self, subID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/subscriptions/{subid}').format(pubid=accountID,subid=subID)
		return (requests.delete(url, headers=headers))
	
	#===========================================
	# folders stuff
	#===========================================
	def GetFolders(self, accountID=None, pageSize=100, pageOffset=0):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders?limit={limit}&offset={offset}').format(pubid=accountID,limit=pageSize, offset=pageOffset)
		return (requests.get(url, headers=headers))

	def CreateFolder(self, folderName, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders').format(pubid=accountID)
		jsonBody = ('{ "name":"' + folderName + '" }')
		return (requests.post(url, headers=headers, data=jsonBody))

	def DeleteFolder(self, folderID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders/{folderid}').format(pubid=accountID, folderid=folderID)
		return (requests.delete(url, headers=headers))

	def GetFolderInformation(self, folderID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders/{folderid}').format(pubid=accountID, folderid=folderID)
		return (requests.get(url, headers=headers))

	def UpdateFolderName(self, folderID, folderName, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders/{folderid}').format(pubid=accountID, folderid=folderID)
		jsonBody = ('{ "name":"' + folderName + '" }')
		return (requests.patch(url, headers=headers, data=jsonBody))

	def AddVideoToFolder(self, folderID, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders/{folderid}/videos/{videoid}').format(pubid=accountID, videoid=videoID)
		return (requests.put(url, headers=headers))

	def RemoveVideoFromFolder(self, folderID, videoID, accountID=None):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders/{folderid}/videos/{videoid}').format(pubid=accountID, videoid=videoID)
		return (requests.delete(url, headers=headers))

	def GetVideosInFolder(self, folderID, accountID=None, pageSize=100, pageOffset=0):
		accountID = accountID or self.__oauth.account_id
		headers = self.__oauth.get_headers()
		url = (CMS.base_url+'/folders/{folderid}/videos?limit={limit}&offset={offset}').format(pubid=accountID,folderid=folderID,limit=pageSize, offset=pageOffset)
		return (requests.get(url, headers=headers))

class DynamicIngest:

	success_responses = [200,201,202,203,204]
	base_url = 'https://ingestion.api.brightcove.com/v1/accounts/{pubid}'

	def __init__(self, oAuth, ingestProfile=None, priorityQueue=None):
		self.__oauth = oAuth
		self.SetIngestProfile(ingestProfile)
		self.SetPriorityQueue(priorityQueue)

	def SetIngestProfile(self, profileID):
		if(self.ProfileExists(accountID=self.__oauth.account_id, profileID=profileID)):
			self.__ingestProfile = profileID
		else:
			self.__ingestProfile = None
		return self.__ingestProfile
	
	def SetPriorityQueue(self, priorityQueue):
		if(priorityQueue in ['low', 'normal', 'high']):
			self.__priorityQueue = priorityQueue
		else:
			self.__priorityQueue = None
		return self.__priorityQueue

	def GetDefaultProfiles(self, accountID):
		headers = self.__oauth.get_headers()
		url = (DynamicIngest.base_url+'/configuration').format(pubid=accountID)
		return requests.get(url=url, headers=headers)
	
	def GetProfile(self, accountID, profileID):
		headers = self.__oauth.get_headers()
		url = (DynamicIngest.base_url+'/profiles/{profileid}').format(pubid=accountID, profileid=profileID)
		return requests.get(url=url, headers=headers)

	def ProfileExists(self, accountID, profileID):
		r = self.GetProfile(accountID=accountID, profileID=profileID)
		if(r.status_code in DynamicIngest.success_responses):
			return True
		else:
			return False
	
	def RetranscodeVideo(self, accountID, videoID, profileID):
		if(self.ProfileExists(accountID=accountID, profileID=profileID) is False):
			return None
		headers = self.__oauth.get_headers()
		url = ('https://ingest.api.brightcove.com/v1/accounts/{pubid}/videos/{videoid}/ingest-requests').format(pubid=accountID, videoid=videoID)
		data =	'{ "profile":"'+profileID+'", "master": { "use_archived_master": true } }'
		return requests.post(url=url, headers=headers, data=data)

	def SubmitIngest(self, accountID, videoID, sourceURL, priorityQueue=None, callBacks=None, ingestProfile=None):
		headers = self.__oauth.get_headers()
		profile = ''
		priority = 'normal'

		if(ingestProfile is not None):
			profile = ingestProfile
		elif(self.__ingestProfile is None):
			r = self.GetDefaultProfiles(accountID=accountID)
			if r.status_code in DynamicIngest.success_responses:
				profile = r.json()['default_profile_id']
		else:
			profile = self.__ingestProfile

		if(priorityQueue is not None):
			priority = priorityQueue
		elif(self.__priorityQueue is not None):
			priority = self.__priorityQueue

		url = ('https://ingest.api.brightcove.com/v1/accounts/{pubid}/videos/{videoid}/ingest-requests').format(pubid=accountID, videoid=videoID)
		data =	'{ "profile":"'+profile+'", "master": { "url": "'+sourceURL+'" }, "priority": "'+priority+'" }'
		return requests.post(url=url, headers=headers, data=data)

	# get_upload_location_and_upload_file first performs an authenticated request to discover
	# a Brightcove-provided location to securely upload a source file
	def UploadFile(self, accountID, videoID, fileName, callBack=None):
		# Perform an authorized request to obtain a file upload location
		url = ('https://cms.api.brightcove.com/v1/accounts/{pubid}/videos/{videoid}/upload-urls/{sourcefilename}').format(pubid=accountID, videoid=videoID, sourcefilename=fileName)
		r = requests.get(url=url, headers=self.__oauth.get_headers())
		if(r.status_code in DynamicIngest.success_responses):
			upload_urls_response = r.json()
		else:
			return None

		try:
			# Upload the contents of our local file to the location provided us
			# This example uses the boto3 library to perform a multipart upload
			# This is the recommended method for uploading large source files
			s3 = boto3.resource('s3',
				aws_access_key_id=upload_urls_response['access_key_id'],
				aws_secret_access_key=upload_urls_response['secret_access_key'],
				aws_session_token=upload_urls_response['session_token'])
			
			def emptyCB(muu):
				pass

			if(callBack is None):
				callBack = emptyCB

			s3.Object(upload_urls_response['bucket'], upload_urls_response['object_key']).upload_file(fileName, Callback=callBack)
			return upload_urls_response
		except Exception as e:
			print (e)
			return None

#===========================================
# read account info from JSON file
#===========================================
def GetAccountInfo(input_filename=None):
	# if no config file was passed we use the default
	if(not input_filename):
		input_filename = expanduser('~')+'/account_info.json'

	# open the config file
	try:
		myfile = open(input_filename, 'r')
	except:
		print(('Error: unable to open {filename}').format(filename=input_filename))
		return None, None, None, None

	# read and parse config file
	obj = json.loads( myfile.read() )

	# grab data, make it strings and strip it
	account = obj.get('account_id')
	if(account):
		account = str(account).strip()

	client = obj.get('client_id')
	if(client):
		client = str(client).strip()

	secret = obj.get('client_secret')
	if(secret):
		secret = str(secret).strip()

	# return the object just in case it's needed later
	return(account, client, secret, obj)

#===========================================
# default processing function
#===========================================
def list_videos(video):
	print(video['id']+', "'+video['name']+'"')

#===========================================
# this is the main loop to process videos
#===========================================
def process_video(inputfile, processVideo=list_videos, searchQuery=None, vidID=None):
	global oauth
	global cms
	global opts
	# get the account info and credentials
	accountID,b,c,opts = GetAccountInfo(inputfile)

	if(None in [accountID,b,c,opts]):
		return False
	
	oauth = OAuth(accountID,b,c)
	cms = CMS(oauth)

	# check if we should process a specific video ID
	if(vidID):
		print(('Processing video ID {videoid} now.').format(videoid=vidID))
		video = cms.GetVideo(accountID=accountID, videoID=vidID)
		if(video.status_code in CMS.success_responses):
			processVideo(video.json())
			return True
		else:
			print(('Error getting information for video ID {videoid}.').format(videoid=vidID))
			return False

	# check if we should process a given list of videos
	videoList = opts.get('video_ids')
	if(videoList and videoList[0] != 'all'):
		print(('Found {numVideos} videos in options file. Processing them now.').format(numVideos=len(videoList)))
		for videoID in videoList:
			#if(videoID=='all'): # not needed?
			#	continue
			video = cms.GetVideo(accountID=accountID, videoID=videoID)
			if(video.status_code in CMS.success_responses):
				processVideo(video.json())
			else:
				print(('Error getting information for video ID {videoid}.').format(videoid=videoID))

		return True

	# if a query was passed along URI encode it
	if(not searchQuery):
		searchQuery = ''
	else:
		searchQuery = requests.utils.quote(searchQuery)

	# ok, let's process all videos
	# get number of videos in account
	numVideos = cms.GetVideoCount(searchQuery=searchQuery)

	if(numVideos>0):
		print(('Found {numVideos} videos in library. Processing them now.').format(numVideos=numVideos))
	else:
		print(('No videos found in account ID {pubid}''s library.').format(pubid=oauth.account_id))
		return False

	currentOffset = 0
	pageSize = 20
	retries = 10

	while(currentOffset<numVideos):
		r = cms.GetVideos(pageSize=pageSize, pageOffset=currentOffset, searchQuery=searchQuery)
		# good result
		if (r.status_code in [200,202]):
			json_data = json.loads(r.text)
			# make sure we actually got some data
			if(len(json_data) > 0):
				for video in json_data:
					processVideo(video)
				retries = 10
				currentOffset += pageSize
			# looks like we got an empty response (it can happen)
			else:
				if(retries>0):
					print('Error: empty API response received.')
					for remaining in range(10, 0, -1):
						sys.stdout.write('\rRetrying in {:2d} seconds.'.format(remaining))
						sys.stdout.flush()
						time.sleep(1)

					retries -= 1
					sys.stdout.write('\rRetrying now ({retries} retries left).\n'.format(retries))

				else:
					print('Error: failed to get non-empty API response.')
					return False

		# token probably expired
		elif(r.status_code == 401):
			if(retries>0):
				retries -= 1
			else:
				print('Error: possible problem with OAuth token:')
				print(r.content)
				return False

		# we received an unexpected status code, let's get out of here
		else:
			print('Error: Received unexpected status code {status}:'.format(r.status_code))
			print(r.json())
			return False

	return True

#===========================================
# parse args and do the thing
#===========================================
def main(process_func):
	# disable certificate warnings
	requests.urllib3.disable_warnings()

	# init the argument parsing
	parser = argparse.ArgumentParser(prog=sys.argv[0])
	parser.add_argument('-i', type=str, help='Name and path of account config information file')
	parser.add_argument('-q', type=str, help='CMS API search query')
	parser.add_argument('-v', type=str, help='Specific video ID to process')

	# parse the args
	args = parser.parse_args()

	# go through the library and do stuff
	process_video(inputfile=args.i, processVideo=process_func, searchQuery=args.q, vidID=args.v)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(list_videos)
