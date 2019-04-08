#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import inspect
import types
from functools import wraps, partial, update_wrapper

from werkzeug.contrib.cache import SimpleCache
from werkzeug.local import LocalProxy, LocalStack
from flask import current_app, json, request as flask_request, _app_ctx_stack
from . import logger


def copy_func(f, name=None):
    """Based on https://stackoverflow.com/a/30714299 (Aaron Hall)"""
    '''
    return a function with same code, globals, defaults, closure, and 
    name (or provide a new name)
    '''
    fn = types.FunctionType(f.__code__, f.__globals__, name or f.__name__,
                            f.__defaults__, f.__closure__)
    # in case f was given attrs (note this dict is a shallow copy):
    fn.__dict__.update(f.__dict__)
    return fn


def find_rak():
    """
    Find our instance of Rak, navigating Local's and possible blueprints.
    """
    if hasattr(current_app, 'rak'):
        return getattr(current_app, 'rak')
    else:
        if hasattr(current_app, 'blueprints'):
            blueprints = getattr(current_app, 'blueprints')
            for blueprint_name in blueprints:
                if hasattr(blueprints[blueprint_name], 'rak'):
                    return getattr(blueprints[blueprint_name], 'rak')


def dbgdump(obj, default=None, cls=None):
    if current_app.config.get('RAK_PRETTY_DEBUG_LOGS', False):
        indent = 2
    else:
        indent = None
    msg = json.dumps(obj, indent=indent, default=default, cls=cls)
    logger.debug(msg)


request = LocalProxy(lambda: find_rak().request)
session = LocalProxy(lambda: find_rak().session)
version = LocalProxy(lambda: find_rak().version)
context = LocalProxy(lambda: find_rak().context)

from . import models


class RAK(object):

    _intent_view_funcs = {}
    _launch_view_func = None
    _default_intent_view_func = None

    def __init__(self, app=None, route=None, blueprint=None):
        self.app = app
        self._route = route

        self._view_name = '_flask_view_func_'
        tmp_view_func = copy_func(self._flask_view_func)
        tmp_view_func.__name__ = self._view_name
        self.addMethod(tmp_view_func)

        if app is not None:
            self.init_app(app)
        elif blueprint is not None:
            self.init_blueprint(blueprint)

    @classmethod
    def removeVariable(cls, name):
        return delattr(cls, name)

    @classmethod
    def addMethod(cls, func):
        return setattr(cls, func.__name__, types.MethodType(func, cls))

    def init_app(self, app):
        """Initializes Ask app by setting configuration variables and maps RAK route to a flask view.
        The RAK instance is given the following configuration variables by calling on Flask's configuration:

        """
        if self._route is None:
            raise TypeError(
                "route is a required argument when app is not None")

        app.rak = self
        app.add_url_rule(self._route, view_func=getattr(self, self._view_name), methods=['POST'])

    def init_blueprint(self, blueprint):
        """Initialize a Flask Blueprint, similar to init_app, but without the access
        to the application config.
        Keyword Arguments:
            blueprint {Flask Blueprint} -- Flask Blueprint instance to initialize (Default: {None})
        """
        if self._route is not None:
            raise TypeError("route cannot be set when using blueprints!")

        blueprint.rak = self
        blueprint.add_url_rule("", view_func=getattr(self, self._view_name), methods=['POST'])

    @property
    def session(self):
        return getattr(_app_ctx_stack.top, '_rak_session', models._Field())

    @session.setter
    def session(self, value):
        setattr(_app_ctx_stack.top, '_rak_session', value)

    @property
    def version(self):
        return getattr(_app_ctx_stack.top, '_rak_version', None)

    @version.setter
    def version(self, value):
        setattr(_app_ctx_stack.top, '_rak_version', value)

    @property
    def context(self):
        return getattr(_app_ctx_stack.top, '_rak_context', None)

    @context.setter
    def context(self, value):
        setattr(_app_ctx_stack.top, '_rak_context', value)

    @classmethod
    def launch(self, f):
        """Decorator maps a view function as the endpoint for an LaunchRequest and starts the app.
        @ask.launch
        def launched():
            return question('Welcome to Foo')
        The wrapped function is registered as the launch view function and renders the response
        for requests to the Launch URL.
        Arguments:
            f {function} -- Launch view function
        """
        self._launch_view_func = f

        @wraps(f)
        def wrapper(*args, **kw):
            self._flask_view_func(*args, **kw)
        return f

    @classmethod
    def intent(self, intent_name):
        """Decorator routes an Rogo IntentRequest.
        Functions decorated as an intent are registered as the view function for the Intent's URL,
        and provide the backend responses to give your Skill its functionality.
        @ask.intent('WeatherIntent')
        def weather(city):
            return statement('I predict great weather for {}'.format(city))
        Arguments:
            intent_name {str} -- Name of the intent request to be mapped to the decorated function
        """
        def decorator(f):
            self._intent_view_funcs[intent_name] = f

            @wraps(f)
            def wrapper(*args, **kw):
                self._flask_view_func(*args, **kw)
            return f
        return decorator

    @classmethod
    def default_intent(self, f):
        """Decorator routes any Rogo IntentRequest that is not matched by any existing intent routing."""
        self._default_intent_view_func = f

        @wraps(f)
        def wrapper(*args, **kw):
            self._flask_view_func(*args, **kw)
        return f

    @classmethod
    def _rogo_request(self):
        raw_body = flask_request.data
        rogo_request_payload = json.loads(raw_body)
        return rogo_request_payload

    def _flask_view_func(self, *args, **kwargs):
        rak_payload = self._rogo_request()
        dbgdump(rak_payload)
        request_body = models._Field(rak_payload)

        self.version = request_body.version
        self.context = getattr(request_body, 'context', models._Field())
        # to keep old session.attributes through AudioRequests
        self.session = getattr(request_body, 'session', self.session)

        if not self.session:
            self.session = models._Field()
        if not self.session.attributes:
            self.session.attributes = models._Field()

        if self.context.type == 'LaunchRequest' and self._launch_view_func:
            result = self._launch_view_func(request_body)
        elif self.context.type == 'IntentRequest' and self._intent_view_funcs:
            result = self._map_intent_to_view_func(self.context.intent)()

        if result is not None:
            if isinstance(result, models._Response):
                return result.render_response()
            return result
        return "", 400

    @classmethod
    def _map_intent_to_view_func(self, intent):
        """Provides appropiate parameters to the intent functions."""
        if intent.label in self._intent_view_funcs:
            view_func = self._intent_view_funcs[intent.label]
        elif self._default_intent_view_func is not None:
            view_func = self._default_intent_view_func
        else:
            raise NotImplementedError(
                'Intent "{}" not found and no default intent specified.'.format(intent.name))

        argspec = inspect.getargspec(view_func)
        arg_names = argspec.args
        arg_values = self._map_params_to_view_args(intent.label, arg_names)

        return partial(view_func, *arg_values)

    @classmethod
    def _map_params_to_view_args(self, view_name, arg_names):
        arg_values = []

        request_data = {}
        entities = getattr(self.context, 'entities', None)
        try:
            dialog_entities = getattr(self.context.dialog, 'entities', None)
        except Exception:
            dialog_entities = None
            
        if entities is not None:
            if dialog_entities is not None:
                entities += dialog_entities
            for entity in entities:
                request_data[entity['entity'].replace('$', '')] = entity
        else:
            for param_name in self.context:
                request_data[param_name] = getattr(self.context, param_name, None)

        for arg_name in arg_names:
            arg_value = request_data.get(arg_name)
            arg_values.append(arg_value)
        return arg_values
