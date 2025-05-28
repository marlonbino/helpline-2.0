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
    Blueprint,
    render_template)
from models import (
    system)
from logsdata import (
    logger)


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

    logger.info("Initialize System Queues")
    system.indexinit()

    """TODO: Migrate BP to MongoDB"""

    # Register AI-Core Blueprints
    from aicore import bp as aibp
    app.register_blueprint(aibp, url_prefix="/aicore")

    # Register Asterisk Blueprints
    import asterisk
    # asterisk.init()
    app.register_blueprint(asterisk.bp, url_prefix="/asterisk")

    # Register CDR Data Blueprints
    from calldata import bp as cdrbp
    app.register_blueprint(cdrbp, url_prefix="/calldata")

    # Register Case Data Blueprints
    from casedata import bp as casebp
    app.register_blueprint(casebp, url_prefix="/casedata")

    # Register Chatbot Blueprints
    from chatbot import bp as chatbp
    app.register_blueprint(chatbp, url_prefix="/chatbot")

    # Register Contacts Data Blueprints
    import userdata
    # userdata.init()
    app.register_blueprint(userdata.bp, url_prefix="/contacts")

    logger.info("Completed Blueprint Registration")

    # Default Route Index
    @app.route("/", methods=['GET'])
    def index():
        logger.info("Helpline Index Page")
        return render_template(
            'index.html', title="Helpline: AI Case Management System")

    # Login Route Index
    @app.route("/login", methods=['GET'])
    def login():
        logger.info("Helpline Login Page")
        return render_template(
            'login.html', title="Login: AI Case Management System")

    # Login Route Index
    @app.route("/register", methods=['GET'])
    def register():
        logger.info("Helpline Register Page")
        return render_template(
            'register.html', title="Register: AI Case Management System")

    # Handle View Errors
    @app.errorhandler(403)
    def forbidden(error):
        logger.warn("Helpline Error 403 " + str(request.headers.get('X-Real-IP')))

        data = {}
        data['code'] = 403
        data['method'] = request.method
        data['remote'] = request.remote_addr
        data['realip'] = request.headers.get('X-Real-IP')
        data['forward'] = request.headers.get('X-Forwarded-For')

        # system.indexcreate(data)

        if request.method == "POST":
            return jsonify({}), 403

        return render_template('errors/403.html')

    @app.errorhandler(404)
    def page_not_found(error):
        logger.warn("Helpline Error 404 " + str(request.headers.get('X-Real-IP')))

        data = {}
        data['code'] = 404
        data['method'] = request.method
        data['remote'] = request.remote_addr
        data['realip'] = request.headers.get('X-Real-IP')
        data['forward'] = request.headers.get('X-Forwarded-For')

        # system.indexcreate(data)

        if request.method == "POST":
            return jsonify({}), 404

        return render_template('errors/404.html')

    @app.errorhandler(405)
    def method_not_allowed(error):
        logger.warn("Helpline Error 405 " + str(request.headers.get('X-Real-IP')))

        data = {}
        data['code'] = 405
        data['method'] = request.method
        data['remote'] = request.remote_addr
        data['realip'] = request.headers.get('X-Real-IP')
        data['forward'] = request.headers.get('X-Forwarded-For')

        # system.indexcreate(data)

        if request.method == "POST":
            return jsonify({}), 405

        return render_template('errors/405.html')

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.warn("Helpline Error 500 " + str(request.headers.get('X-Real-IP')))

        data = {}
        data['code'] = 405
        data['method'] = request.method
        data['remote'] = request.remote_addr
        data['realip'] = request.headers.get('X-Real-IP')
        data['forward'] = request.headers.get('X-Forwarded-For')

        # system.indexcreate(data)

        if request.method == "POST":
            return jsonify({}), 500

        return render_template('errors/500.html')

    return app
