#!/usr/bin/env python3
from mackee import PlayerManagement
from mackee import OAuth
from mackee import LoadAccountInfo

# get account info from config file
account_id, client_id, client_secret, _ = LoadAccountInfo()

if None in [account_id, client_id, client_secret]:
	print('Using default values for credentials.')
	# edit details as required
	account_id = ''
	client_id = ''
	client_secret = ''

# create a Player Management API instance
pms = PlayerManagement( OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret) )

# define the default JSON Body
json_body = '{ "video_cloud": { "base_url": "https://edge-elb.api.brightcove.com/playback/v1/" } }'

# list of accounts that need patching
account_list = [ account_id ]

# process all accounts in the accounts list
for account in account_list:
	print(f'Processing players in account ID {account}:')

	# get the items in the list of players
	player_list = pms.GetListOfPlayers(account_id=account).json()['items']

	# patch every player in the account using the above JSON body
	for player in player_list:
		player_id = player.get('id')
		print(f'Patching player ID {player_id}: {pms.UpdatePlayerConfiguration(account_id=account, player_id=player_id, json_body=json_body).status_code}')
