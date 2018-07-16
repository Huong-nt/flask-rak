
# Rogo Speaker Application Kits for Python

[![NPM Version][npm-image]][npm-url]


Flask-Rak is a `Flask extension` that makes building Rogo applications for the Rogo Speaker easier and much more fun.

This project is heavily inspired and based on John Wheeler's [Flask-ask](https://github.com/johnwheeler/flask-ask) for the Alexa Skills Kit.
## The Basics

A Flask-Rak application looks like:

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify

api = Blueprint('api', __name__)

from flask_rak import RAK, statement, question


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
    

```
In the code above:

1. The ``Rak`` object is created by passing in the Flask application and a route to forward Rogo speaker requests to.
2. The ``intent`` decorator maps ``HelloIntent`` to a view function ``hello``.
3. The intent's ``firstname`` slot is implicitly mapped to ``hello``'s ``firstname`` parameter.

## Installation

To install Flask-Rak
```
pip install flask-ask
```
To install from your local clone or fork of the project, run:
```
python setup.py install
```

## Update pip package:
update new pip package to https://pypi.org/
```
python setup.py sdist
twine upload dist/*
```

<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/pypi/v/flask-rak.svg
[npm-url]: https://pypi.python.org/pypi/flask-rak