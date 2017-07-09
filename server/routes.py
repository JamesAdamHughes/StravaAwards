import flask
from flask import jsonify, request
from service import AwardManager, emailUtilities, ActivityManager
import json
import arrow

import sys
# print sys.path
# Add the workspace folder path to the sys.path list
# sys.path.append('/path/to/workspace/')

stravaRoute = flask.Blueprint('simple_page', __name__, template_folder='templates')

@stravaRoute.route('/')
def hello_world():
    return 'Hello, World!'

@stravaRoute.route('/')
def index():
    return 'Index Page'

@stravaRoute.route('/activity/load/<user_id>', methods=['GET'])
@stravaRoute.route('/activity/load/<user_id>/<from_date>', methods=['GET'])
def activity_load(user_id, from_date="2016-01-01"):
    """
    Returns a list of all a users activites from the from date
    These are also saved to the DB if not already saved
    """
    from_date = str(from_date)
    acts = ActivityManager.get_and_save_actvites_from_api(from_date)
    acts = [ activity.serialize() for activity in acts]
    return jsonify(acts)

@stravaRoute.route('/award/list/<user_id>', methods=['GET'])
def award_list(user_id):
    """
    Returns a JSON of all awards a user has won on a given date
    Also send an email to the user for each award they have won
    """
    res = {
        "ok": True,
        "awards" : []
    }

    date = request.args.get('date')
    onlyNew = request.args.get('onlyNew')

    if date is None:
        date = arrow.now().format("YYYY-M-D")
    
    if onlyNew is None or onlyNew == 'true':
        onlyNew = True
    elif onlyNew == 'false':
        onlyNew = False

    new_awards = AwardManager.get_new_awards_for_user(user_id, date, onlyNew)

    for award in new_awards:
        emailUtilities.send_email(award.name, award.getAwardText(), test=1)
        res["awards"].append(award.serialize())

    res["numberAwards"] = len(res["awards"])
    res["onlyNew"] = onlyNew

    return jsonify(res)

@stravaRoute.route('/strava/callback', methods=['POST', 'GET'])
def stravaCallback():

    if request.method == 'GET':
        hubChallangeToken = request.args.get('hub.challenge')
        print '[server] strava subscription verify callback token: ' + hubChallangeToken

        res = {
            'hub.challenge': hubChallangeToken
        }

    elif request.method == 'POST':
        data = request.data
        dataDict = json.loads(data)
        print dataDict
        res = {
            'ok': True
        }
    
    return jsonify(res)

@stravaRoute.route('/authorized', methods=['GET', 'POST'])
def authorized():

    code = request.values.get('code')

    print "code: " , code

    # access_token = client.exchange_code_for_token(client_id=15341, client_secret='f7e5bc402cb53885ee0c4d445d4e84036fe2a651', code=code)
    # print "access Token: " + str(access_token)

    # return 'Authorised: ' + str(access_token)

@stravaRoute.route('/start', methods=['GET'])
def start():
    
    print 'hello'
    
    print 'done subscription'