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
    time,
    mktime,
    strftime)
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

client = MongoClient(creds.MONGOHOST)

db = client.helpline

edir = os.path.dirname(os.path.realpath(__file__))

epath = edir + "/metadata.py"


def indexinit():
    logger.debug("Initialize System Metadata")

    data = {}
    data['data'] = False
    data['error'] = False
    data['doc'] = "Helpline System"

    try:

        data['items'] = db.system_metadata.count_documents({"type": "queued"})

        if data['items']:
            db.system_metadata.delete_many({"type": "queued"})
        data['data'] = True

    except Exception as e:
        data['error'] = "Error Index-Init Helpline-System {}".format(e)
        logger.critical(data['error'])

    return data


def indexcreate(dat):
    logger.debug("Create System Entry")
    
    data = {}
    data['data'] = False
    data['error'] = False
    data['track'] = False

    try:

        if not all(key in dat for key in ['meta', 'type']):
            logger.warn("Create System Error Keys")

        elif db.system_metadata.count_documents({
            "meta": dat['meta'],
            "type": dat['type'],
            "status": {"$ne": "deleted"}, 
            }):
            logger.debug("Active System Entry")

            x = db.system_metadata.find_one({
                "meta": dat['meta'],
                "type": dat['type'],
                "status": {"$ne": "deleted"}, 
                })
            # data['code'] = x.get('code') # duplicate indicator
            data['track'] = x.get('track')
            data['id'] = str(x.get('_id'))

        else:
            logger.debug("Create System Entry")

            tracks = list(set(string.digits))
            tracks += list(set(string.ascii_uppercase))

            while True:
                random.shuffle(tracks)
                track = "".join(tracks[0:12])
                if not db.system_metadata.count_documents({"track": track}):
                    data['track'] = track
                    break

            x = db.system_metadata.insert_one({
                "admin": {},
                "audit": [],
                "status": "queued",
                "meta": dat['meta'],  # case item
                "type": dat['type'],  # queue, etc
                "track": data['track'],
                "created": int(time()),
                })
            data['id'] = str(x.inserted_id)

            if 'edit' in dat and len(dat['edit']):
                logger.debug("Update System Entry")

                db.system_metadata.update_one({
                    "_id": x.inserted_id},
                    {"$set": dat['edit']})

        data['data'] = True

    except Exception as e:
        data['error'] = "Error Index-Create Helpline-System {}".format(e)
        logger.critical(data['error'])

    if data['error'] and 'id' in data:
        logger.warn("Delete System Entry")
        db.system_metadata.delete_one({"track": data['track']})

    return data


def indexdata(dat):
    logger.logger("Get System Data")

    data = {}
    data['meta'] = []
    data['data'] = False
    data['prev'] = False
    data['next'] = False
    data['error'] = False

    try:

        query = {}
        dat['multi'] = False

        if dat.get('track') is not None and type(dat.get('track')) == str:
            query['track'] = dat['track']

        elif dat.get('id') is not None and type(dat.get('id')) == str:
            query['_id'] = ObjectId(dat['id'])

        else:
            dat['multi'] = True
            query['status'] = {"$ne": "deleted"}

            if 'status' in dat:
                query['status'] = dat['status']

            if 'meta' in dat:
                query['meta'] = dat['meta']

            if 'type' in dat:
                query['type'] = dat['type']

            if 'next' in dat and dat['next']:
                data['prev'] = dat['next']
                query['_id'] = {"$gte": ObjectId(dat['next'])}

            elif 'prev' in dat and dat['prev']:
                data['next'] = dat['prev']
                query['_id'] = {"$lte": ObjectId(dat['prev'])}

        if 'docs' not in dat:
            dat['docs'] = 25

        if 'sort' in dat:
            df = pd.DataFrame(list(db.system_metadata.find(
                query).sort('created', -1).limit(dat['docs'])))
        else:
            df = pd.DataFrame(list(db.system_metadata.find(
                query).limit(dat['docs'])))

        data['total'] = db.system_metadata.count_documents({
            "status": {"$ne": "deleted"}})         

        if len(df):

            DROP = ['created', 'audit']
            df['_id'] =  df._id.apply(str)
            df['audit'] =  df.audit.apply(len)
            df = df.rename(columns={"_id": "id"})

            df['ctime'] = pd.to_datetime(df['created'], unit='s').dt.strftime('%H:%M:%S %p')
            df['cdate'] = pd.to_datetime(df['created'], unit='s').dt.strftime('%d %B %Y')

            df = df.where(df.notna(), lambda x: [{}])

            if dat['multi']:
                df['admin'] =  df.admin.apply(len)

                cols = list(df.columns)

                if 'itemcol' in cols:
                    DROP.append('itemcol')

            df = df.drop(columns=DROP)
            df = df.to_json(orient='records')
            data['meta'] = json.loads(df)

            if not dat['multi']:
                data = data['meta'][0]
                data['error'] = False

            elif not data['next']:
                query['_id'] = {"$gt": ObjectId(data['meta'][-1]["id"])}
                if db.system_metadata.count_documents(query):
                    x = db.system_metadata.find_one(query)
                    data['next'] = str(x.get('_id'))

            del df

        data['source'] = "Helpline System"

        data['data'] = True
    except Exception as e:
        data['error'] = "Error Module-Data Helpline-System {}".format(e)
        logger.critical(data['error'])

    return data



