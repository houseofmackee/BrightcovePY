"""
script to find last used date for players
"""
from pprint import pprint
from mackee import load_account_info
from brightcove.OAuth import OAuth
from brightcove.PlayerManagement import PlayerManagement

account_id = ''
client_id = ''
client_secret = ''
if not all([account_id, client_id, client_secret]):
    account_id, client_id, client_secret, _ = load_account_info()

# create a Player Management API instance
pma = PlayerManagement( OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret) )

# list of accounts that need checking
account_list = [account_id]
player_list = [['account_id', 'player_id', 'last_view']]

# create list of all players in all accounts in the accounts list
for account in account_list:
	# get the items in the list of players
	players = pma.GetListOfPlayers(account_id=account).json().get('items')

	# get last view date for each player
	for player in players:
		player_id = player.get('id')
		last_view = player.get('last_viewed')[0]['date'] if player.get('last_viewed') else '-'
		player_list.append([account, player_id, last_view])

pprint(player_list)
