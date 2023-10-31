#!/usr/bin/env python3
"""This module showcases i18n using a Flask API"""
import flask
from flask import Flask, render_template, request
from flask_babel import Babel, _
from typing import Union
# Hotfix for the ALX SE code checker
_.__doc__ = 'Marks a string for translation'


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


@app.before_request
def before_request() -> None:
    """Runs before each request"""
    flask.g.user = get_user()
    if flask.g.user:
        flask.g.welcome = _('logged_in_as', username=flask.g.user.get('name'))
    else:
        flask.g.welcome = _('not_logged_in')


@app.route('/')
def home() -> str:
    """Default route/homepage"""
    return render_template('5-index.html',
                           welcome_message=flask.g.welcome)


@babel.localeselector
def get_locale() -> str:
    """Set preferred locale"""
    # Check if language was requested by user in query string
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    # Choose most appropriate language from defaults if none was requested
    return request.accept_languages.best_match(app.config['LANGUAGES'])


users = {
    1: {'name': 'Balou', 'locale': 'fr', 'timezone': 'Europe/Paris'},
    2: {'name': 'Beyonce', 'locale': 'en', 'timezone': 'US/Central'},
    3: {'name': 'Spock', 'locale': 'kg', 'timezone': 'Vulcan'},
    4: {'name': 'Teletubby', 'locale': None, 'timezone': 'Europe/London'},
}


def get_user() -> Union[dict, None]:
    """Mocks Flask user login system using users dictionary"""
    # Check if valid user_id was provided in query string
    user_id = request.args.get('login_as')
    if not user_id or not user_id.isnumeric():
        return None
    # Return data for provided user_id if it exists
    return users.get(int(user_id))


if __name__ == '__main__':
    """Tests the code in this module"""
    app.run()
