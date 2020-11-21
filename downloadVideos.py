#!/usr/bin/env python3
from mackee import main, GetCMS
import requests # pip3 install requests
from clint.textui import progress # pip3 install clint

#===========================================
# download highest res MP4 from a video
#===========================================
def downloadVideo(video):
	videoID = str(video.get('id'))
	sourceURL, sourceW, sourceH = None, 0, 0

	# get sources for the video and try to find the biggest MP4 video
	sourceList = GetCMS().GetVideoSources(videoID=videoID).json()
	for source in sourceList:
		sourceType = source.get('container')
		if(sourceType and sourceType=='MP4'):
			w, h = source.get('width'), source.get('height')
			if(h and w and w>sourceW):
				sourceW, sourceH, sourceURL = w, h, source.get('src')

	# if a source was found download it, using the video ID as filename
	if(sourceURL):
		print(videoID+': highest resolution MP4 source is '+str(sourceW)+'x'+str(sourceH)+'. Downloading...')

		r = requests.get(sourceURL, stream=True)
		with open(videoID+".mp4", "wb") as out:
			total_length = int(r.headers.get('content-length'))
			for ch in progress.bar(r.iter_content(chunk_size = 2097152), expected_size=(total_length/2097152) + 1):
				if(ch):
					out.write(ch)
					out.flush()

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(downloadVideo)
