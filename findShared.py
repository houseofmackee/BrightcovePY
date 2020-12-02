#!/usr/bin/env python3
import mackee

#===========================================
# callback to find videos into the account
#===========================================
def find_shared(video):
	shared = video.get('sharing')
	if shared and shared.get('by_external_acct'):
		print(f'{video.get("id")}, {shared}')

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(find_shared)
