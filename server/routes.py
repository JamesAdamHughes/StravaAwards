import flask
from flask import jsonify, request

stravaRoute = flask.Blueprint('simple_page', __name__, template_folder='templates')

@stravaRoute.route('/')
def hello_world():
    return 'Hello, World!'

@stravaRoute.route('/')
def index():
    return 'Index Page'

@stravaRoute.route('/hello')
def hello():
    return 'Hello, World'

@stravaRoute.route('/strava/callback', methods=['POST', 'GET'])
def stravaCallback():

    if request.method == 'GET':
        hubChallangeToken = request.args.get('hub.challenge') 
        
        print '[server] strava subscription verify callback token: ' + hubChallangeToken

        res = {
            'hub.challenge': hubChallangeToken
        }

        return jsonify(res)
    else if request.method == 'POST':
        

@stravaRoute.route('/authorized', methods=['GET', 'POST'])
def authorized():

    code = request.values.get('code')

    print "code: " , code

    access_token = client.exchange_code_for_token(client_id=15341, client_secret='f7e5bc402cb53885ee0c4d445d4e84036fe2a651', code=code)
    print "access Token: " + str(access_token)

    return 'Authorised: ' + str(access_token)

@stravaRoute.route('/start', methods=['GET'])
def start():
    
    print 'hello'
    
    print 'done subscription'