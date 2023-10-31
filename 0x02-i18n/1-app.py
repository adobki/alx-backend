#!/usr/bin/env python3
"""This module showcases i18n using a Flask API"""
from flask import Flask, render_template
from flask_babel import Babel


class Config(object):
    """Configuration options for app and babel"""
    # Available options
    LANGUAGES = ['en', 'fr']
    TIMEZONES = ['UTC', 'GMT']

    # Defaults
    BABEL_DEFAULT_LOCALE = LANGUAGES[0]
    BABEL_DEFAULT_TIMEZONE = TIMEZONES[0]


app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)


@app.route('/', strict_slashes=False)
def home() -> str:
    """Default route/homepage"""
    return render_template('1-index.html')


if __name__ == '__main__':
    """Tests the code in this module"""
    app.run()
