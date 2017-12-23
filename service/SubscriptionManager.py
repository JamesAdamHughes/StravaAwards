from stravalib.client import Client
from StravaAwards.service import ConfigService
import os
import json

def subscribe(user_token):
    print '[subscribeM] doing subscription...'

    client = Client()
    callback_url = getPublicUrl() + '/strava/callback'
    print "callback url: " + callback_url
    print user_token
    print client.create_subscription(
        client_id=ConfigService.getConfigVar('strava.client_id'),
        client_secret=ConfigService.getConfigVar('strava.client_secret'),
        callback_url=callback_url
    )

    return
 
def getPublicUrl():
    enviroment = os.getenv('ENVIROMENT')
    print enviroment
    if enviroment == 'development':
        a = os.popen("curl  http://localhost:4040/api/tunnels > tunnels.json").read()  

        with open('tunnels.json') as data_file:    
            datajson = json.load(data_file)
        for i in datajson['tunnels']:
            public_url = i['public_url']  

        return public_url
    else:
        return 'http://' + ConfigService.getConfigVar('hostname')