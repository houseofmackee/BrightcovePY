#!/usr/bin/env python3
import mackee

#===========================================
# callback to find legacy delivery videos 
#===========================================
def findLegacy(video):
	if(video['delivery_type'] == 'static_origin'):
		print(video['id']+', "'+video['name']+'"')

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(findLegacy)
