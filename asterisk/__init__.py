#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (
    unicode_literals,
    print_function)

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


bp = Blueprint('asterisk', __name__,)

edir = os.path.dirname(os.path.realpath(__file__))

epath = edir + "/__init__.py"


def init():
    logger.debug("""Initialize ARI""")

    data = {}

    try:

        runtime = locate('asterisk.dialplan.runtime')

        if runtime is not None:
            data = runtime.indexinit({})

            if data.get('data'):
                del data['error'], data['data']

    except Exception as e:
        data['error'] = "Error Index-Init Asterisk-ARI {}".format(e)
        logger.critical(data['error'])

    return data

"""
curl -X POST "localhost:50001/asterisk/{create, data, action, stats, index}/item" \
-H "Content-Type: application/json" \
--data "{}"
"""
@bp.route("/", methods=['GET'])
@bp.route("/index", methods=['GET'])
def index():
    logger.debug("""CDR-Data Web Pages""")

    try:

        data = {}
        x = request.args.to_dict()

        if x.get('userid') is None:
            logger.debug("""Asterisk Create""")
            return render_template('viewone/asterisk/index.html')

        # Remove dashboard dependency - just use empty data for now
        # x = dashboard.indexweb(x)
        
        if x.get('item') is not None:
            logger.debug("""Asterisk Template""")
            return render_template('viewone/asterisk/' + x.get(
                'item') + '.html', data=x.get('data'))

    except Exception as e:
        data['error'] = "Error Index-Template CDR-Data {}".format(e)
        logger.critical(data['error'])

    return render_template('errors/404.html')


@bp.route("/endpoint", methods=['POST'])
def endpoint():
    logger.debug("""Asterisk-Endpoint""")

    try:

        data = {}
        x = request.get_json()

        metadata = locate('asterisk.phones')

        if metadata is not None:

            data = metadata.indexcreate(x)

            if data.get('data'):
                del data['error'], data['data']
                return jsonify(data)

    except Exception as e:
        data['error'] = "Error Index-Create Asterisk-Endpoint {}".format(e)
        logger.critical(data['error'])

    return jsonify(data), 404


@bp.route("/dialplan", methods=['POST'])
def dialplan():
    logger.debug("""Asterisk Extensions""")

    try:

        data = {}
        x = request.get_json()

        metadata = locate('asterisk.dialplan')

        if metadata is not None:
            data = metadata.indexdata(x)

            if data.get('data'):
                del data['error'], data['data']
                return jsonify(data)

    except Exception as e:
        data['error'] = "Error Index-Action Asterisk-Dialplan {}".format(e)
        logger.critical(data['error'])

    return jsonify(data), 404


@bp.route("/media", methods=['POST'])
def mediadata():
    logger.debug("""Asterisk Media """)

    try:

        data = {}
        x = request.get_json()

        metadata = locate('asterisk.media')

        if metadata is not None:

            data = metadata.indexdata(x)

            if data.get('data'):
                del data['error'], data['data']
                return jsonify(data)

    except Exception as e:
        data['error'] = "Error Index-Stats Asterisk-Media {}".format(e)
        logger.critical(data['error'])

    return jsonify(data), 404


@bp.route("/media/<filename>", methods=['GET'])
def mediaitem(filename):
    logger.debug("""Asterisk Media """ + filename)

    try:

        data = {}
        x = request.get_json()
        x['file'] = filename

        metadata = locate('asterisk.media')

        if metadata is not None:

            data = metadata.indexdata(x)

            if data.get('data'):
                del data['error'], data['data']
                return jsonify(data)

    except Exception as e:
        data['error'] = "Error Index-Stats Asterisk-Media {}".format(e)
        logger.critical(data['error'])

    return jsonify(data), 404
