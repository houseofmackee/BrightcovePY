#!/usr/bin/env python3
import mackee

#===========================================
# callback to find videos with text tracks
#===========================================
def findNonTT(video):
	tts = video.get('text_tracks')
	if(not tts):
		print( video.get('id') )

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(findNonTT)
