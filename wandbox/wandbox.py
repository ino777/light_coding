import os
import configparser
import logging
import json
import urllib.parse

import requests


logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

BASE_URL = 'https://wandbox.org/api/'


def compile(code, lang, stdinput=''):
    url = urllib.parse.urljoin(BASE_URL, 'compile.json')

    if not config['wandbox_compiler'].get(lang):
        logger.error('No such compiler for {}'.format(lang))
        return json.dumps({
            'status_code': 400,
        })

    data = {
        'code': code,
        'compiler': config['wandbox_compiler'][lang],
        'stdin': stdinput
    }

    headers = {
        'Content-type': 'application/json'
    }

    try:
        r = requests.post(url, data=json.dumps(data), timeout=1.0, headers=headers)
    except requests.ReadTimeout as e:
        return json.dumps({
            'status_code': 500
        })
    if r.status_code != 200:
        return json.dumps({
            'status_code': r.status_code
        })

    return r.json()