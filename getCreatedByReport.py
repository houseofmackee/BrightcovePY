#!/usr/bin/env python3
import mackee

createdByDict = {
	'Unknown':0,
	'API':0
}

videosProcessed = 0

#===========================================
# callback to check who uploaded the video
#===========================================
def getCreatedByReport(video):
	global createdByDict
	global videosProcessed

	createdBy = video.get('created_by')
	if(createdBy):
		ctype = createdBy.get('type')

		if(ctype=='api_key'):
			createdByDict['API'] += 1
		elif (ctype=='user'):
			creator = createdBy.get('email')
			try:
				createdByDict[creator] += 1
			except KeyError:
				createdByDict[creator] = 1
		else:
			createdByDict['Unknown'] += 1
	else:
		createdByDict['Unknown'] += 1

	videosProcessed += 1
	if(videosProcessed%100==0):
		mackee.sys.stderr.write(f'\r{videosProcessed} processed...')
		mackee.sys.stderr.flush()

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	mackee.main(getCreatedByReport)

	mackee.eprint(f'\r{videosProcessed} processed...')
	print('user_id, number_videos')
	for x in createdByDict:
		print(f'{x}, {createdByDict[x]}')
