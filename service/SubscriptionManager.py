from stravalib.client import Client
import ConfigService
import os
import json

def subscribe():
    print '[subscribeM] doing subscription...'

    client = Client()
    callbackUrl = getPublicUrl() + '/strava/callback'
    client_secret = ConfigService.getConfigVar('strava.client_secret')
    client_id = ConfigService.getConfigVar('strava.client_id')
    print "callback url: " + callbackUrl
    print client.create_subscription(client_id=client_id, client_secret=client_secret, callback_url=callbackUrl)
    return
 
def getPublicUrl():
    a = os.popen("curl  http://localhost:4041/api/tunnels > tunnels.json").read()  

    with open('tunnels.json') as data_file:    
        datajson = json.load(data_file)
    for i in datajson['tunnels']:
        public_url = i['public_url']  

    return public_url