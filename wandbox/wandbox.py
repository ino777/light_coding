import logging
import json
import urllib.parse

import requests

from config import config


logger = logging.getLogger(__name__)

BASE_URL = 'https://wandbox.org/api/'


def compile(code, stdinput=''):
    url = urllib.parse.urljoin(BASE_URL, 'compile.json')

    data = {
        'code': code,
        'compiler': config.cfg['wandbox']['compiler'],
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