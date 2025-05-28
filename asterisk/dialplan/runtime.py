#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (
    unicode_literals,
    print_function)

import os
import re
import json
import string
import random
import hashlib
import pandas as pd

from time import (
    time)
from models import (
    system)
from pymongo import (
    MongoClient)
from coreapp import (
    creds)
from datetime import (
    datetime)
from logsdata import (
    logger)
from bson.objectid import (
    ObjectId)
from models.calldata import (
    metadata)

client = MongoClient(credentials.MONGOHOST)
db = client.helpline

edir = os.path.dirname(os.path.realpath(__file__))

epath = edir + "/runtime.py"


def indexinit(dat=False):
    logger.debug("Initialize ARI Runtime")

    data = {}
    data['data'] = False
    data['error'] = False
    data['doc'] = "Asterisk REST Interface"

    try:

        if not db.system_metadata.count_documents({"meta": "ASTERISK"}):
            logger.debug("Created ARI Queue")
            
            system.indexcreate({
                "file": epath,
                "type": "socket",
                "meta": "ASTERISK",
                "name": "Asterisk REST",
                })

        x = db.system_metadata.find_one({"meta": "ASTERISK"})

        dat['track'] = x.get('track')

        data['data'] = True

        x = Thread(target=indexsocket, args=(dat,))
        x.daemon = True
        x.start()

    except Exception as e:
        data['error'] = "Error Index-Init Helpline-Asterisk {}".format(e)
        logger.critical(data['error'])

    return data



def indexdial(dat):
    # logger.debug("""Data Helpline Asterisk Rest API""")

    head = {}
    head['Content-Type'] = 'application/json'
    head['Accept'] = 'application/json'

    try:
        # for item in range(dat['calls']):
        data = {"variables": {}}

        if 'variables' in dat:
            data['variables'] = dat['variables']

            if 'BYPASS' not in data['variables'] and str(
                'VOICE') not in data['variables']:
                logger.debug("""Default Voice Variable""")
                data['variables']['VOICE'] = "Lily"

            if 'BYPASS' not in data['variables'] and str(
                'MEDIAPATH') not in data['variables']:
                logger.debug("""Default Media Dir Variable""")
                data['variables']['MEDIAPATH'] = MEDIA.replace("/Lily", "")

        if type(dat.get('sleep')) == int:
            sleep(dat.get('sleep'))

        x = requests.post(
            "http://" + creds.ARIHOST + ":" + creds.ARIPORT + str(
                "/ari/channels?endpoint=LOCAL/") + str(dat.get(
                    'chan')) + "@" + dat.get('peer') + "&extension=" + dat.get(
                'exten') + "&context=" + dat.get('context'),
            json=data,
            headers=head,
            auth=HTTPBasicAuth(creds.ARIUSER, creds.ARIPASS)
            )
        if x.status_code in [200, 201]:
            # logger.debug("""Success Bridge Call: """ + str(x.json()))
            pass
        else:
            logger.debug("Error Bridge Call: " + str(x.status_code))

    except Exception as e:
        logger.critical("Asterisk ARI Call Error {}".format(e))

    return


