__author__ = 'Ben'

import logging

from gcm import *

API_KEY = 'AIzaSyDkxAhehyf2mH83JfjhzagmvEYEs_A17_k'
URL = 'https://android.googleapis.com/gcm/send'

def sendMessageToServer(registration_ids,messageType, data=None):
    headers = {'Authorization': 'key=%s' % API_KEY}

    headers['Content-Type'] = 'application/json'

    payload = dict()
    payload['messageType'] = messageType
    payload['registration_ids'] =registration_ids
    if data:
        payload['data'] = data
    try:
        req = urllib2.Request(URL, json.dumps(payload), headers)
        response = urllib2.urlopen(req)

    except urllib2.HTTPError as err:
        logging.info(payload)
        logging.info(err.code)
    else:
        logging.info(response.read())


def sendMessageToClients(messageType, registration_ids,is_json=True,data = None):
    headers = {'Authorization': 'key=%s' % API_KEY}

    headers['Content-Type'] = 'application/json'

    payload = dict()
    payload['messageType'] = messageType
    payload['registration_ids'] =registration_ids
    if data:
        payload['data'] = data
    req = urllib2.Request(URL, json.dumps(payload), headers)
    response = urllib2.urlopen(req)
    output = response.read()
    logging.info(output)


