from  flask import Flask, request
from server.routes import stravaRoute
from server.CustomJSONEncoder import CustomJSONEncoder
from StravaAwards.service import ConfigService
import os
from StravaAwards import definitions

app = Flask('server')
app.json_encoder = CustomJSONEncoder
app.register_blueprint(stravaRoute)

ConfigService.read(definitions.ROOT_DIR + '/config.cfg')
ConfigService.addSectionAndValue('production','test', 1) 

print 'root dir: ' + definitions.ROOT_DIR
if __name__ == "__main__":
    app.run()
# run threaded so that we can handle multiple requests (for subscription events)
# app.run(threaded=True)

print '[main] server running at :5000'
