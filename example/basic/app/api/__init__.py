#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify

api = Blueprint('api', __name__)

from flask_rak import RAK, session, context, audio, statement

rak = RAK(api, '/weather')


@rak.launch
def launch(data):
    '''
    data: Type _Field
    '''
    print 'launch: ', data
    return "helllo"

@rak.intent('weather')
def weather(city):
    speech_text = "weather in %s" % city
    return statement(speech_text)

@rak.intent('new_audio')
def new_audio(name):
    speech_text = "chơi bài " + name
    sources = ['link_to_audio_file']
    return audio(speech_text).new(sources)
