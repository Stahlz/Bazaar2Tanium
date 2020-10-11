from datetime import date
import requests
import json


global request, API_KEY, file_name
request = requests.Session()
API_KEY = ''
today = date.today()
date = today.strftime("%d-%m-%Y")
file_name = date + '.txt'

def write_to_file(md5_hash):
	try:
		with open(file_name, 'r+') as dedup:
			output = dedup.read().splitlines()
		for dedup in output:
			if md5_hash in output:
				print('Dupe Found: {0}'.format(md5_hash))
				continue
			else:
				with open(file_name, 'a+') as hashed:
					hashed.write(md5_hash + '\n')
	except Exception as failed_write:
		print(failed_write)


def query_bazaar():
	url = 'https://mb-api.abuse.ch/api/v1/'
	data = {'query': 'get_recent', 'selector': '100'}

	query_it = request.post(url, data=data)
	queried = query_it.json()
	#print(json.dumps(queried, indent=4))
	if queried['query_status'] == 'ok':
		for each in queried['data']:
			if each['md5_hash'] != '' or None:
				write_to_file(each['md5_hash'])
			else:
				print('No New Malware')
	elif queried['query_status'] == 'no_results':
		print('No Results')

query_bazaar()
