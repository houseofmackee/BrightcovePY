#!/usr/bin/env python3
import mackee

#===========================================
# callback to find videos with text tracks
#===========================================
def find_tt(video):
	tts = video.get('text_tracks')
	if tts:
		print(f'{video.get("id")}, "{video.get("name")}"')
		for track in tts:
			print(track.get('srclang'))

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(find_tt)
