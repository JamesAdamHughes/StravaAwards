from stravalib.client import Client
from pprint import pprint
import arrow
from StravaAwards.service import SubscriptionManager
from flask import Flask, request
from server.routes import stravaRoute
from server.CustomJSONEncoder import CustomJSONEncoder

app = Flask('server')
app.json_encoder = CustomJSONEncoder
app.register_blueprint(stravaRoute)

if __name__ == "__main__":
    app.run()

# run threaded so that we can handle multiple requests (for subscription events)
# app.run(threaded=True)

print '[main] server running at :5000'



