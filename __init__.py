import logging
from flask import Flask, request
from StravaAwards.server.middleware import middleware
from StravaAwards.server.blueprints.api import apiRoutes
from StravaAwards.server.blueprints.pages import pageRoutes
from  StravaAwards.server.CustomJSONEncoder import CustomJSONEncoder
from  StravaAwards.service import ConfigService
import StravaAwards.definitions

print '[init] starting application'

# Middleware
app = Flask(__name__)
app.wsgi_app = middleware.LoggingMiddleware(app.wsgi_app)

# Custom modules
app.logger.info('[init] after flask setup')
app.json_encoder = CustomJSONEncoder

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)

app.config['TEMPLATES_AUTO_RELOAD'] = True

# Blueprints
app.register_blueprint(pageRoutes)
app.register_blueprint(apiRoutes, url_prefix="/api")

#Load the config file for the enviroment
ConfigService.read(StravaAwards.definitions.ROOT_DIR + '/config.cfg')


if __name__ == "__main__":
    # This doesn't get run by flask or gunicorn 
    print '[main] server running at :5000'
    app.run(threaded=True)

