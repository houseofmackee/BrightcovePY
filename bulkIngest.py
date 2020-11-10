#!/usr/bin/env python3

from mackee import CMS
from mackee import OAuth
from mackee import LoadAccountInfo
from mackee import DynamicIngest
import sys
import json
import argparse
import os
import sqlite3
import datetime
import hashlib
import threading
import requests # pip3 install requests
import boto3 # pip3 install boto3
import dropbox # pip3 install dropbox

# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# allowed success response codes
successResponses = [200,201,202,203,204]

# globals for API stuff
oauth = None
cms = None
di = None

class IngestHistory:
	def __init__(self, dbName):
		self.dbName = dbName
		self.__dbConn = None
		try:
			self.__dbConn = self.CreateConnection(dbName)
			self.CreateTable()
		except sqlite3.Error as e:
			raise(e)

	# create a database connection to a SQLite database
	def CreateConnection(self, db_file):
		try:
			conn = sqlite3.connect(db_file)
			return conn
		except sqlite3.Error as e:
			raise(e)

	# close database connection
	def CloseConnection(self):
		if(self.__dbConn is not None):
			self.__dbConn.close()

	# commit database updates
	def Commit(self):
		if(self.__dbConn is not None):
			self.__dbConn.commit()

	# commit changes and clsoe database
	def CommitAndCloseConnection(self):
		if(self.__dbConn is not None):
			self.Commit()
			self.CloseConnection()

	# create the history table
	def CreateTable(self):
		sql_create_table = """ CREATE TABLE IF NOT EXISTS ingest_history (
											id integer PRIMARY KEY,
											ingest_hash text NOT NULL,
											ingest_date text,
											account_id text,
											video_id text,
											request_id text,
											remote_path text
										); """
		try:
			c = self.__dbConn.cursor()
			c.execute(sql_create_table)
			return True
		except:
			return False

	# delete all data in history table
	def ResetTable(self):
		sql = '''DELETE FROM ingest_history'''
		cur = self.__dbConn.cursor()
		try:
			cur.execute(sql)
			return True
		except:
			return False

	# create a hash
	def CreateHash(self, salt, value):
		raw_bytes = b"%r"%(str(salt)+str(value))
		return hashlib.sha256(raw_bytes).hexdigest()

	# add an ingest history entry to database
	def AddIngestHistory(self, accountID, videoID, requestID, remoteURL):
		hashValue = self.CreateHash(accountID, remoteURL)
		history = (hashValue, str(datetime.datetime.now()), accountID, videoID, requestID, remoteURL)

		sql = '''INSERT INTO ingest_history(ingest_hash,ingest_date,account_id,video_id,request_id,remote_path) VALUES(?,?,?,?,?,?)'''
		cur = self.__dbConn.cursor()
		try:
			cur.execute(sql, history)
			self.Commit()
			return cur.lastrowid
		except:
			return 0

	# find a hash in the database
	def FindHashInIngestHistory(self, hashValue):
		cur = self.__dbConn.cursor()
		cur.execute("SELECT * FROM ingest_history WHERE ingest_hash=?", (hashValue,))
		rows = cur.fetchall()
		if(len(rows)>0):
			return rows[0]
		else:
			return None

class ProgressPercentage(object):

	def __init__(self, filename):
		self._filename = filename
		self._size = int(os.path.getsize(filename))
		self._seen_so_far = 0
		self._lock = threading.Lock()

	def __call__(self, bytes_amount):
		# To simplify, assume this is hooked up to a single filename
		with self._lock:
			self._seen_so_far += bytes_amount
			percentage = (self._seen_so_far / self._size) * 100
			sys.stdout.write("\rProgress: %s / %s  (%.2f%%)\r" % (self._seen_so_far, self._size, percentage))
			sys.stdout.flush()
# 
def ingest_video(accountID, videoID, sourceURL, priorityQueue):
	r = di.SubmitIngest(accountID=accountID, videoID=videoID, sourceURL=sourceURL, priorityQueue=priorityQueue)
	if(r.status_code in successResponses):
		requestID = r.json()['id']
		print('Ingest Call ('+priorityQueue+') result for video ID ' + videoID + ': ' + str(r.json()))
		return requestID
	elif(r.status_code==429):
		pass # implement retries for when the queue is maxed out
		return None
	else:
		print('Ingest Call ('+priorityQueue+') failed for video ID '+videoID+': ' + str(r.status_code))
		print(r.text)
		return None

