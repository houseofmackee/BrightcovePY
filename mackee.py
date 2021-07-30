#!/usr/bin/env python3
from __future__ import print_function
import sys
import argparse
import time
import logging
from os import path
from json import JSONDecodeError
from queue import Queue, Empty
from typing import cast, Callable, Dict, Any
from threading import Thread
from xlrd import XLRDError
from pandas.errors import ParserError
from requests.exceptions import RequestException
from requests.models import Response
import requests # pip3 install requests

from brightcove.OAuth import OAuth
from brightcove.CMS import CMS
from brightcove.DynamicIngest import DynamicIngest

from brightcove.utils import eprint, static_vars, load_account_info
from brightcove.utils import videos_from_file

mac_logger = logging.getLogger()

# disable certificate warnings
requests.urllib3.disable_warnings() #type: ignore

#===========================================
# returns a DI instance
#===========================================
@static_vars(di=None)
def get_di(oauth: OAuth=None, profile: str='', priority: str='normal') -> DynamicIngest:
    """
    Returns an existing DynamicIngest instance. Creates one if information is provided.

    Args:
        oauth (OAuth, optional): OAuth instance to use. Defaults to None.
        profile (str, optional): Ingest profile ID. Defaults to ''.
        priority (str, optional): Priority queue. Defaults to 'normal'.

    Returns:
        DynamicIngest: DynamicIngest instance. None if none was created yet.
    """
    if not get_di.di and oauth:
        get_di.di = DynamicIngest(oauth=oauth, ingest_profile=profile, priority_queue=priority)
        mac_logger.info('Obtained DI instance')

    return get_di.di

@static_vars(cms=None)
def get_cms(oauth: OAuth=None, query: str='') -> CMS:
    """
    Returns an existing CMS instance. Creates one if information is provided.

    Args:
        oauth (OAuth, optional): OAuth instance to use. Defaults to None.
        query (str, optional): Query string to use. Defaults to None.

    Returns:
        CMS: CMS instance. None if none was created yet.
    """
    if not get_cms.cms and oauth:
        get_cms.cms = CMS(oauth=oauth, query=query)
        mac_logger.info('Obtained CMS instance')
    return get_cms.cms

@static_vars(oauth=None)
def get_oauth(account_id: str='', client_id: str='', client_secret: str='') -> OAuth:
    """
    Returns an OAuth instance. Creates one if it doesn't exist yet.
    """
    if not get_oauth.oauth:
        get_oauth.oauth = OAuth(account_id, client_id, client_secret)
        mac_logger.info('Obtained OAuth instance')
    return get_oauth.oauth

@static_vars(args=None)
def get_args():
    """
    Returns the command line arguments. Parses them if not parsed yet.
    """
    if not get_args.args:
        # init the argument parsing
        parser = argparse.ArgumentParser(prog=sys.argv[0])
        parser.add_argument('-i', type=str, help='Name and path of account config information file')
        parser.add_argument('-q', type=str, help='CMS API search query')
        parser.add_argument('-t', type=str, help='Target account ID')
        parser.add_argument('-v', type=str, help='Specific video ID to process')
        parser.add_argument('-o', type=str, help='Output filename')
        parser.add_argument('-x', type=str, help='XLS/CSV input filename')
        parser.add_argument('-a', type=int, const=10, nargs='?', help='Async processing of videos')
        parser.add_argument('-d', action='store_true', default=False, help='Show debug info messages')
        parser.add_argument('-l', type=int, const=0, nargs='?', help='Limit to first x amount of videos')

        get_args.args = parser.parse_args()

        if get_args.args.d:
            logging.basicConfig(level=logging.INFO, format='[%(levelname)s:%(lineno)d]: %(message)s')
            mac_logger.info('Logging at INFO level enabled')
        else:
            logging.basicConfig(level=logging.CRITICAL, format='[%(levelname)s:%(lineno)d]: %(message)s')

        mac_logger.info('Obtained arguments')

    return get_args.args

@static_vars(session=None)
def get_session():
    """
    Returns a requests session. Creates one if it doesn't exist yet.
    """
    if not get_session.session:
        get_session.session = requests.Session()
        mac_logger.info('Obtained Requests Session')
    return get_session.session

@static_vars(opts=None)
def get_opts(opts: dict = None) -> dict:
    if get_opts.opts is None:
        get_opts.opts = opts
    return get_opts.opts

#===========================================
# default processing function
#===========================================
@static_vars(print_header=True)
def list_videos(video: dict) -> None:
    """
    Default callback function. Prints out video ID and name.
    """
    if list_videos.print_header:
        print('video_id, title')
        list_videos.print_header = False
    print(f'{video.get("id")}, {video.get("name")}')

