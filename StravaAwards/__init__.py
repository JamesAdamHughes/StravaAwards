from flask import Flask, request

print '[init] starting application'

app = Flask(__name__)

from server.routes import stravaRoute
from  server.CustomJSONEncoder import CustomJSONEncoder
from  service import ConfigService
import definitions

app.json_encoder = CustomJSONEncoder
app.register_blueprint(stravaRoute)

#Load the config file for the enviroment
ConfigService.read(definitions.ROOT_DIR + '/config.cfg')

# app.run()

if __name__ == "__main__":
    # This doesn't get run by flask
    print '[main] server running at :5000'
    app.run(threaded=True)

