#!/usr/bin/env python3
import sys
import argparse
from mackee import DeliverySystem
from mackee import OAuth
from mackee import GetAccountInfo

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
account_id, client_id, client_secret, _ = GetAccountInfo(args.config)

# if account ID was provided override the one from config
if(args.account):
	account_id = args.account

# create a CMS API instance
ds = DeliverySystem( OAuth(account_id=account_id,client_id=client_id, client_secret=client_secret) )

# delete one or all subscriptions
if(args.delete):
	# delete a file in a repo?
	if(args.repo and args.file):
		if(args.file=='all'):
			print('Delete all files not supported yet.')
		else:
			r = ds.DeleteFileInRepository(repoName=args.repo, fileName=args.file, accountID=account_id)
			c = r.status_code
			print('Deleting file "'+args.file+'" in repository "'+args.repo+'": '+str(c))
			if(c not in DeliverySystem.success_responses):
				print('Error deleting file to repository: '+r.text)
	# delete a repo?
	elif(args.repo):
		r = ds.DeleteRepository(repoName=args.repo, accountID=account_id)
		c = r.status_code
		print('Deleting repository "'+args.repo+'" in account ID '+account_id+': '+str(c))
		if(c not in DeliverySystem.success_responses):
			print('Error deleting repository: '+r.text)

# add a repo to account or a file to a repo
if(args.add):
	# add a file to a repo?
	if(args.repo and args.file):
		r = ds.AddFileToRepository(repoName=args.repo, fileName=args.file, accountID=account_id)
		c = r.status_code
		print('Adding file "'+args.file+'" to repository "'+args.repo+'": '+str(c))
		if(c in DeliverySystem.success_responses):
			print(r.text)
		else:
			print('Error adding file to repository: '+r.text)
	# add a repo
	elif(args.repo):
		r = ds.CreateRepository(repoName=args.repo, accountID=account_id)
		c = r.status_code
		print('Adding repository "'+args.repo+'" to account ID '+account_id+': '+str(c))
		if(c in DeliverySystem.success_responses):
			print(r.text)
		else:
			print('Error adding repository to account: '+r.text)

# list files in repo or list all repos in account
if(args.list):
	# list files in a repo?
	if(args.repo):
		r = ds.ListFilesInRepository(repoName=args.repo, accountID=account_id)
		if(r.status_code in DeliverySystem.success_responses):
			r = r.json()
			print(str(r['item_count'])+' item(s) found in repository.\n')
			for repoFile in r['items']:
				print(('Name: {filename}\nURL.: {fileurl}\n').format(filename=repoFile['name'], fileurl=repoFile['public_url']))
		else:
			print('Error listing files in repository: '+r.text)
	# list repos in an account
	else:
		r = ds.ListRepositories(accountID=account_id)
		if(r.status_code in DeliverySystem.success_responses):
			r = r.json()
			print(str(r['item_count'])+' item(s) found in account.\n')
			for repo in r['items']:
				print(('Name: {reponame}').format(reponame=repo['name']))
		else:
			print('Error listing repositories in account: '+r.text)
