#!/usr/bin/env python3
"""This module showcases i18n using a Flask API"""
from flask import Flask, render_template, request
from flask_babel import Babel, _


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
babel = Babel(app)
app.config.from_object(Config)


@app.route('/', strict_slashes=False)
def home() -> str:
    """Default route/homepage"""
    return render_template('4-index.html',
                           home_title=_('home_title'),
                           home_header=_('home_header'))


@babel.localeselector
def get_locale() -> str:
    """Set preferred locale"""
    # Check if valid language was requested by user in query string
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    # Choose most appropriate language from defaults if none was requested
    return request.accept_languages.best_match(app.config['LANGUAGES'])


if __name__ == '__main__':
    """Tests the code in this module"""
    app.run()
