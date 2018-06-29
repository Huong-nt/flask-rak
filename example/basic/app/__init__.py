from flask import Flask
from config import config

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from api import api as api_weather
    app.register_blueprint(api_weather, url_prefix='/api/v1')

    return app
