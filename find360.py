#!/usr/bin/env python3
from mackee import main

#===========================================
# callback to find 360 videos 
#===========================================
def find360(video):
	if(video.get('projection') == 'equirectangular'):
		print(str(video.get('id'))+', "'+video.get('name')+'"')

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(find360)