def create_and_ingest(accountID, filename, sourceURL, priority):
	video = cms.CreateVideo(accountID=accountID, videoTitle=filename)
	if(video.status_code in successResponses):
		videoID = video.json()['id']
		reqID = ingest_video(accountID=accountID, videoID=videoID, sourceURL=sourceURL, priorityQueue=priority)
		if(reqID is not None):
			return videoID, reqID
		else:
			return None, None
	else:
		print('Create Video failed: ' + str(video.status_code))
		return None, None

def isVideo(filename):
	# file extensions to check
	extensionsToCheck = ('.m4p', '.m4v', '.avi', '.wmv', '.mov', '.mkv', '.webm', '.mpg', '.mp2', '.mpeg', '.mpe', '.mpv', '.mp4', '.qt', '.flv')
	# check if the filename ends with any extensions from the list
	return (filename.lower().endswith(extensionsToCheck))

#===========================================
# main program starts here
#===========================================
def main(dbHistory):
	# disable certificate warnings
	requests.urllib3.disable_warnings()

	# init the argument parsing
	parser = argparse.ArgumentParser(prog=sys.argv[0])
	parser.add_argument('--priority', metavar='<ingest priority>', type=str, default='normal', help='Set ingest queue priority (low, medium, high)')
	parser.add_argument('--s3bucket', metavar='<S3 bucket name>', type=str, help='Name of the S3 bucket to ingest from')
	parser.add_argument('--s3profile', metavar='<AWS profile name>', type=str, help='Name of the AWS profile to use if other than default', default='default')
	parser.add_argument('--dbxfolder', metavar='<Dropbox folder>', type=str, help='Name of the Dropbox folder to ingest from')
	parser.add_argument('--dbxtoken', metavar='<Dropbox API token>', type=str, help='Token for Dropbox API access')
	parser.add_argument('--folder', metavar='<path to folder>', type=str, help='Name and path of local folder to ingest from (use / or \\\\)')
	parser.add_argument('--file', metavar='<path to file>', type=str, help='Name and path of local file to ingest from (use / or \\\\)')
	parser.add_argument('--account', metavar='<account ID>', type=str, help='Brightcove Account ID to ingest videos into')
	parser.add_argument('--profile', metavar='<ingest profile name>', type=str, help='Brightcove ingest profile name to use to ingest videos')
	parser.add_argument('--config', metavar='<path to config file>', type=str, help='Name and path of account config information file')
	parser.add_argument('--dbreset', action='store_true', help='Resets and clears the ingest history database')
	parser.add_argument('--dbignore', action='store_true', help='Ignores the ingest history database (no delta ingest and no record keeping)')

	# parse the args
	args = parser.parse_args() 

	if(args.dbreset):
		print('Resetting ingest history database.')
		dbHistory.ResetTable()

	# get S3 info if available
	if(args.s3bucket):
		s3bucketName = args.s3bucket
		s3profileName = args.s3profile
	else:
		s3bucketName = None
		s3profileName = None

	# get Dropbox info if available
	if(args.dbxfolder and args.dbxtoken):
		dbxFolder = '/'+args.dbxfolder
		dbxToken = args.dbxtoken
	else:
		dbxFolder = None
		dbxToken = None

	# get local folder if available
	if(args.folder):
		localFolder = args.folder
	else:
		localFolder = None

	# error out if we have neither S3 nor Dropbox info
	if(not s3bucketName and not dbxFolder and not localFolder and not args.dbreset and not args.file):
		print('Error: no S3 bucket, Dropbox, local folder, file or tokens specified.\n')
		return

	# get ingest priority
	if(args.priority in ['low', 'normal', 'high']):
		ingestPriority = args.priority
	else:
		print('Error: invalid ingest queue priority specified.\n')
		return

	# create the OAuth token from the account config info file
	account_id, client_id, client_secret, _ = LoadAccountInfo(args.config)

	# override target account ID if specified
	if(args.account):
		account_id = args.account

	if(args.profile):
		ingest_profile = args.profile
	else:
		ingest_profile = None

	global oauth
	global cms
	global di

	oauth = OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret)
	cms = CMS(oauth)
	di = DynamicIngest(oAuth=oauth, ingestProfile=ingest_profile, priorityQueue=ingestPriority)

	# this needs moving outside, but for now I'm whatever about it
	def ingest_single_file(filePath):
		fileName = os.path.basename(filePath)
		video = cms.CreateVideo(accountID=account_id, videoTitle=fileName)
		if(video.status_code in successResponses):
			videoID=video.json()['id']
			hashValue = dbHistory.CreateHash(account_id, filePath)
			ingestRecord = dbHistory.FindHashInIngestHistory(hashValue)
			if(ingestRecord is None or args.dbignore is True):
				print('Uploading file "'+filePath+'" to temporary S3 bucket.')
				upload_url = di.UploadFile(accountID=account_id, videoID=videoID, fileName=filePath,callBack=ProgressPercentage(filePath))
				if(upload_url):
					reqID = ingest_video(accountID=account_id, videoID=videoID, sourceURL=upload_url['api_request_url'], priorityQueue=ingestPriority)
					if(reqID is not None and args.dbignore is False):
						dbHistory.AddIngestHistory(accountID=account_id, videoID=videoID, requestID=reqID, remoteURL=filePath)
				else:
					print('Error: failed to upload "'+filePath+'" to temporary S3 bucket.')
			else:
				print('Already ingested on '+ingestRecord[2])

	#===========================================
	# do a single file ingest
	#===========================================
	if(args.file):
		ingest_single_file(args.file)

	#===========================================
	# do the S3 bulk ingest
	#===========================================
	if(s3bucketName):
		# Let's use Amazon S3
		try:
			boto3.Session(profile_name=s3profileName)
		except:
			print('Error: no AWS credentials found for profile "'+s3profileName+'"')
		else:
			s3 = boto3.resource('s3')
			bucket = s3.Bucket(s3bucketName)

			try:
				for filename in [obj.key for obj in bucket.objects.all() if isVideo(obj.key)]:
					s3URL = 'https://'+s3bucketName+'.s3.amazonaws.com/'+(filename).replace(' ', '%20')
					print(s3URL)
					hashValue = dbHistory.CreateHash(account_id, s3URL)
					ingestRecord = dbHistory.FindHashInIngestHistory(hashValue)
					if(ingestRecord is None or args.dbignore is True):
						videoID, reqID = create_and_ingest(account_id, filename, s3URL, ingestPriority)
						if(reqID is not None and args.dbignore is False):
							dbHistory.AddIngestHistory(accountID=account_id, videoID=videoID, requestID=reqID, remoteURL=s3URL)
					else:
						print('Already ingested on '+ingestRecord[2])
			except:
				print('Error: bucket "'+s3bucketName+'" not found for profile "'+s3profileName+'".\n')

	#===========================================
	# do the Dropbox bulk ingest
	#===========================================
	if(dbxFolder):
		try:
			dbx = dropbox.Dropbox(dbxToken)
		except:
			print('Error: invalid Dropbox API token.')
		else:
			try:
				for filename in [entry.name for entry in dbx.files_list_folder(path=dbxFolder, include_non_downloadable_files=False).entries if isVideo(entry.name)]:
					dbxPath = dbxFolder+'/'+filename
					print(dbxPath)
					sourceURL = str(dbx.sharing_create_shared_link(path=dbxPath).url).replace('?dl=0','?dl=1')
					hashValue = dbHistory.CreateHash(account_id, sourceURL)
					ingestRecord = dbHistory.FindHashInIngestHistory(hashValue)
					if(ingestRecord is None or args.dbignore is True):
						videoID, reqID = create_and_ingest(account_id, filename, sourceURL, ingestPriority)
						if(reqID is not None and args.dbignore is False):
							dbHistory.AddIngestHistory(accountID=account_id, videoID=videoID, requestID=reqID, remoteURL=sourceURL)
					else:
						print('Already ingested on '+ingestRecord[2])

			except:
				print('Error: folder "'+dbxFolder+'" not found in Dropbox.\n')

	#===========================================
	# do the local bulk ingest
	#===========================================
	if(localFolder):
		try:
			fileList = os.listdir(localFolder)
		except:
			print('Error: unable to access folder "'+localFolder+'"')
		else:
			for filePath in [filePath for filePath in fileList if isVideo(filePath)]:
				ingest_single_file(localFolder+'\\'+filePath)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	try:
		dbHistory = IngestHistory(os.path.expanduser('~')+'/bulkingest.sqlite')
	except:
		print('Error: can not connect to ingest history database.')
	else:
		main(dbHistory)
		dbHistory.CommitAndCloseConnection()
