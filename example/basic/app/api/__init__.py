#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify

api = Blueprint('api', __name__)

from flask_rak import RAK, statement


APP_NAME = 'weather'
weather_app = RAK(
    app_name=APP_NAME,
    app=api,
    route='/weather'
)


@weather_app.launch
def launch(data):
    '''
    data: Type _Field
    '''
    print 'launch: ', data
    return statement(APP_NAME, "helllo")

@weather_app.intent('weather')
def weather(city):
    speech_text = "weather in %s" % city
    return statement(APP_NAME, speech_text)
