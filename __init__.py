from flask import Flask, request

print '[init] starting application'

app = Flask(__name__)

print '[init] after flask setip'

from server.routes import stravaRoute
from  server.CustomJSONEncoder import CustomJSONEncoder
from  service import ConfigService
import definitions
import logging

app.json_encoder = CustomJSONEncoder
app.register_blueprint(stravaRoute)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)

app.logger.info('Log message')

app.logger.debug('Log message')
app.logger.warn('Log message')

#Load the config file for the enviroment
ConfigService.read(definitions.ROOT_DIR + '/config.cfg')

# app.run()

if __name__ == "__main__":
    # This doesn't get run by flask
    print '[main] server running at :5000'
    app.run(threaded=True)

