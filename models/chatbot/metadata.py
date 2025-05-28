#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (
    unicode_literals,
    print_function
    )

import os
from logsdata import (
    logger)


def indexinit(dat=False):
    logger.debug("Chatbot Initialize")

    data = {}
    data['data'] = False
    data['error'] = False

    try:
        data['init'] = "Helpline WhatsApp Chatbot"
        data['data'] = True
    except Exception as e:
        data['error'] = "Error Index-Init Chatbot-Services {}".format(e)
        logger.critical(data['error'])

    return data


def indexcreate(dat):
    logger.debug("Chatbot Create Session")

    data = {}
    data['data'] = False
    data['error'] = False

    try:
        data['data'] = True
    except Exception as e:
        data['error'] = "Error Index-Create Chatbot-Services {}".format(e)
        logger.critical(data['error'])

    return data


def indexaction(dat):
    logger.debug("Chatbot Update Session")

    data = {}
    data['data'] = False
    data['error'] = False

    try:
        data['data'] = True
    except Exception as e:
        data['error'] = "Error Index-Action Chatbot-Services {}".format(e)
        logger.critical(data['error'])

    return data


def indexstats(dat):
    logger.debug("Chatbot Stats Sessions")

    data = {}
    data['data'] = False
    data['error'] = False

    try:
        data['data'] = True
    except Exception as e:
        data['error'] = "Error Index-Stats Chatbot-Services {}".format(e)
        logger.critical(data['error'])

    return data


def indexapis(dat):
    logger.debug("Chatbot APIs Sessions")

    data = {}
    data['data'] = False
    data['error'] = False

    try:
        data['data'] = True
    except Exception as e:
        data['error'] = "Error Index-APIs Chatbot-Services {}".format(e)
        logger.critical(data['error'])

    return data


def indexreset(dat):
    logger.debug("Chatbot Reset Sessions")

    data = {}
    data['data'] = False
    data['error'] = False

    try:
        data['data'] = True
    except Exception as e:
        data['error'] = "Error Index-Reset Chatbot-Services {}".format(e)
        logger.critical(data['error'])

    return data
