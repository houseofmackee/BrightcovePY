"""
script to find players which have the hls flag set to disabled
"""
from pprint import pprint
from mackee import load_account_info
from brightcove.OAuth import OAuth
from brightcove.PlayerManagement import PlayerManagement

# get account info from config file
account_id, client_id, client_secret, _ = load_account_info()

if(account_id is None and client_id is None and client_secret is None):
    print('Using default values for credentials.')
    # edit details as required
    account_id = ''
    client_id = ''
    client_secret = ''

# create a Player Management API instance
pma = PlayerManagement( OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret) )

# list of accounts that need patching
account_list = [ account_id ]

# create list of all players in all accounts in the accounts list
player_list = [['account_id', 'player_id', 'hls_flag']]
for account in account_list:
    # get the items in the list of players
    players = pma.GetListOfPlayers(account_id=account).json().get('items')

    for player in players:
        player_id = player.get('id')
        player_config = pma.GetPlayerConfiguration(account_id=account_id, branch='master', player_id=player_id).json()
        hls_flag = player_config.get('hls')
        player_list.append([account, player_id, hls_flag])

pprint(player_list)
