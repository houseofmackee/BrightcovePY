import sys
import functools
import csv
import json
from threading import Lock
from os.path import expanduser, getsize
from typing import Callable, Tuple, Union, Optional, Dict, Any
from pandas import read_csv, read_excel #type: ignore

class TimeString():
	"""
	Class to provide a simple timestamp string from an int
	"""

	return_format = '{hh:02}:{mm:02}:{ss:02}'

	@classmethod
	def from_milliseconds(cls, millis:Union[int, float], fmt:str=None) -> str:
		seconds = int(int(millis)/1000)
		hours, seconds = divmod(seconds, 60*60)
		minutes, seconds = divmod(seconds, 60)
		fmt = fmt if fmt else cls.return_format
		return fmt.format(hh=hours, mm=minutes, ss=seconds)

	@classmethod
	def from_seconds(cls, seconds:Union[int, float], fmt:str=None) -> str:
		return cls.from_milliseconds(seconds*1000, fmt)

	@classmethod
	def from_minutes(cls, minutes:Union[int, float], fmt:str=None) -> str:
		return cls.from_seconds(minutes*60, fmt)

class ProgressPercentage(object):
	"""
	Class to provide a simple progress indicator
	"""

	def __init__(self, filename=None, target=0):
		self._filename = filename
		self._size = int(getsize(filename)) if filename else target
		self._seen_so_far = 0
		self._lock = Lock()

	def __call__(self, bytes_amount, add_info=''):
		# To simplify, assume this is hooked up to a single filename
		with self._lock:
			self._seen_so_far += bytes_amount
			percentage = (self._seen_so_far / self._size) * 100
			sys.stdout.write("\rProgress: %s / %s  (%.2f%%)%s\r" % (self._seen_so_far, self._size, percentage, add_info))
			sys.stdout.flush()

# function to print to stderr
def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

# decorator for static variables
def static_vars(**kwargs):
	def decorate(func):
		for k in kwargs:
			setattr(func, k, kwargs[k])
		return func
	return decorate

#===========================================
# calculates the aspect ratio of w and h
#===========================================
@functools.lru_cache()
def aspect_ratio(width: int , height: int) -> Tuple[int, int]:
	"""Function to calculate aspect ratio for two given values

	Args:
		width (int): width value
		height (int): height value

	Returns:
		Tuple[int, int]: ratio of width to height
	"""

	def gcd(a, b):
		return a if b == 0 else gcd(b, a % b)

	if width == height:
		return 1,1

	if width > height:
		divisor = gcd(width, height)
	else:
		divisor = gcd(height, width)

	return int(width / divisor), int(height / divisor)

#===========================================
# write list of rows to CSV file
#===========================================
def list_to_csv(row_list:list, filename:Optional[str]):
	"""Function to write a list of rows to a CSV file

	Args:
		row_list (list): A list of lists (the rows)
		filename (str, optional): Name for the CSV file. Defaults to 'report.csv'.

	Returns:
		bool: True if CSV successfully created, False otherwise
	"""

	try:
		with open(filename if filename else 'report.csv', 'w', newline='', encoding='utf-8') as file:
			try:
				writer = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter=',')
				writer.writerows(row_list)
			except Exception as e:
				raise Exception(f'Error writing CSV data to file: {e}')
	except Exception as e:
		raise Exception(f'Error creating outputfile: {e}')

#===========================================
# read account info from JSON file
#===========================================
def load_account_info(input_filename:Optional[str]=None) -> Tuple[str, str, str, dict]:
	"""Function to get information about account from config JSON file

	Args:
		input_filename (str, optional): path and name of the config JSON file. Defaults to None and will use "account_info.json" from the user's home folder.

	Returns:
		Tuple[str, str, str, dict]: account ID, client ID, client secret and the full deserialized JSON object
	"""

	# if no config file was passed we use the default
	input_filename = input_filename or expanduser('~')+'/account_info.json'

	# open the config file
	try:
		with open(input_filename, 'r') as file:
			obj = json.loads( file.read() )
	except:
		raise Exception(f'Error: unable to open {input_filename}')

	# grab data, make it strings and strip it
	account = obj.get('account_id')
	account = str(account).strip() if account else None

	client = obj.get('client_id')
	client = str(client).strip() if client else None

	secret = obj.get('client_secret')
	secret = str(secret).strip() if secret else None

	# return the object just in case it's needed later
	return account, client, secret, obj


