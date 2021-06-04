"""
script to find the most recent playback date for videos which had playback within the last 90 days
"""
from pprint import pprint
from brightcove.Analytics import Analytics, AnalyticsQueryParameters
from brightcove.OAuth import OAuth
from brightcove.utils import load_account_info

# get credentials and instantiate Analytics API
account_id, client_id, client_secret, _ = load_account_info()
oauth = OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret)
aapi = Analytics(oauth)

# set Analytics report query parameters
qstr = AnalyticsQueryParameters(
    accounts = account_id,
    dimensions = 'video,date',
    limit = 'all',
    reconciled = False,
    from_ = '-90d')

# make API call
response = aapi.GetAnalyticsReport(query_parameters=qstr).json().get('items',[])

# create a dictionary with unique video IDs and their most recent playback date
result = {}
for item in response:
    if video := item.get('video'):
        result[video] = max(result.get(video, ''), item.get('date'))

# print result
pprint(result)
