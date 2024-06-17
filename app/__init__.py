import logging
import os

from flask import Flask
from flask_cors import CORS
from flask_basicauth import BasicAuth

from config.constants import CONFIG_NAME_MAPPER


def create_app():
    env_config =  os.getenv('ENV_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_pyfile(CONFIG_NAME_MAPPER[env_config])

    if env_config == 'production':
        app.config['BASIC_AUTH_USERNAME'] = os.getenv('BASIC_AUTH_USERNAME', 'test')
        app.config['BASIC_AUTH_PASSWORD'] = os.getenv('BASIC_AUTH_PASSWORD', 'password')
        app.config['BASIC_AUTH_REALM'] = "Authorization Required!!"
        CORS(app, reousrces={r'/api/*': {"origins": app.config['CORS_ORIGIN']}})

    # Set logger
    logging.getLogger('flask_cors').level = logging.DEBUG
    logging.basicConfig(format=app.config['LOGGER_FORMAT'], level=app.config['LOGGER_LEVEL'])
    basic_auth = BasicAuth(app)

    from app.api import api
    api.init_app(app)
    return app


app = create_app()
