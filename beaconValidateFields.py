"""
Example script showing how to validate Beacon custom fields
"""
import re
import sys
import argparse
from json import JSONDecodeError
from brightcove.CMS import CMS
from brightcove.OAuth import OAuth
from brightcove.utils import load_account_info, eprint

# list of good field names
good_fields = (
    'beacon_genre',
    'beacon_productionyear',
    'beacon_cast_director',
    'beacon_cast_singer',
    'beacon_cast_actor',
    'beacon_cast_composer',
    'beacon_cast_songwriter',
    'beacon_cast_writer',
    'beacon_agerating',
    'beacon_shortdescription',
    'beacon_longdescription',
    'beacon_viewerscore',
    'beacon_trailer_id',
    'beacon_ingest',
    'beacon_rights_<counter>_type',
    'beacon_rights_<counter>_startdate',
    'beacon_rights_<counter>_enddate',
    'beacon_rights_<counter>_devices',
    'beacon_rights_<counter>_locationspermit',
    'beacon_rights_<counter>_locationsdeny',
    'beacon_rights_<counter>_packagename',
    'beacon_rights_<counter>_adconfiguration',
    'beacon_episode_seriename',
    'beacon_episode_seasonnumber',
    'beacon_episode_number',
)

def sanitize(value: str) -> str:
    """
    function to remove counters and sanitize a field name
    """
    return str(re.sub(r'\d+', '<counter>', value))

# init the argument parsing
parser = argparse.ArgumentParser(prog=sys.argv[0])
parser.add_argument('-i', metavar='<config filename>', type=str, help='Name and path of account config information file')
parser.add_argument('-t', metavar='<Brightcove account ID>', type=str, help='Brightcove account ID to use (if different from ID in config)')
parser.add_argument('-l', action='store_true', default=False, help='List all custom fields')

# parse the args
args = parser.parse_args()

# get account info from config file if not hardcoded
try:
    account_id, client_id, client_secret, _ = load_account_info(args.i)
except (OSError, JSONDecodeError) as e:
    print(e)
    sys.exit(2)

# if account ID was provided override the one from config
account_id = args.t or account_id

# create a CMS API instance
cms = CMS(oauth=OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret))

# make API call
response = cms.GetCustomFields()

# list all fields that don't match known Beacon field patterns
if response.status_code == 200:
    custom_fields : dict = response.json()
    for field in custom_fields:
        current_field = field.get('id', '')
        if sanitize(current_field) not in good_fields or args.l:
            print(current_field)
else:
    eprint(f'Error while trying to get custom fields: {response.status_code}')
