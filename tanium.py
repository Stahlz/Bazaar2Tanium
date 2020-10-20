from requests import Session
import configparser

"""Configparser setup"""
configfilepath = './config.py'
config = configparser.ConfigParser()
config.read(configfilepath)

global request,url,username,password
request = requests.Session()
url = config.get('Tanium', 'url')
username = config.get('Tanium', 'username')
password = config.get('Tanium', 'password')


def create_api_token():
