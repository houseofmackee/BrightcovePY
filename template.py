#!/usr/bin/env python3
import mackee

#===========================================
# example callback function
#===========================================
def exampleFunction(video):
	print(video.get('id'), video.get('name'))

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(exampleFunction)