from stravalib.client import Client
from pprint import pprint
import arrow
from service import AwardManager, ActivityManager, emailUtilities, ConfigService, SubscriptionManager
from service.StravaConsistancyAward import StravaConsistancyAward
import subprocess
from flask import Flask, request
from server.routes import stravaRoute
from server.CustomJSONEncoder import CustomJSONEncoder

app = Flask('server')
app.json_encoder = CustomJSONEncoder
app.register_blueprint(stravaRoute)
print '[server] server running at :5000'

