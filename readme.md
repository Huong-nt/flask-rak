
# Rogo Speaker Application Kits for Python

[![NPM Version][npm-image]][npm-url]


Flask-Rak is a `Flask extension` that makes building Rogo applications for the Rogo Speaker easier and much more fun.

This project is heavily inspired and based on John Wheeler's [Flask-ask](https://github.com/johnwheeler/flask-ask) for the Alexa Skills Kit.
## The Basics

A Flask-Rak application looks like:

```
from flask import Flask
from flask_rak import Rak, session, context, statement, audio

app = Flask(__name__)
rak = Rak(app, '/')

@ask.intent('HelloIntent')
def hello(firstname):
    speech_text = "Hello %s" % firstname
    return statement(speech_text)

if __name__ == '__main__':
    app.run()

```
In the code above:

1. The ``Rak`` object is created by passing in the Flask application and a route to forward Rogo speaker requests to.
2. The ``intent`` decorator maps ``HelloIntent`` to a view function ``hello``.
3. The intent's ``firstname`` slot is implicitly mapped to ``hello``'s ``firstname`` parameter.

## Installation

To install Flask-Rak
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