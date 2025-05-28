#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (
    unicode_literals,
    print_function)

import os
import random
from pydoc import (
    locate)
from logsdata import (
    logger)
from models.calldata import (
    metadata)
from asterisk.dialplan import (
    runtime)

edir = os.path.dirname(os.path.realpath(__file__))

epath = edir + "/__init__.py"


def indexdemo(dat=False):
    logger.info("""Create Demo Call""")

    data = {}
    data['data'] = False
    data['error'] = False

    try:

        edit = {}
        edit['INITGO'] = "waitime"
        edit['CALLERID(name)'] = "Demo Helpline"

        if dat.get('code') is None:
            logger.info("""Default Kenya""")
            dat['code'] = "254"

        if dat.get('maxi') is None:
            logger.info("""Create Single Demo""")
            dat['maxi'] = 1

        data['demo'] = {}

        while True:
            for i in range(int(dat['maxi'])):
                edit['WAITIME'] = str(random.randint(90,360))
                edit['CALLERID(num)'] = dat.get('code') + str(random.randint(
                    700, 799)) + str(random.randint(100000, 999999))

                data['demo'][edit['CALLERID(num)']] = strftime('%H:%M %p')

                runtime.indexdata({
                    "chan": "116",
                    "variables": edit,
                    "peer": "helpline",
                    "exten": "helpline",
                    "context": "helpline",
                    })

                sleep(random.randint(2,7))

            break

    except Exception as e:
        data['error'] = "Error Index-Stats ElevenLabs {}".format(e)
        logger.critical(data['error'])

    return data