import flask
from flask import jsonify, request
from StravaAwards.service import AwardManager, emailUtilities, ActivityManager, SubscriptionManager
import json
import arrow

import sys
# print sys.path
# Add the workspace folder path to the sys.path list
# sys.path.append('/path/to/workspace/')

stravaRoute = flask.Blueprint('simple_page', __name__, template_folder='templates')

@stravaRoute.route('/')
def hello_world():
    return 'Hello, World! Watch this space for my Strava App web interface!'

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
        date = arrow.now().format("YYYY-MM-DD HH:mm:ss")
    
    if onlyNew is None or onlyNew == 'true':
        onlyNew = True
    elif onlyNew == 'false':
        onlyNew = False
    
    new_awards = AwardManager.get_new_awards_for_user(user_id, date, onlyNew)
    for award in new_awards:
        emailUtilities.send_email(award.name, award.getAwardText())
        res["awards"].append(award.serialize())

    res["numberAwards"] = len(res["awards"])
    res["onlyNew"] = onlyNew
    res["now_date"] = date

    return jsonify(res)

@stravaRoute.route('/strava/callback', methods=['POST', 'GET'])
def stravaCallback():
    """
    Endpoint handles strava subscriptions
    GET 
        The callback verification for subscribing to events
    POST 
        Called when user uploads an activity
        Need to get the users activites again and re-do award logic

        todo use the activity id to get user id, and call their info again
    """

    if request.method == 'GET':
        hubChallangeToken = request.args.get('hub.challenge')
        print '[server] strava subscription verify callback token: ' + hubChallangeToken

        res = {
            'hub.challenge': hubChallangeToken
        }

    elif request.method == 'POST':
        res = {
            'ok': True,
            "awards" : []
        }

        data_dict = json.loads(request.data)
        print "[server] Subscripton: User uploaded activity " + str(data_dict)

        # Load the users activity data again
        ActivityManager.get_and_save_actvites_from_api()

        new_awards = AwardManager.get_new_awards_for_user(1, 
            arrow.now().replace(hours=-1).format("YYYY-MM-DD HH:mm:ss"))
        for award in new_awards:            
            emailUtilities.send_email(award.name, award.getAwardText())
            res["awards"].append(award.serialize())
        
        res["numberAwards"] = len(res["awards"])
        
    return jsonify(res)

@stravaRoute.route('/authorized', methods=['GET', 'POST'])
def authorized():

    code = request.values.get('code')

    print "code: " , code

    # print "access Token: " + str(access_token)

    # return 'Authorised: ' + str(access_token)

@stravaRoute.route('/strava/subscribe/<user_id>', methods=['GET'])
def subscribe_user(user_id):    

    print '[server] subscribing to user events'
    SubscriptionManager.subscribe()
    print '[server] done subscription'

    return jsonify({
        "ok": True,
        "subscribe_user": user_id
    })
    