def get_accounts(account_parameter: str) -> list:
    """
    Function to generate a list of account IDs from a CSV/XLS file, a comma separated
    command line option or just the default account ID from the config.

    Returns:
        list: [description]
    """
    if path.isfile(account_parameter):
        return videos_from_file(filename=account_parameter, column_name='account_id')

    if ',' in account_parameter:
        return [x.strip() for x in account_parameter.split(sep=',')]

    return [account_parameter]

def limit(input_value: int, limit_value: int) -> int:
    return min(input_value, limit_value) if limit_value else input_value

#===========================================
# function to fill queue with all videos
# from a Video Cloud account
#===========================================
def process_account(work_queue: Queue, account_id: str, cms_obj: CMS) -> None:
    """
    Function to fill a Queue with a list of all video IDs in an account.

    Args:
        work_queue (Queue): Queue to be filled with IDs
        cms_obj (CMS): CMS class instance
        account_id (str): Video Cloud account ID
    """
    # ok, let's process all videos
    # get number of videos in account
    try:
        num_videos = cms_obj.GetVideoCount(account_id=account_id)
    except RequestException as e:
        eprint(f'Error getting number of videos in account ID {account_id} -> {e}')
        return

    if num_videos <= 0:
        eprint(f'No videos found in account ID {account_id}\'s library.')
        return

    num_videos = limit(num_videos, get_args().l)

    eprint(f'Found {num_videos} videos in account ID {account_id}\'s library. Processing them now.')

    current_offset = 0
    page_size = min(50, num_videos)
    retries = 10

    while current_offset < num_videos:

        try:
            response = cms_obj.GetVideos(account_id=account_id, page_size=page_size, page_offset=current_offset)
            status = response.status_code
        except RequestException:
            response = cast(Response, None)
            status = -1

        # good result
        if status in [200,202]:
            json_data = cast(dict, response.json())
            # make sure we actually got some data
            if len(json_data) > 0:
                # let's put all videos in a queue
                for video in json_data:
                    work_queue.put_nowait(video)
                # reset retries count and increase page offset
                retries = 10
                current_offset += page_size
                try:
                    current_num_videos = cms_obj.GetVideoCount(account_id=account_id)
                except RequestException as e:
                    eprint(f'Warning: error refreshing number of videos in account ID {account_id} -> {e}')
                else:
                    if current_num_videos > num_videos:
                        num_videos = limit(current_num_videos, get_args().l)

            # looks like we got an empty response (it can happen)
            else:
                status = -1

        # we hit a retryable error
        if status == -1:
            code = response.status_code if response else 'unknown'
            if retries > 0:
                eprint(f'Error: problem during API call ({code}).')
                for remaining in range(5, 0, -1):
                    sys.stderr.write(f'\rRetrying in {remaining:2d} seconds.')
                    sys.stderr.flush()
                    time.sleep(1)

                retries -= 1
                eprint(f'\rRetrying now ({retries} retries left).')

            else:
                eprint(f'Error: fatal failure during API call ({code}).')
                return

#===========================================
# function to process a single video
#===========================================
def process_single_video_id(account_id: str, video_id: str, cms_obj: CMS, process_callback: Callable[[Dict[Any, Any]], None]) -> bool:
    """
    Function to process a single video using a provided callback function

    Args:
        account_id (str): the account ID
        video_id (str): the video ID
        cms_obj (CMS): CMS class instance
        process_callback (Callable[[], None]): the callback function used for actual processing

    Returns:
        bool: True if there was no error, False otherwise
    """
    response = None
    try:
        response = cms_obj.GetVideo(account_id=account_id, video_id=video_id)
    except RequestException:
        response = None

    if response and response.status_code in CMS.success_responses:
        try:
            process_callback(response.json())
        except Exception as e:
            eprint(f'Error executing callback for video ID {video_id}: {e}')
            return False

    else:
        if response is None:
            code = 'exception'
        else:
            code = str(response.status_code)
        eprint(f'Error getting information for video ID {video_id} ({code}).')
        return False

    return True

class Worker(Thread):
    """
    Worker class for multithreading using queues.
    """
    def __init__(self, queue:Queue, cms_obj: CMS, account_id: str, process_callback: Callable, *args, **kwargs):
        """
        Args:
            queue (Queue): Queue to process.
            cms_obj (CMS): CMS instance to use.
            account_id (str): Brightcove account ID.
            process_callback (Callable): Callback function which processes the data.
        """
        super().__init__(*args, **kwargs)
        self.queue = queue
        self.cms_obj = cms_obj
        self.account_id = account_id
        self.process_callback = process_callback

    def run(self):
        """
        Processes the queue.
        """
        keep_working = True
        while keep_working:
            try:
                work = self.queue.get()
            except Empty:
                mac_logger.info('Queue empty -> exiting worker thread')
                return
            # is it the exit signal?
            if work == 'EXIT':
                mac_logger.info('EXIT found -> exiting worker thread')
                keep_working = False
            # do whatever work you have to do on work
            elif isinstance(work, dict):
                self.process_callback(work)
            else:
                process_single_video_id(account_id=self.account_id,
                                        video_id=work,
                                        cms_obj=self.cms_obj,
                                        process_callback=self.process_callback)
            self.queue.task_done()

