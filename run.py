#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (
    unicode_literals,
    print_function
    )

from coreapp import (
    create_app)
from flask_twisted import (
    Twisted)
from flask_cors import (
    CORS)


app = create_app('development')

CORS(
    app,
    resources=r'/*',
    allow_headers='Content-Type'
    )

twisted = Twisted(app)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=50055,
        # debug=True,
        threaded=True
        )
