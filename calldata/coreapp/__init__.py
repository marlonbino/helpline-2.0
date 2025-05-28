#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (
    unicode_literals,
    print_function
    )

import os
import random

from pydoc import (
    locate)
from config import (
    app_config)
from flask import (
    Flask,
    request,
    jsonify,
    redirect,
    Blueprint)


def create_app(config_name):
    """Create App"""
    app = Flask(
        __name__,
        instance_relative_config=True
        )

    app.config.from_object(
        app_config[config_name])
    app.config.from_pyfile(
        'config.py')
    app.config['SECRET_KEY'] = "\xfb\x12\xdf\xa1@i\xd6>V\xc0\xbb\x8fp\x16#Z\x0b\x81\xeb\x16"

    # Register AI-Core Blueprints
    from aicore import bp as aibp
    app.register_blueprint(aibp, url_prefix="/aicore")

    # Register Chatbot Blueprints
    from chatbot import bp as chatbp
    app.register_blueprint(chatbp, url_prefix="/chatbot")

    # Register CDR Data Blueprints
    from calldata import bp as cdrbp
    app.register_blueprint(cdrbp, url_prefix="/calldata")

    # Register Case Data Blueprints
    from casedata import bp as casebp
    app.register_blueprint(casebp, url_prefix="/casedata")

    # pjsiplog.indexinit()

    # Handle View Errors
    @app.errorhandler(403)
    def forbidden(error):
        """Forbidden"""

        data = {}
        data['code'] = 403
        data['method'] = request.method
        data['remote'] = request.remote_addr
        data['realip'] = request.headers.get('X-Real-IP')
        data['forward'] = request.headers.get('X-Forwarded-For')

        # system.indexcreate(data)

        if request.method == "POST":
            return jsonify({}), 403

        return render_template('viewone/errors/403.html')

    @app.errorhandler(404)
    def page_not_found(error):
        """Log Handle Hits"""

        data = {}
        data['code'] = 404
        data['method'] = request.method
        data['remote'] = request.remote_addr
        data['realip'] = request.headers.get('X-Real-IP')
        data['forward'] = request.headers.get('X-Forwarded-For')

        # system.indexcreate(data)

        if request.method == "POST":
            return jsonify({}), 404

        return render_template('viewone/errors/404.html')

    @app.errorhandler(405)
    def method_not_allowed(error):
        """Not Allowed"""

        data = {}
        data['code'] = 405
        data['method'] = request.method
        data['remote'] = request.remote_addr
        data['realip'] = request.headers.get('X-Real-IP')
        data['forward'] = request.headers.get('X-Forwarded-For')

        # system.indexcreate(data)

        if request.method == "POST":
            return jsonify({}), 405

        return render_template('viewone/errors/405.html')

    @app.errorhandler(500)
    def internal_server_error(error):
        """Server Error"""

        data = {}
        data['code'] = 405
        data['method'] = request.method
        data['remote'] = request.remote_addr
        data['realip'] = request.headers.get('X-Real-IP')
        data['forward'] = request.headers.get('X-Forwarded-For')

        # system.indexcreate(data)

        if request.method == "POST":
            return jsonify({}), 500

        return render_template('viewone/errors/500.html')

    return app