#===========================================
# converts asset ID to string
#===========================================
@functools.lru_cache()
def normalize_id(asset_id:Union[str, int, float]) -> str:
	"""Converts an asset ID to string

	Args:
		asset_id (any): video or playlist ID

	Returns:
		str: string representation of the ID, None if invalid ID
	"""

	_, response = wrangle_id(asset_id)
	return response

#===========================================
# test if a value is a valid ID
#===========================================
@functools.lru_cache()
def is_valid_id(asset_id:Union[str, int, float]) -> bool:
	"""Function to check if a given value is a valid asset ID

	Args:
		asset_id (any): value to check

	Returns:
		bool: True if it's a valid ID, False otherwise
	"""

	response, _ = wrangle_id(asset_id)
	return response

#===========================================
# test if a value is a valid ID and convert
# to string
#===========================================
@functools.lru_cache()
def wrangle_id(asset_id:Union[str, int, float]) -> Tuple[bool, str]:
	"""Converts ID to string and checks if it's a valid ID

	Args:
		asset_id (any): asset ID (video or playlist)

	Returns:
		(bool, str): True and string representation of ID if valid, False and None otherwise
	"""

	is_valid = False
	work_id = ''

	# is it an int?
	if isinstance(asset_id, int) and asset_id > 0:
		try:
			work_id = str(asset_id)
		except:
			is_valid = False
		else:
			is_valid = True

	# is it a string?
	elif isinstance(asset_id, str):
		if asset_id.lower().startswith('ref:') and len(asset_id)<=154:
			work_id = asset_id
			is_valid = True
		else:
			try:
				work_id = str(int(asset_id))
			except:
				is_valid = False
			else:
				is_valid = True

	# is it a float?
	elif isinstance(asset_id, float):
		if asset_id.is_integer():
			work_id = str(int(asset_id))
			is_valid = True

	return is_valid, work_id

#===========================================
# test if a value is a valid JSON string
#===========================================
@functools.lru_cache()
def is_json(myjson:str) -> bool:
	"""Function to check if a string is valid JSON

	Args:
		myjson (str): string to check

	Returns:
		bool: true if myjson is valid JSON, false otherwise
	"""

	try:
		_ = json.loads(myjson)
	except:
		return False
	return True

#===========================================
# read list of video IDs from XLS/CSV
#===========================================
def videos_from_file(filename:str, column_name:str='video_id', validate:bool=True, unique:bool=True) -> list:
	"""Function to read a list of video IDs from an xls/csv file

	Args:
		filename (str): path and name of file to read from
		column_name (str, optional): name of the column in the file which contains the IDs. Defaults to 'video_id'.
		validate (bool, optional): check IDs to make sure they are valid IDs. Defaults to True.
		unique (bool, optional): makes sure all video IDs in the list are unique. Defaults to True.

	Returns:
		List: List object with the video IDs from the file. None if there was an error processing the file.
	"""

	video_list = []
	try:
		if filename.lower().endswith('csv'):
			data = read_csv(filename)
		else:
			data = read_excel(filename)
	except Exception as e:
		eprint(f'Error while trying to read {filename}: {e}')
	else:
		try:
			if validate:
				video_list = [video_id for video_id in data[column_name] if is_valid_id(video_id)]
			else:
				video_list = list(data[column_name])
		except KeyError:
			eprint(f'Error while trying to read {filename} -> missing key: "{column_name}"')

	# make list unique
	if video_list and unique:
		video_list = list(set(video_list))

	return video_list
