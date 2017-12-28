import json
import flask
import requests
from flask import jsonify, request, current_app
from StravaAwards.service import AwardManager, emailUtilities, ActivityManager, SubscriptionManager, UserManager, ConfigService
import arrow

stravaRoute = flask.Blueprint('strava', __name__, template_folder='templates')

trueisms = ('true', '1', 'True')
falseism = ('false', '0', 'False')

@stravaRoute.route('/')
def hello_world():
    current_app.logger.info( 'index')
    return 'Hello, World! Watch this space for my Strava App web interface!'

@stravaRoute.route('/register', methods=['GET'])
def register():
    """
    Shows a page allowing the user to register to use the site

    This page starts the authorisation process
    """
    # Show auth page to user with link to strava auth url
    # Add app details to auth url

    return flask.render_template('strava/register.html', auth = {
        'client_id' : ConfigService.getConfigVar('strava.client_id'),
        'response_type': 'code',
        'redirect_uri' : ConfigService.getConfigVar('hostname') + '/strava/exchange'
    })

@stravaRoute.route('/strava/exchange', methods=['GET'])
def strava_exchange():
    """
    Callback from the user auth call

    Makes a POST to strava to complete the auth process, this also returns user data

    Add this user data to the db TODO redirect user to home page and set cookie
    """

    current_app.logger.info("Got following code: " + request.args.get('code'))

    res = requests.post('https://www.strava.com/oauth/token', data={
        'client_id': ConfigService.getConfigVar('strava.client_id'),
        'client_secret' : ConfigService.getConfigVar('strava.client_secret'),
        'code' : request.args.get('code')
        })
    
    result = UserManager.add_user(res.json())  
    response = {
        'message': ''
    }

    current_app.logger.info('got this far looool')

    if result['ok']:
        try:
            # If we have added the user, then subscribe them to webhook events
            subscribe_user(str(result['user'].strava_id))
            
            response['user'] = result['user'].__dict__
            response['message'] = "Thanks {0}, we've now authed your account. Now get out there running!".format(result['user'].f_name)
        except Exception:
            response['message'] = "An error occured: subscribing to activity events"
    else:
        response['message'] = "An error occured: {0}".format(result['message'])
    
    return jsonify(response)


@stravaRoute.route('/activity/load/<user_id>', methods=['GET'])
@stravaRoute.route('/activity/load/<user_id>/<from_date>', methods=['GET'])
def activity_load(user_id, from_date="2016-01-01"):
    """
    Returns a list of all a users activites from the from date
    These are also saved to the DB if not already saved
    """
    from_date = str(from_date)
    acts = ActivityManager.get_and_save_actvites_from_api(user_id=user_id, after_date=from_date)
    
    if acts:
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
    only_new = request.args.get('onlyNew')
    email = request.args.get('email')

    # Check extra params to modify the behaviour of call
    if date is None:
        date = arrow.now().format("YYYY-MM-DD HH:mm:ss")

    if email is None or email in trueisms:
        email = True
    elif email in falseism:
        email = False

    if only_new is None or only_new in trueisms:
        only_new = True
    elif only_new in falseism:
        only_new = False
    
    new_awards = AwardManager.get_new_awards_for_user(user_id, date, only_new)
    email_sent = False

    # Send the user an email of the awards they have recieved
    if len(new_awards) > 0 and email:
        email_sent = AwardManager.award_user(user_id, new_awards)

    for award in new_awards:
        res["awards"].append(award.serialize())

    res["number_awards"] = len(res["awards"])
    res["only_new"] = only_new
    res["now_date"] = date
    res["email_sent"] = email_sent

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
        current_app.logger.info( '[server] strava subscription verify callback token: ' + hubChallangeToken)

        res = {
            'hub.challenge': hubChallangeToken
        }

    elif request.method == 'POST':
        res = {
            'ok': True,
            "awards" : []
        }

        data_dict = json.loads(request.data)
        user_id = data_dict['owner_id']
        current_app.logger.info( "[server] Subscripton: User uploaded activity " + str(data_dict))

        # Load the users activity data again
        ActivityManager.get_and_save_actvites_from_api(user_id)

        new_awards = AwardManager.get_new_awards_for_user(
            user_id, 
            arrow.now().replace(hours=-1).format("YYYY-MM-DD HH:mm:ss"))
        
        AwardManager.award_user(1, new_awards)
        
        for award in new_awards:            
            res["awards"].append(award.serialize())
        
        res["numberAwards"] = len(res["awards"])
        
    return jsonify(res)

@stravaRoute.route('/authorized', methods=['GET', 'POST'])
def authorized():
    current_app.logger.info('authorized')
    code = request.values.get('code')

    current_app.logger.info("code: " + code)

@stravaRoute.route('/strava/subscribe/<user_id>', methods=['GET'])
def subscribe_user(user_id):    
    current_app.logger.info('/strava/subscribe')
    current_app.logger.info('[server] subscribing to user events')
    SubscriptionManager.subscribe(user_id)
    current_app.logger.info('[server] done subscription')

    return jsonify({
        "ok": True,
        "subscribe_user": user_id
    })
    

@stravaRoute.route('/mail', methods=['GET'])
def mail():
    current_app.logger.info('[routes] sending mail endpoint')

    text = """<br/>
    this is a body. <br/> There was a break. 
    <ul>
    <li>this is a list</li>
    <li>And you also get this won <b>woooo</b></li>
    </ul>
    """

    success = emailUtilities.send_email(subject="Testing mail endpoint", body=text)

    return jsonify({
        "ok": success
    })
