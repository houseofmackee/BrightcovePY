"""
Module implementing utility and helper classes and functions for common tasks.
"""

from json.decoder import JSONDecodeError
from math import isinf, isnan
import sys
import functools
import csv
import json
import inspect
from time import perf_counter
from dataclasses import dataclass, fields as datafields
from threading import Lock
from os.path import expanduser, getsize
from typing import Iterable, Tuple, Union
from pandas import read_csv, read_excel #type: ignore
from pandas.errors import ParserError #type: ignore
from xlrd import XLRDError #type: ignore

@dataclass
class QueryStringDataclassBase:
    """
    Custom dataclass base class implementing a URL query string generator.
    """
    _fix_data = {}
    _valid_data = {}

    def valid_data(self, new_data: dict) -> dict:
        """
        Adds more data to the validation dict.
        """
        self._valid_data.update(new_data)
        return self._valid_data

    def fix_data(self, new_data: dict) -> dict:
        """
        Adds more data to the replacement dict.
        """
        self._fix_data.update(new_data)
        return self._fix_data

    def validate(self, name: str, value: str) -> bool:
        """
        Validates "value" for "name" if a list of allowed values for "name" exists in _valid_data dict.
        """
        check_me = self._valid_data.get(name, [])
        if check_me and not set(value.replace(' ','').split(sep=',')).issubset(check_me):
            return False
        return True

    def fix(self, name: str) -> str:
        """
        Returns replacement for "name" if one exists in _fix_data dict.
        """
        return self._fix_data.get(name, name)

    def __str__(self):
        """
        Returns the dataclass fields as a URL query string.
        """
        result = '?'
        for field in datafields(self):
            name = field.name
            if value := getattr(self, name):
                value = str(value)
                if field.type is bool:
                    value = value.lower()
                name = self.fix(name)
                if self.validate(name, value):
                    result += f'{name}={value}&'
                else:
                    e_msg = f'Error: "{value}" is not a valid value for {name}'
                    raise ValueError(e_msg)
        return result[:-1]

class TimeString():
    """
    Class to provide a simple timestamp string from an int.
    """
    return_format = '{hh:02}:{mm:02}:{ss:02}'

    @classmethod
    def from_milliseconds(cls, millis: Union[int, float], fmt: str='') -> str:
        seconds = int(int(millis)/1000)
        hours, seconds = divmod(seconds, 60*60)
        minutes, seconds = divmod(seconds, 60)
        fmt = fmt if fmt else cls.return_format
        return fmt.format(hh=hours, mm=minutes, ss=seconds)

    @classmethod
    def from_seconds(cls, seconds: Union[int, float], fmt: str='') -> str:
        return cls.from_milliseconds(seconds*1000, fmt)

    @classmethod
    def from_minutes(cls, minutes: Union[int, float], fmt: str='') -> str:
        return cls.from_seconds(minutes*60, fmt)

class SimpleProgressDisplay():
    """
    Class to provide a simple progress indicator.
    """
    def __init__(self, filename: str='', target: int=0, steps: int=1, add_info: str=''):
        self._filename = filename
        self._size = int(getsize(filename)) if filename else target
        self._counter = 0
        self._lock = Lock()
        self._steps = steps
        self._add_info = add_info

    def __call__(self, increase: int=1, force_display: bool=False):
        with self._lock:
            if not force_display:
                self._counter += increase
            if force_display or self._counter%self._steps==0:
                if self._size:
                    percentage = (self._counter / self._size) * 100
                    sys.stdout.write('\rProgress: %s / %s  (%.2f%%) %s\r' % (self._counter, self._size, percentage, self._add_info))
                else:
                    sys.stderr.write('\rProgress: %s %s\r' % (self._counter, self._add_info) )
                sys.stdout.flush()

class SimpleTimer():
    """
    Class to provide a simple execution timer.
    """
    def __init__(self, name: str=''):
        frm = inspect.stack()[1]
        mod = inspect.getmodule(frm[0])
        self.name = name or mod.__file__
        self.start = perf_counter()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        elapsed = perf_counter() - self.start
        eprint(f'\n{self.name}: executed in {TimeString.from_seconds(elapsed)}.')


def empty_function(*args, **kwargs): #pylint: disable = E, W, R, C
    """
    It's an empty function.
    """

