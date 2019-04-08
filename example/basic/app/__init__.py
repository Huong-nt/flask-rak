from flask import Flask
from config import config

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from weather import weather_blueprint
    app.register_blueprint(weather_blueprint, url_prefix='/api/weather/v1')

    # more app here
    # alert, music,...
    return app
