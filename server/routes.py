import flask
from flask import jsonify, request
from service import AwardManager, emailUtilities, ActivityManager
import json

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

@stravaRoute.route('/award/list/<user_id>/<date>', methods=['GET'])
def award_list(user_id, date):
    """
    Returns a JSON of all awards a user has won on a given date
    Also send an email to the user for each award they have won
    """
    valid_awards = []

    for award in AwardManager.createAwards():
        occured = AwardManager.test_award_occured(award, user_id)
        if occured:
            # save award to db, send email
            AwardManager.save_award(award, user_id)

            valid_awards.append(award.serialize())
            print award.getAwardText()
            print 'Sending Email...'
            emailUtilities.send_email(award.name, award.getAwardText(), test=1)
        print '\n'

    return jsonify(valid_awards)

@stravaRoute.route('/strava/callback', methods=['POST', 'GET'])
def stravaCallback():

    if request.method == 'GET':
        hubChallangeToken = request.args.get('hub.challenge')
        print '[server] strava subscription verify callback token: ' + hubChallangeToken

        res = {
            'hub.challenge': hubChallangeToken
        }

        return jsonify(res)
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