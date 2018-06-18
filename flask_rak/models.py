import json
import aniso8601

from .core import session


class _Field(dict):
    """Container to represent Rogo Speaker Request Data.
    Initialized with request_json and creates a dict object with attributes
    to be accessed via dot notation or as a dict key-value.
    Parameters within the request_json that contain their data as a json object
    are also represented as a _Field object.
    Example:
    payload_object = _Field(rogo_json_payload)
    request_type_from_keys = payload_object['request']['type']
    request_type_from_attrs = payload_object.request.type
    assert request_type_from_keys == request_type_from_attrs
    """

    def __init__(self, request_json={}):
        super(_Field, self).__init__(request_json)
        for key, value in request_json.items():
            if isinstance(value, dict):
                value = _Field(value)
            self[key] = value

    def __getattr__(self, attr):
        # converts timestamp str to datetime.datetime object
        if 'timestamp' in attr:
            return aniso8601.parse_datetime(self.get(attr))
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)


class _Response(object):
    '''
    {
        "data": {
                "version": "1.0",
                "response" {
                        "speech": {
                                "type": "raw",
                                "value": "string"
                        },
                        "reprompt": {
                                "speech": {
                                        "type": "raw",
                                        "value": "string"
                                }
                        },
                        "action": {
                                "audio": {
                                        "interface": "new"
                                        "sources": []
                                }
                        }
                },
                "attributes": {
                        "state": "state": "_COMMANDMODE"

                }
        }
    }
    '''

    def __init__(self, speech):
        self._json_default = None
        self._response = {
            'speech': {'type': 'raw', 'value': speech}
        }

    def render_response(self):
        response_wrapper = {
            'version': '1.0',
            'response': self._response,
            'attributes': session.attributes
        }
        return json.dumps(response_wrapper)


class statement(_Response):
    def __init__(self, speech):
        super(statement, self).__init__(speech)
        self._response['shouldEndSession'] = True


class audio(_Response):
    """Returns a response object with an AudioPlayer Directive.
    Responses for LaunchRequests and IntentRequests may include outputSpeech in addition to an audio directive
    Note that responses to AudioPlayer requests do not allow outputSpeech.
    @ask.intent('NewFooAudioIntent')
    def new_foo_audio():
        speech = 'playing from foo'
        stream_urls = ['www.foo.com']
        return audio(speech).new(stream_urls)
    @ask.intent('PauseIntent')
    def stop_audio():
        return audio('Ok, stopping the audio').pause()
    """

    def __init__(self, speech=''):
        super(audio, self).__init__(speech)
        if not speech:
            self._response = {}
        self._response['action'] = {}
        self._response['action']['audio'] = {}

    def new(self, sources):
        """Sends a Play Directive to begin playback and replace current and enqueued streams."""
        self._response['shouldEndSession'] = True
        self._response['action']['audio']['interface'] = 'new'
        self._response['action']['audio']['sources'] = sources
        return self

    def stop(self):
        """Send signal to stop the current stream playback"""
        self._response['shouldEndSession'] = True
        self._response['action']['audio']['interface'] = 'stop'
        self._response['action']['audio']['sources'] = []
        return self

    def play(self):
        """Send signal to resume playback at the paused offset"""
        self._response['shouldEndSession'] = True
        self._response['action']['audio']['interface'] = 'play'
        self._response['action']['audio']['sources'] = []
        return self

    def pause(self):
        """Send signal to resume playback at the paused offset"""
        self._response['shouldEndSession'] = True
        self._response['action']['audio']['interface'] = 'pause'
        self._response['action']['audio']['sources'] = []
        return self

    def next(self):
        """Send signal to resume playback at the paused offset"""
        self._response['shouldEndSession'] = True
        self._response['action']['audio']['interface'] = 'next'
        self._response['action']['audio']['sources'] = []
        return self
