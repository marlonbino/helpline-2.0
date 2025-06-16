#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (
    unicode_literals,
    print_function
    )

import os

from pydoc import (
    locate)
from flask import (
    request,
    jsonify,
    Blueprint,
    render_template)
from flask.helpers import (
    send_file,
    url_for)
from logsdata import (
    logger)


bp = Blueprint(
    'contacts', __name__,
    )

edir = os.path.dirname(os.path.realpath(__file__))

epath = edir + "/__init__.py"


def init():
    logger.debug("""Initialize Queue""")

    data = {}

    try:

        runtime = locate('models.contacts.runtime')

        if runtime is not None:
            data = runtime.indexinit({})

            if data.get('data'):
                del data['error'], data['data']

    except Exception as e:
        data['error'] = "Error Index-Action Contacts {}".format(e)
        logger.critical(data['error'])

    return data


"""
curl -X POST "localhost:50001/contacts/{create, data, action, stats, index}/item" \
-H "Content-Type: application/json" \
--data "{}"
"""
@bp.route("/", methods=['GET'])
@bp.route("/index", methods=['GET'])
def index():
    logger.debug("""Contacts Web Pages""")

    try:

        data = {}
        x = request.args.to_dict()

        if x.get('userid') is None:
            logger.debug("""Contacts Create""")
            return render_template('sneat/contacts/index.html')

        # Remove dashboard dependency - just use empty data for now
        # x = dashboard.indexweb(x)
        
        if x.get('item') is not None:
            logger.debug("""Contacts Template""")
            return render_template('sneat/contacts/' + x.get(
                'item') + '.html', data=x.get('data'))

    except Exception as e:
        data['error'] = "Error Index-Template Contacts {}".format(e)
        logger.critical(data['error'])

    return render_template('errors/404.html')


@bp.route("/data/<filename>", methods=['POST'])
def data(filename):
    logger.debug("""Contacts Data""")

    try:

        data = {}
        x = request.get_json()
        if 'next' not in x:
            x['next'] = False
        if 'prev' not in x:
            x['prev'] = False

        metadata = locate('models.contacts.' + filename)

        if metadata is not None:

            data = metadata.indexdata(x)

            if data.get('data'):
                del data['error'], data['data']
                return jsonify(data)

    except Exception as e:
        data['error'] = "Error Index-Data Contacts {}".format(e)
        logger.critical(data['error'])

    return jsonify(data), 404


@bp.route("/action/<filename>", methods=['POST'])
def action(filename):
    logger.debug("""Contacts Action: """ + filename)

    try:

        data = {}
        x = request.get_json()

        metadata = locate('models.contacts.' + filename)

        if metadata is not None:
            data = metadata.indexaction(x)

            if data.get('data'):
                del data['error'], data['data']
                return jsonify(data)

    except Exception as e:
        data['error'] = "Error Index-Action Contacts {}".format(e)
        logger.critical(data['error'])

    return jsonify(data), 404


@bp.route("/stats/<filename>", methods=['POST'])
def stats(filename):
    logger.debug("""Contacts Stats: """ + filename)

    try:

        data = {}
        x = request.get_json()

        metadata = locate('models.contacts.' + filename)

        if metadata is not None:

            data = metadata.indexstats(x)

            if data.get('data'):
                del data['error'], data['data']
                return jsonify(data)

    except Exception as e:
        data['error'] = "Error Index-Stats Contacts {}".format(e)
        logger.critical(data['error'])

    return jsonify(data), 404


@bp.route("/reset/<filename>", methods=['POST'])
def resets(filename):
    logger.debug("""Contacts Reset: """ + filename)

    try:

        data = {}
        x = request.get_json()

        metadata = locate('models.contacts.' + filename)

        if metadata is not None:

            data = metadata.indexreset(x)

            if data.get('data'):
                del data['error'], data['data']
                return jsonify(data)

    except Exception as e:
        data['error'] = "Error Index-Stats Contacts {}".format(e)
        logger.critical(data['error'])

    return jsonify(data), 404

