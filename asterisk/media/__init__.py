#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (
    unicode_literals,
    print_function)

import os
from logsdata import (
    logger)


def indexdata(dat):
    logger.debug("""CDR-Data Web Pages""")

    data = {}
    data['data'] = False
    data['error'] = False

    try:
        pass
    except Exception as e:
        logger.critical("Asterisk Media Data Error {}".format())

    return data
