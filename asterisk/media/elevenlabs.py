#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (
    unicode_literals,
    print_function
    )

import os
import json
import random
import hashlib
import requests

from time import (
    time,
    sleep,
    mktime,
    strftime)
from klinik import (
    creds)
from datetime import (
    datetime)
from threading import (
    Thread)
from elevenlabs import (
    ElevenLabs)
from logsdata import (
    logger)
from models.callsdata import (
    mediadata as metadata)

edir = os.path.dirname(os.path.realpath(__file__))

epath = edir + "/elevenlabs.py"


def indexinit(dat=False):
    logger.info("""Init ElevenLabs""")

    data = {}
    data['data'] = False
    data['error'] = False

    try:
        data['data'] = True
        data['module'] = "ElevenLabs Text-to-Speech Services"
    except Exception as e:
        data['error'] = "Error Index-Init ElevenLabs {}".format(e)
        logger.critical(data['error'])

    return data


def indexdata(dat):
    logger.debug("""Data ElevenLabs""")

    data = {}
    data['data'] = False
    data['error'] = False
    data['module'] = "ElevenLabs"

    try:

        if dat['item'] == "voices":
            logger.info("""Data Voices""")
            if not os.path.isfile(creds.MEDIA + "/elevenlabs-voices.json"):
                dat['item'] = "getvoices"

        if dat['item'] == "getvoices":
            logger.info("""Generate Voices""")
            url = "https://api.elevenlabs.io/v1/voices"
            headers = {
              "Accept": "application/json",
              "Content-Type": "application/json",
              "xi-api-key": creds.ELEVENLABS[dat['keys']],
            }
            response = requests.get(url, headers=headers)

            if response.status_code in [200, 201]:
                voices = response.json()
                data['voices'] = response.json()['voices']

                with open(creds.MEDIA + "/elevenlabs-voices.json", 'w') as fp:
                    fp.write(json.dumps(response.json(), indent=4))

        data['data'] = True
    except Exception as e:
        data['error'] = "Error Index-Data ElevenLabs {}".format(e)
        logger.critical(data['error'])

    return data


