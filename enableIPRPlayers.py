#!/usr/bin/env python3
import sys
from mackee import PlayerManagement
from mackee import OAuth
from mackee import GetAccountInfo

# get account info from config file
account_id, client_id, client_secret, _ = GetAccountInfo()

# create a Player Management API instance
pms = PlayerManagement( OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret) )

# get the items in the list of players
playerList = pms.GetListOfPlayers(accountID=account_id).json()['items']

# define the default JSON Body
jsonBody = '{ "video_cloud": { "base_url": "https://edge-elb.api.brightcove.com/playback/v1/" } }'

# patch every player in the account using the above JSON body
for player in playerList:
	playerID = player.get('id')
	print('Patching player ID '+playerID+': '+str(pms.UpdatePlayerConfiguration(accountID=account_id, playerID=playerID, jsonBody=jsonBody).status_code))
