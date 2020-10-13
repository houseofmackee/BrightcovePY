#!/usr/bin/env python3
import mackee

#===========================================
# callback to find videos into the account
#===========================================
def findShared(video):
	shared = video.get('sharing')
	if(shared and shared.get('by_external_acct')):
		print(str(video.get('id'))+', '+str(shared))

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(findShared)
