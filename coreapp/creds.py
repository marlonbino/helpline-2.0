#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (
    unicode_literals,
    print_function)

import os
import sys
import random
import locale
import string

from datetime import datetime
from time import time, strftime
from urllib.parse import urlencode

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

SYSADMIN = "254728851746"

RUNSTATUS = "development"  # production

# Datasets
DATASETS = os.getcwd() +  "/datasets"

# MongoDB Host
MONGOHOST = "localhost"

# Asterisk REST Interface
ARIPORT = "50506"
ARIUSER = "helpline"
ARIPASS = "helpline"
ARIHOST = "127.0.0.1"


def tocurrency(dat):
    """Return Currency Format"""
    amount = "0.00"
    if type(dat) == int:
        amount = locale.currency(round(float(dat)), grouping=True)
    return amount.replace("$", "")


def strtoalpha(x: string):
    dat = str.maketrans('', '', string.punctuation)
    data = x.translate(dat)
    return data.replace("  ", " ").rstrip().lstrip()


def ordinaldate(dat):
    """Ordinal Date"""
    SUFFIXES = {1: 'st', 2: 'nd', 3: 'rd'}

    try:
        dat['day'] = int(datetime.fromtimestamp(dat['item']).strftime('%a'))
        dat['date'] = int(datetime.fromtimestamp(dat['item']).strftime('%d'))
        if 10 <= int(dat['date']) % 100 <= 20:
            dat['date'] += "th"
        else:
            dat['date'] += SUFFIXES.get(int(dat['date']) % 10, 'th')
        dat['date'] += " " + datetime.fromtimestamp(dat['item']).strftime('%b %Y')

        dat['time'] = int(datetime.fromtimestamp(dat['item']).strftime('%H:%M %p'))
    except Exception as e:
        dat['error'] = "{}".format(e)

    return dat