def indexapis(dat):
    logger.debug("""Init APIs-Media ElevenLabs """ + strftime('%H:%M %p'))

    i = 0
    data = []
    CHUNK = 1024

    head = {}
    head['Accept'] = "application/json"
    head['Content-Type'] = "application/json"

    URLDATA = "https://klinik.buzz/klinik/data/private/ivrdata"
    URLPOST = "https://klinik.buzz/klinik/action/private/ivrdata/TRACK"
    URLINIT = "https://klinik.buzz/klinik/stats/private/ivrdata/initmedia"
    URLAPIS = "https://api.elevenlabs.io/v1/text-to-speech/VOICEID/stream"

    try:
        x = requests.post(
            URLINIT, headers=head, json={"source": "sipserver"}
            )
        x = x.json()
        if type(x.get('media')) == list and len(x.get('media')):
            data = x.get('media')
            logger.info("""ElevenLabs Tasks """ + str(len(data)))
        else:
            logger.info("""Zero ElevenLabs Tasks """ + str(x))
            return

    except Exception as e:
        logger.critical("Error Index-Action ElevenLabs {}".format(e))
        return

    with open(creds.MEDIA + "/elevenlabs-voices.json", 'r') as fp:
        voices = json.loads(fp.read()).get('voices')

    credits = {}
    for item in list(creds.ELEVENLABS.keys()):
        try:
            # logger.info("Media Credentials ElevenLabs " + str(item))
            client = ElevenLabs(api_key=creds.ELEVENLABS[item])
            x = client.user.get_subscription().__dict__
            credits[item] = x['character_limit'] - x['character_count']
        except Exception as e:
            logger.error("Credit-Token Error {}".format(e))

    if len(credits) < len(list(creds.ELEVENLABS.keys())):
        logger.critical("Credit-Token Details Missing ")
        return


    while True:

        for item in data:

            edit = {}
            voice = False
            head['xi-api-key'] = "create-value"

            try:
                xx = requests.post(
                    URLDATA, headers=head, json={"track": item}
                    )
                xx = xx.json()

                PATH = creds.MEDIA + "/" + xx.get('path') + "/" + xx.get('voice')

                logger.info("ElevenLabs Create ID " + item)

                if not os.path.isdir(PATH):
                    logger.info("Media Directory ElevenLabs " + PATH)
                    cmd = "mkdir -p " + PATH
                    os.system(cmd)

                PATH += "/" + xx.get('file')

                while True:
                    for x in voices:
                        if x.get('name').lower() == xx.get('voice').lower() and type(
                            x.get('labels')) == dict and 'accent' in x.get('labels'):
                            # logger.info("""Got Voice Match""")

                            if str(x.get('labels')['accent']).lower(
                                ) == xx.get('accent').lower():
                                # logger.info("""Got Voice Hit """ + x.get('voice_id'))
                                voice = x.get('voice_id')
                                break
                    break

                if voice:
                    # logger.info("Got Voice Hit " + voice)
                    credits = dict(sorted(
                        credits.items(),
                        key=lambda idx: idx[1],
                        reverse=True))

                    if list(credits.values())[0] > len(xx.get('text')):
                        logger.info("Media Credit ElevenLabs " + str(list(
                            credits.values())[0]) + " " + str(list(
                            credits.keys())[0]))

                        head['xi-api-key'] = creds.ELEVENLABS[list(credits.keys())[0]]

                if head['xi-api-key'] != "create-value":

                    labs = {}
                    labs['text'] = str(xx.get('text'))
                    labs['model_id'] = "eleven_multilingual_v2"

                    labs['voice_settings'] = {}
                    labs['voice_settings']['style'] = 0.0
                    labs['voice_settings']['stability'] = 0.5
                    labs['voice_settings']['similarity_boost'] = 0.5
                    labs['voice_settings']['use_speaker_boost'] = True

                    edit['engine.id'] = voice
                    edit['engine.mp3'] = False
                    edit['engine.wav'] = False
                    edit['engine.api'] = "elevenlabs"
                    edit['engine.tokens'] = len(xx.get('text'))
                    edit['engine.key'] = list(credits.keys())[0]

                    if os.path.isfile(PATH):
                        logger.error("Duplicate Media - Skip")

                        edit['engine.mp3'] = True
                        edit['engine.wav'] = True

                    else:
                        x = requests.post(
                            URLAPIS.replace("VOICEID", voice),
                            headers=head,
                            json=labs,
                            stream=True
                            )

                        if x.ok:
                            with open(PATH + "-raw.mp3", "wb") as fp:
                                for chunk in x.iter_content(chunk_size=CHUNK):
                                    fp.write(chunk)

                            VOL = "5"

                            cmd = "ffmpeg -report -i " + PATH + "-raw.mp3 -af \"volumedetect\" "
                            cmd += "-vn -sn -dn -f null - > " + PATH + ".txt 2>&1"
                            os.system(cmd)

                            cmd = "ffmpeg -i " + PATH + "-raw.mp3 -af \"volume=" + VOL + "\" "
                            cmd += PATH + ".mp3 > /dev/null 2>&1"
                            os.system(cmd)

                            cmd = "ffmpeg -i " + PATH + ".mp3 -acodec pcm_s16le "
                            cmd += "-ac 1 -ar 8000 " + PATH + ".wav > /dev/null 2>&1"
                            os.system(cmd)

                            cmd = "chown asterisk:asterisk " + PATH + ".wav"
                            os.system(cmd)

                            cmd = "rm " + PATH + "-raw.mp3 " + PATH + ".txt " + os.getcwd(
                                ) + "/ffmpeg-*.log"
                            os.system(cmd)

                            edit['engine.mp3'] = True
                            edit['engine.wav'] = True

                        else:
                            logger.error("Error Create Media ElevenLabs " + str(x.text))
                            edit = {}
                            return

                if len(edit):
                    post = {}
                    post['edit'] = edit
                    post['item'] = "edit"

                    credits[edit['engine.key']] -= edit['engine.tokens']

                    xx = requests.post(
                        URLPOST.replace("TRACK", item), headers=head, json=post
                        )

                sleep(50)

            except Exception as e:
                logger.critical("Error Index-APIs ElevenLabs {}".format(e))

        break

    logger.info("Exiting Create Media ElevenLabs " + strftime('%H:%M %p'))

    return


def indexstats(dat):
    logger.info("""Stats ElevenLabs""")

    data = {}
    data['data'] = False
    data['error'] = False
    data['module'] = "ElevenLabs"

    try:
        if dat['item'] == "createmedia":
            logger.info("""ElevenLabs Create Media""")

            data['data'] = True

            thread = Thread(
                target=indexapis,
                args=({},)
                )
            thread.daemon = True
            thread.start()

    except Exception as e:
        data['error'] = "Error Index-Stats ElevenLabs {}".format(e)
        logger.critical(data['error'])

    return data
