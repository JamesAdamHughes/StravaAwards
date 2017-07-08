import Server
import 

def subscribe(client):
    print 'doing subscription...'

    client = Client()
    callbackUrl = getPublicUrl()

    print client.create_subscription(client_id=15341, client_secret='', callback_url=callbackUrl)

 
def getPublicUrl():
    a = os.popen("curl  http://localhost:4041/api/tunnels > tunnels.json").read()  

    with open('tunnels.json') as data_file:    
        datajson = json.load(data_file)
    for i in datajson['tunnels']:
        public_url = i['public_url']  
    print 'Public Url: ' + public_url

    return public_url