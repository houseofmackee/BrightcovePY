#!/usr/bin/env python3
import mackee

#===========================================
# callback to find videos with text tracks
#===========================================
def findTT(video):
	tts = video['text_tracks']
	if(len(tts)>0):
		print(video['id']+', "'+video['name']+'"')
		for track in tts:
			print(track['srclang'])

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(findTT)