def indexsocket(dat):
    # logger.debug("""Run Helpline Asterisk Rest API """ + str(dat))

    data = {}
    data['bridge'] = False

    init = int(time())

    EXCLUDE = ['ChannelHangupRequest', 'ChannelVarset', 'ChannelDialplan']
    EXCLUDE += ['ChannelStateChange', 'ChannelCreated', 'ChannelDestroyed']
    EXCLUDE += ['ChannelEnteredBridge', 'ChannelLeftBridge', 'BridgeCreated']
    EXCLUDE += ['DeviceStateChanged', 'BridgeDestroyed', 'ChannelDtmfReceived']
    EXCLUDE += ['Dial', 'PeerStatusChange', 'ContactStatusChange', 'ChannelCallerId']
    EXCLUDE += ['ChannelConnectedLine']

    SETVARS = ["BRIDGEID", "INITGO", "RTPAUDIOQOSLOSS", "RTPAUDIOQOSMES", "BRIDGEPEER"]
    SETVARS += ["MEDIAPATH", "CONFBRIDGE_RESULT", "RTPAUDIOQOS", "RTPAUDIOQOSJITTER"]
    SETVARS += ["RTPAUDIOQOSRTT", "CONFKICKSTATUS", "VOICE", "SIPDOMAIN", "CONSOLE"]

    CONNECT = ["MAINMENU", "CALLBACK", "SKIPCALL"]

    ws = websocket.WebSocket()

    while True:

        try:

            ws.connect("ws://" + creds.ARIHOST + ":" + data['port'] + str(
                "/ari/events?api_key=") + data['user'] + ":" + str(
                data['pass']) + "&app=awamu&subscribeAll=true")

            data['loop'] = 0
            data['peers'] = {}

            while True:

                sock = ws.recv()

                if sock:
                    # if data is not received break
                    dat = json.loads(sock)

                    if dat.get('type') is not None and dat.get('type') not in EXCLUDE:
                        pass
                        logger.debug("ARI Type " + str(dat.get('type')))

                    elif dat.get('type') in ["ChannelCreated"]:
                        """Create Inboung CDR Data"""

                        x = dat.get('channel')

                        if x.get('dialplan')['exten'] == "pbchelpline":

                            bridge = str(x.get('id').split(".")[0])
                            bridge += str(int(x.get('caller')['number']))

                            xx = metadata.indexstats({
                                "bridge": bridge,
                                "item": "incoming",
                                "uniqueid": x.get('id'),
                                "channel": x.get('name'),
                                "phone": str(int(x.get('caller')['number']))
                                })

                            if 'track' in xx and xx['track']:
                                logger.debug("Create Inboung CDR Data " + xx['track'])

                                soc = {}
                                soc['status'] = "offline"
                                soc['ipad'] = "localhost"
                                soc['port'] = "60060"
                                soc['uuid'] = str(uuid.uuid4())

                                data['peers'][x.get('id')] = xx['track'] 

                                data[xx['track']] = {}
                                data[xx['track']]['dtmf'] = {}
                                data[xx['track']]['bridge'] = bridge
                                data[xx['track']]['service'] = False
                                data[xx['track']]['meta'] = xx['meta']
                                data[xx['track']]['status'] = xx['status']
                                data[xx['track']]['channel'] = x.get('id')

                        elif x.get('dialplan')['exten'] == "dialbridge":
                            logger.debug("Channel Outbound " + str(dat))

                        """
                        logger.debug("We've " + dat['type'].replace(
                            "Channel", "")  + " Call Channel " + str(
                            dat['channel']['name']) + " " + str(
                            dat['channel']['id']) + " to Dialplan " + str(
                            dat['channel']['dialplan']['context']) + ", " + str(
                            dat['channel']['dialplan']['exten']))
                        """

                    elif dat.get('type') in ["ChannelDestroyed"]:
                        # logger.debug("Hangup/Destroy Channel ")

                        if dat.get('channel')['caller']['num'] in CONNECT and dat.get(
                            'channel')['caller']['name'] in CONNECT and dat.get(
                            'channel')['dialplan']['exten'] in data:
                            logger.debug("Check Pre-DTMF Service")

                            track = dat.get('channel')['dialplan']['exten']

                            x = data[track]

                            if dat.get('channel')['caller']['name'] == "BRIDGECLOSE":
                                logger.debug("Close Conference Bridge")

                                if x.get('channel') in data['peers']:
                                    del data['peers'][x.get('channel')]

                                del data[track]

                            elif not len(x.get('dtmf')) and x.get('service') == "callback":
                                logger.debug("Skipped Callback Service")

                                edit = {}
                                edit['BYPASS'] = "yes"
                                edit['SKIPCALL'] = track
                                edit['BRIDGEID'] = track
                                edit['INITGO'] = "hangup"
                                edit['CALLERID(name)'] = "SKIPCALL"

                                data[track]['service'] = "services"

                                indexdial({
                                    "chan": track,
                                    "variables": edit,
                                    "peer": "helpline",
                                    "exten": "helpline",
                                    "context": "helpline",
                                    })

                        elif dat.get('channel')['id'] in data['peers']:
                            logger.debug("Hangup Incoming Channel")

                            track = data['peers'][dat.get('channel')['id']]

                            edit = {}
                            edit['status'] = "hangup"
                            edit['hangup.created'] = int(time())
                            edit['hangup.cause'] = dat.get('cause_txt')

                            metadata.indexaction({
                                "edit": edit,
                                "item": "edit",
                                "track": data['peers'][dat.get('channel')['id']]
                                })

                            edit = {}
                            edit['BYPASS'] = "yes"
                            # edit['BRIDGECLOSE'] = track
                            edit['INITGO'] = "bridgeclose"
                            edit['CALLERID(num)'] = "BRIDGECLOSE"
                            edit['CALLERID(name)'] = "BRIDGECLOSE"
                            edit['BRIDGEID'] = data[track]['bridge']

                            indexdial({
                                "chan": track,
                                "variables": edit,
                                "peer": "helpline",
                                "exten": "helpline",
                                "context": "helpline",
                                })


                        else:
                            pass
                            logger.debug(dat)

                    else:
                        pass
                        logger.debug(dat)

        except Exception as e:
            logger.error("Asterisk ARI Worker Error {}".format(e))
            data['loop'] += 1
            sleep(60)
            if data['loop'] >= 5:
                logger.critical("Asterisk ARI Disconnecting after " + str(
                    data['loop']) + " Attempts")
                break

    ws.close()

    return
