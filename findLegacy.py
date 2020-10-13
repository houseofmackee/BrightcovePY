#!/usr/bin/env python3
import mackee

#===========================================
# callback to find legacy delivery videos 
#===========================================
def findLegacy(video):
	if(video.get('delivery_type') == 'static_origin'):
		print(str(video.get('id'))+', "'+video.get('name')+'"')

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(findLegacy)
