from datetime import date
from pathlib import Path
import subprocess
import requests
import json


global request, API_KEY, file_name
request = requests.Session()
API_KEY = ''
today = date.today()
date = today.strftime("%m-%d-%Y")
file_name = date + '.txt'

def check_if_outfile_exists():
    does_file_exist = Path("./output/{}".format(file_name))
    if does_file_exist.is_file():
    	pass
    else:
    	open('./output/{}'.format(file_name), 'a').close()

def make_list():
	global outputs
	with open('./output/{}'.format(file_name), 'r+') as read_output:
		outputs = read_output.read().splitlines()
		read_output.close()

def write_to_file(md5_hash):
	with open('./output/{}'.format(file_name), 'a+') as write_output:
		if not outputs:
			outputs.append(md5_hash)
			write_output.write(md5_hash + '\n')
		else:
			if md5_hash in outputs:
				pass
			else:
				outputs.append(md5_hash)
				write_output.write(md5_hash + '\n')

def query_bazaar():
	url = 'https://mb-api.abuse.ch/api/v1/'
	data = {'query': 'get_recent', 'selector': 'time'}

	query_it = request.post(url, data=data)
	queried = query_it.json()
	if queried['query_status'] == 'ok':
		for each in queried['data']:
			write_to_file(each['md5_hash'])
	elif queried['query_status'] == 'no_results':
		print('No Results')

check_if_outfile_exists()
make_list()
query_bazaar()
