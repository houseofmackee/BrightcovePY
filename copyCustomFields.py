"""
Example script showing how to copy custom fields from one account to another.
"""
import sys
import argparse
from json import JSONDecodeError
from brightcove.CMS import CMS
from brightcove.OAuth import OAuth
from brightcove.utils import load_account_info, eprint

# init the argument parsing
parser = argparse.ArgumentParser(prog=sys.argv[0])
parser.add_argument('-i', metavar='<config filename>', type=str, help='Name and path of account config information file')
parser.add_argument('-f', metavar='<Brightcove account ID>', type=str, help='Brightcove account ID to use as source)')
parser.add_argument('-t', metavar='<Brightcove account ID>', type=str, help='Brightcove account ID to use as target')

# parse the args
args = parser.parse_args()

if not all([args.f, args.t]):
    print('Need from and to account IDs')
    sys.exit(2)

# get account info from config file if not hardcoded
try:
    account_id, client_id, client_secret, _ = load_account_info(args.i)
except (OSError, JSONDecodeError) as e:
    print(e)
    sys.exit(2)

# if account ID was provided override the one from config
account_id = args.f or account_id

# create a CMS API instance
cms = CMS(oauth=OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret))

# make API call
response = cms.GetCustomFields()

# copy all fields from one account to the other
if response.status_code == 200:
    custom_fields : dict = response.json()
    for field in custom_fields:
        r = cms.CreateCustomField(account_id=args.t, json_body=field)
        print(field.get('id'), r.status_code, sep=', ')
else:
    eprint(f'Error while trying to get custom fields: {response.status_code}')
