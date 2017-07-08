from flask import Flask, request
from stravalib.client import Client
import json
import os 
import requests
from routes import stravaRoute

app = Flask('Server')
app.register_blueprint(stravaRoute)
print '[server] server running at :5000'

# client = Client()
# print 'doing sub...'
# print client.create_subscription(client_id=15341, client_secret='f7e5bc402cb53885ee0c4d445d4e84036fe2a651', callback_url='http://127.0.0.1:5000/strava/callback')
# print 'done subscription'
# authorize_url = client.authorization_url(client_id=15341, redirect_uri='http://127.0.0.1:5000/authorized', approval_prompt='force', scope='view_private,write')
# print authorize_url