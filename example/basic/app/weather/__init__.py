#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify

weather_blueprint = Blueprint('api', __name__)

from flask_rak import RAK, session, context, statement, question, dialog


weather_app = RAK(
    app=weather_blueprint,
    route='/'
)


@weather_app.launch
def launch(data):
    '''
    data: Type _Field
    '''
    print('launch: ', data)
    print('session: ', session)
    return statement("helllo")

@weather_app.intent('weather')
def weather(city):
    if city is None:
        # dialog to get city value
        return dialog(
            speech="Bạn muốn biết thời tiết ở thành phố nào?",
            dialog_type='PREDICT',
            updated_context={
                'state': 'INPROGRESS',
                'expectEntity': ['city'],
                'intent': context.intent,
                'entities': context.entities
            }
        )

    speech_text = "weather in %s" % city['value']
    return statement(speech_text)

