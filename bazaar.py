from datetime import date
from pathlib import Path
import subprocess
import requests
import json


global request, API_KEY, file_name
request = requests.Session()
API_KEY = 'bb025a4d75d99a2a02991d22fd6b5b11'
today = date.today()
date = today.strftime("%m-%d-%Y")
file_name = date + '.txt'

def check_if_outfile_exists():
    does_file_exist = Path("./output/{}".format(file_name))
    if does_file_exist.is_file():
    	pass
    else:
    	open('./output/{}'.format(file_name), 'a').close()

def write_to_file(md5_hash):
	with open('./output/{}'.format(file_name), 'r+') as output:
		hashes = output.read().splitlines()
		#output.close()
		for hashe in hashes:
			print(hashe)
			if md5_hash == hashe:
				print('Dupe: {}'.format(md5_hash))
			else:
				with open('./output/{}'.format(file_name), 'a+') as hashes:
					hashes.write(hashe)


def query_bazaar():
	url = 'https://mb-api.abuse.ch/api/v1/'
	data = {'query': 'get_recent', 'selector': '100'}

	query_it = request.post(url, data=data)
	queried = query_it.json()
	#print(json.dumps(queried, indent=4))
	if queried['query_status'] == 'ok':
		for each in queried['data']:
			write_to_file(each['md5_hash'])
	elif queried['query_status'] == 'no_results':
		print('No Results')

check_if_outfile_exists()
query_bazaar()


