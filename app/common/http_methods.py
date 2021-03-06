# -*- coding: utf-8 -*-

import random
import re
import time
from HTMLParser import HTMLParser

from google.appengine.api.urlfetch_errors import InternalTransientError
from app.common.logger import logger
from app.common.session_manager import get_session, save_session_in_cache
from app.common.target_strings import LOGOUT_STRING
from app.common.target_urls import LOGIN_PAGE
from app.common.target_urls import POST_LOGIN_PAGE
from fm.databases.database_django import save_session_to_db
from lib import requests
from app.common.constants import USERNAME, PASSWORD, HEADER
from lib.requests import RequestException

parser = HTMLParser()


def authenticate_with_server():
    http_session = requests.session()
    http_session.get(LOGIN_PAGE, headers=HEADER)
    data = {"pseudo": USERNAME, "passe": PASSWORD, "souvenir": 1}
    http_session.post(POST_LOGIN_PAGE, data, headers=HEADER)
    logger.warning('LOGIN')
    save_session_in_cache(http_session)
    save_session_to_db()
    return http_session


def wait():
    time.sleep(0.3 + random.random() / 2)


def is_connected(page):
    p = re.compile(LOGOUT_STRING)
    return len(p.findall(page)) == 0


def __send_request_process_response(http_session, method_name, address, post_data):
    request_retries = 3
    for _ in range(request_retries):
        try:
            response = getattr(http_session, method_name)(address, data=post_data, headers=HEADER)
            response.encoding = 'utf-8'
            html_page = response.text
            return parser.unescape(html_page)
        # except (RequestException, InternalTransientError, HTTPException, DeadlineExceededError):
        except (RequestException, InternalTransientError):
            wait()
            logger.warning('Request failed, will retry')
            continue


def __generic_request(method_name, address, post_data=None):
    http_session = get_session()
    if not http_session:
        logger.warning('No previous session found')
        http_session = authenticate_with_server()
    html_page = __send_request_process_response(http_session, method_name, address, post_data)
    if not is_connected(html_page):
        logger.warning('Session expired')
        http_session = authenticate_with_server()
        html_page = __send_request_process_response(http_session, method_name, address, post_data)
    save_session_in_cache(http_session)
    wait()
    return html_page


def get_request(address):
    return __generic_request('get', address)


def post_request(address, data):
    return __generic_request('post', address, data)
