#!/usr/bin/env python3
import sys
import json
import argparse
import os
import sqlite3
import datetime
import hashlib
import threading
import botocore
import requests # pip3 install requests
import boto3 # pip3 install boto3
import dropbox # pip3 install dropbox
from pathlib import Path
from mackee import CMS
from mackee import OAuth
from mackee import LoadAccountInfo
from mackee import DynamicIngest

# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# allowed success response codes
success_responses = [200,201,202,203,204]

# globals for API stuff
cms = None
di = None

class IngestHistory:
	def __init__(self, db_name):
		self.db_name = db_name
		self.__db_conn = None
		try:
			self.__db_conn = self.CreateConnection(db_name)
			self.CreateTable()
		except sqlite3.Error as e:
			raise(e)

	# create a hash
	@staticmethod
	def CreateHash(salt, value):
		raw_bytes = b"%r"%(str(salt)+str(value))
		return hashlib.sha256(raw_bytes).hexdigest()

	# create a database connection to a SQLite database
	@staticmethod
	def CreateConnection(db_file):
		try:
			conn = sqlite3.connect(db_file)
			return conn
		except sqlite3.Error as e:
			raise(e)

	# close database connection
	def CloseConnection(self):
		if self.__db_conn:
			self.__db_conn.close()

	# commit database updates
	def Commit(self):
		if self.__db_conn:
			self.__db_conn.commit()

	# commit changes and clsoe database
	def CommitAndCloseConnection(self):
		if self.__db_conn:
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
			c = self.__db_conn.cursor()
			c.execute(sql_create_table)
			return True
		except:
			return False

	# delete all data in history table
	def ResetTable(self):
		cur = self.__db_conn.cursor()
		try:
			cur.execute('DELETE FROM ingest_history')
			return True
		except:
			return False

	# add an ingest history entry to database
	def AddIngestHistory(self, account_id, video_id, request_id, remote_url):
		hash_value = self.CreateHash(account_id, remote_url)
		history = (hash_value, str(datetime.datetime.now()), account_id, video_id, request_id, remote_url)

		sql = 'INSERT INTO ingest_history(ingest_hash,ingest_date,account_id,video_id,request_id,remote_path) VALUES(?,?,?,?,?,?)'
		cur = self.__db_conn.cursor()
		try:
			cur.execute(sql, history)
			self.Commit()
			return cur.lastrowid
		except:
			return 0

	# find a hash in the database
	def FindHashInIngestHistory(self, hash_value):
		cur = self.__db_conn.cursor()
		cur.execute('SELECT * FROM ingest_history WHERE ingest_hash=?', (hash_value,))
		rows = cur.fetchall()
		return rows[0] if rows else None

	# find a hash in the database
	def ListIngestHistory(self):
		cur = self.__db_conn.cursor()
		cur.execute('SELECT * FROM ingest_history')
		rows = cur.fetchall()

		row_list =[['id','ingest_hash','ingest_date','account_id','video_id','request_id','remote_path']]
		for row in rows:
			row_list.append(list(row))

		return row_list

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
def ingest_video(account_id, video_id, source_url, priority_queue):
	response = di.SubmitIngest(account_id=account_id, video_id=video_id, source_url=source_url, priority_queue=priority_queue)
	if response.status_code in success_responses:
		request_id = response.json().get('id')
		print(f'Ingest Call ({priority_queue}) result for video ID {video_id}: {response.json()}')
		return request_id
	elif response.status_code==429:
		pass # implement retries for when the queue is maxed out
	else:
		print(f'Ingest Call ({priority_queue}) failed for video ID {video_id}: {response.status_code}')
		print(response.text)
	return None

def create_and_ingest(account_id, filename, source_url, priority):
	video = cms.CreateVideo(account_id=account_id, video_title=filename)
	if video.status_code in success_responses:
		video_id = video.json().get('id')
		request_id = ingest_video(account_id=account_id, video_id=video_id, source_url=source_url, priority_queue=priority)
		if request_id:
			return video_id, request_id
	else:
		print(f'Create Video failed: {video.status_code}')
	return None, None

def is_video(filename):
	# file extensions to check
	extensions_to_check = ('.m4p', '.m4v', '.avi', '.wmv', '.mov', '.mkv', '.webm', '.mpg', '.mp2', '.mpeg', '.mpe', '.mpv', '.mp4', '.qt', '.flv')
	# check if the filename ends with any extensions from the list
	return filename.lower().endswith(extensions_to_check)

#===========================================
# main program starts here
#===========================================
def main(db_history:IngestHistory):
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
	parser.add_argument('--history', action='store_true', help='Displays the ingest history')

	# parse the args
	args = parser.parse_args()

	if args.dbreset:
		print('Resetting ingest history database.')
		db_history.ResetTable()

	if args.history:
		for row in db_history.ListIngestHistory():
			print(*row, sep=', ')
		return

	# get S3 info if available
	s3_bucket_name = args.s3bucket
	s3_profile_name = args.s3profile

	# get Dropbox info if available
	dbx_folder = args.dbxfolder
	dbx_token = args.dbxtoken

	# get local folder if available
	local_folder = args.folder

	# error out if we have neither S3 nor Dropbox info
