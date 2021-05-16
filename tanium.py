import requests
import configparser
import json
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""Configparser setup"""
configfilepath = './config.py'
config = configparser.ConfigParser()
config.read(configfilepath)

global request,url,username,password,domain
request = requests.Session()
base_url = config.get('Tanium', 'url').strip("'")
username = config.get('Tanium', 'username').strip("'")
password = config.get('Tanium', 'password').strip("'")
domain = ''

def authentication():
    header = {'Content-Type': 'application/octet-stream', 'cache-control': 'no-cache'}
    data = "{\n  \"username\" : \"" + username + "\",\n    \"password\" : \"" + password + "\",\n    \"Domain\": \"" + domain + "\"\n}"
    url = '{}/api/v2/session/login'.format(base_url)
    get_auth_token = request.post(url, headers=header, data=data, verify=False)
    json_token = get_auth_token.json()
    global token
    token = json_token['data']['session']

def results_asked_question(id):
	header = {'Content-Type': 'application/json', 'cache-control': 'no-cache', 'session': '{}'.format(token)}
	url = '{0}/api/v2/result_data/question/{1}?include_hashes_flag=1'.format(base_url,id)
	question_result = request.post(url, headers=header, verify=False)
	question_result = question_result.json()
	print(json.dumps(question_result, indent=4))


def ask_question():
	header = {'Content-Type': 'application/octet-stream', 'cache-control': 'no-cache', 'session': '{}'.format(token)}
	url = '{}/api/v2/questions'.format(base_url)
	question = 'Get Sample Sensor from all machines'
	question_query = request.post(url, headers=header, json=question, verify=False)
	question_query = question_query.json()
	question_id = question_query['data']['id']
	time.sleep(30)
	results_asked_question(question_id)


authentication()
ask_question()
