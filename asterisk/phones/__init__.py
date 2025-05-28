#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (
    unicode_literals,
    print_function)

import os
from time import (
    strftime)
from coreapp import (
    creds)
from logsdata import (
    logger)

edir = os.path.dirname(os.path.realpath(__file__))
epath = edir + "/__init__.py"


def indexcreate(dat):
    logger.info("Create Asterisk Endpoint")

    data = {}
    data['data'] = False
    data['error'] = True

    try:

        CONF = edir + "/" + dat.get('phone') + ".conf"

        text = ";=======EXTENSION " + dat.get('phone') + "========\n"
        text += "\n[" + dat.get('phone') + "](endpoint-basic)\n"
        text += "auth=" + dat.get('phone') + "\n"
        text += "aors=" + dat.get('phone') + "\n"
        text += "context=" + dat.get('context') + "\n"

        if dat.get('callerid') is not None:
            # text += "outbound_auth=" + dat.get('phone') + "\n"
            text += "callerid=" + dat.get('callerid') + " <" + dat.get('phone') + ">\n"
            
        text += "\n"
        text += "[" + dat.get('phone') + "](auth-userpass)\n"
        text += "password=" + dat.get('auth') + "\n"
        text += "username=" + dat.get('phone') + "\n"
        text += "\n"
        text += "[" + dat.get('phone') + "](aor-single-reg)\n"
        text += "\n;=======CREATED " + strftime('%d %b %Y %H:%M:%S') + "========\n"

        if os.path.isfile(CONF):
            """Delete File"""
            CMD = "rm -rf " + CONF
            os.system(CMD)


        with open(CONF, 'w') as fp:
            fp.write(text)


        logger.info("""Reload PJSIP Drivers: """ + dat.get('phone'))
        cmd = "asterisk -rx \"core reload\" > " + PATH + "/coreload.log"
        os.system(cmd)

        data['data'] = True
        data['error'] = False

    except Exception as e:
        data['error'] = "Error Index-Create SIP-Server {}".format(e)
        logger.critical(data['error'])

    return data
