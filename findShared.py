#!/usr/bin/env python3
from mackee import main

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
	main(find_shared)
