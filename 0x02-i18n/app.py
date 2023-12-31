#!/usr/bin/env python3
"""This module showcases i18n using a Flask API"""
import flask
from datetime import datetime
from flask import Flask, render_template, request
from flask_babel import _, Babel, format_datetime
from pytz import timezone
from pytz.exceptions import UnknownTimeZoneError
from typing import Union


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


@app.before_request
def before_request() -> None:
    """Runs before each request"""
    # Mock login and set welcome message based on user login status
    flask.g.user = get_user()
    if flask.g.user:
        flask.g.welcome = _('logged_in_as', username=flask.g.user.get('name'))
    else:
        flask.g.welcome = _('not_logged_in')

    # Set timezone based on selected preference or default
    time = format_datetime(datetime.now(tz=timezone(get_timezone())))
    flask.g.time = _('current_time_is', current_time=time)


@app.route('/')
def home() -> str:
    """Default route/homepage"""
    return render_template('index.html',
                           welcome_message=flask.g.welcome,
                           current_time_is=flask.g.time)


@babel.localeselector
def get_locale() -> str:
    """Sets locale as user's choice if a valid choice is given, else default"""
    choices = {
        'query_string': request.args.get('locale'),
        'user_setting': flask.g.user.get('locale') if flask.g.user else None,
        'request_header': request.headers.get('locale'),
        'default': request.accept_languages.best_match(app.config['LANGUAGES'])
    }
    # Loop through choices for preferred locale and choose first valid one
    for locale in choices.values():
        if locale and locale in app.config['LANGUAGES']:
            return locale


@babel.timezoneselector
def get_timezone() -> str:
    """Sets timezone as user's choice if valid choice is given, else default"""
    choices = {
        'query_string': request.args.get('timezone'),
        'user_setting': flask.g.user.get('timezone') if flask.g.user else None,
        'default': Config.BABEL_DEFAULT_TIMEZONE
    }
    # Loop through choices for preferred timezone and choose first valid one
    for tz in choices.values():
        try:
            if tz and timezone(tz):
                return timezone(tz).zone
        except UnknownTimeZoneError:
            # Prevents error on invalid timezone string
            pass


users = {
    1: {'name': 'Balou', 'locale': 'fr', 'timezone': 'Europe/Paris'},
    2: {'name': 'Beyonce', 'locale': 'en', 'timezone': 'US/Central'},
    3: {'name': 'Spock', 'locale': 'kg', 'timezone': 'Vulcan'},
    4: {'name': 'Teletubby', 'locale': None, 'timezone': 'Europe/London'},
    5: {'name': 'Donald', 'locale': 'fr', 'timezone': 'Africa/Lagos'},
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