# function to print to stderr
def eprint(*args, **kwargs):
    """
    Print message to stderr.
    """
    print(*args, file=sys.stderr, **kwargs)

# decorator for static variables
def static_vars(**kwargs):
    """
    Static variables decorator.
    """
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

def is_a_in_b(a: Iterable, b: Iterable) -> bool:
    """
    checks if a is a subset of b
    """
    return set(a).issubset(set(b))

def is_number(value: str) -> bool:
    """
    Check to see if a given str is a valid/useable number.
    """
    try:
        num_value = float(value)
    except ValueError:
        return False
    return not (isnan(num_value) or isinf(num_value))

def is_shared_by(video: dict) -> bool:
    """
    Checks if a video was shared by an account.
    Returns True if it was shared by another account, False otherwise.
    """
    shared = video.get('sharing')
    if shared and shared.get('by_external_acct'):
        return True
    return False

def is_shared_to(video: dict) -> bool:
    """
    Checks if a video was shared to an account.
    Returns True if it was shared to another account, False otherwise.
    """
    shared = video.get('sharing')
    if shared and shared.get('to_external_acct'):
        return True
    return False

@functools.lru_cache()
def aspect_ratio(width: int , height: int) -> Tuple[int, int]:
    """
    Function to calculate aspect ratio for two given values.

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

def list_to_csv(row_list: list, filename: str=''):
    """
    Function to write a list of rows to a CSV file.

    Args:
        row_list (list): A list of lists (the rows).
        filename (str, optional): Name for the CSV file. Defaults to 'report.csv'.

    Returns:
        bool: True if CSV successfully created, False otherwise.
    """

    # convert single column list to required format
    if not isinstance(row_list[0], (list, tuple)):
        row_list = [(line,) for line in row_list]

    # write csv file
    try:
        with open(filename if filename else 'report.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter=',')
            writer.writerows(row_list)
    except OSError as e:
        raise OSError(f'Error creating outputfile: {e}') from e
    except csv.Error as e:
        raise csv.Error(f'Error writing CSV data to file: {e}') from e

def load_account_info(input_filename: str='') -> Tuple[str, str, str, dict]:
    """
    Function to get information about account from config JSON file.

    Args:
        input_filename (str, optional): path and name of the config JSON file.
            Defaults to '' and will use "account_info.json" from the user's home folder.

    Returns:
        Tuple[str, str, str, dict]: account ID, client ID, client secret and the full deserialized JSON object.
    """
    # if no config file was passed we use the default
    input_filename = input_filename or expanduser('~')+'/account_info.json'

    # open the config file
    try:
        with open(input_filename, 'r') as file:
            obj = json.loads( file.read() )
    except OSError as e:
        raise Exception(f'Error: unable to open {input_filename} -> {e}') from e
    except json.JSONDecodeError as e:
        raise Exception(f'Error: error parsing {input_filename} -> {e}') from e

    # grab data, make it strings and strip it
    account = obj.get('account_id')
    account = str(account).strip() if account else None

    client = obj.get('client_id')
    client = str(client).strip() if client else None

    secret = obj.get('client_secret')
    secret = str(secret).strip() if secret else None

    # return the object just in case it's needed later
    return account, client, secret, obj

@functools.lru_cache()
def normalize_id(asset_id: Union[str, int, float]) -> str:
    """
    Converts an asset ID to string.

    Args:
        asset_id (any): video or playlist ID to normalize.

    Returns:
        str: string representation of the ID, None if invalid ID.
    """
    _, response = wrangle_id(asset_id)
    return response

@functools.lru_cache()
def is_valid_id(asset_id: Union[str, int, float]) -> bool:
    """
    Function to check if a given value is a valid asset ID.

    Args:
        asset_id (any): value to check.

    Returns:
        bool: True if it's a valid ID, False otherwise.
    """
    response, _ = wrangle_id(asset_id)
    return response

@functools.lru_cache()
def wrangle_id(asset_id: Union[str, int, float]) -> Tuple[bool, str]:
    """
    Converts ID to string and checks if it's a valid ID.

    Args:
        asset_id (any): asset ID (video or playlist).

    Returns:
        (bool, str): True and string representation of ID if valid, False and None otherwise.
    """
    is_valid = False
    work_id = ''

    # is it an int?
    if isinstance(asset_id, int) and asset_id > 0:
            work_id = str(asset_id)
            is_valid = True
    # is it a string?
    elif isinstance(asset_id, str):
        if asset_id.startswith('ref:') and len(asset_id)<=154:
            work_id = asset_id
            is_valid = True
        else:
            try:
                work_id = str(int(asset_id))
            except ValueError:
                is_valid = False
            else:
                is_valid = True
    # is it a float?
    elif isinstance(asset_id, float):
        if asset_id.is_integer():
            work_id = str(int(asset_id))
            is_valid = True

    return is_valid, work_id

@functools.lru_cache()
def is_json(myjson: str) -> bool:
    """
    Function to check if a string is valid JSON.

    Args:
        myjson (str): string to check.

    Returns:
        bool: true if myjson is valid JSON, false otherwise.
    """
    try:
        _ = json.loads(myjson)
    except (TypeError, OverflowError, ValueError, JSONDecodeError):
        return False
    return True

def videos_from_file(filename: str, column_name: str='video_id', validate: bool=True, unique: bool=True) -> list:
    """
    Function to read a list of video IDs from an xls/csv file.

    Args:
        filename (str): path and name of file to read from.
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
    except XLRDError as e:
        raise XLRDError(f'Error while trying to parse XLS file {filename}: {e}') from e
    except ParserError as e:
        raise ParserError(f'Error while trying to parse CSV file {filename}: {e}') from e
    except OSError as e:
        raise OSError(f'Error while trying to read {filename} -> {e}') from e
    else:
        try:
            if validate:
                video_list = [video_id for video_id in data[column_name] if is_valid_id(video_id)]
            else:
                video_list = list(data[column_name])
        except KeyError as e:
            raise KeyError(f'Error while trying to parse {filename} -> missing key: "{column_name}"') from e

    # make list unique
    if video_list and unique:
        video_list = list(set(video_list))

    return video_list

