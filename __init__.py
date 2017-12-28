import logging
from flask import Flask, request
from StravaAwards.server.middleware import middleware
from StravaAwards.server.routes import stravaRoute
from  StravaAwards.server.CustomJSONEncoder import CustomJSONEncoder
from  StravaAwards.service import ConfigService
import StravaAwards.definitions

print '[init] starting application'

app = Flask(__name__)
app.wsgi_app = middleware.LoggingMiddleware(app.wsgi_app)

app.logger.info('[init] after flask setup')
app.json_encoder = CustomJSONEncoder
app.register_blueprint(stravaRoute)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)


#Load the config file for the enviroment
ConfigService.read(StravaAwards.definitions.ROOT_DIR + '/config.cfg')


if __name__ == "__main__":
    # This doesn't get run by flask
    print '[main] server running at :5000'
    app.run(threaded=True)

