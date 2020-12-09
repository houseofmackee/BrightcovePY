#!/usr/bin/env python3
from mackee import main, get_cms, get_args
from brightcove.utils import list_to_csv, eprint
from brightcove.utils import TimeString
import sys
import time
from threading import Lock

videos_processed = 0
counter_lock = Lock()
data_lock = Lock()

row_list = [ ['video_id','delivery_type','master_size','hls_renditions_size','mp4_renditions_size','audio_renditions_size', 'flv_size'] ]

def show_progress(progress: int) -> None:
	sys.stderr.write(f'\r{progress} processed...\r')
	sys.stderr.flush()

#===========================================
# function to get size of master
#===========================================
def get_master_storage(video: dict) -> int:
	master_size = 0
	response = None

	if video.get('has_digital_master'):
		try:
			response = get_cms().GetDigitalMasterInfo(video_id=video.get('id'))
		except:
			response = None
			master_size = -1

		if response and response.status_code == 200:
			master_size = response.json().get('size')

	return master_size

#===========================================
# function to get size of all renditions
#===========================================
def get_rendition_sizes(video: dict) -> dict:
	sizes = {
		'hls_size':0,
		'mp4_size':0,
		'audio_size':0,
		'flv_size':0
	}

	response = None
	delivery_type = video.get('delivery_type')
	video_id = video.get('id')

	try:
		if delivery_type == 'static_origin':
			response = get_cms().GetRenditionList(video_id=video_id)
		elif delivery_type == 'dynamic_origin':
			response = get_cms().GetDynamicRenditions(video_id=video_id)
	except:
		response = None
		sizes = { key:-1 for key in sizes }

	if response and response.ok:
		renditions = response.json()
		for rendition in renditions:
			size = rendition.get('size')
			# legacy mp4 and hls
			if rendition.get('video_container') == 'MP4':
				sizes['mp4_size'] += size
			elif rendition.get('video_container') == 'M2TS':
				sizes['hls_size'] += size
			elif rendition.get('video_container') == 'FLV':
				sizes['flv_size'] += size

			# dyd audio and video
			elif rendition.get('media_type') == 'audio':
				sizes['audio_size'] += size
			elif rendition.get('media_type') == 'video':
				sizes['hls_size'] += size

		# if it's Dynamic Delivery we need to get MP4 sizes from the sources endpoint
		if delivery_type == 'dynamic_origin' and sizes['mp4_size'] == 0:
			try:
				response = get_cms().GetVideoSources(video_id=video_id)
			except:
				sizes['mp4_size'] = -1
			else:
				if response.status_code in get_cms().success_responses:
					sizes['mp4_size'] += sum(set([rendition.get('size') for rendition in response.json() if rendition.get('container') == 'MP4']))

	return sizes

#===========================================
# callback getting storage sizes
#===========================================
def find_storage_size(video: dict) -> None:
	global videos_processed

	row = [ video.get('id'), video.get('delivery_type') ]

	shared = video.get('sharing')
	if shared and shared.get('by_external_acct'):
		row.extend( [0 for _ in range(len(row_list[0])-len(row))] )
	else:
		row.append( get_master_storage(video) )
		sizes = get_rendition_sizes(video)
		row.extend( [sizes["hls_size"], sizes["mp4_size"], sizes["audio_size"], sizes["flv_size"]] )

	# add a new row to the CSV data
	with data_lock:
		row_list.append(row)

	# increase processed videos counter
	with counter_lock:
		videos_processed += 1

	# display counter every 100 videos
	if videos_processed%100==0:
		show_progress(videos_processed)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	s = time.perf_counter()
	main(find_storage_size)
	show_progress(videos_processed)

	#write list to file
	list_to_csv(row_list, get_args().o)

	elapsed = time.perf_counter() - s
	eprint(f"\n{__file__} executed in {TimeString.from_seconds(elapsed)}.")