def fetch_value(data: dict, key: str, default: str=''):
    """
    Function to get a value from a key in a dict.
    Supports getting values from an array index.

    Args:
        data (dict): A dictionary.
        key (str): Key for which to get the value. Can have an index attached as [index].
        default (str, optional): Default return value if key is empty or doesn't exist. Defaults to ''.

    Returns:
        [type]: Value of key in dictionary if it exists, otherwise the provided default value.

    Raises:
        IndexError: If provided index is out of bounds.
    """
    value = default

    if data and key:
        try:
            start = key.index('[')
            end = key.index(']')
            value = data.get(key[:start], default)[int(key[start+1:end])]
        except ValueError:
            value = data.get(key, default)
        except IndexError as e:
            raise IndexError(f'index error using key -> {key}') from e
        except AttributeError:
            pass

    return value if value else default

def get_value(data: dict, field: str, default: str=''):
    """
    Function to get the value, represented as a string, from a dictionary.
    Walks down recursively multiple levels of fields separated to
    be able to support custom fields and similar.

    Args:
        data (dict): A dictionary.
        field (str): Name of the field to get the value from.
        default (str, optional): Default return value. Defaults to ''.

    Returns:
        str: Content of the field or default value if field doesn't exist.
    """
    if '.' in field:
        primary, secondary = field.split('.', 1)
        try:
            value = fetch_value(data, primary, default)
            if value == default or value is None:
                return default
            return get_value(value, secondary, default)
        except TypeError:
            return f'ERROR: primary/secondary field error -> {primary}/{secondary}'
        except IndexError as e:
            return f'ERROR: {e}'
    else:
        try:
            return fetch_value(data, field, default)
        except IndexError as e:
            return f'ERROR: {e}'

def default_split(data: str, separator: str=' ', default: str='', maxsplits: int=0) -> list:
    """
    Function to split a string and return a list of substring.
    If more splits requested than there are substrings then a
    default value is used.

    Args:
        data (str): String to be split.
        separator (str, optional): Seperator. Defaults to ' '.
        default (str, optional): Default split value. Defaults to ''.
        maxsplits (int, optional): Number of splits to perform. Defaults to 0 which means all.

    Returns:
        list: List of split values.
    """
    result = []

    if maxsplits <= 0:
        maxsplits = data.count(separator)

    while maxsplits:
        try:
            value, data = data.split(separator, 1)
        except ValueError:
            value = data
            data = default

        result.append(value)
        maxsplits -= 1

    result.append(data)
    return result
