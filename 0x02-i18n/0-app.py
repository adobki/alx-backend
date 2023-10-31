#!/usr/bin/env python3
"""This module showcases i18n using a Flask API"""
from flask import Flask, render_template, request
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)


@app.route('/', strict_slashes=False)
def home() -> str:
    """Default route/homepage"""
    return render_template('0-index.html')


if __name__ == '__main__':
    """Tests the code in this module"""
    app.run()
