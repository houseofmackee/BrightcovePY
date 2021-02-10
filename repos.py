#!/usr/bin/env python3
import sys
import argparse
from brightcove.DeliverySystem import DeliverySystem
from brightcove.OAuth import OAuth
from brightcove.utils import load_account_info

# init the argument parsing
parser = argparse.ArgumentParser(prog=sys.argv[0])
parser.add_argument('--list', action='store_true', default=False, help='List all repositories or files in account or repository')
parser.add_argument('--add', action='store_true', default=False, help='Add a repository or file to account or repository')
parser.add_argument('--delete', action='store_true', default=False, help='Delete a repository or file in account or repository')
parser.add_argument('--repo', metavar='<repository name>', type=str, help='Name of repository')
parser.add_argument('--file', metavar='<filename>', type=str, help='File name')
parser.add_argument('--config', metavar='<config filename>', type=str, help='Name and path of account config information file')
parser.add_argument('--account', metavar='<Brightcove Account ID>', type=str, help='Brightcove Account ID to use (if different from ID in config)')

# parse the args
args = parser.parse_args()

# get account info from config file
try:
    account_id, client_id, client_secret, _ = load_account_info(args.config)
except Exception as e:
    print(e)
    sys.exit(2)

# if account ID was provided override the one from config
account_id = args.account or account_id

# create a Delivery System API instance
ds = DeliverySystem(OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret))

# delete one or all subscriptions
if args.delete:
    # delete a file in a repo?
    if args.repo and args.file:
        if args.file=='all':
            print('Delete all files not supported yet.')
        else:
            response = ds.DeleteFileInRepository(repo_name=args.repo, file_name=args.file, account_id=account_id)
            code = response.status_code
            print(f'Deleting file "{args.file}" in repository "{args.repo}": {code}')
            if code not in DeliverySystem.success_responses:
                print(f'Error deleting file to repository: {response.text}')
    # delete a repo?
    elif args.repo:
        response = ds.DeleteRepository(repo_name=args.repo, account_id=account_id)
        code = response.status_code
        print(f'Deleting repository "{args.repo}" in account ID {account_id}: {code}')
        if code not in DeliverySystem.success_responses:
            print(f'Error deleting repository: {response.text}')

# add a repo to account or a file to a repo
if args.add:
    # add a file to a repo?
    if args.repo and args.file:
        response = ds.AddFileToRepository(repo_name=args.repo, file_name=args.file, account_id=account_id)
        code = response.status_code
        print(f'Adding file "{args.file}" to repository "{args.repo}": {code}')
        if code in DeliverySystem.success_responses:
            print(response.text)
        else:
            print(f'Error adding file to repository: {response.text}')
    # add a repo
    elif args.repo:
        response = ds.CreateRepository(repo_name=args.repo, account_id=account_id)
        code = response.status_code
        print(f'Adding repository "{args.repo}" to account ID {account_id}: {code}')
        if code in DeliverySystem.success_responses:
            print(response.text)
        else:
            print(f'Error adding repository to account: {response.text}')

# list files in repo or list all repos in account
if args.list:
    # list files in a repo?
    if args.repo:
        response = ds.ListFilesInRepository(repo_name=args.repo, account_id=account_id)
        if response.status_code in DeliverySystem.success_responses:
            response = response.json()
            print(f'{response["item_count"]} item(s) found in repository.\n')
            for repo_file in response['items']:
                print(f'Name: {repo_file["name"]}\nURL.: {repo_file["public_url"]}\n')
        else:
            print(f'Error listing files in repository: {response.text}')
    # list repos in an account
    else:
        response = ds.ListRepositories(account_id=account_id)
        if response.status_code in DeliverySystem.success_responses:
            response = response.json()
            print(f'{response["item_count"]} item(s) found in account.\n')
            for repo in response['items']:
                print(f'Name: {repo["name"]}')
        else:
            print(f'Error listing repositories in account: {response.text}')