def indexaction(dat):
    logger.logger("Update/Edit System Data")

    data = {}
    data['data'] = False
    data['error'] = False
    try:
        edit = {}
        audit = {}

        info = {}
        if 'track' in dat:
            info['track'] = dat['track']

        elif 'id' in dat:
            info['_id'] = ObjectId(dat['id'])

        else:
            data['error'] = "System Meta Error. One-Of `track` or `id`."
            data['data'] = True
            return data

        if not db.system_metadata.count_documents(info):
            data['error'] = "System Meta Action: Data not Found"
            data['data'] = True
            return data

        x = db.system_metadata.find_one(info)


        if dat['item'] == "pull":
            logger.debug("System Update - Pull")
            db.system_metadata.update_one(
                {"track": x.get('track')},
                {"$unset": {dat['pull']: ""}}
                )

        if dat['item'] == "push":
            logger.debug("System Update - Push")
            db.system_metadata.update_one(
                {"track": x.get('track')},
                {"$push": {dat['push']: dat['data']}}
                )

        if dat['item'] == "edit" or len(edit):
            logger.debug("System Update - Edit")
            if len(edit):
                dat['edit'] = edit
            db.system_metadata.update_one(
                {"track": x.get('track')},
                {"$set": dat['edit']}
                )

        if dat['item'] == "audit" or len(audit):
            logger.debug("System Update - Audit")
            if len(audit):
                dat['audit'] = audit
            dat['audit']['createdate'] = datetime.fromtimestamp(
                int(time())).strftime('%d %B %Y')
            dat['audit']['createtime'] = datetime.fromtimestamp(
                int(time())).strftime('%H:%M:%S %p')
            db.system_metadata.update_one(
                {"track": x.get('track')},
                {"$push": {"audit": dat['audit']}}
                )

        data['data'] = True
    except Exception as e:
        data['error'] = "Error Index-Action Helpline-System {}".format(e)
        logger.critical(data['error'])

    return data


def indexstats(dat):
    logger.debug("System Stats Info")

    data = {}
    data['data'] = False
    data['error'] = False

    try:

        tdy = int(mktime(datetime(
            int(strftime('%Y')),
            int(strftime('%m')),
            int(strftime('%d'))
            ).timetuple()))

        if dat['item'] == "item":
            logger.debug("System Stats Item")

        data['data'] = True
    except Exception as e:
        data['error'] = "Error Index-Stats Helpline-System {}".format(e)
        logger.critical(data['error'])

    return data


def indexapis(dat):
    logger.debug("System API Run")

    data = {}
    data['data'] = False
    data['error'] = False

    try:
        pass
        
    except Exception as e:
        logger.critical("Error Index-APIs Helpline-System {}".format(e))

    return


def indexreset(dat=False):
    logger.debug("System Reset Data")

    data = {}
    data['data'] = False
    data['error'] = False
    data['source'] = "Helpline System"
    
    try:

        if dat.get('track') is not None:
            if db.system_metadata.count_documents({"track": dat.get('track')}):
                logger.debug("System Reset Item")

                edit = {}
                edit['status'] = "deleted"
                edit['admin.deleted'] = int(time())

                db.system_metadata.update_one(
                    {"track": dat['track']},
                    {"$set": edit}
                    )

                data['status'] = "Deleted"

        elif dat.get('backup') is not None:
            logger.debug("System Backup")

            core = []
            if db.system_metadata.count_documents({}):
                df = pd.DataFrame(list(db.system_metadata.find({})))
                df = df.drop(columns=['_id'])
                df = df.to_json(orient='records')
                core = json.loads(df)

            backup = creds.DATASETS + "/backup"
            if not os.path.isdir(backup):
                cmd = "mkdir -p " + backup

            if len(core):
                with open(backup + "/system_metadata.json", 'w') as fp:
                    fp.write(json.dumps(core, indent=2))

            data['meta'] = len(core)

        elif not dat and creds.RUNSTATUS == 'production':
            logger.debug("System Mark-as-Deleted")

            data['meta'] = db.system_metadata.count_documents({
                "status": {"$ne": "deleted"}})

            if data['meta']:

                edit = {}
                edit['status'] = "deleted"
                edit['admin.deleted'] = int(time())

                db.system_metadata.update_many(
                    {"status": {"$ne": "deleted"}},
                    {"$set": edit}
                    )

        elif not dat:
            logger.debug("System Deleted Dev")
            data['meta'] = db.system_metadata.count_documents({})
            if data['meta']:
                db.system_metadata.delete_many({})
                
        data['data'] = True
    except Exception as e:
        data['error'] = "Error Index-Reset Helpline-System {}".format(e)
        logger.critical(data['error'])

    return data
    