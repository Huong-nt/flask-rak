#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify

weather_blueprint = Blueprint('api', __name__)

from flask_rak import RAK, statement, question


weather_app = RAK(
    app=weather_blueprint,
    route='/'
)


@weather_app.launch
def launch(data):
    '''
    data: Type _Field
    '''
    print 'launch: ', data
    return statement("helllo")

@weather_app.intent('weather')
def weather(city):
    speech_text = "weather in %s" % city['value']
    return statement(speech_text)


@weather_app.intent('ask_city')
def ask_city():
    speech_text = "Bạn muốn nghe thời tiết ở thành phố nào"
    reprompt_text = "Hãy nói tên 1 thành phố"
    return question(speech_text).reprompt(reprompt_text)