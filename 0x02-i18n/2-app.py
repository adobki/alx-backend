#!/usr/bin/env python3
"""This module showcases i18n using a Flask API"""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config(object):
    """Configuration options for app and babel"""
    LANGUAGES = ['en', 'fr']
    TIMEZONES = ['UTC', 'GMT']

    @property
    def GET_LANG(self) -> str:
        """Selects first language as config language"""
        return Config.LANGUAGES[0]

    @property
    def GET_TZ(self) -> str:
        """Selects first timezone as config timezone"""
        return Config.TIMEZONES[0]


app = Flask(__name__)
babel = Babel(app,
              default_locale=Config().GET_LANG,
              default_timezone=Config().GET_TZ)
app.config.from_object(Config)


@app.route('/', strict_slashes=False)
def home() -> str:
    """Default route/homepage"""
    return render_template('2-index.html')


@babel.localeselector
def get_locale() -> str:
    """Set preferred locale"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


if __name__ == '__main__':
    """Tests the code in this module"""
    app.run()