#	if not s3_bucket_name and not dbx_folder and not local_folder and not args.dbreset and not args.file:
	if not (s3_bucket_name or dbx_folder or local_folder or args.file):
		print('Error: no S3 bucket, Dropbox folder, local folder, file or tokens specified.\n')
		return

	# get ingest priority
	if(args.priority in ['low', 'normal', 'high']):
		ingest_priority = args.priority
	else:
		print('Error: invalid ingest queue priority specified.\n')
		return

	# create the OAuth token from the account config info file
	account_id, client_id, client_secret, _ = LoadAccountInfo(args.config)

	account_id = args.account or account_id
	ingest_profile = args.profile

	global cms
	global di

	oauth = OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret)
	cms = CMS(oauth)
	di = DynamicIngest(oAuth=oauth, ingest_profile=ingest_profile, priority_queue=ingest_priority)

	# this needs moving outside, but for now I'm whatever about it
	def ingest_single_file(file_path:str):
		file_name = os.path.basename(file_path)
		video = cms.CreateVideo(account_id=account_id, video_title=file_name)
		if video.status_code in success_responses:
			video_id=video.json().get('id')
			hash_value = db_history.CreateHash(account_id, file_path)
			ingest_record = db_history.FindHashInIngestHistory(hash_value)
			if ingest_record is None or args.dbignore:
				print(f'Uploading file "{file_path}" to temporary S3 bucket.')
				upload_url = di.UploadFile(account_id=account_id, video_id=video_id, file_name=file_path,callback=ProgressPercentage(file_path))
				if upload_url:
					request_id = ingest_video(account_id=account_id, video_id=video_id, source_url=upload_url['api_request_url'], priority_queue=ingest_priority)
					if request_id and not args.dbignore:
						db_history.AddIngestHistory(account_id=account_id, video_id=video_id, request_id=request_id, remote_url=file_path)
				else:
					print(f'Error: failed to upload "{file_path}" to temporary S3 bucket.')
			else:
				print(f'Already ingested on {ingest_record[2]}')

	#===========================================
	# do a single file ingest
	#===========================================
	if args.file:
		ingest_single_file(args.file)

	#===========================================
	# do the S3 bulk ingest
	#===========================================
	if s3_bucket_name:
		# Let's use Amazon S3
		try:
			boto3.Session(profile_name=s3_profile_name)
		except:
			print(f'Error: no AWS credentials found for profile "{s3_profile_name}"')
		else:
			try:
				s3 = boto3.resource('s3')
				bucket = s3.Bucket(s3_bucket_name).objects.all()
				filenames = [obj.key for obj in bucket if is_video(obj.key)]
			except Exception as e:
				print(f'Error accessing bucket "{s3_bucket_name}" for profile "{s3_profile_name}".\n')
			else:
				for filename in filenames:
					s3_url = f'https://{s3_bucket_name}.s3.amazonaws.com/'+((filename).replace(' ', '%20'))
					hash_value = db_history.CreateHash(account_id, s3_url)
					ingest_record = db_history.FindHashInIngestHistory(hash_value)
					if ingest_record is None or args.dbignore:
						print(f'Ingesting: "{s3_url}"')
						video_id, request_id = create_and_ingest(account_id, filename, s3_url, ingest_priority)
						if request_id and not args.dbignore:
							db_history.AddIngestHistory(account_id=account_id, video_id=video_id, request_id=request_id, remote_url=s3_url)
					else:
						print(f'Already ingested on {ingest_record[2]}: "{s3_url}"')

	#===========================================
	# do the Dropbox bulk ingest
	#===========================================
	if dbx_folder:
		try:
			dbx = dropbox.Dropbox(dbx_token)
		except:
			print('Error: invalid Dropbox API token.')
		else:
			try:
				dbx_folder = f'/{dbx_folder}'
				filenames = [entry.name for entry in dbx.files_list_folder(path=dbx_folder, include_non_downloadable_files=False).entries if is_video(entry.name)]
			except:
				print(f'Error: folder "{dbx_folder}" not found in Dropbox.\n')
			else:
				for filename in filenames:
					dbx_path = f'{dbx_folder}/{filename}'
					source_url = str(dbx.sharing_create_shared_link(path=dbx_path).url).replace('?dl=0','?dl=1')
					hash_value = db_history.CreateHash(account_id, source_url)
					ingest_record = db_history.FindHashInIngestHistory(hash_value)
					if ingest_record is None or args.dbignore:
						print(f'Ingesting: "{dbx_path}"')
						video_id, request_id = create_and_ingest(account_id, filename, source_url, ingest_priority)
						if request_id and not args.dbignore:
							db_history.AddIngestHistory(account_id=account_id, video_id=video_id, request_id=request_id, remote_url=source_url)
					else:
						print(f'Already ingested on {ingest_record[2]}: "{dbx_path}"')

	#===========================================
	# do the local bulk ingest
	#===========================================
	if local_folder:
		def get_list_of_files_in_dir(directory: str, file_types: str ='*') -> list:
			return [str(f) for f in Path(directory).glob(file_types) if f.is_file()]

		try:
			file_list = get_list_of_files_in_dir(local_folder)
		except:
			print(f'Error: unable to access folder "{local_folder}"')
		else:
			for file_path in [file for file in file_list if is_video(file)]:
				ingest_single_file(file_path)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	try:
		db_history = IngestHistory(os.path.expanduser('~')+'/bulkingest.sqlite')
	except:
		print('Error: can not connect to ingest history database.')
	else:
		main(db_history)
		db_history.CommitAndCloseConnection()
