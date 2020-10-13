#!/usr/bin/env python3
import mackee

#===========================================
# callback to find videos with text tracks
#===========================================
def findTT(video):
	tts = video.get('text_tracks')
	if(tts and len(tts)>0):
		print(str(video.get('id')+', "'+video.get('name')+'"'))
		for track in tts:
			print(track.get('srclang'))

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(findTT)
