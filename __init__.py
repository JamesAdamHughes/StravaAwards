from  flask import Flask, request
from server.routes import stravaRoute
from server.CustomJSONEncoder import CustomJSONEncoder
from StravaAwards.service import ConfigService
import os
from StravaAwards import definitions

app = Flask('server')
app.json_encoder = CustomJSONEncoder
app.register_blueprint(stravaRoute)

#Load the config file for the enviroment
ConfigService.read(definitions.ROOT_DIR + '/config.cfg')

print '[init] root dir: ' + definitions.ROOT_DIR
if __name__ == "__main__":
    print '[main] server running at :5000'
    app.run()

