#!/usr/bin/env python3
import sys
from mackee import PlayerManagement
from mackee import OAuth
from mackee import GetAccountInfo

# get account info from config file
account_id, client_id, client_secret, _ = GetAccountInfo()

# create a Player Management API instance
pms = PlayerManagement( OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret) )

# define the default JSON Body
jsonBody = '{ "video_cloud": { "base_url": "https://edge-elb.api.brightcove.com/playback/v1/" } }'

# list of accounts that need patching
accountList = [ account_id ]

for account in accountList:
	print('Processing players in account ID '+str(account)+':')
	# get the items in the list of players
	playerList = pms.GetListOfPlayers(accountID=account).json()['items']

	# patch every player in the account using the above JSON body
	for player in playerList:
		playerID = player.get('id')
		print('Patching player ID '+playerID+': '+str(pms.UpdatePlayerConfiguration(accountID=account, playerID=playerID, jsonBody=jsonBody).status_code))
