from flask import Flask, request
from stravalib.client import Client
import json
import os 
import requests



@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/strava/callback', methods=['POST', 'GET'])
def stravaCallback():
    print 'strava callback'
    return 'Hello, World'

@app.route('/authorized', methods=['GET', 'POST'])
def authorized():

    code = request.values.get('code')

    print "code: " , code

    access_token = client.exchange_code_for_token(client_id=15341, client_secret='f7e5bc402cb53885ee0c4d445d4e84036fe2a651', code=code)
    print "access Token: " + str(access_token)

    return 'Authorised: ' + str(access_token)

@app.route('/start', methods=['GET'])
def start():
    
    print 'hello'
    
    print 'done subscription'


def getPublicUrl():
    a = os.popen("curl  http://localhost:4041/api/tunnels > tunnels.json").read()  

    with open('tunnels.json') as data_file:    
        datajson = json.load(data_file)
    for i in datajson['tunnels']:
        public_url = i['public_url']  
    print 'Public Url: ' + public_url
    return public_url

app = Flask('main')

# client = Client()
# print 'doing sub...'
# print client.create_subscription(client_id=15341, client_secret='f7e5bc402cb53885ee0c4d445d4e84036fe2a651', callback_url='http://127.0.0.1:5000/strava/callback')
# print 'done subscription'
# authorize_url = client.authorization_url(client_id=15341, redirect_uri='http://127.0.0.1:5000/authorized', approval_prompt='force', scope='view_private,write')
# print authorize_url