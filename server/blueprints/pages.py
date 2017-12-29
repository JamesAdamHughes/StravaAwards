import flask
from flask import jsonify, request, current_app
from StravaAwards.service import ConfigService

pageRoutes = flask.Blueprint('pages', __name__, template_folder='../templates', static_folder='../client/static')


@pageRoutes.route('/')
def index():
    current_app.logger.info( 'index')
    return 'Hello, World! Watch this space for my Strava App web interface!'

@pageRoutes.route('/home')
def home():
    current_app.logger.info( 'index')
    return pageRoutes.send_static_file('home.html')

@pageRoutes.route('/register', methods=['GET'])
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
        'redirect_uri' : ConfigService.getConfigVar('hostname') + '/api/strava/exchange'
    })