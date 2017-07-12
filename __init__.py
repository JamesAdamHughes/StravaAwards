from  flask import Flask, request
from server.routes import stravaRoute
from server.CustomJSONEncoder import CustomJSONEncoder
from StravaAwards.service import ConfigService
import os

app = Flask('server')
app.json_encoder = CustomJSONEncoder
app.register_blueprint(stravaRoute)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

ConfigService.read(ROOT_DIR + '/config.cfg')
ConfigService.addSectionAndValue('production','test', 1) 

print 'root dir: ' + ROOT_DIR
if __name__ == "__main__":
    app.run()
# run threaded so that we can handle multiple requests (for subscription events)
# app.run(threaded=True)

print '[main] server running at :5000'
