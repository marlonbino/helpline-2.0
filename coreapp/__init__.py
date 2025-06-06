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
    url_for,  # Added url_for
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
    from asterisk import bp as asteriskbp
    app.register_blueprint(asteriskbp, url_prefix="/asterisk")

    # Register User Data Blueprints
    import userdata
    # userdata.init()
    app.register_blueprint(userdata.bp, url_prefix="/contacts")

    # Add Users and Roles API Routes
    @app.route('/api/users', methods=['POST'])
    def add_user():
        try:
            data = request.get_json()
            # TODO: Implement user creation logic
            # For now, just return a mock response
            return jsonify({
                'username': data['username'],
                'role': data['role'],
                'status': data['status']
            }), 201
        except Exception as e:
            logger.error(f"Error adding user: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/roles', methods=['POST'])
    def add_role():
        try:
            data = request.get_json()
            # TODO: Implement role creation logic
            # For now, just return a mock response
            return jsonify({
                'name': data['roleName'],
                'permissions': data['permissions']
            }), 201
        except Exception as e:
            logger.error(f"Error adding role: {str(e)}")
            return jsonify({'error': str(e)}), 500

    # Register Case Data Blueprints
    from casedata import bp as casebp
    app.register_blueprint(casebp, url_prefix="/casedata")

    # Register Chatbot Blueprints
    from chatbot import bp as chatbp
    app.register_blueprint(chatbp, url_prefix="/chatbot")

    logger.info("Completed Blueprint Registration")

    # Default Route Index
    @app.route("/", methods=['GET'])
    def index():
        logger.info("Helpline Index Page")
        return render_template(
            'index.html', title="Helpline: AI Case Management System")

    # Login Route Index
    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            # Placeholder for actual user authentication logic.
            # You should validate username and password here.
            # Example (if using Flask-Login):
            # from flask_login import login_user
            # user = User.query.filter_by(username=request.form.get('username')).first()
            # if user and user.check_password(request.form.get('password')):
            #     login_user(user, remember=request.form.get('remember'))
            #     logger.info(f"User {user.username} logged in successfully, redirecting to dashboard.")
            #     return redirect(url_for('dashboard'))
            # else:
            #     logger.warning("Login failed for user.")
            #     # You might want to flash a message here: flash('Invalid username or password')
            #     return render_template('login.html', title="Login: AI Case Management System", error="Invalid credentials")

            # For now, directly redirecting assuming login is successful.
            logger.info("Login attempt via POST, redirecting to dashboard.")
            return redirect(url_for('dashboard'))
        
        # For GET request
        logger.info("Helpline Login Page (GET)")
        return render_template(
            'login.html', title="Login: AI Case Management System")

    # Register Route Index
    @app.route("/register", methods=['GET'])
    def register():
        logger.info("Helpline Register Page")
        return render_template(
            'register.html', title="Register: AI Case Management System")

    # Dashboard Route
    @app.route("/dashboard", methods=['GET'])
    # @login_required  # Uncomment this line if you are using Flask-Login and the dashboard should be protected
    def dashboard():
        logger.info("Helpline Dashboard Page")
        # You can pass any necessary data to your dashboard template here
        return render_template('dashboard_content.html', title="Dashboard")

    # Call Data Route
    @app.route("/call-data", methods=['GET'])
    def call_data():
        logger.info("Helpline Call Data Page")
        return render_template('call_data_content.html', title="Call Data")

    # Case Data Route
    @app.route("/case-data", methods=['GET'])
    def case_data():
        logger.info("Helpline Case Data Page")
        return render_template('case_data_content.html', title="Case Data")

    # AI Services Route
    @app.route("/ai-services", methods=['GET'])
    def ai_services():
        logger.info("Helpline AI Services Page")
        return render_template('ai_services_content.html', title="AI Services")

    # Users & Roles Route
    @app.route("/users-roles", methods=['GET'])
    def users_roles():
        logger.info("Helpline Users & Roles Page")
        return render_template('users_roles_content.html', title="Users & Roles")

    # System Services Route
    @app.route("/system-services", methods=['GET'])
    def system_services():
        logger.info("Helpline System Services Page")
        return render_template('system_services_content.html', title="System Services")

    # Chatbot Route
    @app.route("/chatbot", methods=['GET'])
    def chatbot():
        logger.info("Helpline Chatbot Page")
        return render_template('chatbot_content.html', title="Chatbot")

    # Documentation Route
    @app.route("/documentation", methods=['GET'])
    def documentation():
        logger.info("Helpline Documentation Page")
        return render_template('documentation_content.html', title="Documentation")

    # Call Center Routes
    @app.route("/calls/form", methods=['GET'])
    def calls_form():
        logger.info("Call Center Form Page")
        return render_template('forms/form_calls.html', title="Call Center Form")

    @app.route("/calls/table", methods=['GET'])
    def calls_table():
        logger.info("Call Center Table Page")
        return render_template('tables/table_calls.html', title="Call Center Table")

    # Cases Routes
    @app.route("/cases/form", methods=['GET'])
    def cases_form():
        logger.info("Cases Form Page")
        return render_template('forms/form_cases.html', title="Cases Form")

    @app.route("/cases/table", methods=['GET'])
    def cases_table():
        logger.info("Cases Table Page")
        return render_template('tables/table_cases.html', title="Cases Table")

    # Users Routes
    @app.route("/users/form", methods=['GET'])
    def users_form():
        logger.info("Users Form Page")
        return render_template('forms/form_users.html', title="Users Form")

    @app.route("/users/table", methods=['GET'])
    def users_table():
        logger.info("Users Table Page")
        return render_template('tables/table_users.html', title="Users Table")

    # Clients Routes (using Users templates)
    @app.route("/clients/form", methods=['GET'])
    def clients_form():
        logger.info("Clients Form Page")
        return render_template('forms/form_users.html', title="Clients Form") # Uses users form template

    @app.route("/clients/table", methods=['GET'])
    def clients_table():
        logger.info("Clients Table Page")
        return render_template('tables/table_users.html', title="Clients Table") # Uses users table template

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