#===========================================
# this is the main loop to process videos
#===========================================
def process_input(account_info_file: str='', process_callback: Callable=list_videos, video_id: str='') -> bool:
    """
    Function to process whatever was passed to the script.

    Args:
        account_info_file (str, optional): Account info JSON file to use. Defaults to ''.
        process_callback (Callable, optional): Name of function to process the data. Defaults to list_videos.
        video_id (str, optional): Video ID to process. Defaults to ''.

    Returns:
        bool: True if video processed successfully, False otehrwise.
    """
    # get the account info and credentials
    try:
        account_id, client_id, client_secret, opts = load_account_info(account_info_file)
    except (OSError, JSONDecodeError) as e:
        print(e)
        return False

    if None in [account_id, client_id, client_secret, opts]:
        return False

    # update account ID if passed in command line or if a list is in the JSON options
    # command line options override JSON config account ID(s)
    account_id_list = opts.get('account_ids')
    if not account_id_list or get_args().t:
        account_id_list = get_accounts(get_args().t or account_id)
    account_id = account_id_list[0]

    get_oauth(account_id, client_id, client_secret)
    get_cms(oauth=get_oauth(), query=get_args().q)
    get_di(oauth=get_oauth())
    get_opts(opts=opts)

    # if async is enabled use more than one thread
    max_threads = get_args().a or 1
    mac_logger.info('Using %d thread(s) for processing', max_threads)

    #=========================================================
    #=========================================================
    # check if we should process a specific video ID
    #=========================================================
    #=========================================================
    if video_id:
        print(f'Processing video ID {video_id} now.')
        return process_single_video_id(account_id, video_id, get_cms(), process_callback)

    # create the work queue because everything below uses it
    work_queue:Queue = Queue(maxsize=0)

    #=========================================================
    #=========================================================
    # check if we should process a given list of videos
    #=========================================================
    #=========================================================
    video_list = []
    if get_args().x:
        try:
            video_list = videos_from_file(get_args().x)
        except (OSError, KeyError, JSONDecodeError, XLRDError, ParserError) as e:
            print(e)
            sys.exit(2)
    else:
        video_list = opts.get('video_ids', [])

    if video_list and video_list[0] != 'all':
        # limit number of videos to be processed if a limit was provided using -l
        num_videos = limit(len(video_list), get_args().l)
        eprint(f'Found {num_videos} videos in file. Processing them now.')
        # let's put all video IDs in a queue
        for video_id_ in video_list:
            work_queue.put_nowait(video_id_)
        # starting worker threads on queue processing
        num_threads = min(max_threads, num_videos)
        for _ in range(num_threads):
            work_queue.put_nowait("EXIT")
            Worker(	queue=work_queue,
                    cms_obj=get_cms(),
                    account_id=account_id,
                    process_callback=process_callback).start()
        # now we wait until the queue has been processed
        if not work_queue.empty():
            work_queue.join()

        return True

    #=========================================================
    #=========================================================
    # here we process the whole account
    #=========================================================
    #=========================================================

    for account_id in account_id_list:
        get_oauth().account_id = account_id
        # start thread to fill the queue
        account_page_thread = Thread(target=process_account, args=[work_queue, account_id, get_cms()])
        account_page_thread.start()

        # starting worker threads on queue processing
        for _ in range(max_threads):
            Worker(queue=work_queue, cms_obj=get_cms(), account_id=account_id, process_callback=process_callback).start()

        # first wait for the queue filling thread to finish
        account_page_thread.join()

        # once the queue is filled with videos add exit signals
        for _ in range(max_threads):
            work_queue.put_nowait("EXIT")

        # now we wait until the queue has been processed
        if not work_queue.empty():
            work_queue.join()

    return True

#===========================================
# parse args and do the thing
#===========================================
def main(process_func: Callable) -> None:
    """
    This will parse command line arguments, get account credentials and then processess
    whatever was passed along.

    Args:
        process_func (Callable): Name of function to process the data.
    """
    # parse the args
    get_args()

    # go through the library and do stuff
    process_input(account_info_file=get_args().i, process_callback=process_func, video_id=get_args().v)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
    main(list_videos)
