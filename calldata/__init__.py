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


bp = Blueprint(
    'calldata', __name__,
    )

edir = os.path.dirname(os.path.realpath(__file__))

epath = edir + "/__init__.py"


"""
curl -X POST "localhost:50001/calldata/{create, data, action, stats, index}/item" \
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
            logger.debug("""CDR-Data Create""")
            return render_template('viewone/calldata/index.html')

        x = dashboard.indexweb(x)
        
        if x.get('item') is not None:
            logger.debug("""CDR-Data Template""")
            return render_template('viewone/calldata/' + x.get(
                'item') + '.html', data=x.get('data'))

    except Exception as e:
        data['error'] = "Error Index-Template CDR-Data {}".format(e)
        logger.critical(data['error'])

    return render_template('viewone/errors/404.html')


@bp.route("/data/<filename>", methods=['POST'])
def data(filename):
    logger.debug("""CDR-Data Data""")

    try:

        data = {}
        x = request.get_json()
        if 'next' not in x:
            x['next'] = False
        if 'prev' not in x:
            x['prev'] = False

        metadata = locate('models.calldata.' + filename)

        if metadata is not None:

            data = metadata.indexdata(x)

            if data.get('data'):
                del data['error'], data['data']
                return jsonify(data)

    except Exception as e:
        data['error'] = "Error Index-Data CDR-Data-Core {}".format(e)
        logger.critical(data['error'])

    return jsonify(data), 404


@bp.route("/action/<filename>", methods=['POST'])
def action(filename):
    logger.debug("""CDR-Data Action: """ + filepath)

    try:

        data = {}
        x = request.get_json()

        metadata = locate('models.calldata.' + filename)

        if metadata is not None:
            data = metadata.indexaction(x)

            if data.get('data'):
                del data['error'], data['data']
                return jsonify(data)

    except Exception as e:
        data['error'] = "Error Index-Action CDR-Data-Core {}".format(e)
        logger.critical(data['error'])

    return jsonify(data), 404


@bp.route("/stats/<filename>", methods=['POST'])
def stats(filename):
    logger.debug("""CDR-Data Stats: """ + filepath)

    try:

        data = {}
        x = request.get_json()

        metadata = locate('models.calldata.' + filename)

        if metadata is not None:

            data = metadata.indexstats(x)

            if data.get('data'):
                del data['error'], data['data']
                return jsonify(data)

    except Exception as e:
        data['error'] = "Error Index-Stats CDR-Data-Core {}".format(e)
        logger.critical(data['error'])

    return jsonify(data), 404


@bp.route("/reset/<filename>", methods=['POST'])
def resets(filename):
    logger.debug("""CDR-Data Reset: """ + filepath)

    try:

        data = {}
        x = request.get_json()

        metadata = locate('models.calldata.' + filename)

        if metadata is not None:

            data = metadata.indexreset(x)

            if data.get('data'):
                del data['error'], data['data']
                return jsonify(data)

    except Exception as e:
        data['error'] = "Error Index-Stats CDR-Data-Core {}".format(e)
        logger.critical(data['error'])

    return jsonify(data), 404
