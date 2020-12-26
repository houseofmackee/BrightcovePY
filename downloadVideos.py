#!/usr/bin/env python3
import requests # pip3 install requests
from clint.textui import progress # pip3 install clint
from mackee import main, get_cms

#===========================================
# download highest res MP4 from a video
#===========================================
def download_video(video: dict):
	"""
	This will download the highest resolution MP4 from a video.
	"""
	video_id = str(video.get('id'))
	source_url, source_w, source_h = None, 0, 0

	# get sources for the video and try to find the biggest MP4 video
	sourceList = get_cms().GetVideoSources(video_id=video_id).json()
	for source in sourceList:
		sourceType = source.get('container')
		if sourceType and sourceType=='MP4':
			w, h = source.get('width'), source.get('height')
			if h and w and w>source_w:
				source_w, source_h, source_url = w, h, source.get('src')

	# if a source was found download it, using the video ID as filename
	if source_url:
		print(f'{video_id}: highest resolution MP4 source is {source_w}x{source_h}. Downloading...')

		r = requests.get(source_url, stream=True)
		with open(f'{video_id}.mp4', 'wb') as out:
			total_length = int(r.headers.get('content-length'))
			for ch in progress.bar(r.iter_content(chunk_size = 2097152), expected_size=(total_length/2097152) + 1):
				if ch:
					out.write(ch)
					out.flush()

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(download_video)
